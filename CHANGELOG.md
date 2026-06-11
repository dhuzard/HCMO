# Changelog

All notable changes to the HCMO / MAPP ontology are documented here. Versions
track `owl:versionInfo` of the ontology (`https://w3id.org/hcm/mapp`).

## [0.0.1] - 2026-06-11

First release of the **MAPP** ontology line (Monitoring and Analytics for
Physiological Processes) and the reorganized, tool-consumable repository layout.

### ⚠️ Namespace change (BREAKING)

The base namespace changed from the previous repository ontology:

- **Old:** `https://w3id.org/hcmo/ontology/hcm#` (ontology IRI
  `https://w3id.org/hcmo/ontology/hcm`, version 1.0.0 — now under `ontology/legacy/`).
- **New:** `https://w3id.org/hcm/` (ontology IRI `https://w3id.org/hcm/mapp`,
  `owl:versionInfo "0.0.1"`).

These are **two different ontologies**, not a renamed one. MAPP 0.0.1 introduces
the sub-namespaces `hcm-bio:` (`…/bio/`), `hcm-env:` (`…/env/`), and `hcm-obs:`
(`…/obs/`). There is **no automatic 1:1 migration map** from the legacy HCMO
terms to MAPP terms; downstream consumers should treat MAPP 0.0.1 as a new
baseline. The legacy ontology is preserved verbatim under `ontology/legacy/`.

`owl:versionIRI` was set to `https://w3id.org/hcm/mapp/0.0.1` (none was authored
in the source; added because the namespace changed).

### Added
- `hcmo.yaml` — stable release manifest (the contract for downstream tools).
- `ontology/modules/` — hand-authored modular sources, split from the authored
  Chowlk export by namespace: `hcm-core`, `hcm-bio`, `hcm-env`, `hcm-obs`.
- `dist/` — generated artifacts: `hcmo.ttl` (merged, canonical), `hcmo.owl`
  (RDF/XML), `hcmo.json` (JSON-LD), `profile.json` (flat term inventory).
- `tooling/build.py` — reproducible, idempotent dist/profile generator.
- `tooling/validate.py` — parse + pySHACL + competency-query gate.
- `.github/workflows/release.yml` — tag-triggered release that attaches `dist/`.
- `queries/competency_questions.yaml` — competency-question index.
- `docs/MISSING-DEFINITIONS.md` — list of terms lacking labels/definitions and
  the Chowlk placeholder/erroneous terms, for authors to fix (not fabricated).

### Changed
- `.github/workflows/validate.yml` now runs `tooling/validate.py` and checks
  that `dist/` is up to date.
- `examples/abox-minimal.ttl` (legacy): added the `hcm:hasSpaceRegion` →
  `hcm:PhysicalSpace` link (existing terms only) so it conforms to the legacy
  shapes as the README documents.

### Moved (history preserved via `git mv`)
- `ontology/hcm.ttl`, `ontology/hcm-align.ttl`, `ontology/hcm-metadata.ttl`,
  `ontology/hcm-bridge-animal.ttl` → `ontology/legacy/`.

### Renamed
- None within the MAPP line (first release). The namespace change above is a
  wholesale ontology replacement vs. the legacy `hcmo` namespace, not a set of
  term renames. Future releases will list per-term `old -> new` renames here,
  diffed against the committed `dist/profile.json`.

### Known issues (see `docs/MISSING-DEFINITIONS.md`)
- All 143 authored class/property terms lack `rdfs:comment` definitions.
- 1 term lacks a label (`https://w3id.org/hcm/obs/`).
- 43 Chowlk placeholder/erroneous terms preserved as-authored (`UNKNOWN:*`,
  `ns:Class2`, `ns:objectProperty`, `xsd:boolean`/`xsd:integer` typed as
  properties).
- `shapes/`, `examples/`, `queries/` still target the legacy `hcmo` namespace
  and need re-authoring for MAPP; competency queries currently return 0 rows
  against the MAPP graph.
