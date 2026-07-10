# Protege reasoner check for HCMO v2

Status: reproducible reasoner check in place; Protege Desktop open check and
manual HermiT UI pass recorded.

Primary source to test in Protege:
`ontology/v2/hcmo-v2-merged-clean.owl`.

Review source with placeholders, if needed: `ontology/v2/hcmo-v2-merged.ttl`.

## Goal

Open the v2 merged ontology in Protege and run an OWL reasoner to check logical
coherence before promotion. This is an ontology-level check, not a data-shape
validation pass.

Current Protege result: Protege Desktop 5.6.9 opens the clean artifact and
reports successful ontology/imports-closure loading in its log.

Current automated result: the clean artifact loads 33 classes, contains no
`UNKNOWN:` IRIs, and HermiT reports 0 inconsistent classes.

## Protocol

1. Open Protege.
2. Load `ontology/v2/hcmo-v2-merged-clean.owl`.
3. Confirm that the ontology IRI is `https://w3id.org/hcmo/ontology/hcm`.
4. Confirm that the class hierarchy shows `hcm:MonitoredEnclosure` and
   `hcm:Enclosure` as classes, not properties.
5. Confirm that `time:hasBeginning` and `time:hasEnd` appear as object
   properties.
6. Start with ELK if available for a fast classification pass.
7. Run HermiT for the stricter OWL DL consistency check.
8. Record:
   - whether the ontology is consistent;
   - any unsatisfiable classes;
   - unexpected inferred superclass/subclass placements;
   - parse/import warnings shown by Protege;
   - whether any `UNKNOWN:` placeholders appear in the loaded clean file.

## Reproducible command-line check

The same HermiT-family consistency check is available without opening Protege:

```bash
pip install -r tooling/reasoning-requirements.txt
python tooling/reason_v2.py --build-clean --java-memory 2000
```

On local 32-bit Java, use a smaller heap:

```bash
python tooling/reason_v2.py --build-clean --java-memory 512
```

The command fails if the clean artifact contains `UNKNOWN:` IRIs or if HermiT
reports inconsistent classes.

Current command-line result:

| Check | Result |
|---|---:|
| RDF triples in clean OWL | 803 |
| Declared OWL classes | 33 |
| Object properties | 46 |
| Datatype properties | 54 |
| `UNKNOWN:` IRIs | 0 |
| Classes loaded by HermiT | 33 |
| Inconsistent classes | 0 |

## Expected current caveats

The former seven v2 placeholders have been resolved in the draft modules and no
`UNKNOWN:` IRIs remain in either the merged draft or the clean Protege file.
The clean v2 artifact also includes OOPS-driven fixes for untyped
`schema:Person`, reused-vocabulary annotations, and the `hcm-obs:hasResult` /
`sosa:hasResult` alignment.

## Why no SHACL for now

SHACL validates instance data and application constraints: required fields,
cardinalities for records, numeric ranges, and valid/invalid example ABoxes.
The current SHACL shapes, examples, and competency queries still target the
legacy/live term set, while `ontology/v2/` is a draft re-modularisation.

Running SHACL now would mostly test stale shapes against a moving ontology, and
any failures would mix two different questions: "is the ontology logically
coherent?" and "do our future data-entry rules match v2?". For this stage, the
priority is OWL consistency in Protege. SHACL should be re-authored after the v2
terms are promoted or frozen enough to become the validation target.

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
