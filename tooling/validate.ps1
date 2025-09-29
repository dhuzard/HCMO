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

$parseScript = @"
import glob
import sys
from rdflib import Graph

PATTERNS = ('ontology/*.ttl', 'shapes/*.ttl', 'examples/*.ttl')

for pattern in PATTERNS:
    matches = sorted(glob.glob(pattern))
    if not matches:
        print(f'[WARN] No files matched {pattern}')
    for path in matches:
        graph = Graph()
        try:
            graph.parse(path, format='turtle')
            print(f'[OK] Parsed: {path}')
        except Exception as exc:
            print(f'[ERR] Parse failed: {path}: {exc}')
            sys.exit(2)
"@

python -c $parseScript

if ($LASTEXITCODE -ne 0) {
  Write-Host "Parsing failed." -ForegroundColor Red
  exit 1
}

python -m pyshacl -s $Shapes -m -i rdfs -a -f human $Data

if ($LASTEXITCODE -eq 0) {
  Write-Host "Validation passed." -ForegroundColor Green
} else {
  Write-Host "Validation failed." -ForegroundColor Red
  exit 1
}
