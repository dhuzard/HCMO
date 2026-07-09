# FOOPS assessment — 2026-07-09

Assessed artifact: `ontology/v2/hcmo-v2-merged-clean.owl`

Tool: FOOPS `fair_ontologies-0.4.0.jar`, local API `POST /assessOntologyFile`.

Archived machine reports:

- Baseline: `docs/paper/FOOPS-REPORT-2026-07-09.initial.json`
- After metadata fixes: `docs/paper/FOOPS-REPORT-2026-07-09.after-metadata.json`
- After definition fixes: `docs/paper/FOOPS-REPORT-2026-07-09.after-definitions.json`
- After logo metadata: `docs/paper/FOOPS-REPORT-2026-07-09.after-logo.json`

## Result

| Run | Overall score | Main result |
|---|---:|---|
| Initial v2 clean OWL | 0.49444446 | Missing license, namespace URI/prefix, citation, creation date, DOI, publisher, status, source, issued date, logo, and term definitions. |
| After ontology-header metadata fixes | 0.92222226 | Minimum metadata, recommended metadata, license, provenance, prefix, vocabulary reuse, labels, and version IRI checks pass. |
| After v2 term definitions | 0.9888889 | `VOC4` passes: definitions found for all 111 assessed v2 terms. The only remaining scored failure is logo metadata. |
| After logo metadata | 1.0 | All FOOPS checks pass for the v2 clean OWL artifact. |

## Corrective changes applied

- Added FAIR ontology metadata to `ontology/v2/modules/hcm-core.ttl`: resolvable CC BY 4.0 license, VANN namespace URI/prefix, DOI, citation, source repository, created/issued/modified dates, publisher, and draft status.
- Added `rdfs:comment` definitions to all 111 FOOPS-assessed v2 classes and properties in `ontology/v2/modules/*.ttl`.
- Added `schema:logo` metadata pointing to `HCMO-logo3.png`.
- Added BIBO and VANN namespace bindings to `tooling/build_v2_clean.py`.
- Regenerated `ontology/v2/hcmo-v2-merged.ttl`, `ontology/v2/hcmo-v2-merged-clean.ttl`, and `ontology/v2/hcmo-v2-merged-clean.owl` from source modules.

## Remaining FOOPS findings

- None in the 2026-07-09 after-logo run.

Optional FOOPS warnings remain for contributor, previous version, and backward compatibility. Add them only when they are semantically justified by release metadata.
