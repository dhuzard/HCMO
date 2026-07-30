#!/usr/bin/env python3
"""Validate HCMO's pinned external-vocabulary contract.

The default check is offline and is part of tooling/validate.py. Use
--verify-network to download each pinned artifact and verify its SHA-256.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
import urllib.request
from pathlib import Path

import yaml
from rdflib import Graph, URIRef
from rdflib.namespace import OWL, RDF, RDFS, SKOS

ROOT = Path(__file__).resolve().parent.parent
CONTRACT_PATH = ROOT / "external-vocabularies.yaml"
MANIFEST_PATH = ROOT / "hcmo.yaml"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")

EXPECTED_MANIFEST_KEYS = {
    "name",
    "title",
    "version",
    "namespace",
    "prefix",
    "ontology_iri",
    "version_iri",
    "modules",
    "dist",
    "shapes",
    "queries",
    "examples",
}
EXPECTED_DIST_KEYS = {
    "merged_ttl",
    "merged_owl",
    "jsonld",
    "profile",
    "context",
}
EXPECTED_QUERY_KEYS = {"index", "dir"}


def _load_yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path.name} must contain a mapping")
    return data


def _check_manifest_shape(notes: list[str]) -> bool:
    ok = True
    manifest = _load_yaml(MANIFEST_PATH)
    if set(manifest) != EXPECTED_MANIFEST_KEYS:
        ok = False
        notes.append(
            "[FAIL] hcmo.yaml top-level API shape changed: "
            f"expected={sorted(EXPECTED_MANIFEST_KEYS)}, actual={sorted(manifest)}"
        )
    if set(manifest.get("dist", {})) != EXPECTED_DIST_KEYS:
        ok = False
        notes.append("[FAIL] hcmo.yaml dist API shape changed")
    if set(manifest.get("queries", {})) != EXPECTED_QUERY_KEYS:
        ok = False
        notes.append("[FAIL] hcmo.yaml queries API shape changed")
    if ok:
        notes.append("[OK]   hcmo.yaml API shape unchanged")
    return ok


def _check_contract(notes: list[str]) -> tuple[bool, dict]:
    ok = True
    contract = _load_yaml(CONTRACT_PATH)
    if contract.get("contract_version") != 1:
        ok = False
        notes.append("[FAIL] external contract_version must be 1")

    vocabularies = contract.get("vocabularies")
    if not isinstance(vocabularies, dict) or not vocabularies:
        return False, contract

    all_terms: set[str] = set()
    artifact_count = 0
    for vocab_id, entry in vocabularies.items():
        if not isinstance(entry, dict):
            ok = False
            notes.append(f"[FAIL] vocabulary {vocab_id} must be a mapping")
            continue
        for field in (
            "status",
            "authoritative_version",
            "version_iri",
            "canonical_term_namespaces",
            "artifacts",
            "used_terms",
        ):
            if not entry.get(field):
                ok = False
                notes.append(f"[FAIL] vocabulary {vocab_id} missing {field}")

        namespaces = entry.get("canonical_term_namespaces", [])
        terms = entry.get("used_terms", [])
        artifacts = entry.get("artifacts", [])
        if not isinstance(namespaces, list) or not all(
            isinstance(namespace, str) and namespace.startswith(("http://", "https://"))
            for namespace in namespaces
        ):
            ok = False
            notes.append(f"[FAIL] vocabulary {vocab_id} has invalid namespaces")
        if not isinstance(terms, list) or not all(
            isinstance(term, str) and term.startswith(("http://", "https://"))
            for term in terms
        ):
            ok = False
            notes.append(f"[FAIL] vocabulary {vocab_id} has invalid used_terms")
        if len(terms) != len(set(terms)):
            ok = False
            notes.append(f"[FAIL] vocabulary {vocab_id} has duplicate used_terms")
        all_terms.update(terms)

        if not isinstance(artifacts, list) or not artifacts:
            ok = False
            notes.append(f"[FAIL] vocabulary {vocab_id} has no artifacts")
            continue
        for artifact in artifacts:
            artifact_count += 1
            if not isinstance(artifact, dict):
                ok = False
                notes.append(f"[FAIL] vocabulary {vocab_id} has malformed artifact")
                continue
            url = artifact.get("url")
            checksum = artifact.get("sha256")
            if not isinstance(url, str) or not url.startswith("https://"):
                ok = False
                notes.append(f"[FAIL] vocabulary {vocab_id} artifact URL is not HTTPS")
            if not isinstance(checksum, str) or not SHA256_RE.fullmatch(checksum):
                ok = False
                notes.append(f"[FAIL] vocabulary {vocab_id} has invalid SHA-256")

    subset = contract.get("curated_upper_subset", {})
    subset_path = ROOT / str(subset.get("path", ""))
    expected_terms = set(subset.get("terms", []))
    if not subset_path.exists():
        ok = False
        notes.append(f"[FAIL] curated upper subset missing: {subset_path}")
    elif not expected_terms:
        ok = False
        notes.append("[FAIL] curated upper subset term list is empty")
    else:
        graph = Graph().parse(subset_path, format="turtle")
        declared = {
            str(term)
            for term in graph.subjects(RDF.type, OWL.Class)
            if isinstance(term, URIRef)
        }
        if declared != expected_terms:
            ok = False
            notes.append(
                "[FAIL] curated upper subset terms differ from contract: "
                f"missing={sorted(expected_terms - declared)}, "
                f"unexpected={sorted(declared - expected_terms)}"
            )
        missing_metadata = []
        for term in map(URIRef, expected_terms):
            if graph.value(term, RDFS.label) is None or graph.value(term, SKOS.definition) is None:
                missing_metadata.append(str(term))
        if missing_metadata:
            ok = False
            notes.append(
                "[FAIL] curated upper terms missing label/definition: "
                f"{sorted(missing_metadata)}"
            )
        if not expected_terms <= all_terms:
            ok = False
            notes.append(
                "[FAIL] curated upper terms are not covered by vocabulary allowlists"
            )

    if ok:
        notes.append(
            f"[OK]   external contract: {len(vocabularies)} vocabularies, "
            f"{artifact_count} checksummed artifacts"
        )
        notes.append(
            f"[OK]   curated upper subset: {len(expected_terms)} source terms"
        )
    return ok, contract


def _verify_network(contract: dict, notes: list[str]) -> bool:
    ok = True
    request_headers = {"User-Agent": "HCMO-external-vocabulary-audit/1"}
    for vocab_id, entry in contract["vocabularies"].items():
        for artifact in entry["artifacts"]:
            request = urllib.request.Request(artifact["url"], headers=request_headers)
            try:
                with urllib.request.urlopen(request, timeout=60) as response:
                    digest = hashlib.sha256(response.read()).hexdigest()
            except Exception as exc:  # noqa: BLE001
                ok = False
                notes.append(
                    f"[FAIL] download {vocab_id}/{artifact['role']}: {exc}"
                )
                continue
            if digest != artifact["sha256"]:
                ok = False
                notes.append(
                    f"[FAIL] checksum {vocab_id}/{artifact['role']}: "
                    f"expected={artifact['sha256']}, actual={digest}"
                )
            else:
                notes.append(
                    f"[OK]   checksum {vocab_id}/{artifact['role']}: {digest}"
                )
    return ok


def validate_contract(verify_network: bool = False) -> tuple[bool, list[str]]:
    notes: list[str] = []
    ok = _check_manifest_shape(notes)
    contract_ok, contract = _check_contract(notes)
    ok &= contract_ok
    if verify_network and contract_ok:
        ok &= _verify_network(contract, notes)
    return ok, notes


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--verify-network",
        action="store_true",
        help="download every pinned artifact and verify its SHA-256",
    )
    args = parser.parse_args()
    ok, notes = validate_contract(args.verify_network)
    print("\n".join(notes))
    print(f"External vocabulary contract: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
