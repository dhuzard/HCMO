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
PREFIX_RE = re.compile(r"(?im)^\s*PREFIX\s+([\w-]+):\s*<([^>]+)>")
PREFIXED_TERM_RE = re.compile(r"\b([\w-]+):([A-Za-z_][\w.-]*)")
IRI_RE = re.compile(r"<(https?://[^>]+)>")


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
    namespace_terms: dict[str, set[str]] = {}
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
        for namespace in namespaces:
            namespace_terms.setdefault(namespace, set()).update(terms)

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
        expected_presentation_parents = {
            "http://purl.obolibrary.org/obo/BFO_0000001": str(OWL.Thing),
            "http://purl.obolibrary.org/obo/BFO_0000015":
                "http://purl.obolibrary.org/obo/BFO_0000001",
            "http://purl.obolibrary.org/obo/BFO_0000019":
                "http://purl.obolibrary.org/obo/BFO_0000001",
            "http://purl.obolibrary.org/obo/BFO_0000040":
                "http://purl.obolibrary.org/obo/BFO_0000001",
            "http://purl.obolibrary.org/obo/IAO_0000030":
                "http://purl.obolibrary.org/obo/BFO_0000001",
        }
        actual_presentation_parents = {
            term: {
                str(parent)
                for parent in graph.objects(URIRef(term), RDFS.subClassOf)
                if isinstance(parent, URIRef)
            }
            for term in expected_terms
        }
        unexpected_parent_sets = {
            term: sorted(actual_presentation_parents[term])
            for term, parent in expected_presentation_parents.items()
            if actual_presentation_parents.get(term) != {parent}
        }
        if unexpected_parent_sets:
            ok = False
            notes.append(
                "[FAIL] end-user upper presentation is not the reviewed "
                f"five-category hierarchy: {unexpected_parent_sets}"
            )

    developer = contract.get("developer_upper_profile", {})
    developer_path = ROOT / str(developer.get("path", ""))
    developer_terms = set(developer.get("terms", []))
    if not developer_path.exists():
        ok = False
        notes.append(f"[FAIL] developer upper profile missing: {developer_path}")
    elif not developer_terms:
        ok = False
        notes.append("[FAIL] developer upper profile term list is empty")
    else:
        developer_graph = Graph().parse(developer_path, format="turtle")
        developer_declared = {
            str(term)
            for term in developer_graph.subjects(RDF.type, OWL.Class)
            if isinstance(term, URIRef)
        }
        if developer_declared != developer_terms:
            ok = False
            notes.append(
                "[FAIL] developer upper profile terms differ from contract: "
                f"missing={sorted(developer_terms - developer_declared)}, "
                f"unexpected={sorted(developer_declared - developer_terms)}"
            )
        developer_missing_metadata = [
            str(term)
            for term in map(URIRef, developer_terms)
            if developer_graph.value(term, RDFS.label) is None
            or developer_graph.value(term, SKOS.definition) is None
        ]
        if developer_missing_metadata:
            ok = False
            notes.append(
                "[FAIL] developer upper terms missing label/definition: "
                f"{sorted(developer_missing_metadata)}"
            )
        if not developer_terms <= all_terms:
            ok = False
            notes.append(
                "[FAIL] developer upper terms are not covered by vocabulary allowlists"
            )
        expected_developer_parents = {
            "http://purl.obolibrary.org/obo/BFO_0000001": {str(OWL.Thing)},
            "http://purl.obolibrary.org/obo/BFO_0000002": {
                "http://purl.obolibrary.org/obo/BFO_0000001"
            },
            "http://purl.obolibrary.org/obo/BFO_0000003": {
                "http://purl.obolibrary.org/obo/BFO_0000001"
            },
            "http://purl.obolibrary.org/obo/BFO_0000004": {
                "http://purl.obolibrary.org/obo/BFO_0000002"
            },
            "http://purl.obolibrary.org/obo/BFO_0000015": {
                "http://purl.obolibrary.org/obo/BFO_0000003"
            },
            "http://purl.obolibrary.org/obo/BFO_0000019": {
                "http://purl.obolibrary.org/obo/BFO_0000020"
            },
            "http://purl.obolibrary.org/obo/BFO_0000020": {
                "http://purl.obolibrary.org/obo/BFO_0000002"
            },
            "http://purl.obolibrary.org/obo/BFO_0000027": {
                "http://purl.obolibrary.org/obo/BFO_0000040"
            },
            "http://purl.obolibrary.org/obo/BFO_0000031": {
                "http://purl.obolibrary.org/obo/BFO_0000002"
            },
            "http://purl.obolibrary.org/obo/BFO_0000040": {
                "http://purl.obolibrary.org/obo/BFO_0000004"
            },
            "http://purl.obolibrary.org/obo/IAO_0000030": {
                "http://purl.obolibrary.org/obo/BFO_0000031"
            },
        }
        actual_developer_parents = {
            term: {
                str(parent)
                for parent in developer_graph.objects(
                    URIRef(term), RDFS.subClassOf
                )
                if isinstance(parent, URIRef)
            }
            for term in developer_terms
        }
        unexpected_developer_parent_sets = {
            term: sorted(actual_developer_parents[term])
            for term, parents in expected_developer_parents.items()
            if actual_developer_parents.get(term) != parents
        }
        if unexpected_developer_parent_sets:
            ok = False
            notes.append(
                "[FAIL] developer upper profile differs from the pinned "
                f"source hierarchy: {unexpected_developer_parent_sets}"
            )
        experimental_group = URIRef(
            "https://w3id.org/hcmo/ontology/hcm/bio#ExperimentalGroup"
        )
        object_aggregate = URIRef(
            "http://purl.obolibrary.org/obo/BFO_0000027"
        )
        if (
            experimental_group,
            RDFS.subClassOf,
            object_aggregate,
        ) not in developer_graph:
            ok = False
            notes.append(
                "[FAIL] developer upper profile does not refine "
                "ExperimentalGroup as a BFO object aggregate"
            )

    manifest = _load_yaml(MANIFEST_PATH)
    source_paths = [
        *(ROOT / path for path in manifest.get("modules", [])),
        *(ROOT / path for path in manifest.get("examples", [])),
        *sorted((ROOT / "shapes").glob("*.ttl")),
    ]
    source_graph = Graph()
    for path in source_paths:
        source_graph.parse(path, format="turtle")
    experimental_group = URIRef(
        "https://w3id.org/hcmo/ontology/hcm/bio#ExperimentalGroup"
    )
    material_entity = URIRef("http://purl.obolibrary.org/obo/BFO_0000040")
    object_aggregate = URIRef("http://purl.obolibrary.org/obo/BFO_0000027")
    if (experimental_group, RDFS.subClassOf, material_entity) not in source_graph:
        ok = False
        notes.append(
            "[FAIL] default hierarchy does not place ExperimentalGroup under "
            "BFO material entity"
        )
    if (experimental_group, RDFS.subClassOf, object_aggregate) in source_graph:
        ok = False
        notes.append(
            "[FAIL] default hierarchy exposes the developer-only "
            "ExperimentalGroup/object aggregate refinement"
        )
    used_iris = {
        str(term)
        for triple in source_graph
        for term in triple
        if isinstance(term, URIRef)
    }
    for query_path in sorted((ROOT / manifest["queries"]["dir"]).glob("cq-*.rq")):
        query_text = query_path.read_text(encoding="utf-8")
        prefixes = dict(PREFIX_RE.findall(query_text))
        used_iris.update(set(IRI_RE.findall(query_text)) - set(prefixes.values()))
        used_iris.update(
            prefixes[prefix] + local
            for prefix, local in PREFIXED_TERM_RE.findall(query_text)
            if prefix in prefixes
        )

    uncovered = sorted(
        iri
        for iri in used_iris
        if any(iri.startswith(namespace) for namespace in namespace_terms)
        and not any(
            iri in allowed
            for namespace, allowed in namespace_terms.items()
            if iri.startswith(namespace)
        )
    )
    if uncovered:
        ok = False
        notes.append(
            "[FAIL] external IRIs used outside contract allowlists: "
            f"{uncovered}"
        )

    if ok:
        notes.append(
            f"[OK]   external contract: {len(vocabularies)} vocabularies, "
            f"{artifact_count} checksummed artifacts"
        )
        notes.append(
            f"[OK]   end-user upper presentation: {len(expected_terms)} "
            "canonical anchors"
        )
        notes.append(
            f"[OK]   optional developer upper profile: {len(developer_terms)} "
            "source terms"
        )
        notes.append("[OK]   active RDF and query IRIs covered by term allowlists")
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
