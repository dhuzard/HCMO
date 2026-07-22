#!/usr/bin/env python3
"""Run reproducible checks that support the HCMO property audit.

This tool reports source counts and tests selected entailments. It does not
write an inventory or modify ontology sources.
"""
from __future__ import annotations

from pathlib import Path

import yaml
from owlrl import DeductiveClosure, OWLRL_Semantics
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import OWL, RDF

ROOT = Path(__file__).resolve().parent.parent
HCM = Namespace("https://w3id.org/hcmo/ontology/hcm#")
HCM_TECH = Namespace("https://w3id.org/hcmo/ontology/hcm/tech#")
EX = Namespace("https://w3id.org/hcmo/audit/example#")


def load_manifest() -> dict:
    return yaml.safe_load((ROOT / "hcmo.yaml").read_text(encoding="utf-8"))


def load_modules(paths: list[str]) -> Graph:
    graph = Graph()
    for relative_path in paths:
        graph.parse(ROOT / relative_path, format="turtle")
    return graph


def declared_properties(graph: Graph) -> tuple[set[URIRef], set[URIRef]]:
    object_properties = set(graph.subjects(RDF.type, OWL.ObjectProperty))
    datatype_properties = set(graph.subjects(RDF.type, OWL.DatatypeProperty))
    return object_properties, datatype_properties


def is_deprecated(graph: Graph, term: URIRef) -> bool:
    return any(
        isinstance(value, Literal) and bool(value.toPython())
        for value in graph.objects(term, OWL.deprecated)
    )


def check_source_snapshot(manifest: dict) -> None:
    active_paths = [
        path for path in manifest["modules"] if not path.endswith("hcm-compat.ttl")
    ]
    compatibility_paths = [
        path for path in manifest["modules"] if path.endswith("hcm-compat.ttl")
    ]
    active_graph = load_modules(active_paths)
    compatibility_graph = load_modules(compatibility_paths)

    active_object, active_datatype = declared_properties(active_graph)
    active = {
        term
        for term in active_object | active_datatype
        if not is_deprecated(active_graph, term)
    }
    compatibility_object, compatibility_datatype = declared_properties(
        compatibility_graph
    )
    compatibility = {
        term
        for term in compatibility_object | compatibility_datatype
        if is_deprecated(compatibility_graph, term)
    }

    print("Property source snapshot")
    print(f"  Active object properties: {len(active_object)}")
    print(f"  Active datatype properties: {len(active_datatype)}")
    print(f"  Active non-deprecated total: {len(active)}")
    print(f"  Deprecated compatibility total: {len(compatibility)}")

    if len(active) != 81:
        raise SystemExit(f"ERROR: expected 81 active properties, found {len(active)}")
    if len(compatibility) != 49:
        raise SystemExit(
            "ERROR: expected 49 deprecated compatibility properties, "
            f"found {len(compatibility)}"
        )


def closure_for(assertion: tuple[URIRef, URIRef, URIRef], manifest: dict) -> Graph:
    active_paths = [
        path for path in manifest["modules"] if not path.endswith("hcm-compat.ttl")
    ]
    graph = load_modules(active_paths)
    graph.add(assertion)
    DeductiveClosure(OWLRL_Semantics).expand(graph)
    return graph


def require(graph: Graph, triple: tuple[URIRef, URIRef, URIRef], name: str) -> None:
    if triple not in graph:
        raise SystemExit(f"ERROR: expected entailment missing: {name}")
    print(f"  [entailed] {name}")


def check_monitored_installation(manifest: dict) -> None:
    cage = EX["portable-sensor-cage"]
    sensor = EX["portable-sensor"]

    monitored_graph = closure_for((cage, HCM_TECH.monitoredBy, sensor), manifest)
    print("monitoredBy assertion consequences")
    require(
        monitored_graph,
        (sensor, HCM_TECH.installedIn, cage),
        "sensor installedIn cage",
    )
    require(
        monitored_graph,
        (cage, RDF.type, HCM.MonitoredEnclosure),
        "cage rdf:type MonitoredEnclosure",
    )
    require(
        monitored_graph,
        (sensor, RDF.type, HCM_TECH.Sensor),
        "sensor rdf:type Sensor",
    )

    installed_graph = closure_for((sensor, HCM_TECH.installedIn, cage), manifest)
    print("installedIn assertion consequences")
    require(
        installed_graph,
        (cage, HCM_TECH.monitoredBy, sensor),
        "cage monitoredBy sensor",
    )
    require(
        installed_graph,
        (sensor, RDF.type, HCM_TECH.Sensor),
        "sensor rdf:type Sensor",
    )
    require(
        installed_graph,
        (cage, RDF.type, HCM.MonitoredEnclosure),
        "cage rdf:type MonitoredEnclosure",
    )


def main() -> int:
    manifest = load_manifest()
    check_source_snapshot(manifest)
    print()
    check_monitored_installation(manifest)
    print("Property audit checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
