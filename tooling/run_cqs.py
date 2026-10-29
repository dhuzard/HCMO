#!/usr/bin/env python3
"""Run the competency questions against a remote SPARQL endpoint.

`tooling/validate.py` evaluates every `queries/cq-*.rq` on the merged graph built
in memory from `dist/hcmo.ttl` and the positive examples of `hcmo.yaml`. This
script sends the same queries to a SPARQL 1.1 Protocol endpoint (Fuseki, the
Metadatapp public endpoint, ...) and compares the rows with the reviewed
`expected_answers` of `queries/competency_questions.yaml`, using the same
canonical row form as the validator (unbound variables as null, literals by
their lexical form).

Usage:
    python tooling/run_cqs.py --endpoint https://host/hcmo/sparql
    python tooling/run_cqs.py --endpoint URL --only animals-by-enclosure
    python tooling/run_cqs.py --endpoint URL --user admin --password ...
    python tooling/run_cqs.py --endpoint URL --no-compare   # just print rows
    python tooling/run_cqs.py --print-files   # files the dataset must contain

Exit status is 0 when every selected question matches its expected answers
(or when --no-compare is given and every query ran), 1 otherwise. The hosted
dataset must contain the ontology and the manifest examples for the expected
rows to match; a mismatch on a dataset loaded differently is a difference in
content, not necessarily a defect in the query.
"""
from __future__ import annotations

import argparse
import base64
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "hcmo.yaml"


def load_questions() -> list[dict]:
    manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    index = ROOT / manifest["queries"]["index"]
    data = yaml.safe_load(index.read_text(encoding="utf-8"))
    return data["questions"]


def evaluation_files() -> list[str]:
    """Files whose union is the validator's CQ evaluation graph."""
    manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    files = [manifest["dist"]["merged_ttl"]]
    files += [
        rel for rel in manifest.get("examples", [])
        if not any(t in Path(rel).name.lower() for t in ("edge", "invalid"))
    ]
    return files


def sparql_select(
    endpoint: str,
    query: str,
    auth: tuple[str, str] | None,
    timeout: float,
    method: str,
) -> dict:
    headers = {"Accept": "application/sparql-results+json"}
    if auth:
        token = base64.b64encode(f"{auth[0]}:{auth[1]}".encode()).decode()
        headers["Authorization"] = f"Basic {token}"
    if method == "GET":
        url = f"{endpoint}?{urllib.parse.urlencode({'query': query})}"
        request = urllib.request.Request(url, headers=headers)
    else:
        headers["Content-Type"] = "application/sparql-query"
        request = urllib.request.Request(
            endpoint, data=query.encode("utf-8"), headers=headers, method="POST"
        )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.load(response)


def canonical_rows(results: dict) -> list[dict[str, str | None]]:
    variables = results["head"]["vars"]
    rows = []
    for binding in results["results"]["bindings"]:
        rows.append(
            {
                variable: binding[variable]["value"] if variable in binding else None
                for variable in variables
            }
        )
    return sorted(rows, key=lambda row: json.dumps(row, sort_keys=True))


def canonical_expected(expected: list[dict]) -> list[dict[str, str | None]]:
    rows = [
        {key: None if value is None else str(value) for key, value in row.items()}
        for row in expected
    ]
    return sorted(rows, key=lambda row: json.dumps(row, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--endpoint", help="SPARQL query endpoint URL")
    parser.add_argument(
        "--print-files", action="store_true",
        help="Print the files the dataset must hold for the expected answers, then exit",
    )
    parser.add_argument("--user", help="HTTP basic auth user (optional)")
    parser.add_argument("--password", help="HTTP basic auth password (optional)")
    parser.add_argument("--only", action="append", help="Question id to run (repeatable)")
    parser.add_argument("--no-compare", action="store_true", help="Print rows, skip the comparison")
    parser.add_argument("--method", choices=["GET", "POST"], default="GET")
    parser.add_argument("--timeout", type=float, default=60.0, help="Seconds per query")
    args = parser.parse_args()
    if args.print_files:
        print("\n".join(evaluation_files()))
        return 0
    if not args.endpoint:
        parser.error("--endpoint is required")

    auth = (args.user, args.password) if args.user else None
    questions = load_questions()
    if args.only:
        unknown = set(args.only) - {q["id"] for q in questions}
        if unknown:
            print(f"unknown question id(s): {sorted(unknown)}", file=sys.stderr)
            return 2
        questions = [q for q in questions if q["id"] in args.only]

    print(f"endpoint: {args.endpoint}")
    all_ok = True
    for question in questions:
        qid = question["id"]
        query = (ROOT / question["file"]).read_text(encoding="utf-8")
        try:
            results = sparql_select(args.endpoint, query, auth, args.timeout, args.method)
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", "replace")[:500]
            print(f"[FAIL] {qid}: HTTP {exc.code} {exc.reason}\n       {body.strip()}")
            all_ok = False
            continue
        except (urllib.error.URLError, TimeoutError, ValueError) as exc:
            print(f"[FAIL] {qid}: {exc}")
            all_ok = False
            continue
        actual = canonical_rows(results)
        if args.no_compare:
            print(f"[ROWS] {qid}: {len(actual)} row(s)")
            for row in actual:
                print(f"       {json.dumps(row, sort_keys=True)}")
            continue
        expected = canonical_expected(question.get("expected_answers") or [])
        if actual == expected:
            print(f"[OK]   {qid}: {len(actual)} exact answer(s)")
        else:
            all_ok = False
            print(f"[FAIL] {qid}: exact-answer mismatch")
            print(f"       expected={json.dumps(expected, sort_keys=True)}")
            print(f"       actual={json.dumps(actual, sort_keys=True)}")
    print(f"result: {'PASS' if all_ok else 'FAIL'}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
