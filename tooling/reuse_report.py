#!/usr/bin/env python3
"""Classify the external terms reused in the merged HCMO graph by reuse kind.

Reads the generated merged graph (hcmo.yaml -> dist.merged_ttl) and writes
docs/EXTERNAL-REUSE.md, a GENERATED report. Each external vocabulary term is
assigned one kind, by how the graph uses it:

  semantic     target of a logical statement: subclass or subproperty parent,
               domain or range, restriction property or filler, or a member of
               a class expression. These terms carry HCM meaning.
  metadata     used only as an annotation predicate, or as the type of a
               metadata record (for example schema:Person on the creators).
  replacement  named only as the replacement of a deprecated HCMO term
               (dcterms:isReplacedBy); counted separately, not as reuse.

A term declared but never used (only `rdf:type` statements about it) is listed
and not counted. IRIs outside the vocabulary table below (ORCID iDs, licence
and repository URLs, artifact IRIs) are values, not reused terms, unless the
graph uses one as a predicate or in a logical statement; then the run fails
until the vocabulary is added to VOCABULARIES.

Usage:
  python tooling/reuse_report.py          # write docs/EXTERNAL-REUSE.md
  python tooling/reuse_report.py --check  # exit 1 if the report is stale
"""
from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path

import yaml
from rdflib import OWL, RDF, RDFS, BNode, Graph, URIRef
from rdflib.collection import Collection

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "hcmo.yaml"
CONTRACT = ROOT / "external-vocabularies.yaml"
REPORT = ROOT / "docs" / "EXTERNAL-REUSE.md"

HCMO_PREFIX = "https://w3id.org/hcmo/"
BUILTIN_PREFIXES = (
    str(OWL),
    str(RDFS),
    str(RDF),
    "http://www.w3.org/2001/XMLSchema#",
)

# Display name -> term namespaces. Every canonical term namespace pinned in
# external-vocabularies.yaml must appear here (checked at run time); the
# metadata vocabularies are listed here only.
VOCABULARIES: dict[str, tuple[str, ...]] = {
    "BFO": ("http://purl.obolibrary.org/obo/BFO_",),
    "IAO": ("http://purl.obolibrary.org/obo/IAO_",),
    "OBI": ("http://purl.obolibrary.org/obo/OBI_",),
    "STATO": ("http://purl.obolibrary.org/obo/STATO_",),
    "SOSA": ("http://www.w3.org/ns/sosa/",),
    "PROV-O": ("http://www.w3.org/ns/prov#",),
    "OWL-Time": ("http://www.w3.org/2006/time#",),
    "QUDT": ("http://qudt.org/schema/qudt/", "http://qudt.org/vocab/unit/"),
    "SemTS": ("https://w3id.org/semts/ontology#",),
    "schema.org": ("https://schema.org/", "http://schema.org/"),
    "Bioschemas": ("https://bioschemas.org/",),
    "DCTERMS": ("http://purl.org/dc/terms/",),
    "DC elements": ("http://purl.org/dc/elements/1.1/",),
    "SKOS": ("http://www.w3.org/2004/02/skos/core#",),
    "VANN": ("http://purl.org/vocab/vann/",),
    "BIBO": ("http://purl.org/ontology/bibo/",),
    "MOD": ("https://w3id.org/mod#",),
}
# Contract namespaces that name alignment artifacts, not term namespaces.
CONTRACT_ARTIFACT_NAMESPACES = {
    "http://www.w3.org/ns/sosa/prov",
    "https://raw.githubusercontent.com/BFO-Mappings/PROV-to-BFO/",
}

LOGICAL_PREDICATES = {
    RDFS.subClassOf: "subclass parent",
    RDFS.subPropertyOf: "subproperty parent",
    RDFS.domain: "domain",
    RDFS.range: "range",
    OWL.equivalentClass: "equivalent class",
    OWL.equivalentProperty: "equivalent property",
    OWL.inverseOf: "inverse",
    OWL.disjointWith: "disjoint class",
    OWL.onProperty: "restriction property",
    OWL.someValuesFrom: "restriction filler",
    OWL.allValuesFrom: "restriction filler",
    OWL.hasValue: "restriction filler",
    OWL.onClass: "restriction filler",
}
CLASS_EXPRESSION_LISTS = (OWL.unionOf, OWL.intersectionOf, OWL.oneOf)
IS_REPLACED_BY = URIRef("http://purl.org/dc/terms/isReplacedBy")
KINDS = ("semantic", "metadata", "replacement")


def vocabulary_of(term: URIRef) -> str | None:
    iri = str(term)
    best, best_len = None, 0
    for name, namespaces in VOCABULARIES.items():
        for ns in namespaces:
            if iri.startswith(ns) and len(iri) > len(ns) and len(ns) > best_len:
                best, best_len = name, len(ns)
    return best


def is_external(node) -> bool:
    return (
        isinstance(node, URIRef)
        and not str(node).startswith(HCMO_PREFIX)
        and not str(node).startswith(BUILTIN_PREFIXES)
    )


def check_table_covers_contract() -> list[str]:
    contract = yaml.safe_load(CONTRACT.read_text(encoding="utf-8"))
    known = {ns for nss in VOCABULARIES.values() for ns in nss}
    missing = []
    for key, entry in contract["vocabularies"].items():
        for ns in entry.get("canonical_term_namespaces") or []:
            covered = any(ns.startswith(k) for k in known)
            if not covered and ns not in CONTRACT_ARTIFACT_NAMESPACES:
                missing.append(f"{key}: {ns}")
    return missing


def classify(g: Graph) -> tuple[dict, list[str], list[str]]:
    """Return ({term: {"vocab", "kind", "uses"}}, declared_only, errors)."""
    uses: dict[URIRef, set[str]] = defaultdict(set)
    logical: set[URIRef] = set()
    metadata: set[URIRef] = set()
    replacement: set[URIRef] = set()
    mentioned: set[URIRef] = set()
    errors: list[str] = []

    def note_logical(term, label: str) -> None:
        if is_external(term):
            logical.add(term)
            uses[term].add(label)

    for s, p, o in g:
        for node in (s, p, o):
            if is_external(node):
                mentioned.add(node)
        if p in LOGICAL_PREDICATES:
            note_logical(o, LOGICAL_PREDICATES[p])
            if p in (RDFS.subClassOf, RDFS.subPropertyOf, RDFS.domain, RDFS.range):
                # The subject of an axiom is constrained too (for example the
                # curated BFO/IAO upper presentation declares parents).
                if is_external(s):
                    logical.add(s)
                    uses[s].add("axiom subject")
        elif p in CLASS_EXPRESSION_LISTS and isinstance(o, BNode):
            for member in Collection(g, o):
                note_logical(member, "class-expression member")
        elif p == IS_REPLACED_BY:
            if is_external(o):
                replacement.add(o)
                uses[o].add("replacement of a deprecated HCMO term")
        if is_external(p) and p not in LOGICAL_PREDICATES:
            metadata.add(p)
            uses[p].add("annotation predicate")
        if p == RDF.type and is_external(o) and not str(s).startswith(HCMO_PREFIX):
            if not isinstance(s, URIRef) or vocabulary_of(s) is None:
                metadata.add(o)
                uses[o].add("type of a metadata record")

    terms = {}
    for term in sorted(logical | metadata | replacement, key=str):
        vocab = vocabulary_of(term)
        if vocab is None:
            errors.append(f"unknown vocabulary for used term {term}; add it to VOCABULARIES")
            continue
        kind = "semantic" if term in logical else "metadata" if term in metadata else "replacement"
        terms[term] = {"vocab": vocab, "kind": kind, "uses": sorted(uses[term])}
    declared_only = sorted(
        str(t) for t in mentioned
        if t not in terms and vocabulary_of(t) is not None
    )
    return terms, declared_only, errors


def render(terms: dict, declared_only: list[str], source: str, triples: int) -> str:
    by_kind: dict[str, dict[str, list]] = {k: defaultdict(list) for k in KINDS}
    for term, info in terms.items():
        by_kind[info["kind"]][info["vocab"]].append((term, info["uses"]))

    def vocab_list(kind: str) -> str:
        groups = by_kind[kind]
        ordered = sorted(groups, key=lambda v: (-len(groups[v]), v))
        return ", ".join(f"{v} {len(groups[v])}" for v in ordered) or "none"

    lines = [
        "<!-- DO NOT EDIT — GENERATED by tooling/reuse_report.py from the merged graph. -->",
        "",
        "# External reuse by kind",
        "",
        f"Source: `{source}` ({triples} triples). Regenerate with "
        "`python tooling/build.py` (or `python tooling/reuse_report.py`); "
        "`tooling/validate.py` fails when this file is stale.",
        "",
        "Rules: a term is **semantic** reuse when it is the target of a logical "
        "statement (subclass or subproperty parent, domain or range, restriction "
        "property or filler, class-expression member); **metadata** reuse when it "
        "is only an annotation predicate or the type of a metadata record; a "
        "**replacement target** when it is named only as the replacement of a "
        "deprecated HCMO term. Values such as ORCID iDs, licence and repository "
        "URLs are not counted. Example data (ABox) are not included.",
        "",
        "## Summary",
        "",
        "| Kind | Terms | Vocabularies | Breakdown |",
        "| --- | ---: | ---: | --- |",
    ]
    for kind, label in (
        ("semantic", "Semantic (HCM meaning)"),
        ("metadata", "Ontology metadata"),
        ("replacement", "Replacement target only"),
    ):
        n_terms = sum(len(v) for v in by_kind[kind].values())
        lines.append(f"| {label} | {n_terms} | {len(by_kind[kind])} | {vocab_list(kind)} |")

    for kind, title in (
        ("semantic", "Semantic reuse"),
        ("metadata", "Metadata reuse"),
        ("replacement", "Replacement targets"),
    ):
        lines += ["", f"## {title}", "", "| Vocabulary | Term | Used as |", "| --- | --- | --- |"]
        for vocab in sorted(by_kind[kind]):
            for term, used in sorted(by_kind[kind][vocab], key=lambda x: str(x[0])):
                lines.append(f"| {vocab} | `{term}` | {'; '.join(used)} |")

    lines += ["", "## Declared but not used (not counted)", ""]
    lines += [f"- `{t}`" for t in declared_only] or ["- none"]
    return "\n".join(lines) + "\n"


def build_report() -> tuple[str, list[str]]:
    manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    source = manifest["dist"]["merged_ttl"]
    g = Graph().parse(ROOT / source, format="turtle")
    errors = [f"vocabulary table misses contract namespace {m}" for m in check_table_covers_contract()]
    terms, declared_only, classify_errors = classify(g)
    errors += classify_errors
    return render(terms, declared_only, source, len(g)), errors


def write_report() -> list[str]:
    text, errors = build_report()
    if not errors:
        REPORT.write_text(text, encoding="utf-8", newline="\n")
    return errors


def check_report() -> tuple[bool, list[str]]:
    text, errors = build_report()
    if errors:
        return False, [f"[FAIL] reuse report: {e}" for e in errors]
    current = REPORT.read_text(encoding="utf-8") if REPORT.exists() else ""
    if current != text:
        return False, [f"[FAIL] {REPORT.relative_to(ROOT).as_posix()} is stale; run python tooling/build.py"]
    return True, [f"[OK]   {REPORT.relative_to(ROOT).as_posix()} matches the merged graph"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="fail if the report is stale")
    args = parser.parse_args()
    if args.check:
        ok, notes = check_report()
        print("\n".join(notes))
        return 0 if ok else 1
    errors = write_report()
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"wrote {REPORT.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
