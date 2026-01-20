#!/usr/bin/env bash
set -euo pipefail

DATA="${1:-examples/abox-minimal.ttl}"
SHAPES="${2:-shapes/hcm-shapes.ttl}"

PYTHON_BIN="${PYTHON_BIN:-}"
if [ -z "${PYTHON_BIN}" ]; then
  if command -v python >/dev/null 2>&1; then
    PYTHON_BIN="python"
  elif command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="python3"
  else
    echo "Python not found on PATH. Set PYTHON_BIN or install python3." >&2
    exit 127
  fi
fi

VENV_DIR="${VENV_DIR:-.venv}"

echo "Validating data '${DATA}' against shapes '${SHAPES}' with pySHACL..."

set +e
"${PYTHON_BIN}" - <<'PY'
import importlib.util
import sys

sys.exit(0 if importlib.util.find_spec("pyshacl") else 1)
PY
PYSHACL_PRESENT=$?
set -e

if [ ${PYSHACL_PRESENT} -ne 0 ]; then
  echo "Installing dependencies (pyshacl, rdflib)"
  if [ ! -x "${VENV_DIR}/bin/python" ]; then
    "${PYTHON_BIN}" -m venv "${VENV_DIR}"
  fi
  PYTHON_BIN="${VENV_DIR}/bin/python"
  "${PYTHON_BIN}" -m pip install -r tooling/requirements.txt
fi

"${PYTHON_BIN}" - <<'PY'
import glob
import sys
from rdflib import Graph

patterns = ("ontology/*.ttl", "shapes/*.ttl", "examples/*.ttl")

for pattern in patterns:
    matches = sorted(glob.glob(pattern))
    if not matches:
        print(f"[WARN] No files matched {pattern}")
    for path in matches:
        graph = Graph()
        try:
            graph.parse(path, format="turtle")
            print(f"[OK] Parsed: {path}")
        except Exception as exc:
            print(f"[ERR] Parse failed: {path}: {exc}")
            sys.exit(2)
PY

"${PYTHON_BIN}" -m pyshacl -s "${SHAPES}" -m -i rdfs -a -f human "${DATA}"

if [ $? -eq 0 ]; then
  echo "Validation passed."
else
  echo "Validation failed."
  exit 1
fi
