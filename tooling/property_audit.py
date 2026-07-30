#!/usr/bin/env python3
"""Run reproducible checks that support the HCMO property audit.

This tool reports source counts and tests selected entailments. It does not
write an inventory or modify ontology sources.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import re

import yaml
from owlrl import DeductiveClosure, OWLRL_Semantics
from rdflib import BNode, Graph, Literal, Namespace, URIRef
from rdflib.namespace import OWL, RDF, RDFS

ROOT = Path(__file__).resolve().parent.parent
HCM = Namespace("https://w3id.org/hcmo/ontology/hcm#")
HCM_BIO = Namespace("https://w3id.org/hcmo/ontology/hcm/bio#")
HCM_ENV = Namespace("https://w3id.org/hcmo/ontology/hcm/env#")
HCM_OBS = Namespace("https://w3id.org/hcmo/ontology/hcm/obs#")
HCM_TECH = Namespace("https://w3id.org/hcmo/ontology/hcm/tech#")
SCHEMA = Namespace("https://schema.org/")
SOSA = Namespace("http://www.w3.org/ns/sosa/")
EX = Namespace("https://w3id.org/hcmo/audit/example#")
DCTERMS_SOURCE = URIRef("http://purl.org/dc/terms/source")
DCTERMS_IS_REPLACED_BY = URIRef("http://purl.org/dc/terms/isReplacedBy")


def load_manifest() -> dict:
    return yaml.safe_load((ROOT / "hcmo.yaml").read_text(encoding="utf-8"))


def load_modules(paths: list[str]) -> Graph:
    graph = Graph()
    for relative_path in paths:
        graph.parse(ROOT / relative_path, format="turtle")
    return graph


def active_module_paths(manifest: dict) -> list[str]:
    return [
        path for path in manifest["modules"] if not path.endswith("hcm-compat.ttl")
    ]


def compatibility_module_paths(manifest: dict) -> list[str]:
    return [
        path for path in manifest["modules"] if path.endswith("hcm-compat.ttl")
    ]


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
    active_paths = active_module_paths(manifest)
    compatibility_paths = compatibility_module_paths(manifest)
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


def check_property_metadata(manifest: dict) -> None:
    active_graph = load_modules(active_module_paths(manifest))
    compatibility_graph = load_modules(compatibility_module_paths(manifest))
    active_object, active_datatype = declared_properties(active_graph)
    compatibility_object, compatibility_datatype = declared_properties(
        compatibility_graph
    )

    missing: list[str] = []
    for term in sorted(active_object | active_datatype, key=str):
        required = {
            RDFS.label: "label",
            RDFS.comment: "definition",
            RDFS.domain: "domain",
            RDFS.range: "range",
        }
        for predicate, field in required.items():
            if active_graph.value(term, predicate) is None:
                missing.append(f"{term}: {field}")
    if missing:
        raise SystemExit("ERROR: active property metadata missing: " + "; ".join(missing))

    compatibility_missing: list[str] = []
    type_changes: list[tuple[URIRef, URIRef]] = []
    replacements = 0
    for term in sorted(compatibility_object | compatibility_datatype, key=str):
        for predicate, field in (
            (RDFS.label, "label"),
            (RDFS.comment, "definition"),
            (DCTERMS_SOURCE, "source"),
            (OWL.deprecated, "deprecated marker"),
        ):
            if compatibility_graph.value(term, predicate) is None:
                compatibility_missing.append(f"{term}: {field}")
        replacement = compatibility_graph.value(term, DCTERMS_IS_REPLACED_BY)
        if not isinstance(replacement, URIRef):
            continue
        replacements += 1
        old_object = term in compatibility_object
        new_object = replacement in active_object
        new_datatype = replacement in active_datatype
        if not new_object and not new_datatype:
            compatibility_missing.append(f"{term}: undeclared replacement {replacement}")
        elif old_object != new_object:
            type_changes.append((term, replacement))
    if compatibility_missing:
        raise SystemExit(
            "ERROR: compatibility property metadata missing: "
            + "; ".join(compatibility_missing)
        )

    print("Property metadata completeness")
    print("  Active properties with label/definition/domain/range: 81")
    print("  Compatibility properties with label/definition/source/deprecation: 49")
    print(f"  Declared compatibility replacements: {replacements}")
    print(f"  Type-changing replacements requiring migration: {len(type_changes)}")
    for old, new in type_changes:
        print(f"    - {old} -> {new}")


def check_documented_decisions(manifest: dict) -> None:
    active_graph = load_modules(active_module_paths(manifest))
    compatibility_graph = load_modules(compatibility_module_paths(manifest))
    for prefix, namespace in active_graph.namespaces():
        compatibility_graph.bind(prefix, namespace)
    active_object, active_datatype = declared_properties(active_graph)
    compatibility_object, compatibility_datatype = declared_properties(
        compatibility_graph
    )
    expected_active = {
        qname(active_graph, term) for term in active_object | active_datatype
    }
    expected_compatibility = {
        qname(compatibility_graph, term)
        for term in compatibility_object | compatibility_datatype
    }

    notes = (ROOT / "docs" / "PROPERTY-AUDIT-WORKING-NOTES.md").read_text(
        encoding="utf-8"
    )
    active_rows = re.findall(
        r"^\| `([^`]+)` \| `(keep|needs evidence|revise definition|revise axiom|split|deprecate)` \|",
        notes,
        flags=re.MULTILINE,
    )
    compatibility_rows = re.findall(
        r"^\| `([^`]+)` \| (?:`[^`]+`|-) \| `keep deprecated` \|",
        notes,
        flags=re.MULTILINE,
    )
    documented_active = [term for term, _ in active_rows]
    if len(documented_active) != len(set(documented_active)):
        raise SystemExit("ERROR: duplicate active property decision rows")
    if set(documented_active) != expected_active:
        missing = sorted(expected_active - set(documented_active))
        unexpected = sorted(set(documented_active) - expected_active)
        raise SystemExit(
            f"ERROR: active decision coverage mismatch; missing={missing}; "
            f"unexpected={unexpected}"
        )
    if len(compatibility_rows) != len(set(compatibility_rows)):
        raise SystemExit("ERROR: duplicate compatibility property decision rows")
    if set(compatibility_rows) != expected_compatibility:
        missing = sorted(expected_compatibility - set(compatibility_rows))
        unexpected = sorted(set(compatibility_rows) - expected_compatibility)
        raise SystemExit(
            f"ERROR: compatibility decision coverage mismatch; missing={missing}; "
            f"unexpected={unexpected}"
        )
    print("Documented property decisions")
    print(f"  Active local decision rows: {len(documented_active)}")
    print(f"  Compatibility decision rows: {len(compatibility_rows)}")


def closure_for(assertion: tuple[URIRef, URIRef, URIRef], manifest: dict) -> Graph:
    graph = load_modules(active_module_paths(manifest))
    graph.add(assertion)
    DeductiveClosure(OWLRL_Semantics).expand(graph)
    return graph


def require(graph: Graph, triple: tuple[URIRef, URIRef, URIRef], name: str) -> None:
    if triple not in graph:
        raise SystemExit(f"ERROR: expected entailment missing: {name}")
    print(f"  [entailed] {name}")


def require_absent(
    graph: Graph, triple: tuple[URIRef, URIRef, URIRef], name: str
) -> None:
    if triple in graph:
        raise SystemExit(f"ERROR: unintended entailment present: {name}")
    print(f"  [not entailed] {name}")


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


def check_priority_entailments(manifest: dict) -> None:
    enclosure = EX["enclosure"]
    place = EX["facility-place"]
    location_graph = closure_for((enclosure, HCM.locatedIn, place), manifest)
    print("locatedIn assertion consequences")
    require(location_graph, (enclosure, RDF.type, HCM.Enclosure), "subject rdf:type Enclosure")
    require(location_graph, (place, RDF.type, SCHEMA.Place), "object rdf:type schema:Place")

    profile = EX["environment-holder"]
    temperature = EX["ambient-temperature"]
    environment_graph = closure_for(
        (profile, HCM_ENV.AmbientTemperature, temperature), manifest
    )
    union_domain = environment_graph.value(HCM_ENV.AmbientTemperature, RDFS.domain)
    if not isinstance(union_domain, BNode):
        raise SystemExit("ERROR: AmbientTemperature union domain not found")
    print("shared environmental-property assertion consequences")
    require(
        environment_graph,
        (profile, RDF.type, union_domain),
        "subject rdf:type asserted anonymous union",
    )
    require(
        environment_graph,
        (temperature, RDF.type, HCM_ENV.EnvironmentalProperty),
        "object rdf:type EnvironmentalProperty",
    )
    for named_class in (
        HCM_ENV.EnvironmentProfile,
        HCM_ENV.MeasurementSpecification,
        HCM_OBS.EnvironmentObservation,
    ):
        require_absent(
            environment_graph,
            (profile, RDF.type, named_class),
            f"subject rdf:type {named_class.split('#')[-1]}",
        )

    observation = EX["observation"]
    condition = EX["condition"]
    condition_graph = closure_for(
        (observation, HCM_OBS.hasCondition, condition), manifest
    )
    print("hasCondition assertion consequences")
    require(
        condition_graph,
        (observation, RDF.type, SOSA.Observation),
        "subject rdf:type sosa:Observation",
    )

    animal = EX["animal"]
    occupancy_graph = closure_for(
        (enclosure, HCM.hasMonitoredAnimals, animal), manifest
    )
    print("hasMonitoredAnimals assertion consequences")
    require(
        occupancy_graph,
        (enclosure, RDF.type, HCM.MonitoredEnclosure),
        "subject rdf:type MonitoredEnclosure",
    )
    require(
        occupancy_graph,
        (animal, RDF.type, HCM_BIO.Subject),
        "object rdf:type Subject",
    )

    behavior_observation = EX["behavior-observation"]
    shortcut_graph = closure_for(
        (animal, HCM_BIO.hasBehaviorObservation, behavior_observation), manifest
    )
    print("subject-to-observation shortcut consequences")
    require(
        shortcut_graph,
        (animal, RDF.type, HCM_BIO.Subject),
        "subject rdf:type Subject",
    )
    require(
        shortcut_graph,
        (behavior_observation, RDF.type, HCM_OBS.BehaviorObservation),
        "object rdf:type BehaviorObservation",
    )
    require_absent(
        shortcut_graph,
        (behavior_observation, SOSA.hasFeatureOfInterest, animal),
        "observation sosa:hasFeatureOfInterest subject",
    )

    sensor = EX["sensor"]
    observed_property = EX["observed-property"]
    captures_graph = closure_for(
        (sensor, HCM_TECH.captures, observed_property), manifest
    )
    print("captures assertion consequences")
    require(
        captures_graph,
        (sensor, SOSA.observes, observed_property),
        "sensor sosa:observes property",
    )
    require(
        captures_graph,
        (sensor, RDF.type, HCM_TECH.Sensor),
        "subject rdf:type Sensor",
    )
    require(
        captures_graph,
        (observed_property, RDF.type, SOSA.Property),
        "object rdf:type sosa:Property",
    )


def qname(graph: Graph, term: URIRef) -> str:
    try:
        return graph.namespace_manager.normalizeUri(term)
    except Exception:  # noqa: BLE001
        return f"<{term}>"


def render_class_expression(graph: Graph, term: URIRef | BNode | None) -> str:
    if term is None:
        return "-"
    if isinstance(term, URIRef):
        return qname(graph, term)
    union_head = graph.value(term, OWL.unionOf)
    if union_head is not None:
        members = [qname(graph, value) for value in graph.items(union_head)]
        return "union(" + ", ".join(members) + ")"
    return "anonymous expression"


def property_usage(manifest: dict, graph: Graph, term: URIRef) -> str:
    uses: list[str] = []
    restriction_count = sum(1 for _ in graph.subjects(OWL.onProperty, term))
    if restriction_count:
        uses.append(f"restriction:{restriction_count}")

    shape_graph = Graph().parse(ROOT / manifest["shapes"], format="turtle")
    shape_count = sum(1 for _ in shape_graph.subjects(URIRef("http://www.w3.org/ns/shacl#path"), term))
    if shape_count:
        uses.append(f"shape:{shape_count}")

    example_names = []
    for path in sorted((ROOT / "examples").glob("*.ttl")):
        example_graph = Graph().parse(path, format="turtle")
        if any(True for _ in example_graph.triples((None, term, None))):
            example_names.append(path.stem)
    if example_names:
        uses.append("examples:" + ",".join(example_names))

    compact = qname(graph, term)
    cq_ids = []
    query_index = yaml.safe_load(
        (ROOT / manifest["queries"]["index"]).read_text(encoding="utf-8")
    )
    for question in query_index["questions"]:
        query_text = (ROOT / question["file"]).read_text(encoding="utf-8")
        if compact in query_text or f"<{term}>" in query_text:
            cq_ids.append(question["id"])
    if cq_ids:
        uses.append("cq:" + ",".join(cq_ids))
    return "; ".join(uses) if uses else "none found"


def print_catalog(manifest: dict) -> None:
    active_paths = active_module_paths(manifest)
    active_graph = load_modules(active_paths)
    compatibility_graph = load_modules(compatibility_module_paths(manifest))
    for prefix, namespace in active_graph.namespaces():
        compatibility_graph.bind(prefix, namespace)

    print("\nActive property source catalogue")
    print("| Module | Property | Kind | Asserted domain | Asserted range | Parent | Inverse | Uses |")
    print("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for path in active_paths:
        module_graph = Graph().parse(ROOT / path, format="turtle")
        properties = set(module_graph.subjects(RDF.type, OWL.ObjectProperty))
        properties.update(module_graph.subjects(RDF.type, OWL.DatatypeProperty))
        for term in sorted(properties, key=str):
            kind = (
                "object"
                if (term, RDF.type, OWL.ObjectProperty) in module_graph
                else "datatype"
            )
            domain = render_class_expression(active_graph, active_graph.value(term, RDFS.domain))
            range_value = render_class_expression(active_graph, active_graph.value(term, RDFS.range))
            parent = active_graph.value(term, RDFS.subPropertyOf)
            inverse = active_graph.value(term, OWL.inverseOf)
            uses = property_usage(manifest, active_graph, term)
            print(
                f"| `{Path(path).stem}` | `{qname(active_graph, term)}` | {kind} | "
                f"`{domain}` | `{range_value}` | "
                f"`{qname(active_graph, parent) if isinstance(parent, URIRef) else '-'}` | "
                f"`{qname(active_graph, inverse) if isinstance(inverse, URIRef) else '-'}` | "
                f"{uses} |"
            )

    print("\nDeprecated compatibility property catalogue")
    print("| Property | Kind | Replacement |")
    print("| --- | --- | --- |")
    compatibility_object, compatibility_datatype = declared_properties(
        compatibility_graph
    )
    for term in sorted(compatibility_object | compatibility_datatype, key=str):
        kind = "object" if term in compatibility_object else "datatype"
        replacement = compatibility_graph.value(term, DCTERMS_IS_REPLACED_BY)
        replacement_text = (
            qname(compatibility_graph, replacement)
            if isinstance(replacement, URIRef)
            else "-"
        )
        print(
            f"| `{qname(compatibility_graph, term)}` | {kind} | `{replacement_text}` |"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--catalog",
        action="store_true",
        help="Print asserted active and compatibility property catalogues.",
    )
    args = parser.parse_args()
    manifest = load_manifest()
    check_source_snapshot(manifest)
    check_property_metadata(manifest)
    check_documented_decisions(manifest)
    print()
    check_monitored_installation(manifest)
    print()
    check_priority_entailments(manifest)
    if args.catalog:
        print_catalog(manifest)
    print("Property audit checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
