#!/usr/bin/env python3
"""Validation gate for the Home-Cage Monitoring Ontology (HCMO).

Steps (any failure -> non-zero exit):
  1. Parse every TTL under ontology/, shapes/, and examples/, plus all generated
     RDF distribution serializations declared in hcmo.yaml.
  2. Validate release-bearing metadata surfaces and the pinned external-
     vocabulary contract without network access.
  3. Run pySHACL of shapes/ against each isolated example with the canonical
     ontology supplied as an ontology graph and RDFS inference enabled.
     Examples whose name contains "edge" or "invalid" are NEGATIVE tests
     (expected to be non-conformant); all others are expected to conform.
  4. Validate the dedicated ISA/STATO evidence graph, including an injected
     process-cycle negative probe.
  5. Validate the accepted lossless extended-crate round-trip fixture, exact
     semantic invariants, and negative housing-overlap probe.
  6. Validate the review-only semantic mapping and controlled-loss exchange
     registries.
  7. Run every indexed competency query against the canonical ontology plus all
     positive examples. The canonicalized result rows must equal the reviewed
     answers in queries/competency_questions.yaml.

Usage: python tooling/validate.py
"""
from __future__ import annotations

import glob
import csv
import json
import re
import sys
from pathlib import Path

import yaml
from rdflib import RDF, Graph, Literal, Namespace, URIRef, XSD
from rdflib.compare import isomorphic
from pyshacl import validate as shacl_validate
from external_vocab import validate_contract

ROOT = Path(__file__).resolve().parent.parent


def load_manifest() -> dict:
    with open(ROOT / "hcmo.yaml") as f:
        return yaml.safe_load(f)


def merged_graph(manifest: dict) -> Graph:
    g = Graph()
    for rel in manifest["modules"]:
        g.parse(ROOT / rel, format="turtle")
    return g


def is_negative_example(relative_path: str) -> bool:
    return any(
        token in Path(relative_path).name.lower() for token in ("edge", "invalid")
    )


def competency_questions(manifest: dict) -> list[dict]:
    index_path = ROOT / manifest["queries"]["index"]
    index = yaml.safe_load(index_path.read_text(encoding="utf-8"))
    if str(index.get("version")) != str(manifest.get("version")):
        raise ValueError(
            "competency question index version "
            f"{index.get('version')!r} does not match hcmo.yaml "
            f"{manifest.get('version')!r}"
        )
    questions = index.get("questions", [])
    if not isinstance(questions, list):
        raise ValueError("competency question index must contain a questions list")
    if not all(isinstance(question, dict) for question in questions):
        raise ValueError("every competency question entry must be a mapping")
    return questions


def step_release_surfaces(
    manifest: dict, ontology_graph: Graph
) -> tuple[bool, list[str]]:
    """Require release-bearing machine surfaces to agree with hcmo.yaml."""
    expected_version = str(manifest["version"])
    notes: list[str] = []
    mismatches: list[str] = []

    citation = yaml.safe_load((ROOT / "CITATION.cff").read_text(encoding="utf-8"))
    if str(citation.get("version")) != expected_version:
        mismatches.append(
            f"CITATION.cff version {citation.get('version')!r} != {expected_version!r}"
        )

    form_path = ROOT / "docs/hcm-systems/contribute/index.html"
    form_text = form_path.read_text(encoding="utf-8")
    form_match = re.search(r'ontologyVersion:\s*"([^"]+)"', form_text)
    form_version = form_match.group(1) if form_match else None
    if form_version != expected_version:
        mismatches.append(
            f"contribution-form ontologyVersion {form_version!r} != {expected_version!r}"
        )

    ontology = URIRef(manifest["ontology_iri"])
    bibo_doi = URIRef("http://purl.org/ontology/bibo/doi")
    ontology_dois = {str(value) for value in ontology_graph.objects(ontology, bibo_doi)}
    citation_doi = str(citation.get("doi"))
    if ontology_dois != {citation_doi}:
        mismatches.append(
            f"ontology bibo:doi {sorted(ontology_dois)!r} != CITATION.cff {citation_doi!r}"
        )

    if mismatches:
        notes.extend(f"[FAIL] release metadata: {item}" for item in mismatches)
        return False, notes
    notes.append(
        f"[OK]   release metadata surfaces agree on HCMO {expected_version} "
        f"and DOI {citation_doi}"
    )
    return True, notes


def evaluation_graph(manifest: dict, ontology_graph: Graph) -> Graph:
    graph = Graph()
    for triple in ontology_graph:
        graph.add(triple)
    for relative_path in manifest.get("examples", []):
        if not is_negative_example(relative_path):
            graph.parse(ROOT / relative_path, format="turtle")
    return graph


def step_parse_all(manifest: dict) -> tuple[bool, list[str]]:
    ok = True
    notes = []
    patterns = ["ontology/**/*.ttl", "shapes/**/*.ttl", "examples/**/*.ttl"]
    files = {Path(p) for pat in patterns for p in glob.glob(str(ROOT / pat), recursive=True)}
    files.update(
        {
            ROOT / manifest["dist"]["merged_ttl"],
            ROOT / manifest["dist"]["merged_owl"],
            ROOT / manifest["dist"]["jsonld"],
        }
    )
    formats = {".ttl": "turtle", ".owl": "xml", ".json": "json-ld"}
    for f in sorted(files):
        rel = str(Path(f).relative_to(ROOT))
        try:
            Graph().parse(f, format=formats[Path(f).suffix.lower()])
            notes.append(f"[OK]   parsed {rel}")
        except Exception as e:  # noqa: BLE001
            ok = False
            notes.append(f"[FAIL] parse {rel}: {e}")
    return ok, notes


def step_shacl(manifest: dict, ontology_graph: Graph) -> tuple[bool, list[str]]:
    ok = True
    notes = []
    shapes_path = ROOT / manifest["shapes"]
    if not shapes_path.exists():
        return False, [f"[FAIL] shapes file missing: {manifest['shapes']}"]
    shapes_g = Graph().parse(shapes_path, format="turtle")
    for rel in manifest.get("examples", []):
        path = ROOT / rel
        negative = is_negative_example(rel)
        if not path.exists():
            ok = False
            notes.append(f"[FAIL] example missing: {rel}")
            continue
        data_g = Graph().parse(path, format="turtle")
        inference_probe = Path(rel).name == "abox-inferred-invalid.ttl"
        if inference_probe:
            baseline_conforms, _, _ = shacl_validate(
                data_g,
                shacl_graph=shapes_g,
                inference="none",
                abort_on_first=False,
                do_owl_imports=False,
            )
            if not baseline_conforms:
                ok = False
                notes.append(
                    f"[FAIL] SHACL {rel}: fixture is not inference-dependent"
                )
                continue
        conforms, _, _ = shacl_validate(
            data_g,
            shacl_graph=shapes_g,
            ont_graph=ontology_graph,
            inference="rdfs",
            abort_on_first=False,
            do_owl_imports=False,
        )
        expect = "non-conformant" if negative else "conformant"
        actual = "conformant" if conforms else "non-conformant"
        passed = (conforms is not negative)  # positive->conform, negative->not
        if not passed:
            ok = False
            notes.append(f"[FAIL] SHACL {rel}: expected {expect}, got {actual}")
        else:
            notes.append(f"[OK]   SHACL {rel}: {actual} (expected {expect})")
            if inference_probe:
                notes.append(
                    "[OK]   ontology-aware target probe: conformant without "
                    "ontology, non-conformant with ontology + RDFS"
                )
    return ok, notes


def step_isa_evidence() -> tuple[bool, list[str]]:
    data_path = ROOT / "examples/isa-hcmo-bridge.ttl"
    shapes_path = ROOT / "shapes/isa-hcmo-evidence-shapes.ttl"
    if not data_path.exists() or not shapes_path.exists():
        return False, ["[FAIL] ISA/STATO evidence graph or shapes file missing"]

    data_g = Graph().parse(data_path, format="turtle")
    shapes_g = Graph().parse(shapes_path, format="turtle")
    conforms, _, report = shacl_validate(
        data_g,
        shacl_graph=shapes_g,
        inference="none",
        abort_on_first=False,
        do_owl_imports=False,
    )
    if not conforms:
        return False, [f"[FAIL] ISA/STATO evidence graph: {report}"]

    cycle_g = Graph()
    for triple in data_g:
        cycle_g.add(triple)
    ex = Namespace("https://example.org/hcmo/isa-crate/")
    schema = Namespace("http://schema.org/")
    cycle_g.add(
        (
            URIRef(ex["activity-summary-process"]),
            URIRef(schema.result),
            URIRef(ex["activity-file"]),
        )
    )
    cycle_conforms, _, _ = shacl_validate(
        cycle_g,
        shacl_graph=shapes_g,
        inference="none",
        abort_on_first=False,
        do_owl_imports=False,
    )
    if cycle_conforms:
        return False, ["[FAIL] ISA/STATO acyclic-process negative probe conformed"]
    return True, [
        "[OK]   ISA/STATO evidence graph: conformant",
        "[OK]   ISA/STATO acyclic-process negative probe: non-conformant",
    ]


def step_isa_roundtrip(ontology_graph: Graph) -> tuple[bool, list[str]]:
    """Validate the accepted HCMO/ISA/STATO round-trip policy fixture."""
    ok = True
    notes: list[str] = []
    fixture_root = ROOT / "examples" / "isa-roundtrip"
    canonical_path = fixture_root / "canonical.ttl"
    crate_path = fixture_root / "ro-crate-metadata.json"
    base = "https://example.org/hcmo/isa-roundtrip/"
    try:
        canonical = Graph().parse(canonical_path, format="turtle", publicID=base)
        crate = Graph().parse(crate_path, format="json-ld", publicID=base)
    except Exception as exc:  # noqa: BLE001
        return False, [f"[FAIL] ISA round-trip fixture parse: {exc}"]

    if not isomorphic(canonical, crate):
        ok = False
        notes.append("[FAIL] canonical HCMO RDF and extended ISA RO-Crate are not graph-isomorphic")
    else:
        notes.append(f"[OK]   lossless HCMO RDF/extended ISA RO-Crate graph: {len(canonical)} triples")

    monitored_animals = URIRef("https://w3id.org/hcmo/ontology/hcm#hasMonitoredAnimals")
    if any(canonical.triples((None, monitored_animals, None))):
        ok = False
        notes.append(
            "[FAIL] historical fixture materializes hcm:hasMonitoredAnimals without a single stated evaluation time"
        )
    else:
        notes.append("[OK]   housing history uses assignments, not a timeless monitored-animal shortcut")

    shapes = Graph()
    for rel in ("shapes/hcm-shapes.ttl", "shapes/isa-hcmo-roundtrip-shapes.ttl"):
        shapes.parse(ROOT / rel, format="turtle")
    conforms, _, report = shacl_validate(
        canonical,
        shacl_graph=shapes,
        ont_graph=ontology_graph,
        inference="rdfs",
        abort_on_first=False,
        do_owl_imports=False,
    )
    if not conforms:
        ok = False
        notes.append(f"[FAIL] ISA round-trip semantic invariants: {report}")
    else:
        notes.append("[OK]   ISA round-trip semantic invariants: conformant")

    # Move the second assignment's beginning one day earlier: the standard
    # profile must reject the resulting overlap without changing the fixture.
    overlap = Graph()
    for triple in canonical:
        overlap.add(triple)
    time = Namespace("http://www.w3.org/2006/time#")
    ex = Namespace(base)
    overlap.set(
        (
            URIRef(ex["instant-1-rehousing-begin"]),
            URIRef(time.inXSDDateTime),
            Literal(
                "2026-01-03T00:00:00+00:00",
                datatype=XSD.dateTime,
            ),
        )
    )
    overlap_conforms, _, _ = shacl_validate(
        overlap,
        shacl_graph=shapes,
        ont_graph=ontology_graph,
        inference="rdfs",
        abort_on_first=False,
        do_owl_imports=False,
    )
    if overlap_conforms:
        ok = False
        notes.append("[FAIL] overlapping-housing negative probe conformed")
    else:
        notes.append("[OK]   overlapping-housing negative probe: non-conformant")

    def copy_fixture() -> Graph:
        copied = Graph()
        for triple in canonical:
            copied.add(triple)
        return copied

    def require_nonconforming(label: str, probe: Graph) -> None:
        nonlocal ok
        probe_conforms, _, _ = shacl_validate(
            probe,
            shacl_graph=shapes,
            ont_graph=ontology_graph,
            inference="rdfs",
            abort_on_first=False,
            do_owl_imports=False,
        )
        if probe_conforms:
            ok = False
            notes.append(f"[FAIL] {label} negative probe conformed")
        else:
            notes.append(f"[OK]   {label} negative probe: non-conformant")

    hcm_bio = Namespace("https://w3id.org/hcmo/ontology/hcm/bio#")
    hcm_obs = Namespace("https://w3id.org/hcmo/ontology/hcm/obs#")
    prov = Namespace("http://www.w3.org/ns/prov#")
    schema = Namespace("http://schema.org/")

    orphan = copy_fixture()
    orphan.remove((ex["animal-2"], hcm_bio.hasHousingAssignment, ex["assignment-2"]))
    require_nonconforming("orphan HousingAssignment", orphan)

    reversed_interval = copy_fixture()
    reversed_interval.set(
        (
            ex["instant-2-begin"],
            time.inXSDDateTime,
            Literal("2026-01-12T00:00:00+00:00", datatype=XSD.dateTime),
        )
    )
    require_nonconforming("reversed housing interval", reversed_interval)

    incomplete_allocation = copy_fixture()
    incomplete_allocation.remove((ex["process-initial-allocation"], prov.used, ex["cage-2"]))
    require_nonconforming("incomplete allocation execution", incomplete_allocation)

    untyped_allocation = copy_fixture()
    untyped_allocation.remove((ex["process-initial-allocation"], RDF.type, prov.Activity))
    untyped_allocation.remove(
        (
            ex["process-initial-allocation"],
            RDF.type,
            URIRef("https://bioschemas.org/LabProcess"),
        )
    )
    require_nonconforming("untyped allocation execution", untyped_allocation)

    generated_animal = copy_fixture()
    generated_animal.add((ex["process-recording"], schema.result, ex["animal-2"]))
    require_nonconforming("unchanged animal as ISA result", generated_animal)

    wrong_observation_cage = copy_fixture()
    wrong_observation_cage.remove((ex["observation-1-day-1"], hcm_obs.occursIn, ex["cage-9"]))
    wrong_observation_cage.add((ex["observation-1-day-1"], hcm_obs.occursIn, ex["cage-1"]))
    require_nonconforming("observation outside authoritative housing", wrong_observation_cage)

    index_path = fixture_root / "competency_questions.yaml"
    try:
        index = yaml.safe_load(index_path.read_text(encoding="utf-8"))
        questions = index["questions"]
        for question in questions:
            query_path = ROOT / question["file"]
            actual = canonical_result_rows(canonical.query(query_path.read_text(encoding="utf-8")))
            expected = sorted(
                question["expected_answers"],
                key=lambda row: json.dumps(row, sort_keys=True),
            )
            if actual != expected:
                ok = False
                notes.append(
                    f"[FAIL] ISA round-trip CQ {question['id']}: "
                    f"expected={json.dumps(expected, sort_keys=True)} "
                    f"actual={json.dumps(actual, sort_keys=True)}"
                )
            else:
                notes.append(f"[OK]   ISA round-trip CQ {question['id']}: {len(actual)} exact answer(s)")
    except Exception as exc:  # noqa: BLE001
        ok = False
        notes.append(f"[FAIL] ISA round-trip competency questions: {exc}")

    return ok, notes


def step_mapping_contracts() -> tuple[bool, list[str]]:
    """Validate review-only semantic and exchange mapping registries."""
    ok = True
    notes: list[str] = []
    semantic_path = ROOT / "mappings" / "semantic" / "hcmo-external.sssom.tsv"
    metadata_path = ROOT / "mappings" / "semantic" / "hcmo-external.sssom.yml"
    required_columns = {
        "subject_id",
        "predicate_id",
        "object_id",
        "mapping_justification",
        "subject_source_version",
        "object_source_version",
        "author_label",
        "confidence",
        "review_status",
        "comment",
    }
    try:
        with semantic_path.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle, delimiter="\t"))
        metadata = yaml.safe_load(metadata_path.read_text(encoding="utf-8"))
        prefixes = metadata.get("prefix_map", {})
        if not metadata.get("mapping_set_id") or not metadata.get("license") or not prefixes:
            raise ValueError("SSSOM metadata lacks mapping_set_id, license, or prefix_map")
        columns = set(rows[0]) if rows else set()
        missing = required_columns - columns
        if missing:
            ok = False
            notes.append(f"[FAIL] semantic mapping registry missing columns: {sorted(missing)}")
        identities: set[tuple[str, str, str]] = set()
        allowed_statuses = {"deferred", "registry-only", "exchange-only", "rejected", "approved"}
        for row in rows:
            identity = (row["subject_id"], row["predicate_id"], row["object_id"])
            if identity in identities:
                raise ValueError(f"duplicate mapping identity {identity}")
            identities.add(identity)
            confidence = float(row["confidence"])
            if not 0 <= confidence <= 1:
                raise ValueError(f"confidence outside [0,1] for {identity}")
            if row["review_status"] not in allowed_statuses:
                raise ValueError(f"invalid review status for {identity}")
            for field in ("subject_id", "predicate_id", "object_id", "mapping_justification", "subject_source_version", "object_source_version"):
                value = row[field]
                if ":" not in value or value.split(":", 1)[0] not in prefixes:
                    raise ValueError(f"unresolved CURIE {value!r} in {field}")
            if row["predicate_id"] in {"owl:equivalentClass", "rdfs:subClassOf"} and row["review_status"] == "approved":
                raise ValueError(f"logical mapping entered approved state without a materialization review: {identity}")
        notes.append(f"[OK]   semantic mapping registry: {len(rows)} review-only mapping(s)")
    except Exception as exc:  # noqa: BLE001
        ok = False
        notes.append(f"[FAIL] semantic mapping registry: {exc}")

    try:
        exchange = yaml.safe_load((ROOT / "mappings" / "exchange" / "isa-ro-crate.yaml").read_text(encoding="utf-8"))
        targets = exchange["targets"]
        if targets["ro_crate"]["profile_uri"] != "https://w3id.org/ro/crate/1.2":
            raise ValueError("RO-Crate 1.2 target is not pinned")
        if targets["isa_ro_crate"]["profile_uri"] is not None:
            raise ValueError("an unconfirmed ISA profile URI was asserted")
        required_rule_fields = {"id", "source", "target", "direction", "cardinality", "rule", "loss"}
        ids = set()
        for rule in exchange["transformations"]:
            missing = required_rule_fields - set(rule)
            if missing:
                raise ValueError(f"exchange rule missing fields {sorted(missing)}")
            if rule["id"] in ids:
                raise ValueError(f"duplicate exchange rule id {rule['id']}")
            ids.add(rule["id"])
            if set(rule["loss"]) != {"isa_json", "isa_tab"}:
                raise ValueError(f"exchange rule {rule['id']} lacks both projection loss statements")
        for name in ("isa-json.yaml", "isa-tab.yaml"):
            loss_path = ROOT / "examples" / "isa-roundtrip" / "loss" / name
            loss = yaml.safe_load(loss_path.read_text(encoding="utf-8"))
            if loss.get("status") != "controlled-loss-contract" or not loss.get("lost_or_extension_dependent"):
                raise ValueError(f"incomplete controlled-loss manifest {name}")
            executable = loss.get("executable_scope", {})
            validator = executable.get("validator")
            if not validator or not (loss_path.parent / validator).resolve().is_file():
                raise ValueError(f"controlled-loss manifest {name} lacks an executable projection validator")
            losses = " ".join(loss["lost_or_extension_dependent"])
            if "factor" not in losses.lower() or "Sample" not in losses:
                raise ValueError(f"controlled-loss manifest {name} does not expose the Source/factor boundary")
        notes.append(
            f"[OK]   exchange registry: {len(ids)} directional rule(s), "
            "two controlled-loss manifests with an executable native overlap"
        )
    except Exception as exc:  # noqa: BLE001
        ok = False
        notes.append(f"[FAIL] exchange mapping registry: {exc}")
    return ok, notes


def canonical_result_rows(result) -> list[dict[str, str | None]]:
    variables = [str(variable) for variable in result.vars]
    rows = []
    for row in result:
        rows.append(
            {
                variable: None if row[index] is None else str(row[index])
                for index, variable in enumerate(variables)
            }
        )
    return sorted(rows, key=lambda row: json.dumps(row, sort_keys=True))


def step_queries(
    manifest: dict, graph: Graph
) -> tuple[bool, list[str], dict[str, int | None]]:
    ok = True
    notes = []
    rowcounts: dict[str, int | None] = {}
    try:
        questions = competency_questions(manifest)
    except Exception as exc:  # noqa: BLE001
        return False, [f"[FAIL] competency question index: {exc}"], rowcounts

    ids = [question.get("id") for question in questions]
    indexed_files = [question.get("file") for question in questions]
    discovered_files = {
        Path(path).relative_to(ROOT).as_posix()
        for path in glob.glob(str(ROOT / manifest["queries"]["dir"] / "cq-*.rq"))
    }
    if len(ids) != len(set(ids)):
        ok = False
        notes.append("[FAIL] competency question index contains duplicate IDs")
    if len(indexed_files) != len(set(indexed_files)):
        ok = False
        notes.append("[FAIL] competency question index contains duplicate files")
    missing_from_index = discovered_files - set(indexed_files)
    stale_index_entries = set(indexed_files) - discovered_files
    if missing_from_index or stale_index_entries:
        ok = False
        notes.append(
            "[FAIL] competency question file coverage: "
            f"unindexed={sorted(missing_from_index)}, "
            f"missing={sorted(stale_index_entries)}"
        )

    for question in questions:
        rel = question.get("file")
        question_id = question.get("id")
        expected = question.get("expected_answers")
        if not isinstance(rel, str) or not isinstance(question_id, str):
            ok = False
            notes.append(f"[FAIL] malformed competency question entry: {question}")
            continue
        if not isinstance(expected, list) or not all(
            isinstance(row, dict) for row in expected
        ):
            ok = False
            notes.append(
                f"[FAIL] query {question_id}: expected_answers must be a list "
                "of row mappings"
            )
            continue
        path = ROOT / rel
        try:
            res = graph.query(path.read_text(encoding="utf-8"))
            actual = canonical_result_rows(res)
            expected = sorted(
                expected, key=lambda row: json.dumps(row, sort_keys=True)
            )
            n = len(actual)
            rowcounts[rel] = n
            if actual != expected:
                ok = False
                notes.append(
                    f"[FAIL] query {question_id} ({rel}): exact-answer mismatch\n"
                    f"       expected={json.dumps(expected, sort_keys=True)}\n"
                    f"       actual={json.dumps(actual, sort_keys=True)}"
                )
            else:
                notes.append(
                    f"[OK]   query {question_id} ({rel}): {n} exact answer(s)"
                )
        except Exception as e:  # noqa: BLE001
            ok = False
            rowcounts[rel] = None
            notes.append(f"[FAIL] query {question_id} ({rel}): {e}")
    return ok, notes, rowcounts


def main() -> int:
    manifest = load_manifest()
    ontology_graph = merged_graph(manifest)
    all_ok = True

    print("== 1. Parse ontology and generated RDF artifacts ==")
    ok, notes = step_parse_all(manifest)
    print("\n".join(notes))
    all_ok &= ok

    print("\n== 2. Release and external vocabulary contracts ==")
    ok, notes = step_release_surfaces(manifest, ontology_graph)
    print("\n".join(notes))
    all_ok &= ok

    ok, notes = validate_contract(verify_network=False)
    print("\n".join(notes))
    all_ok &= ok

    print("\n== 3. SHACL (shapes vs examples) ==")
    ok, notes = step_shacl(manifest, ontology_graph)
    print("\n".join(notes))
    all_ok &= ok

    print("\n== 4. ISA/STATO evidence graph ==")
    ok, notes = step_isa_evidence()
    print("\n".join(notes))
    all_ok &= ok

    print("\n== 5. Accepted ISA/STATO round-trip policy ==")
    ok, notes = step_isa_roundtrip(ontology_graph)
    print("\n".join(notes))
    all_ok &= ok

    print("\n== 6. Mapping and exchange contracts ==")
    ok, notes = step_mapping_contracts()
    print("\n".join(notes))
    all_ok &= ok

    print("\n== 7. Competency queries vs ontology and positive examples ==")
    query_graph = evaluation_graph(manifest, ontology_graph)
    ok, notes, rowcounts = step_queries(manifest, query_graph)
    print("\n".join(notes))
    all_ok &= ok

    returned = [q for q, n in rowcounts.items() if n]
    print("\n== Summary ==")
    print(f"  ontology graph triples: {len(ontology_graph)}")
    print(f"  CQ evaluation graph triples: {len(query_graph)}")
    print(f"  queries returning rows: {returned or 'none'}")
    print(f"  result: {'PASS' if all_ok else 'FAIL'}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
