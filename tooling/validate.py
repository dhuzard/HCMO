#!/usr/bin/env python3
"""Validation gate for the HCMO / MAPP ontology.

Steps (any failure -> non-zero exit):
  1. Parse every TTL under ontology/, shapes/, examples/, and dist/.
  2. Run pySHACL of shapes/ against each example. Examples whose name contains
     "edge" or "invalid" are NEGATIVE tests (expected to be non-conformant);
     all others are expected to conform.
  3. Run every queries/cq-*.rq against the merged graph; a query that raises an
     error fails the gate. Empty result sets are reported but allowed (a
     competency question may legitimately match nothing in the current ABox).

Usage: python tooling/validate.py
"""
from __future__ import annotations

import glob
import sys
from pathlib import Path

import yaml
import rdflib
from rdflib import Graph
from pyshacl import validate as shacl_validate

ROOT = Path(__file__).resolve().parent.parent


def load_manifest() -> dict:
    with open(ROOT / "hcmo.yaml") as f:
        return yaml.safe_load(f)


def merged_graph(manifest: dict) -> Graph:
    g = Graph()
    for rel in manifest["modules"]:
        g.parse(ROOT / rel, format="turtle")
    return g


def step_parse_all() -> tuple[bool, list[str]]:
    ok = True
    notes = []
    patterns = ["ontology/**/*.ttl", "shapes/**/*.ttl", "examples/**/*.ttl", "dist/*.ttl"]
    files = sorted({p for pat in patterns for p in glob.glob(str(ROOT / pat), recursive=True)})
    for f in files:
        rel = str(Path(f).relative_to(ROOT))
        try:
            Graph().parse(f, format="turtle")
            notes.append(f"[OK]   parsed {rel}")
        except Exception as e:  # noqa: BLE001
            ok = False
            notes.append(f"[FAIL] parse {rel}: {e}")
    return ok, notes


def step_shacl(manifest: dict) -> tuple[bool, list[str]]:
    ok = True
    notes = []
    shapes_path = ROOT / manifest["shapes"]
    if not shapes_path.exists():
        return False, [f"[FAIL] shapes file missing: {manifest['shapes']}"]
    shapes_g = Graph().parse(shapes_path, format="turtle")
    for rel in manifest.get("examples", []):
        path = ROOT / rel
        negative = any(t in Path(rel).name.lower() for t in ("edge", "invalid"))
        if not path.exists():
            ok = False
            notes.append(f"[FAIL] example missing: {rel}")
            continue
        data_g = Graph().parse(path, format="turtle")
        conforms, _, report = shacl_validate(
            data_g, shacl_graph=shapes_g, inference="rdfs", abort_on_first=False,
        )
        expect = "non-conformant" if negative else "conformant"
        actual = "conformant" if conforms else "non-conformant"
        passed = (conforms is not negative)  # positive->conform, negative->not
        if not passed:
            ok = False
            notes.append(f"[FAIL] SHACL {rel}: expected {expect}, got {actual}")
        else:
            notes.append(f"[OK]   SHACL {rel}: {actual} (expected {expect})")
    return ok, notes


def step_queries(g: Graph) -> tuple[bool, list[str], dict]:
    ok = True
    notes = []
    rowcounts = {}
    for f in sorted(glob.glob(str(ROOT / "queries" / "cq-*.rq"))):
        rel = str(Path(f).relative_to(ROOT))
        try:
            res = g.query(Path(f).read_text())
            n = len(list(res))
            rowcounts[rel] = n
            notes.append(f"[OK]   query {rel}: {n} row(s)")
        except Exception as e:  # noqa: BLE001
            ok = False
            rowcounts[rel] = None
            notes.append(f"[FAIL] query {rel}: {e}")
    return ok, notes, rowcounts


def main() -> int:
    manifest = load_manifest()
    all_ok = True

    print("== 1. Parse all TTL ==")
    ok, notes = step_parse_all()
    print("\n".join(notes))
    all_ok &= ok

    print("\n== 2. SHACL (shapes vs examples) ==")
    ok, notes = step_shacl(manifest)
    print("\n".join(notes))
    all_ok &= ok

    print("\n== 3. Competency queries vs merged graph ==")
    g = merged_graph(manifest)
    ok, notes, rowcounts = step_queries(g)
    print("\n".join(notes))
    all_ok &= ok

    returned = [q for q, n in rowcounts.items() if n]
    print("\n== Summary ==")
    print(f"  merged graph triples: {len(g)}")
    print(f"  queries returning rows: {returned or 'none'}")
    print(f"  result: {'PASS' if all_ok else 'FAIL'}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
