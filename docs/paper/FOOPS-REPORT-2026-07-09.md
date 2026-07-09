# FOOPS assessment — 2026-07-09

Assessed artifact: `ontology/v2/hcmo-v2-merged-clean.owl`

Tool: FOOPS `fair_ontologies-0.4.0.jar`, local API `POST /assessOntologyFile`.

Archived machine reports:

- Baseline: `docs/paper/FOOPS-REPORT-2026-07-09.initial.json`
- After metadata fixes: `docs/paper/FOOPS-REPORT-2026-07-09.after-metadata.json`

## Result

| Run | Overall score | Main result |
|---|---:|---|
| Initial v2 clean OWL | 0.49444446 | Missing license, namespace URI/prefix, citation, creation date, DOI, publisher, status, source, issued date, logo, and term definitions. |
| After ontology-header metadata fixes | 0.92222226 | Minimum metadata, recommended metadata, license, provenance, prefix, vocabulary reuse, labels, and version IRI checks pass. |

## Corrective changes applied

- Added FAIR ontology metadata to `ontology/v2/modules/hcm-core.ttl`: resolvable CC BY 4.0 license, VANN namespace URI/prefix, DOI, citation, source repository, created/issued/modified dates, publisher, and draft status.
- Added BIBO and VANN namespace bindings to `tooling/build_v2_clean.py`.
- Regenerated `ontology/v2/hcmo-v2-merged.ttl`, `ontology/v2/hcmo-v2-merged-clean.ttl`, and `ontology/v2/hcmo-v2-merged-clean.owl` from source modules.

## Remaining FOOPS findings

- `OM3`: 5/6 detailed metadata checks pass; the missing required item is a project logo. Do not add `schema:logo`/`foaf:logo` until a canonical HCMO logo exists.
- `VOC4`: 0/111 v2 terms have definitions. Add real `rdfs:comment` and/or `IAO:0000115` definitions in `ontology/v2/modules/*.ttl`; do not generate definitions from labels.

Optional FOOPS warnings remain for contributor, previous version, and backward compatibility. Add them only when they are semantically justified by release metadata.
