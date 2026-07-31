#!/usr/bin/env python3
"""Validation gate for the Home-Cage Monitoring Ontology (HCMO).

Steps (any failure -> non-zero exit):
  1. Parse every TTL under ontology/, shapes/, and examples/, plus all generated
     RDF distribution serializations declared in hcmo.yaml.
  2. Validate the pinned external-vocabulary contract without network access.
  3. Run pySHACL of shapes/ against each isolated example with the canonical
     ontology supplied as an ontology graph and RDFS inference enabled.
     Examples whose name contains "edge" or "invalid" are NEGATIVE tests
     (expected to be non-conformant); all others are expected to conform.
  4. Validate the dedicated ISA/STATO evidence graph, including an injected
     process-cycle negative probe.
  5. Run every indexed competency query against the canonical ontology plus all
     positive examples. The canonicalized result rows must equal the reviewed
     answers in queries/competency_questions.yaml.

Usage: python tooling/validate.py
"""
from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

import yaml
from rdflib import Graph, Namespace, URIRef
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
    questions = index.get("questions", [])
    if not isinstance(questions, list):
        raise ValueError("competency question index must contain a questions list")
    if not all(isinstance(question, dict) for question in questions):
        raise ValueError("every competency question entry must be a mapping")
    return questions


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
    schema = Namespace("https://schema.org/")
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

    print("\n== 2. External vocabulary contract ==")
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

    print("\n== 5. Competency queries vs ontology and positive examples ==")
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
