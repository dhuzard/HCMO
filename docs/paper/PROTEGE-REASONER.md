# Protege reasoner check for HCMO v2

Status: working protocol for Cyril's post-meeting task.

Primary source to test: `ontology/v2/hcmo-v2-merged-clean.owl` on `main`.

Review source with placeholders, if needed: `ontology/v2/hcmo-v2-merged.ttl`.

## Goal

Open the v2 merged ontology in Protege and run an OWL reasoner to check logical
coherence before promotion. This is an ontology-level check, not a data-shape
validation pass.

## Protocol

1. Open Protege.
2. Load `ontology/v2/hcmo-v2-merged-clean.owl`.
3. Confirm that the ontology IRI is `https://w3id.org/hcmo/ontology/hcm`.
4. Start with ELK if available for a fast classification pass.
5. Run HermiT for the stricter OWL DL consistency check.
6. Record:
   - whether the ontology is consistent;
   - any unsatisfiable classes;
   - unexpected inferred superclass/subclass placements;
   - parse/import warnings shown by Protege;
   - any issue linked to the remaining `UNKNOWN:` placeholders.

## Expected current caveats

The v2 draft graph still has seven placeholders isolated in
`ontology/v2/modules/hcm-placeholders.ttl`, but the clean BioPortal/Protege file
excludes them:

- `UNKNOWN:captures`
- `UNKNOWN:hasActuators`
- `UNKNOWN:hasCondition`
- `UNKNOWN:hasEnrichmentReq`
- `UNKNOWN:hasSensors`
- `UNKNOWN:hasType`
- `UNKNOWN:partOF`

These should be commented/debugged in the draft graph, but they should not be
silently renamed or re-modeled without a modeling decision.

## Why no SHACL for now

SHACL validates instance data and application constraints: required fields,
cardinalities for records, numeric ranges, and valid/invalid example ABoxes.
The current SHACL shapes, examples, and competency queries still target the
legacy/live term set, while `ontology/v2/` is a draft re-modularisation.

Running SHACL now would mostly test stale shapes against a moving ontology.
For this stage, the priority is OWL consistency in Protege. SHACL should be
re-authored after the v2 terms are promoted or frozen enough to become the
validation target.

## Output to archive

Create a short report after the Protege pass with:

- Protege version;
- reasoner name and version if visible;
- tested file path and git commit;
- consistency result;
- list of unsatisfiable classes, or "none";
- notes on warnings/debugging decisions.

Pre-check and HermiT results started at
`docs/paper/PROTEGE-DRY-RUN-2026-07-06.md`.
