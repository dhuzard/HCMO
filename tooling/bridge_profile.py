#!/usr/bin/env python3
"""Build and test the optional BFO/SOSA bridge profile (ADR-0005).

The profile composes two published one-way alignments, W3C SOSA -> PROV-O and
PROV-O -> BFO (Prudhomme et al. 2025), so that SOSA terms get a BFO placement
without HCMO asserting anything about W3C terms. This script never touches the
default release: it assembles the closure in a scratch directory, runs HermiT
over it, and checks the gates recorded in ADR-0005.

Commands
  check    verify pins, assemble the chains, reason, run the probes (default)
  package  write self-contained reasoner bundles for review in Protege

Reasoning needs the dependencies of tooling/reasoning-requirements.txt, Java
and network access (once) to download the pinned BFO, IAO, SOSA and PROV-O
files, which are cached under .cache/bridge/ after their SHA-256 is verified.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import itertools
import json
import subprocess
import sys
import urllib.request
from pathlib import Path

import yaml
from rdflib import BNode, Graph, URIRef
from rdflib.compare import graph_diff, to_isomorphic
from rdflib.namespace import OWL, RDF, RDFS

ROOT = Path(__file__).resolve().parent.parent
CONTRACT = ROOT / "external-vocabularies.yaml"
MANIFEST = ROOT / "hcmo.yaml"
PROFILE = ROOT / "ontology" / "profiles" / "bfo-sosa-bridge.ttl"
DEV_PROFILE = ROOT / "ontology" / "profiles" / "external-upper-developer.ttl"
SHAPES = ROOT / "shapes" / "profiles" / "bfo-sosa-bridge-shapes.ttl"
PROBE_DIR = ROOT / "examples" / "profiles" / "bfo-sosa-bridge"
CACHE = ROOT / ".cache" / "bridge"
DEFAULT_OUT = ROOT / "build" / "bridge"

HCM_NS = "https://w3id.org/hcmo/ontology/hcm"
SOSA_NS = "http://www.w3.org/ns/sosa/"
BFO_NS = "http://purl.obolibrary.org/obo/BFO_"
TAXONOMY_PREFIXES = (HCM_NS, SOSA_NS, BFO_NS)
# Differences between the pinned BFO and the alignment's target release are
# expected to be annotation-only.
ANNOTATION_PREDICATES = {
    "http://www.w3.org/2002/07/owl#versionIRI",
    "http://www.w3.org/2004/02/skos/core#definition",
    "http://www.w3.org/2004/02/skos/core#scopeNote",
}
PREFIX_LINES = (
    b"@prefix : <https://raw.githubusercontent.com/BFO-Mappings/PROV-to-BFO/main/"
    b"prov-bfo-directmappings.ttl#> .\n"
    b"@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n"
)
# The pinned tag also misspells one annotation predicate (`rdfs:comment:`, a
# distinct IRI). ROBOT 1.9.10 rejects the file on it (replay by Cyril Gilbert,
# 2026-10-09), so the repair corrects that one token as well. Upstream fixed it
# on main (their #41).
TYPO_OLD = b"rdfs:comment: "
TYPO_NEW = b"rdfs:comment "
TYPO_IRI = URIRef("http://www.w3.org/2000/01/rdf-schema#comment:")


class Report:
    def __init__(self) -> None:
        self.rows: list[tuple[bool, str]] = []
        self.sections: dict[str, str] = {}

    def check(self, ok: bool, message: str) -> bool:
        self.rows.append((ok, message))
        print(f"[{'OK' if ok else 'FAIL'}] {message}", flush=True)
        return ok

    @property
    def ok(self) -> bool:
        return all(ok for ok, _ in self.rows)


def sha256(path_or_bytes: Path | bytes) -> str:
    data = path_or_bytes if isinstance(path_or_bytes, bytes) else path_or_bytes.read_bytes()
    return hashlib.sha256(data).hexdigest()


def contract() -> dict:
    return yaml.safe_load(CONTRACT.read_text(encoding="utf-8"))["vocabularies"]


def artifact(vocab: str, role: str) -> dict:
    for item in contract()[vocab]["artifacts"]:
        if item["role"] == role:
            return item
    raise KeyError(f"{vocab}/{role} not in {CONTRACT.name}")


def fetch(vocab: str, role: str) -> Path:
    """Return a checksum-verified cached copy of a pinned artifact."""
    item = artifact(vocab, role)
    CACHE.mkdir(parents=True, exist_ok=True)
    name = Path(item["url"].split("?")[0]).name or f"{vocab}-{role}"
    target = CACHE / f"{item['sha256'][:12]}-{name}"
    if target.exists() and sha256(target) == item["sha256"]:
        return target
    request = urllib.request.Request(item["url"], headers={"User-Agent": "HCMO-bridge-profile/1"})
    with urllib.request.urlopen(request, timeout=120) as response:
        data = response.read()
    if sha256(data) != item["sha256"]:
        raise SystemExit(
            f"ERROR: checksum mismatch for {vocab}/{role}: expected {item['sha256']}, "
            f"got {sha256(data)}"
        )
    target.write_bytes(data)
    return target


def vendored(vocab: str, role: str) -> Path:
    path = ROOT / artifact(vocab, role)["vendored_path"]
    if sha256(path) != artifact(vocab, role)["sha256"]:
        raise SystemExit(f"ERROR: vendored file {path} does not match its pinned SHA-256")
    return path


def check_vendor(report: Report) -> dict[str, Path]:
    original = ROOT / artifact("prov-bfo-alignment", "alignment-original")["vendored_path"]
    repair = contract()["prov-bfo-alignment"]["repair"]
    fixed = ROOT / repair["vendored_path"]
    sosa_prov = ROOT / artifact("sosa-prov-alignment", "alignment")["vendored_path"]
    report.check(
        sha256(original) == artifact("prov-bfo-alignment", "alignment-original")["sha256"],
        "PROV-to-BFO original is byte-identical to the pinned upstream file",
    )
    original_bytes = original.read_bytes()
    report.check(
        original_bytes.count(TYPO_OLD) == 1,
        "upstream original still contains the single `rdfs:comment:` typo (repair still needed)",
    )
    expected = PREFIX_LINES + original_bytes.replace(TYPO_OLD, TYPO_NEW, 1)
    report.check(
        fixed.read_bytes() == expected and sha256(fixed) == repair["sha256"],
        "repaired copy is exactly the two documented prefix lines + the original bytes "
        "with the one `rdfs:comment:` token corrected",
    )
    report.check(
        [line for line in PREFIX_LINES.decode().splitlines()] == repair["prepended_lines"],
        "documented prepended lines match external-vocabularies.yaml",
    )
    report.check(
        repair["replaced_once"] == {"from": TYPO_OLD.decode().strip(), "to": TYPO_NEW.decode().strip()},
        "documented token replacement matches external-vocabularies.yaml",
    )
    report.check(
        sha256(sosa_prov) == artifact("sosa-prov-alignment", "alignment")["sha256"],
        "W3C SOSA-to-PROV-O alignment matches its pinned SHA-256",
    )
    try:
        Graph().parse(original, format="turtle")
        report.check(False, "upstream original unexpectedly parses: the repair may be obsolete")
    except Exception:  # noqa: BLE001
        report.check(True, "upstream original still fails to parse (repair still needed)")
    fixed_graph = Graph().parse(fixed, format="turtle")
    report.check(
        (None, TYPO_IRI, None) not in fixed_graph,
        "repaired copy no longer uses the misspelled `rdfs:comment:` predicate",
    )
    return {"fixed": fixed, "sosa_prov": sosa_prov}


def load_core() -> Graph:
    graph = Graph()
    for module in yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))["modules"]:
        graph.parse(ROOT / module, format="turtle")
    return graph


def build_graphs(bfo_role: str, mode: str, core: Graph, vend: dict[str, Path]) -> tuple[Graph, Graph]:
    """Return (baseline, chain) graphs for one BFO file and presentation mode."""
    base = Graph()
    base += core
    base.parse(fetch("bfo", bfo_role))
    base.parse(fetch("iao", "ontology"))
    base.parse(fetch("sosa-2017", "ontology"))
    base.parse(fetch("prov-o", "ontology"))
    if mode == "developer":
        base.parse(DEV_PROFILE, format="turtle")
    base.remove((None, OWL.imports, None))
    chain = Graph()
    chain += base
    chain.parse(vend["sosa_prov"], format="turtle")
    chain.parse(vend["fixed"], format="turtle")
    chain.remove((None, OWL.imports, None))
    return base, chain


def positive_examples() -> list[Path]:
    paths = []
    for path in sorted((ROOT / "examples").rglob("*.ttl")):
        rel = path.relative_to(ROOT / "examples").as_posix()
        if rel.startswith("profiles/") or any(tag in path.name for tag in ("invalid", "edge")):
            continue
        paths.append(path)
    return paths


# --------------------------------------------------------------------------
# Reasoning (one JVM per file, in a subprocess)
# --------------------------------------------------------------------------

def reason_worker(nt_path: Path, out_json: Path, java_memory: int) -> None:
    import owlready2 as ow

    ow.reasoning.JAVA_MEMORY = java_memory
    result: dict = {"input": nt_path.name, "owlready2": ow.VERSION}
    try:
        world = ow.World()
        world.get_ontology(str(nt_path.resolve())).load(format="ntriples")
        ow.sync_reasoner(world, debug=0)
        result["status"] = "consistent"
        result["unsatisfiable"] = sorted(
            c.iri for c in world.inconsistent_classes() if c is not ow.Nothing and hasattr(c, "iri")
        )
        result["ancestors"] = {
            c.iri: sorted(
                a.iri
                for a in c.ancestors()
                if hasattr(a, "iri") and a.iri.startswith(TAXONOMY_PREFIXES)
            )
            for c in world.classes()
            if c.iri.startswith(TAXONOMY_PREFIXES)
        }
    except ow.OwlReadyInconsistentOntologyError as exc:
        result["status"] = "inconsistent"
        result["error"] = str(exc)[:300]
    except Exception as exc:  # noqa: BLE001
        result["status"] = "error"
        result["error"] = f"{type(exc).__name__}: {exc}"[:500]
    out_json.write_text(json.dumps(result), encoding="utf-8")


def run_reasoner(graph: Graph, name: str, out: Path, java_memory: int, timeout: int) -> dict:
    nt = out / f"{name}.nt"
    graph.serialize(nt, format="nt")
    out_json = out / f"{name}.result.json"
    if out_json.exists():
        out_json.unlink()
    try:
        subprocess.run(
            [sys.executable, str(Path(__file__).resolve()), "_reason", str(nt), str(out_json), str(java_memory)],
            check=False,
            timeout=timeout,
            capture_output=True,
            text=True,
        )
    except subprocess.TimeoutExpired:
        return {"status": "error", "error": f"timeout after {timeout}s", "input": nt.name}
    if not out_json.exists():
        return {"status": "error", "error": "reasoner produced no result", "input": nt.name}
    return json.loads(out_json.read_text(encoding="utf-8"))


# --------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------

def explicit_disjointness(graph: Graph) -> list[tuple]:
    pairs = [(s, o) for s, o in graph.subject_objects(OWL.disjointWith)]
    for axiom in graph.subjects(RDF.type, OWL.AllDisjointClasses):
        members = graph.value(axiom, OWL.members)
        if members is not None:
            pairs.extend(itertools.combinations(list(graph.items(members)), 2))
    return pairs


def describe(graph: Graph, node) -> str:
    if isinstance(node, URIRef):
        return str(node)
    for predicate, tag in ((OWL.unionOf, "OR"), (OWL.intersectionOf, "AND")):
        head = graph.value(node, predicate)
        if head is not None:
            return "(" + f" {tag} ".join(describe(graph, x) for x in graph.items(head)) + ")"
    complement = graph.value(node, OWL.complementOf)
    if complement is not None:
        return "NOT " + describe(graph, complement)
    return node.n3() if isinstance(node, BNode) else str(node)


def new_subsumptions(baseline: dict, chain: dict) -> list[str]:
    found = []
    for iri, ancestors in chain.items():
        for prefix in TAXONOMY_PREFIXES:
            if iri.startswith(prefix):
                for ancestor in set(ancestors) - set(baseline.get(iri, [])):
                    if ancestor.startswith(prefix):
                        found.append(f"{iri} <= {ancestor}")
    return sorted(found)


def shacl_outcome(probe: Path, core: Graph) -> tuple[bool, str]:
    from pyshacl import validate

    data = Graph()
    data += core
    data.parse(probe, format="turtle")
    shapes = Graph().parse(SHAPES, format="turtle")
    conforms, _, text = validate(data, shacl_graph=shapes, inference="none", advanced=False)
    return conforms, text


def check_bfo_drift(report: Report, out: Path) -> None:
    pinned = Graph().parse(fetch("bfo", "ontology"))
    target = Graph().parse(fetch("bfo", "alignment-target-comparison"))
    both, only_pin, only_target = graph_diff(to_isomorphic(pinned), to_isomorphic(target))
    predicates = {str(p) for _, p, _ in itertools.chain(only_pin, only_target)}
    unexpected = sorted(predicates - ANNOTATION_PREDICATES)
    (out / "bfo-only-pinned.nt").write_text(only_pin.serialize(format="nt"), encoding="utf-8")
    (out / "bfo-only-target.nt").write_text(only_target.serialize(format="nt"), encoding="utf-8")
    report.check(
        not unexpected,
        f"pinned BFO vs alignment-target BFO: {len(both)} shared, {len(only_pin)} pin-only, "
        f"{len(only_target)} target-only triples; "
        + ("annotation-only" if not unexpected else f"non-annotation predicates {unexpected}"),
    )


def check_default_release(report: Report) -> None:
    manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    report.check(
        not any("bfo-sosa-bridge" in m or "profiles" in m for m in manifest["modules"]),
        "profile is not listed in hcmo.yaml modules",
    )
    dist = Graph().parse(ROOT / manifest["dist"]["merged_ttl"], format="turtle")
    report.check((None, OWL.imports, None) not in dist, "dist/hcmo.ttl has no owl:imports")
    leaked = [
        (s, o)
        for s, o in dist.subject_objects(RDFS.subClassOf)
        if isinstance(s, URIRef)
        and str(s).startswith(SOSA_NS)
        and isinstance(o, URIRef)
        and (str(o).startswith(BFO_NS) or str(o).startswith("http://www.w3.org/ns/prov#"))
    ]
    report.check(not leaked, "dist/hcmo.ttl asserts no axiom on a sosa: term towards BFO or PROV-O")
    profile = Graph().parse(PROFILE, format="turtle")
    ontology_subjects = set(profile.subjects(RDF.type, OWL.Ontology))
    stray = [t for t in profile if t[0] not in ontology_subjects]
    report.check(not stray, "profile ontology declares no axiom of its own (annotations and imports only)")


def run_check(args: argparse.Namespace) -> int:
    report = Report()
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    vend = check_vendor(report)
    check_default_release(report)
    core = load_core()
    roles = {"pinned": ["ontology"], "target": ["alignment-target-comparison"],
             "both": ["ontology", "alignment-target-comparison"]}[args.bfo]
    if "alignment-target-comparison" in roles:
        check_bfo_drift(report, out)
    probes = yaml.safe_load((PROBE_DIR / "probes.yaml").read_text(encoding="utf-8"))
    modes = [m for m in args.modes.split(",") if m]
    positives = positive_examples()
    summary: dict = {}

    for role in roles:
        for mode in modes:
            tag = f"{'pinned' if role == 'ontology' else 'target'}-{mode}"
            base, chain = build_graphs(role, mode, core, vend)
            jobs: dict[str, Graph] = {f"{tag}-baseline": base, f"{tag}-chain": chain}
            union = Graph()
            union += chain
            for path in positives:
                union.parse(path, format="turtle")
            jobs[f"{tag}-examples-union"] = union
            if args.thorough:
                for path in sorted((ROOT / "examples").rglob("*.ttl")):
                    rel = path.relative_to(ROOT / "examples").as_posix()
                    if rel.startswith("profiles/"):
                        continue
                    one = Graph()
                    one += chain
                    one.parse(path, format="turtle")
                    jobs[f"{tag}-example-{rel.replace('/', '__')}"] = one
            for probe in probes["probes"]:
                g = Graph()
                g += chain
                g.parse(PROBE_DIR / probe["file"], format="turtle")
                jobs[f"{tag}-probe-{probe['id']}"] = g
                if probe["owl"] == "inconsistent":
                    # Discrimination: without the alignments the same probe must be
                    # consistent, otherwise the alignments are not what causes it.
                    plain = Graph()
                    plain += base
                    plain.parse(PROBE_DIR / probe["file"], format="turtle")
                    jobs[f"{tag}-baseline-probe-{probe['id']}"] = plain
            with concurrent.futures.ThreadPoolExecutor(args.jobs) as pool:
                futures = {
                    name: pool.submit(run_reasoner, g, name, out, args.java_memory, args.timeout)
                    for name, g in jobs.items()
                }
                results = {name: f.result() for name, f in futures.items()}
            summary[tag] = {k: {x: v[x] for x in v if x != "ancestors"} for k, v in results.items()}

            for name in (f"{tag}-baseline", f"{tag}-chain", f"{tag}-examples-union"):
                res = results[name]
                report.check(
                    res["status"] == "consistent" and not res.get("unsatisfiable"),
                    f"{name}: {res['status']}, unsatisfiable={res.get('unsatisfiable', 'n/a')}"
                    + (f" ({res.get('error')})" if res.get("error") else ""),
                )
            if args.thorough:
                for name, res in results.items():
                    if "-example-" in name:
                        report.check(res["status"] == "consistent", f"{name}: {res['status']}")
            for probe in probes["probes"]:
                res = results[f"{tag}-probe-{probe['id']}"]
                report.check(
                    res["status"] == probe["owl"],
                    f"{tag} probe {probe['id']}: expected {probe['owl']}, got {res['status']}"
                    + (f" ({res.get('error')})" if res["status"] == "error" else ""),
                )
            for probe in probes["probes"]:
                if probe["owl"] == "inconsistent":
                    res = results[f"{tag}-baseline-probe-{probe['id']}"]
                    report.check(
                        res["status"] == "consistent",
                        f"{tag} probe {probe['id']} without the alignments: expected consistent, got {res['status']}",
                    )
            baseline_anc = results[f"{tag}-baseline"].get("ancestors", {})
            chain_anc = results[f"{tag}-chain"].get("ancestors", {})
            delta = new_subsumptions(baseline_anc, chain_anc)
            (out / f"{tag}-new-subsumptions.txt").write_text("\n".join(delta), encoding="utf-8")
            report.check(
                not delta,
                f"{tag}: {len(delta)} new named subsumptions inside the HCMO, SOSA or BFO hierarchies",
            )
            for iri, required in probes["placements"].items():
                missing = [r for r in required if r not in chain_anc.get(iri, [])]
                report.check(not missing, f"{tag} placement {iri.rsplit('/', 1)[-1].rsplit('#', 1)[-1]}: "
                             + ("ok" if not missing else f"missing {missing}"))
            lines = []
            for x, y in sorted(explicit_disjointness(chain), key=lambda t: (describe(chain, t[0]), describe(chain, t[1]))):
                left = sorted(i for i, a in chain_anc.items() if str(x) in a and i.startswith((HCM_NS, SOSA_NS)))
                right = sorted(i for i, a in chain_anc.items() if str(y) in a and i.startswith((HCM_NS, SOSA_NS)))
                lines.append(f"{describe(chain, x)} DISJOINT {describe(chain, y)} | left: {', '.join(left)} | right: {', '.join(right)}")
            (out / f"{tag}-disjointness.txt").write_text("\n".join(lines), encoding="utf-8")
            report.check(True, f"{tag}: {len(lines)} explicit disjointness axioms listed for review "
                               f"({out.name}/{tag}-disjointness.txt)")

    for probe in probes["probes"]:
        conforms, _ = shacl_outcome(PROBE_DIR / probe["file"], core)
        expected = probe["shacl"] == "conforms"
        report.check(conforms == expected, f"SHACL probe {probe['id']}: expected {probe['shacl']}, "
                                           f"got {'conforms' if conforms else 'violates'}")

    (out / "results.json").write_text(json.dumps({"ok": report.ok, "summary": summary,
                                                   "checks": [{"ok": o, "message": m} for o, m in report.rows]},
                                                  indent=2), encoding="utf-8")
    print(f"\nBridge profile check: {'PASS' if report.ok else 'FAIL'} ({len(report.rows)} checks; {out})")
    return 0 if report.ok else 1


def run_package(args: argparse.Namespace) -> int:
    out = Path(args.out).resolve() / "protege"
    (out / "probes").mkdir(parents=True, exist_ok=True)
    report = Report()
    vend = check_vendor(report)
    core = load_core()
    probes = yaml.safe_load((PROBE_DIR / "probes.yaml").read_text(encoding="utf-8"))["probes"]
    for mode in ("default", "developer"):
        base, chain = build_graphs("ontology", mode, core, vend)
        base.serialize(out / f"baseline-{mode}.ttl", format="turtle")
        chain.serialize(out / f"chain-{mode}.ttl", format="turtle")
        for probe in probes:
            g = Graph()
            g += chain
            g.parse(PROBE_DIR / probe["file"], format="turtle")
            g.serialize(out / "probes" / f"{probe['id']}-{mode}.ttl", format="turtle")
    (out / "README.md").write_text(
        "# HCMO BFO/SOSA bridge: reasoner bundle\n\n"
        "Self-contained Turtle files (no owl:imports): HCMO + pinned BFO 2020, IAO, SOSA 2017, PROV-O + the W3C\n"
        "SOSA-to-PROV-O alignment + the PROV-to-BFO alignment (prefix- and typo-repaired, see third_party/bfo-sosa-bridge/README.md).\n\n"
        "- `baseline-*.ttl`: everything except the two alignments.\n"
        "- `chain-*.ttl`: baseline + both alignments. `default` = end-user upper presentation, `developer` = with the\n"
        "  developer BFO/IAO profile.\n"
        "- `probes/<id>-<mode>.ttl`: chain + one probe. Expected outcomes are in\n"
        "  `examples/profiles/bfo-sosa-bridge/probes.yaml`.\n\n"
        "## What to report (Protege: open a file, Reasoner > HermiT > Start reasoner)\n\n"
        "1. Protege and HermiT versions; does each file load without errors or missing imports?\n"
        "2. `chain-default.ttl` and `chain-developer.ttl`: consistent? Any unsatisfiable class?\n"
        "3. Inferred superclasses of sosa:Sensor, sosa:Actuator, sosa:Observation, sosa:Result and\n"
        "   hcm-obs:BehaviorObservation (compare with `placements` in probes.yaml).\n"
        "4. For each probe file: consistent or inconsistent? Expected: software-sensor,\n"
        "   direct-concretizes and process-foi are inconsistent; the other four are consistent.\n"
        "5. Does the carrier pattern (`probes/carrier-pattern-*.ttl`: the running installation is the\n"
        "   sensor and bears a quality that concretizes the code) read as acceptable for a real\n"
        "   software tracker (DeepLabCut, SLEAP, Live Mouse Tracker)?\n"
        "6. Same checks with ROBOT (`robot reason --reasoner HermiT --input chain-default.ttl`) if available.\n",
        encoding="utf-8",
    )
    print(f"Wrote reasoner bundle to {out}")
    return 0 if report.ok else 1


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "_reason":
        reason_worker(Path(sys.argv[2]), Path(sys.argv[3]), int(sys.argv[4]))
        return 0
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", nargs="?", choices=["check", "package"], default="check")
    parser.add_argument("--out", default=str(DEFAULT_OUT), help="scratch/output directory (default build/bridge)")
    parser.add_argument("--modes", default="default,developer", help="presentations to test (comma separated)")
    parser.add_argument("--bfo", choices=["pinned", "target", "both"], default="pinned",
                        help="BFO file(s): the pinned one, the alignment's target release, or both")
    parser.add_argument("--thorough", action="store_true", help="also reason over every example file separately")
    parser.add_argument("--jobs", type=int, default=2, help="parallel HermiT runs")
    parser.add_argument("--java-memory", type=int, default=2048, help="HermiT heap per run, MB")
    parser.add_argument("--timeout", type=int, default=900, help="per-run timeout, seconds")
    args = parser.parse_args()
    return run_check(args) if args.command == "check" else run_package(args)


if __name__ == "__main__":
    raise SystemExit(main())
