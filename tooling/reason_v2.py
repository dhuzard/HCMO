#!/usr/bin/env python3
"""Run an OWL reasoner over the clean HCMO v2 artifact.

This is the reproducible counterpart to the Protege/HermiT check requested for
the v2 review. It targets the clean BioPortal/Protege RDF/XML file, which is
generated from ontology/v2/modules while excluding unresolved placeholders.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import owlready2.reasoning as owl_reasoning
from owlready2 import default_world, get_ontology, sync_reasoner
from rdflib import Graph, URIRef
from rdflib.namespace import RDF, OWL

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SOURCE = ROOT / "ontology" / "v2" / "hcmo-v2-merged-clean.owl"
DEFAULT_TTL = ROOT / "ontology" / "v2" / "hcmo-v2-merged-clean.ttl"


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def build_clean() -> None:
    cmd = [sys.executable, str(ROOT / "tooling" / "build_v2_clean.py")]
    subprocess.run(cmd, cwd=ROOT, check=True)


def parse_graphs(source: Path, ttl: Path | None) -> tuple[int, int, int, int]:
    graph = Graph().parse(source)
    if ttl and ttl.exists():
        Graph().parse(ttl, format="turtle")

    classes = set(graph.subjects(RDF.type, OWL.Class))
    object_props = set(graph.subjects(RDF.type, OWL.ObjectProperty))
    data_props = set(graph.subjects(RDF.type, OWL.DatatypeProperty))
    both = object_props & data_props
    if both:
        values = ", ".join(sorted(str(x) for x in both))
        raise SystemExit(f"ERROR: properties typed both object and datatype: {values}")
    return len(graph), len(classes), len(object_props), len(data_props)


def count_unknown(source: Path) -> int:
    graph = Graph().parse(source)
    unknown = {
        term
        for triple in graph
        for term in triple
        if isinstance(term, URIRef) and "owl-ontologies.com/UNKNOWN" in str(term)
    }
    return len(unknown)


def run_hermit(source: Path, java_memory: int) -> list[str]:
    owl_reasoning.JAVA_MEMORY = java_memory
    ontology = get_ontology(str(source.resolve())).load()
    loaded_classes = len(list(ontology.classes()))
    print(f"Loaded classes: {loaded_classes}")
    sync_reasoner(debug=1)
    return [cls.name for cls in default_world.inconsistent_classes()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        type=Path,
        default=DEFAULT_SOURCE,
        help="Clean RDF/XML artifact to reason over.",
    )
    parser.add_argument(
        "--ttl",
        type=Path,
        default=DEFAULT_TTL,
        help="Optional clean Turtle artifact to parse as a companion check.",
    )
    parser.add_argument(
        "--build-clean",
        action="store_true",
        help="Regenerate clean v2 artifacts before reasoning.",
    )
    parser.add_argument(
        "--java-memory",
        type=int,
        default=512,
        help="HermiT JVM heap size in MB. 512 works on local 32-bit Java.",
    )
    args = parser.parse_args()

    if args.build_clean:
        build_clean()

    source = args.source if args.source.is_absolute() else ROOT / args.source
    ttl = args.ttl if args.ttl is None or args.ttl.is_absolute() else ROOT / args.ttl
    if not source.exists():
        raise SystemExit(f"ERROR: source not found: {rel(source)}")

    triples, classes, object_props, data_props = parse_graphs(source, ttl)
    unknown_count = count_unknown(source)
    print(f"Source: {rel(source)}")
    print(f"Triples: {triples}")
    print(f"Classes: {classes}")
    print(f"Object properties: {object_props}")
    print(f"Datatype properties: {data_props}")
    print(f"UNKNOWN IRIs: {unknown_count}")

    inconsistent = run_hermit(source, args.java_memory)
    print(f"Inconsistent classes: {len(inconsistent)}")
    for name in inconsistent:
        print(f"  - {name}")

    if unknown_count:
        raise SystemExit("ERROR: clean artifact contains UNKNOWN placeholder IRIs")
    if inconsistent:
        raise SystemExit("ERROR: HermiT reported inconsistent classes")
    print("HermiT consistency check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
