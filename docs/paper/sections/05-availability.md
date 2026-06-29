# 5. Engineering & availability

- Release manifest (`hcmo.yaml`) as a stable contract for downstream tools.
- Modular Turtle sources → reproducible, byte-identical `dist/` (TTL/OWL/JSON-LD)
  via `tooling/build.py`; clean diffs.
- Validation gate (`tooling/validate.py`): TTL parse + pySHACL + competency
  queries; same check runs in CI.
- Availability (CfP hard gate): PURL `w3id.org/hcmo/ontology/hcm`, Zenodo DOI,
  open repo, downloadable artifacts, **+ a public SPARQL endpoint** (HITL R3 —
  to be hosted before submission, T0-dependent; see TODO).
- License: CC BY 4.0. Canonical citation: CITATION.cff.
- Documentation: WIDOCO HTML (human + machine readable) → FAIR.
- FAIR mapping table (see metadata/resource-metadata.md).
- Figure F1: architecture & build/release pipeline.
