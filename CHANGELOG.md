# Changelog

All notable changes to the HCMO / MAPP ontology are documented here. Versions
track `owl:versionInfo` of the ontology (`https://w3id.org/hcmo/ontology/hcm`).

## [0.0.1] - 2026-06-11

First release of the **MAPP** ontology line (Monitoring and Analytics for
Physiological Processes) and the reorganized, tool-consumable repository layout.

### Namespace

The active ontology keeps the established namespace
**`https://w3id.org/hcmo/ontology/hcm#`** (the same base the prior repository
ontology used; the `w3id` redirect is to be created). The attached source was
authored on `https://w3id.org/hcm/`; its terms were re-namespaced onto
`https://w3id.org/hcmo/ontology/hcm#` (string-level IRI remap — **no local term
names changed**). Module sub-namespaces are path segments under the base:

- core → `https://w3id.org/hcmo/ontology/hcm#`
- bio  → `https://w3id.org/hcmo/ontology/hcm/bio#`
- env  → `https://w3id.org/hcmo/ontology/hcm/env#`
- obs  → `https://w3id.org/hcmo/ontology/hcm/obs#`

- **Ontology IRI:** `https://w3id.org/hcmo/ontology/hcm`
- **`owl:versionIRI`:** `https://w3id.org/hcmo/ontology/hcm/0.0.1` (none was
  authored in the source; added to match `owl:versionInfo "0.0.1"`).

Note: this is a **new term set** (MAPP 0.0.1: MonitoredEnclosure, Subject,
observation classes, …) sharing the same namespace as the legacy HCMO 1.0.0
ontology now under `ontology/legacy/`. The two are different term sets; only
`ontology/modules/` is merged into `dist/`. `owl:versionInfo` is `0.0.1` as
authored (note it sorts below the legacy `1.0.0`).

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
- None (first release of the MAPP term set). No local term names were changed;
  the source IRIs were only re-namespaced from `https://w3id.org/hcm/*` onto the
  retained `https://w3id.org/hcmo/ontology/hcm#` base. Future releases will list
  per-term `old -> new` renames here, diffed against the committed
  `dist/profile.json`.

### Known issues (see `docs/MISSING-DEFINITIONS.md`)
- All 143 authored class/property terms lack `rdfs:comment` definitions.
- 1 term lacks a label (`https://w3id.org/hcmo/ontology/hcm/obs#`).
- 43 Chowlk placeholder/erroneous terms preserved as-authored (`UNKNOWN:*`,
  `ns:Class2`, `ns:objectProperty`, `xsd:boolean`/`xsd:integer` typed as
  properties).
- `shapes/`, `examples/`, `queries/` use the `hcmo` namespace but reference the
  legacy term set (e.g. `hcm:System`, `hcm:ObservationWindow`), which the MAPP
  0.0.1 term set does not define; they need re-authoring against the MAPP terms.
  Competency queries currently return 0 rows against the MAPP graph.
