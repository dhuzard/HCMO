#!/usr/bin/env python3
"""Check the evidence inventory for the accepted A06 HCMO class audit.

This tool reads ontology and review sources. It never rewrites ontology terms.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re

import yaml
from rdflib import BNode, Graph, URIRef
from rdflib.namespace import OWL, RDF, RDFS

ROOT = Path(__file__).resolve().parent.parent
AUDIT_PATH = ROOT / "docs" / "CLASS-AUDIT-WORKING-NOTES.md"
LOCAL_PREFIX = "https://w3id.org/hcmo/ontology/hcm"

EXTERNAL_ANCHORS = {
    URIRef("http://purl.obolibrary.org/obo/BFO_0000019"),
    URIRef("http://purl.obolibrary.org/obo/BFO_0000027"),
    URIRef("http://purl.obolibrary.org/obo/BFO_0000040"),
    URIRef("http://purl.obolibrary.org/obo/IAO_0000030"),
    URIRef("http://www.w3.org/ns/sosa/Actuator"),
    URIRef("http://www.w3.org/ns/sosa/Observation"),
    URIRef("http://www.w3.org/ns/sosa/Property"),
    URIRef("http://www.w3.org/ns/sosa/Result"),
    URIRef("http://www.w3.org/ns/sosa/Sensor"),
    URIRef("https://schema.org/Person"),
    URIRef("https://schema.org/Place"),
    URIRef("https://w3id.org/semts/ontology/120#DataDimension"),
    URIRef("https://w3id.org/semts/ontology/120#TimeSeriesSegment"),
}

DECISIONS = (
    "keep",
    "revise definition",
    "revise axiom",
    "map",
    "deprecate",
    "needs evidence",
)

CANONICAL_PREFIXES = {
    "http://purl.obolibrary.org/obo/BFO_": "BFO:",
    "http://purl.obolibrary.org/obo/IAO_": "IAO:",
}


def load_manifest() -> dict:
    return yaml.safe_load((ROOT / "hcmo.yaml").read_text(encoding="utf-8"))


def active_module_paths(manifest: dict) -> list[str]:
    return [
        path for path in manifest["modules"] if not path.endswith("hcm-compat.ttl")
    ]


def load_modules(paths: list[str]) -> Graph:
    graph = Graph()
    for relative_path in paths:
        graph.parse(ROOT / relative_path, format="turtle")
    return graph


def qname(graph: Graph, term: URIRef) -> str:
    iri = str(term)
    for namespace, prefix in CANONICAL_PREFIXES.items():
        if iri.startswith(namespace):
            return prefix + iri.removeprefix(namespace)
    try:
        return graph.namespace_manager.normalizeUri(term)
    except Exception:
        return str(term)


def active_classes(graph: Graph) -> set[URIRef]:
    return {
        term
        for term in graph.subjects(RDF.type, OWL.Class)
        if isinstance(term, URIRef) and str(term).startswith(LOCAL_PREFIX)
    }


def restriction_fillers(graph: Graph) -> set[URIRef]:
    fillers = set()
    for restriction in graph.subjects(RDF.type, OWL.Restriction):
        for predicate in (OWL.someValuesFrom, OWL.allValuesFrom, OWL.onClass):
            fillers.update(
                value
                for value in graph.objects(restriction, predicate)
                if isinstance(value, URIRef)
            )
    return fillers


def referenced_external_anchors(graph: Graph) -> set[URIRef]:
    references = restriction_fillers(graph)
    for predicate in (RDFS.subClassOf, RDFS.domain, RDFS.range):
        references.update(
            value
            for value in graph.objects(None, predicate)
            if isinstance(value, URIRef)
        )
    references.update(
        class_iri
        for class_iri in graph.objects(None, RDF.type)
        if class_iri in {URIRef("https://schema.org/Person")}
    )
    return references & EXTERNAL_ANCHORS


def check_source_snapshot(manifest: dict) -> tuple[Graph, set[URIRef]]:
    graph = load_modules(active_module_paths(manifest))
    classes = active_classes(graph)
    anchors = referenced_external_anchors(graph)
    print("Class source snapshot")
    print(f"  Active local classes: {len(classes)}")
    print(f"  Directly used external class anchors: {len(anchors)}")
    if len(classes) != 29:
        raise SystemExit(f"ERROR: expected 29 active local classes, found {len(classes)}")
    if anchors != EXTERNAL_ANCHORS:
        missing = sorted(map(str, EXTERNAL_ANCHORS - anchors))
        unexpected = sorted(map(str, anchors - EXTERNAL_ANCHORS))
        raise SystemExit(
            "ERROR: external anchor snapshot mismatch; "
            f"missing={missing}; unexpected={unexpected}"
        )
    return graph, classes


def check_metadata(graph: Graph, classes: set[URIRef]) -> None:
    missing = []
    for term in sorted(classes, key=str):
        for predicate, field in (
            (RDFS.label, "label"),
            (RDFS.comment, "definition"),
            (RDFS.subClassOf, "asserted parent or restriction"),
        ):
            if graph.value(term, predicate) is None:
                missing.append(f"{term}: {field}")
    if missing:
        raise SystemExit("ERROR: active class metadata missing: " + "; ".join(missing))
    print("Class metadata completeness")
    print("  Active classes with label/definition/subClassOf: 29")


def check_generated_profile(graph: Graph, classes: set[URIRef]) -> None:
    profile = json.loads((ROOT / "dist" / "profile.json").read_text(encoding="utf-8"))
    profile_classes = {entry["iri"]: entry for entry in profile["classes"]}
    mismatches = []
    for term in sorted(classes, key=str):
        entry = profile_classes.get(str(term))
        if entry is None:
            mismatches.append(f"{term}: absent from dist/profile.json")
            continue
        expected_label = str(graph.value(term, RDFS.label))
        expected_comment = str(graph.value(term, RDFS.comment))
        if entry.get("label") != expected_label:
            mismatches.append(f"{term}: label differs from dist/profile.json")
        if entry.get("comment") != expected_comment:
            mismatches.append(f"{term}: definition differs from dist/profile.json")
    if mismatches:
        raise SystemExit("ERROR: generated profile mismatch: " + "; ".join(mismatches))
    print("Generated profile agreement")
    print("  Active class IRI/label/definition records matched: 29")


def check_documented_decisions(graph: Graph, classes: set[URIRef]) -> None:
    notes = AUDIT_PATH.read_text(encoding="utf-8")
    decision_pattern = "|".join(map(re.escape, DECISIONS))
    rows = re.findall(
        rf"^\| `([^`]+)` \| `({decision_pattern})` \|",
        notes,
        flags=re.MULTILINE,
    )
    documented = [term for term, _ in rows]
    expected = {qname(graph, term) for term in classes}
    if len(documented) != len(set(documented)):
        raise SystemExit("ERROR: duplicate active class decision rows")
    if set(documented) != expected:
        missing = sorted(expected - set(documented))
        unexpected = sorted(set(documented) - expected)
        raise SystemExit(
            "ERROR: active class decision coverage mismatch; "
            f"missing={missing}; unexpected={unexpected}"
        )
    decision_counts = Counter(decision for _, decision in rows)
    expected_counts = Counter({"keep": 23, "needs evidence": 6})
    if decision_counts != expected_counts:
        raise SystemExit(
            "ERROR: active class decision totals mismatch; "
            f"expected={dict(expected_counts)}; actual={dict(decision_counts)}"
        )

    anchor_rows = re.findall(
        rf"^\| `([^`]+)` \| [^|]+ \| [^|]+ \| `({decision_pattern})` \|",
        notes,
        flags=re.MULTILINE,
    )
    documented_anchors = [term for term, _ in anchor_rows]
    expected_anchors = {qname(graph, term) for term in EXTERNAL_ANCHORS}
    if len(documented_anchors) != len(set(documented_anchors)):
        raise SystemExit("ERROR: duplicate external class anchor rows")
    if set(documented_anchors) != expected_anchors:
        missing = sorted(expected_anchors - set(documented_anchors))
        unexpected = sorted(set(documented_anchors) - expected_anchors)
        raise SystemExit(
            "ERROR: external class anchor coverage mismatch; "
            f"missing={missing}; unexpected={unexpected}"
        )
    print("Documented class decisions")
    print(f"  Active local decision rows: {len(documented)}")
    print(f"  External anchor rows: {len(documented_anchors)}")


def render_expression(graph: Graph, value) -> str:
    if isinstance(value, URIRef):
        return qname(graph, value)
    if not isinstance(value, BNode):
        return "-"
    if (value, RDF.type, OWL.Restriction) in graph:
        property_iri = graph.value(value, OWL.onProperty)
        for predicate, symbol in (
            (OWL.someValuesFrom, "some"),
            (OWL.allValuesFrom, "only"),
            (OWL.onClass, "onClass"),
        ):
            filler = graph.value(value, predicate)
            if filler is not None:
                prop = qname(graph, property_iri) if isinstance(property_iri, URIRef) else "?"
                target = qname(graph, filler) if isinstance(filler, URIRef) else "anonymous"
                return f"{prop} {symbol} {target}"
        return "restriction"
    return "anonymous class"


def print_catalog(manifest: dict, graph: Graph, classes: set[URIRef]) -> None:
    print("\nActive class source catalogue")
    print("| Module | Class | Definition | Asserted parents/restrictions |")
    print("| --- | --- | --- | --- |")
    for path in active_module_paths(manifest):
        module_graph = Graph().parse(ROOT / path, format="turtle")
        module_classes = active_classes(module_graph)
        for term in sorted(module_classes, key=str):
            definition = str(graph.value(term, RDFS.comment)).replace("|", "\\|")
            parents = "; ".join(
                render_expression(graph, value)
                for value in graph.objects(term, RDFS.subClassOf)
            )
            print(
                f"| `{Path(path).stem}` | `{qname(graph, term)}` | "
                f"{definition} | `{parents}` |"
            )

    print("\nDirectly used external class anchors")
    print("| Anchor |")
    print("| --- |")
    for term in sorted(EXTERNAL_ANCHORS, key=str):
        print(f"| `{qname(graph, term)}` |")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--catalog",
        action="store_true",
        help="Print the asserted class catalogue used during human review.",
    )
    args = parser.parse_args()
    manifest = load_manifest()
    graph, classes = check_source_snapshot(manifest)
    check_metadata(graph, classes)
    check_generated_profile(graph, classes)
    check_documented_decisions(graph, classes)
    if args.catalog:
        print_catalog(manifest, graph, classes)
    print("Class audit checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
