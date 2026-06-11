#!/usr/bin/env python3
"""Regenerate the dist/ artifacts and profile.json from ontology/modules/ + hcmo.yaml.

Everything written to dist/ is GENERATED. Do not hand-edit dist/ files; edit the
hand-authored modules in ontology/modules/ and re-run this script.

Outputs (paths come from hcmo.yaml):
  dist/hcmo.ttl   merged graph, canonicalized + sorted Turtle (reproducible diffs)
  dist/hcmo.owl   merged graph, RDF/XML
  dist/hcmo.json  merged graph, JSON-LD
  dist/profile.json  flat term inventory {namespace, version, classes, ...}

The build is idempotent and reproducible: blank nodes are canonicalized with
rdflib.compare.to_canonical_graph so the same modules always serialize identically.
"""
from __future__ import annotations

import os
import sys

# Pin the hash seed so set/dict iteration in the RDF/XML and JSON-LD serializers
# is stable across separate process runs (reproducible diffs). Re-exec once.
if os.environ.get("PYTHONHASHSEED") != "0":
    os.environ["PYTHONHASHSEED"] = "0"
    os.execv(sys.executable, [sys.executable] + sys.argv)

import json
from pathlib import Path

import yaml
import rdflib
from rdflib import RDF, RDFS, OWL, URIRef, Literal, Graph, Namespace
from rdflib.compare import to_canonical_graph

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "hcmo.yaml"

IAO_DEF = URIRef("http://purl.obolibrary.org/obo/IAO_0000115")
DCTERMS = Namespace("http://purl.org/dc/terms/")
DC = Namespace("http://purl.org/dc/elements/1.1/")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")

GENERATED_HEADER = (
    "# DO NOT EDIT — GENERATED FILE.\n"
    "# Produced by tooling/build.py from ontology/modules/*.ttl.\n"
    "# Edit the modules and re-run `python tooling/build.py` to regenerate.\n"
)


def load_manifest() -> dict:
    with open(MANIFEST) as f:
        return yaml.safe_load(f)


def load_merged(manifest: dict) -> Graph:
    g = Graph()
    for rel in manifest["modules"]:
        p = ROOT / rel
        if not p.exists():
            raise SystemExit(f"ERROR: module not found: {rel}")
        g.parse(p, format="turtle")
    return g


def bind_prefixes(g: Graph, manifest: dict) -> None:
    prefix = manifest.get("prefix", "hcm")
    ns = manifest.get("namespace")
    g.bind(prefix, Namespace(ns), replace=True)
    g.bind("hcm-bio", Namespace("https://w3id.org/hcmo/ontology/hcm/bio#"), replace=True)
    g.bind("hcm-env", Namespace("https://w3id.org/hcmo/ontology/hcm/env#"), replace=True)
    g.bind("hcm-obs", Namespace("https://w3id.org/hcmo/ontology/hcm/obs#"), replace=True)
    g.bind("owl", OWL, replace=True)
    g.bind("rdfs", RDFS, replace=True)
    g.bind("dc", DC, replace=True)
    g.bind("dcterms", DCTERMS, replace=True)
    g.bind("schema", Namespace("https://schema.org/"), replace=True)
    g.bind("skos", SKOS, replace=True)
    g.bind("sosa", Namespace("http://www.w3.org/ns/sosa/"), replace=True)
    g.bind("time", Namespace("http://www.w3.org/2006/time#"), replace=True)
    g.bind("semts", Namespace("https://w3id.org/semts/ontology/120#"), replace=True)
    g.bind("mod", Namespace("https://w3id.org/mod#"), replace=True)
    g.bind("UNKNOWN", Namespace("http://www.owl-ontologies.com/UNKNOWN#"), replace=True)
    g.bind("ns", Namespace("http://www.owl-ontologies.com/ns#"), replace=True)


def label_of(g: Graph, s) -> str | None:
    v = g.value(s, RDFS.label)
    return str(v) if v is not None else None


def comment_of(g: Graph, s) -> str | None:
    for p in (RDFS.comment, IAO_DEF, DCTERMS.description, SKOS.definition):
        v = g.value(s, p)
        if v is not None:
            return str(v)
    return None


def terms(g: Graph, rdf_type) -> list:
    return sorted(
        (s for s in g.subjects(RDF.type, rdf_type) if isinstance(s, URIRef)),
        key=str,
    )


def build_profile(g: Graph, manifest: dict) -> dict:
    def entry(s):
        return {"iri": str(s), "label": label_of(g, s), "comment": comment_of(g, s)}

    classes = [entry(s) for s in terms(g, OWL.Class)]
    obj_props = [entry(s) for s in terms(g, OWL.ObjectProperty)]
    dt_props = [entry(s) for s in terms(g, OWL.DatatypeProperty)]
    ann_props = [entry(s) for s in terms(g, OWL.AnnotationProperty)]
    return {
        "namespace": manifest["namespace"],
        "version": manifest["version"],
        "ontology_iri": manifest["ontology_iri"],
        "version_iri": manifest.get("version_iri"),
        "classes": classes,
        "object_properties": obj_props,
        "datatype_properties": dt_props,
        "annotation_properties": ann_props,
        "counts": {
            "classes": len(classes),
            "object_properties": len(obj_props),
            "datatype_properties": len(dt_props),
            "annotation_properties": len(ann_props),
            "triples": len(g),
        },
    }


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def main() -> int:
    manifest = load_manifest()
    g = load_merged(manifest)

    # Canonicalize blank nodes for reproducible serialization across runs.
    # to_canonical_graph returns a read-only aggregate; copy into a fresh Graph
    # so we can bind prefixes and serialize.
    # Insert canonicalized triples in sorted order so the in-memory store
    # iterates deterministically — this makes the RDF/XML serializers stable too.
    canon = Graph()
    for triple in sorted(to_canonical_graph(g), key=lambda t: (str(t[0]), str(t[1]), str(t[2]))):
        canon.add(triple)
    bind_prefixes(canon, manifest)

    dist = manifest["dist"]

    ttl = canon.serialize(format="turtle")
    write_text(ROOT / dist["merged_ttl"], GENERATED_HEADER + ttl)

    owl_xml = canon.serialize(format="pretty-xml")
    write_text(
        ROOT / dist["merged_owl"],
        "<!-- DO NOT EDIT — GENERATED by tooling/build.py from ontology/modules/*.ttl -->\n"
        + owl_xml,
    )

    jsonld = canon.serialize(format="json-ld", auto_compact=True, sort_keys=True)
    # Sort the @graph by @id for stable, diff-friendly output.
    doc = json.loads(jsonld)
    if isinstance(doc, dict) and isinstance(doc.get("@graph"), list):
        doc["@graph"].sort(key=lambda n: str(n.get("@id", "")))
    write_text(ROOT / dist["jsonld"], json.dumps(doc, indent=2, sort_keys=True) + "\n")

    profile = build_profile(canon, manifest)
    profile["_generated"] = "tooling/build.py — DO NOT EDIT; regenerate from ontology/modules/"
    write_text(ROOT / dist["profile"], json.dumps(profile, indent=2, sort_keys=True) + "\n")

    print("Build complete:")
    print(f"  {dist['merged_ttl']}  ({len(canon)} triples)")
    print(f"  {dist['merged_owl']}")
    print(f"  {dist['jsonld']}")
    print(f"  {dist['profile']}")
    c = profile["counts"]
    print(
        f"  terms: {c['classes']} classes, {c['object_properties']} object props, "
        f"{c['datatype_properties']} datatype props, {c['annotation_properties']} annotation props"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
