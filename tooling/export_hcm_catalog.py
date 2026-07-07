#!/usr/bin/env python3
"""Export docs/hcm-systems/CATALOG.md as an RDF instance graph.

The catalog remains the hand-maintained source. This script emits a Turtle ABox
for Fuseki loading using existing HCMO instance patterns:

- system/vendor rows become resources with rdf:type assertions
- system-to-vendor links are object-property triples
- table cells become literal annotations/datatype-property triples
"""
from __future__ import annotations

import re
from pathlib import Path

from rdflib import Graph, Literal, Namespace, RDF, RDFS, URIRef

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "docs" / "hcm-systems" / "CATALOG.md"
OUT = ROOT / "docs" / "hcm-systems" / "catalog.ttl"

HCM = Namespace("https://w3id.org/hcmo/ontology/hcm#")
HCID = Namespace("https://w3id.org/hcmo/id/catalog/")
DCTERMS = Namespace("http://purl.org/dc/terms/")
SCHEMA = Namespace("https://schema.org/")


def clean_markdown(value: str) -> str:
    value = re.sub(r"`([^`]+)`", r"\1", value)
    value = re.sub(r"\*\*([^*]+)\*\*", r"\1", value)
    value = re.sub(r"✅\s*\[[^\]]+\]\([^)]+\)", "", value)
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    value = re.sub(r"<br\s*/?>", "; ", value, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", value).strip()


def slugify(value: str) -> str:
    value = clean_markdown(value).lower()
    value = value.replace("®", "").replace("™", "")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "unnamed"


def split_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def table_rows(markdown: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    section = ""
    lines = markdown.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("## "):
            section = clean_markdown(line.removeprefix("## "))
            i += 1
            continue
        if line.startswith("|") and i + 1 < len(lines) and re.match(r"^\|\s*:?-+", lines[i + 1].strip()):
            headers = [clean_markdown(cell) for cell in split_table_row(line)]
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = split_table_row(lines[i])
                row = {headers[idx]: clean_markdown(cells[idx]) if idx < len(cells) else "" for idx in range(len(headers))}
                row["_section"] = section
                rows.append(row)
                i += 1
            continue
        i += 1
    return rows


def add_literal(g: Graph, subject: URIRef, predicate: URIRef, value: str) -> None:
    if value and value not in {"—", "-", "(named only)", "(none listed)"}:
        g.add((subject, predicate, Literal(value)))


def classify(row: dict[str, str]) -> tuple[str, URIRef]:
    section = row.get("_section", "")
    item_type = row.get("Type", "")
    if "AI / computer-vision toolchains" in section:
        return "software", HCM.Software
    if "Sensor components & standards" in section:
        if "standard" in item_type.lower():
            return "resource", SCHEMA.CreativeWork
        if re.search(r"sensor|camera|microphone|rfid|co₂|co2|air-quality", item_type, flags=re.IGNORECASE):
            return "sensor", HCM.Sensor
        if "repository" in item_type.lower():
            return "resource", SCHEMA.Dataset
        return "resource", SCHEMA.CreativeWork
    return "system", HCM.System


def main() -> int:
    g = Graph()
    g.bind("hcm", HCM)
    g.bind("hcid", HCID)
    g.bind("dcterms", DCTERMS)
    g.bind("rdfs", RDFS)
    g.bind("schema", SCHEMA)

    markdown = CATALOG.read_text(encoding="utf-8")
    for row in table_rows(markdown):
        raw_name = row.get("System") or row.get("Tool") or row.get("Item")
        if not raw_name:
            continue

        kind, rdf_class = classify(row)
        slug = row.get("slug") or slugify(raw_name)
        system = URIRef(HCID[f"{kind}/{slug}"])
        g.add((system, RDF.type, rdf_class))
        g.add((system, RDFS.label, Literal(raw_name)))
        add_literal(g, system, HCM.hasCategory, row.get("_section", ""))
        add_literal(g, system, HCM.hasDescription, row.get("Key measured parameters", "") or row.get("Task", "") or row.get("Note", ""))
        add_literal(g, system, DCTERMS.source, row.get("Data / links", "") or row.get("Reference", ""))
        add_literal(g, system, DCTERMS.type, row.get("Modality", "") or row.get("Type", ""))
        add_literal(g, system, DCTERMS.subject, row.get("Prio", ""))

        maker_value = row.get("Vendor") or row.get("Authors")
        if maker_value:
            maker_slug = slugify(maker_value)
            maker = URIRef(HCID[f"agent/{maker_slug}"])
            g.add((maker, RDF.type, HCM.Supplier))
            g.add((maker, RDFS.label, Literal(maker_value)))
            g.add((system, HCM.producedBy, maker))
            add_literal(g, system, HCM.hasManufacturer, maker_value)

    OUT.write_text(
        "# DO NOT EDIT BY HAND - generated by tooling/export_hcm_catalog.py from CATALOG.md.\n"
        + g.serialize(format="turtle"),
        encoding="utf-8",
        newline="\n",
    )
    print(f"Wrote {OUT.relative_to(ROOT)} ({len(g)} triples)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
