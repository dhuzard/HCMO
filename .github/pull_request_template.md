## What and why

<!-- One semantic concern per PR. Link the issue or term request. -->

## Semantic effect

- Modules / files touched:
- Terms added, changed or deprecated (IRIs; no IRI is renamed or deleted):
- Expected effect on reasoning, shapes or competency questions:

## Checklist

- [ ] New/changed terms have an `rdfs:label`, a definition and a provenance note
- [ ] Edited the source in `ontology/modules/` (nothing under `dist/` was hand-edited)
- [ ] `python tooling/build.py` run; regenerated `dist/` committed (re-running gives no diff)
- [ ] `python tooling/validate.py` passes
- [ ] `CHANGELOG.md` updated under `[Unreleased]` (`### Renamed` section if a term moved, as `old -> new`)
