param(
  [string]$Data = "examples/abox-minimal.ttl",
  [string]$Shapes = "shapes/hcm-shapes.ttl"
)

Write-Host "Validating data '$Data' against shapes '$Shapes' with pySHACL..." -ForegroundColor Cyan

pip show pyshacl | Out-Null
if ($LASTEXITCODE -ne 0) {
  Write-Host "Installing dependencies (pyshacl, rdflib)" -ForegroundColor Yellow
  pip install -r tooling/requirements.txt
}

python - << 'PY'
import sys, glob
from rdflib import Graph

def check_parse(paths):
    for p in paths:
        g = Graph()
        try:
            g.parse(p, format='turtle')
            print(f"[OK] Parsed: {p}")
        except Exception as e:
            print(f"[ERR] Parse failed: {p}: {e}")
            sys.exit(2)

check_parse(glob.glob('ontology/*.ttl'))
check_parse(glob.glob('shapes/*.ttl'))
check_parse(glob.glob('examples/*.ttl'))
PY

python -m pyshacl -s $Shapes -m -i rdfs -a -f human $Data

if ($LASTEXITCODE -eq 0) {
  Write-Host "Validation passed." -ForegroundColor Green
} else {
  Write-Host "Validation failed." -ForegroundColor Red
  exit 1
}

