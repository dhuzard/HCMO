"""Create a compact, non-gating summary of an AskWol beta response."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


KNOWN_EXCEPTIONS = (
    (
        "auxiliary-header-selection",
        "AskWol may select the merged external-upper presentation's "
        "owl:Ontology node instead of HCMO's root ontology header; creator, "
        "publisher, and date findings on that selected node are not missing "
        "root metadata.",
    ),
    (
        "stable-modular-namespace",
        "The hcm# core and hcm/bio#, hcm/env#, hcm/obs#, and hcm/tech# module "
        "namespaces are the published modular IRI policy. They are not re-minted "
        "to satisfy the mixed-strategy heuristic.",
    ),
    (
        "historical-version-provenance",
        "https://w3id.org/hcmo/ontology/hcm/0.0.1 is cited as historical "
        "dcterms:source provenance, not used as an undeclared HCMO term.",
    ),
    (
        "external-namespace-resolution",
        "Namespace-base resolution findings for governed external vocabularies "
        "are reviewed against external-vocabularies.yaml and do not authorize "
        "copying or changing external terms.",
    ),
    (
        "language-tags",
        "The current English-only annotation policy does not require language "
        "tags; localization remains a documented future enhancement.",
    ),
)


def status_rows(payload: dict[str, Any]) -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    for key, value in payload.items():
        if isinstance(value, dict) and value.get("status"):
            message = str(value.get("message") or "").replace("\n", " ")
            rows.append((key, str(value["status"]), message))
    metadata = payload.get("ontology_metadata", {})
    if isinstance(metadata, dict):
        for check in metadata.get("checks", []):
            if isinstance(check, dict):
                rows.append(
                    (
                        f"ontology_metadata/{check.get('key', 'unknown')}",
                        str(check.get("status", "unknown")),
                        str(check.get("message") or "").replace("\n", " "),
                    )
                )
    namespaces = payload.get("namespaces", [])
    if isinstance(namespaces, list):
        for namespace in namespaces:
            if not isinstance(namespace, dict):
                continue
            resolution = namespace.get("resolution", {})
            if isinstance(resolution, dict) and resolution.get("status") not in (None, "ok"):
                rows.append(
                    (
                        f"namespace/{namespace.get('uri', 'unknown')}",
                        str(resolution.get("status", "unknown")),
                        str(resolution.get("error") or "").replace("\n", " "),
                    )
                )
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--ref", default="unknown")
    parser.add_argument("--request-exit-code", type=int, default=0)
    args = parser.parse_args()

    raw = args.input.read_bytes() if args.input.exists() else b""
    digest = hashlib.sha256(raw).hexdigest() if raw else "not available"
    payload: dict[str, Any] = {}
    parse_error = ""
    if raw:
        try:
            loaded = json.loads(raw)
            if isinstance(loaded, dict):
                payload = loaded
            else:
                parse_error = "Response JSON was not an object."
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            parse_error = f"Response was not valid JSON: {exc}"

    rows = status_rows(payload)
    counts = {"ok": 0, "warn": 0, "fail": 0, "other": 0}
    for _, status, _ in rows:
        counts[status if status in counts else "other"] += 1

    lines = [
        "# AskWol release evidence",
        "",
        f"- Assessed ref: `{args.ref}`",
        "- Service: `https://lod-4tu.tudelft.nl/askwol/` (beta)",
        f"- Request exit code: `{args.request_exit_code}`",
        f"- Raw-response SHA-256: `{digest}`",
        "- Policy: archived, review-only evidence; **not a release gate**",
        "",
    ]
    if parse_error or args.request_exit_code:
        lines.extend(
            [
                "## Service result",
                "",
                parse_error or "The external request did not complete successfully.",
                "This is recorded as service availability evidence and does not block the release.",
                "",
            ]
        )
    else:
        lines.extend(
            [
                "## Machine summary",
                "",
                f"Top-level and ontology-metadata checks: {counts['ok']} ok, "
                f"{counts['warn']} warn, {counts['fail']} fail, {counts['other']} other.",
                "",
                "| Check | Status | Message |",
                "| --- | --- | --- |",
            ]
        )
        for key, status, message in rows:
            safe_message = message.replace("|", "\\|")
            lines.append(f"| `{key}` | `{status}` | {safe_message or '—'} |")
        reasoner = payload.get("reasoner", {})
        if isinstance(reasoner, dict):
            lines.extend(
                [
                    "",
                    "## Reasoner snapshot",
                    "",
                    f"- Consistent: `{reasoner.get('consistent', 'unknown')}`",
                    f"- Unsatisfiable classes: `{len(reasoner.get('unsatisfiable_classes', []))}`",
                    f"- Inconsistent individuals: `{len(reasoner.get('inconsistent_individuals', []))}`",
                ]
            )

    lines.extend(["", "## Documented exceptions", ""])
    for key, explanation in KNOWN_EXCEPTIONS:
        lines.append(f"- **{key}:** {explanation}")
    lines.extend(
        [
            "",
            "Any new finding outside these categories requires human triage. "
            "No AskWol result authorizes changing or re-minting a published HCMO IRI.",
            "",
        ]
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
