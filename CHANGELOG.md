# Changelog

All notable changes to the Home-Cage Monitoring Ontology (HCMO) are documented here. Versions
track `owl:versionInfo` of the ontology (`https://w3id.org/hcmo/ontology/hcm`).

## [Unreleased]

### Added

- Expanded the signed C01 property audit across all 81 active local
  properties, directly used external property groups, and all 49 deprecated
  compatibility properties, with reproducible metadata, migration, domain,
  range, inverse, parent, and shortcut-entailment checks.
- Added an intentionally invalid example whose SHACL targets are selected only
  after ontology domain/range inference.

### Changed

- Made pySHACL validation ontology-aware with the documented RDFS entailment
  contract, while keeping OWL consistency checking in HermiT.
- Run competency questions over the ontology plus positive examples and require
  reviewed exact row counts instead of accepting unexamined empty results.
- No ontology terms, axioms, shapes, or generated release artifacts changed.

### Renamed

- None.

## [0.2.0] - 2026-07-17

Updated the public contribution workflow to emit current HCMO instance data and
to capture conditions, explicit observation results, and richer time-series
file metadata. The stable ontology and term namespaces are unchanged.

### Added

- Ordered `bibo:authorList` ontology metadata with Damien Huzard as first
  author, while retaining the existing `dcterms:creator` assertions.
- A triple CSV form view and download with `subject`, `predicate`, and `object`
  columns, absolute IRIs, and RDF lexical literals.
- A conditions/context form section projected through
  `hcm-obs:hasCondition`.
- Separate representative-result rows projected as SOSA observations and HCMO
  quantitative, categorical, behavioral, or location-table results.
- Time-series file name, version, format, sampling, volume, schema, license,
  and storage-path capture using `hcm-tech:TimeSeries` and existing metadata
  properties.

### Changed

- Advanced the release metadata and `owl:versionIRI` from `0.1.0` to `0.2.0`;
  the base namespace remains `https://w3id.org/hcmo/ontology/hcm#`.
- Migrated the contribution form's Turtle projection from deprecated 0.0.1
  system-catalog terms to the active core, bio, env, obs, tech, and SOSA model.
- Separated measurement parameters (`hcm-env:MeasurementSpecification`) from
  observation results.

### Removed

- Biological-sex collection from the system contribution form. The ontology
  term remains available for subject-level datasets; no term or IRI was deleted.

### Renamed

- None.

## [0.1.0] - 2026-07-16

Expert-review cleanup and promotion of the modular HCMO term set. This is a
pre-1.0 breaking release: the ontology IRI and base namespace are unchanged,
while moved 0.0.1 IRIs are retained as deprecated mapped terms.

### Added

- `hcm-tech` module for sensors, actuators, hardware, software, and time-series
  metadata.
- `hcm-compat` module preserving valid published 0.0.1 HCMO IRIs with
  `owl:deprecated true` and, where justified, `dcterms:isReplacedBy`.
- BFO/IAO upper anchors for active domain classes and SOSA anchors for sensors,
  actuators, observations, properties, and results.
- Explicit `rdfs:domain` and `rdfs:range` axioms for every active HCMO object and
  datatype property; generic `hasName`/`hasDescription` use `owl:Thing` domains.
- ISA/ISA RO-Crate mapping guidance and an executable RDF bridge example for
  animal sources, housing assignments, cages, sensors, observations, and files.

### Changed

- Corrected ontology title/description and repository branding from MAPP to
  **Home-Cage Monitoring Ontology (HCMO)**.
- Replaced the flattened `MonitoredEnclosure` restriction block with a coherent
  hierarchy rooted in `hcm:Enclosure` and scoped links to dimensions, subjects,
  environment profiles, and sensors.
- Removed the invalid `StudyFactors rdfs:subClassOf MonitoredEnclosure` axiom;
  study factors are now modeled as independent-variable information-content
  entities, with the preferred singular label “Study Factor”.
- Added definitions to all active terms and completed active property metadata.
- Standardized observation/result modeling on SOSA, including canonical
  `sosa:hasResult`; observation subclasses now anchor to `sosa:Observation` and
  result subclasses to `sosa:Result`.
- Re-authored SHACL shapes, ABox examples, JSON-LD context, and competency
  queries around the enclosure → housing assignment → subject pattern.
- Switched RDF/XML generation to rdflib's collection-preserving serializer.
- Repointed the automated HermiT check from the retired v2 review source tree
  to the active generated release artifacts declared in `hcmo.yaml`.
- Kept date, time, and duration lexical validation as SHACL constraints while
  using OWL 2-compatible literal ranges in the ontology.
- Removed a misplaced `hasCategory` cardinality restriction that caused every
  environment observation, including gas-concentration observations, to be
  inferred as a categorical result.

### Deprecated

- `hcm:OWL-Timeintervaltable`: invalid Chowlk/spreadsheet artifact, with no
  asserted replacement. SOSA temporal properties and OWL-Time entities are the
  supported temporal model.
- Local 0.0.1 duplicates such as `hcm:hasResult` and `hcm-env:hasUnit`. Use
  canonical `sosa:hasResult` for new observations and consolidated
  `hcm:hasUnit` for units; no equivalence is asserted for the directionally
  inconsistent legacy `hcm:hasResult` relation.
- Other superseded 0.0.1 terms listed in `ontology/modules/hcm-compat.ttl`.

### Removed

- Active `UNKNOWN:`/`ns:` placeholders, datatype IRIs misdeclared as properties,
  and the dangling bare `https://w3id.org/hcmo/ontology/hcm/obs#` object property.
  Their original source is retained under `ontology/legacy/mapp-0.0.1/`.

### Renamed

- `hcm:Actuator` -> `hcm-tech:Actuator`
- `hcm:CategoricalResult` -> `hcm-obs:CategoricalResult`
- `hcm:Dimensions` -> `hcm:EnclosureDimensions`
- `hcm:Hardware` -> `hcm-tech:Hardware`
- `hcm:ObservationResult` -> `hcm-obs:ObservationResult`
- `hcm:QuantityValue` -> `hcm-obs:QuantityValue`
- `hcm:Sensor` -> `hcm-tech:Sensor`
- `hcm:Software` -> `hcm-tech:Software`
- `hcm:Structural&LocationTable` -> `hcm-obs:LocationResultTable`
- `hcm:StudyFactors` -> `hcm-bio:StudyFactors`
- `hcm:TimeSeries` -> `hcm-tech:TimeSeries`
- `hcm-env:EnclosureDimensions` -> `hcm:EnclosureDimensions`
- `hcm-obs:HousingAssignment` -> `hcm-bio:HousingAssignment`
- `hcm-obs:assignedToEnclosure` -> `hcm-bio:assignedToEnclosure`
- `hcm:captures` -> `hcm-tech:captures`
- `hcm:communicatesWith` -> `hcm-tech:communicatesWith`
- `hcm:installedIn` -> `hcm-tech:installedIn`
- `hcm:monitoredBy` -> `hcm-tech:monitoredBy`
- `hcm:hasFileFormat` -> `hcm-tech:hasFileFormat`
- `hcm:hasSamplingRate` -> `hcm-tech:hasSamplingRate`
- `hcm:hasStoragePath` -> `hcm-tech:hasStoragePath`
- `hcm:hasVersion` -> `hcm-tech:hasVersion`
- `hcm:hasCategory` -> `hcm-obs:hasCategory`
- `hcm:hasNumericValue` -> `hcm-obs:hasNumericValue`
- `hcm:hasThriveProfile` -> `hcm-env:hasThriveProfile`
- `hcm-env:hasDimUnit` -> `hcm:hasDimUnit`
- `hcm-env:hasHeight` -> `hcm:hasHeight`
- `hcm-env:hasLength` -> `hcm:hasLength`
- `hcm-env:hasUnit` -> `hcm:hasUnit`
- `hcm-env:hasWidth` -> `hcm:hasWidth`

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
