#!/usr/bin/env python3
"""Validate the hand-authored HCMO ISA example in ``examples/isa-authoring``.

Runs the ISA-API validators with the HCMO configuration shipped next to the
example, converts the ISA-Tab to ISA-JSON with that configuration, and compares
the structure of the conversion with the committed ``isajson/isa.json``.  The
ISA-API mints UUID identifiers on every conversion, so the comparison is
structural, not byte-for-byte.  ``--write`` regenerates the committed file.
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
import warnings
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

EXPECTED_ISATOOLS = "0.14.3"
ROOT = Path(__file__).resolve().parent.parent
EXAMPLE = ROOT / "examples" / "isa-authoring"
ISATAB_DIR = EXAMPLE / "isatab"
INVESTIGATION = ISATAB_DIR / "i_Investigation_hcmo.txt"
ISAJSON = EXAMPLE / "isajson" / "isa.json"
XML_CONFIG = EXAMPLE / "config" / "xml"
JSON_CONFIG = EXAMPLE / "config" / "json" / "default"
# Warning codes that mean the instance disagrees with the configuration.
STRUCTURAL_WARNING_CODES = {4004}


def check_isatools_version() -> None:
    try:
        installed = version("isatools")
    except PackageNotFoundError as exc:
        raise SystemExit("isatools is not installed; pip install -r tooling/interoperability-requirements.txt") from exc
    if installed != EXPECTED_ISATOOLS:
        print(f"[WARN] isatools {installed} installed; the example is pinned to {EXPECTED_ISATOOLS}")


def annotation(value: object) -> tuple:
    if isinstance(value, dict):
        return (value.get("annotationValue", ""), value.get("termSource", ""), value.get("termAccession", ""))
    return (str(value), "", "")


def signature(document: dict) -> dict:
    """Identifier-independent description of the ISA-JSON content."""
    study = document["studies"][0]
    materials = study["materials"]
    categories = {c["@id"]: annotation(c["characteristicType"])[0] for c in study.get("characteristicCategories", [])}
    factors = {f["@id"]: f["factorName"] for f in study.get("factors", [])}

    def category_name(ref: object, table: dict) -> str:
        if isinstance(ref, dict):
            return table.get(ref.get("@id", ""), ref.get("@id", ""))
        return str(ref)

    sources = {
        source["name"]: sorted(
            (category_name(c["category"], categories), annotation(c["value"])) for c in source.get("characteristics", [])
        )
        for source in materials["sources"]
    }
    samples = {
        sample["name"]: sorted(
            (category_name(fv["category"], factors), annotation(fv["value"])) for fv in sample.get("factorValues", [])
        )
        for sample in materials["samples"]
    }
    return {
        "investigation": document["identifier"],
        "study": study["identifier"],
        "sources": sources,
        "samples": samples,
        "protocols": sorted((p["name"], annotation(p["protocolType"])) for p in study["protocols"]),
        "factors": sorted((f["factorName"], annotation(f["factorType"])) for f in study["factors"]),
        "study_processes": len(study["processSequence"]),
        "assays": sorted(
            (
                a["filename"],
                annotation(a["measurementType"]),
                annotation(a["technologyType"]),
                len(a["materials"]["samples"]),
                len(a["materials"]["otherMaterials"]),
                sorted((d["name"], d["type"]) for d in a["dataFiles"]),
                len(a["processSequence"]),
            )
            for a in study["assays"]
        ),
    }


def report_problems(label: str, report: dict) -> list[str]:
    problems = [f"{label}: error {e.get('code')}: {e.get('message')} ({e.get('supplemental')})" for e in report["errors"]]
    for w in report["warnings"]:
        if w.get("code") in STRUCTURAL_WARNING_CODES:
            problems.append(f"{label}: warning {w.get('code')}: {w.get('message')} ({w.get('supplemental')})")
    if not report.get("validation_finished", True):
        problems.append(f"{label}: validator did not finish")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="regenerate isajson/isa.json from isatab/")
    args = parser.parse_args()

    check_isatools_version()
    warnings.filterwarnings("ignore")
    logging.disable(logging.CRITICAL)
    from isatools import isajson, isatab, isatab2json  # noqa: E402  (optional dependency)

    problems: list[str] = []

    with INVESTIGATION.open(encoding="utf-8") as fp:
        tab_report = isatab.validate(fp, config_dir=str(XML_CONFIG))
    problems += report_problems("ISA-Tab", tab_report)
    print(f"[INFO] ISA-Tab: {len(tab_report['errors'])} errors, {len(tab_report['warnings'])} warnings")

    converted = isatab2json.convert(str(ISATAB_DIR), config_dir=str(JSON_CONFIG), use_new_parser=True, validate_first=False)
    if not isinstance(converted, dict):
        problems.append("ISA-Tab to ISA-JSON conversion returned nothing")
    else:
        if args.write:
            ISAJSON.parent.mkdir(parents=True, exist_ok=True)
            ISAJSON.write_text(json.dumps(converted, indent=2) + "\n", encoding="utf-8")
            print(f"[OK]   wrote {ISAJSON.relative_to(ROOT)}")
        committed = json.loads(ISAJSON.read_text(encoding="utf-8"))
        fresh_sig, committed_sig = signature(converted), signature(committed)
        if fresh_sig != committed_sig:
            for key in fresh_sig:
                if fresh_sig[key] != committed_sig.get(key):
                    problems.append(f"isajson/isa.json is stale: '{key}' differs from a fresh conversion (run with --write)")
        study = committed["studies"][0]
        for protocol in study["protocols"]:
            if not annotation(protocol["protocolType"])[0]:
                problems.append(f"protocol '{protocol['name']}' has no protocol type (empty Protocol REF in a table?)")
        used = {s["@id"] for a in study["assays"] for s in a["materials"]["samples"]}
        orphans = sorted(s["name"] for s in study["materials"]["samples"] if s["@id"] not in used)
        if orphans:
            problems.append(f"samples not used by any assay: {orphans}")
        for assay in study["assays"]:
            names = [d["name"] for d in assay["dataFiles"]]
            if len(names) != len(set(names)):
                problems.append(f"{assay['filename']}: duplicate data file names {sorted(set(n for n in names if names.count(n) > 1))}")

    with ISAJSON.open(encoding="utf-8") as fp:
        json_report = isajson.validate(fp, config_dir=str(JSON_CONFIG))
    problems += report_problems("ISA-JSON", json_report)
    print(f"[INFO] ISA-JSON: {len(json_report['errors'])} errors, {len(json_report['warnings'])} warnings")

    for problem in problems:
        print(f"[FAIL] {problem}")
    if problems:
        return 1
    print("[OK]   examples/isa-authoring validates against its HCMO ISA configuration")
    return 0


if __name__ == "__main__":
    sys.exit(main())
