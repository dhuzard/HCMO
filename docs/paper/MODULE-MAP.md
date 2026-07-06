# HCMO re-modularisation — term → module map (build spec for T3b)

**Decided shape (HITL R5, 2026-07-03):** 5 modules
`hcm` **core = enclosure only** · `bio` · `obs` (observations **+** results) · `env` · **`tech`** (new).

- Namespaces: `…/hcm#` (core) · `…/hcm/bio#` · `…/hcm/obs#` · `…/hcm/env#` · `…/hcm/tech#` (new).
- Decisions applied: results → obs (Q20); `tech` own module (Q19); `HousingAssignment` → bio (#2);
  `EnclosureDimensions` **and its dimension properties** → core (#3); QUDT/OM = open (Q21).
- This is the spec, **not yet implemented**. All §6 micro-decisions **RESOLVED 2026-07-03**.
- Placeholders (`UNKNOWN:` / `ns:` / `xsd:*`-as-property) are assigned to their likely module **and**
  flagged for T4 (define or drop). Reused external terms (§5) are **not** HCMO-minted and don't move.

Source of truth for the inventory: `dist/profile.json` (31 classes · 39 obj · 74 data props).

---

## 1. `hcm` core — enclosure only

| Term | Kind | Note |
|------|------|------|
| `MonitoredEnclosure` | Class | The hub / central Feature-of-Interest. Keeps its restrictions (they reference bio/obs/env/tech → expected cross-module axioms). Drop the cruft axiom `⊑ ObservationResult`. |
| `Enrichment` | Class | Housing enrichment. |
| `EnclosureDimensions` | Class | Moved from env (#3). |
| `hasDimensions` | ObjProp | enclosure → dimensions. |
| `hasHeight` `hasLength` `hasWidth` `hasDimUnit` | DataProp | **Move from env → core** — they describe `EnclosureDimensions` (#3 consequence). |
| `hasCapacity` `hasEnclosureIdentifier` `isOccupied` | DataProp | Enclosure attributes. |
| `hasEnrichment` `locatedIn` `hasMonitoredAnimals` | ObjProp | Enclosure relations. |
| `hasName` `hasDescription` | DataProp | Generic identity/label — kept in core as shared. |
| `hasManufacturer` (enclosure) | DataProp | Enclosure manufacturer (M5). Device manufacturer = separate prop in `tech`. |
| `hasEnvironment` | ObjProp | → concern **env**; relation to `EnvironmentProfile`. |

## 2. `bio` — biological subjects & grouping

| Term | Kind | Note |
|------|------|------|
| `Subject` `ExperimentalGroup` | Class | |
| `StudyFactors` | Class | **Moved from core (M1)**; drop the `⊑ MonitoredEnclosure` axiom — it's experimental design, not an enclosure. |
| `HousingAssignment` | Class | **Moved from obs (#2)** — it's a subject↔enclosure relation, not an observation. |
| `belongsToGroup` `hasMember` `hasHousingAssignment` | ObjProp | Grouping & housing. |
| `hasBehaviorObservation` `hasHealthStatusObservation` `hasWeightObservation` | ObjProp | bio→obs links (direction = T3c; bio↔obs cycle accepted for V1). |
| `hasBiologicalSex` `hasDateOfBirth` `hasSpecies` `hasStrain` `hasTreatment` | DataProp | Subject attributes. |
| `assignedToEnclosure` | ObjProp | ⚠ follows `HousingAssignment` → **bio** (was obs). |

## 3. `obs` — observations **and** results

| Term | Kind | Note |
|------|------|------|
| `BehaviorObservation` `EnvironmentObservation` `GasConcentrationObservation` `HealthStatusObservation` `WeightObservation` | Class | Observations. |
| `ObservationResult` `BehaviorResult` `CategoricalResult` `QuantityValue` | Class | **Results → obs (Q20).** `CategoricalResult` is an orphan (unused) — define + wire or drop (T4). `QuantityValue` ⚠ candidate for QUDT/OM (Q21). |
| `Structural&LocationTable` | Class | **→ obs** as `LocationResultTable` (it's a result table); illegal `&` IRI and legacy label removed in v2. |
| `hasResult` `occursIn` | ObjProp | |
| `hasBehaviorType` `hasHealthStatusTerm` `hasConfidenceScore` `hasInterval` `hasCategory` | DataProp | Observation/result attributes. |
| ~~`hasUnit` (core-ns)~~ `hasNumericValue` | DataProp | `hasUnit` **removed → QUDT/OM** (M4). `hasNumericValue`/`hasValue` are QUDT/OM candidates (Q21). |

## 4. `env` — environmental parameters (specified / target side)

| Term | Kind | Note |
|------|------|------|
| `EnvironmentProfile` `EnvironmentalProperty` `GasConcentrationProfile` `LightCycle` `MeasurementSpecification` `ThriveProfile` | Class | |
| `AmbientTemperature` `RelativeHumidity` `OxygenConcentration` `CarbonDioxideConcentration` `AmmoniaConcentration` `LightIntensity` `LightState` | ObjProp | Environmental properties. |
| `hasGasConcentrationProfile` `hasLightCycle` `hasMeasurementSpec` `hasThriveProfile` | ObjProp | Profile links (`hasThriveProfile` ⚠ domain enclosure). |
| `hasGasType` `hasValue` | DataProp | Measurement values. `hasUnit` (env-ns) **removed → QUDT/OM** (M4); `hasValue` = QUDT/OM candidate (Q21). |

## 5. `tech` — devices & data (NEW module, `…/hcm/tech#`)

| Term | Kind | Note |
|------|------|------|
| `Sensor` `Hardware` `Software` | Class | **IRIs move `…/hcm#` → `…/hcm/tech#`** (breaking; before T9). |
| `TimeSeries` | Class | → **tech** (M2); aligns with reused `semts:TimeSeriesSegment`. |
| `installedIn` `monitoredBy` | ObjProp | Device↔enclosure — placed with **tech** (M6). |
| `hasFileFormat` `hasSamplingRate` `hasStoragePath` `hasVersion` | DataProp | Device/software attributes; `hasVersion` = software (M5). |
| *device-manufacturer* | DataProp | New prop for device manufacturer (M5 split from enclosure `hasManufacturer`). |

## 6. Micro-decisions — ✅ RESOLVED 2026-07-03

| # | Term(s) | Decision |
|---|---------|----------|
| M1 | `StudyFactors` | → **bio**; **drop** the `⊑ MonitoredEnclosure` axiom. |
| M2 | `TimeSeries` | → **tech**. |
| M3 | `hasHeight/Length/Width/DimUnit` | → **core** (leave env), following `EnclosureDimensions`. |
| M4 | `hasUnit` ×2 (core-ns + env-ns) | **Fold into QUDT/OM** — remove both HCMO `hasUnit`; represent units via QUDT/OM (**commits Q21 for units**). `hasValue`/`hasNumericValue` become QUDT/OM candidates too. |
| M5 | `hasManufacturer`, `hasVersion` | **Split by domain**: enclosure-manufacturer → **core**; device-manufacturer + `hasVersion` (software) → **tech** (mint separate props where needed). |
| M6 | `monitoredBy` / `installedIn` | → **tech** (place with the device concern; matches T3c policy). |
| M7 | `OWL-Timeintervaltable` | **Drop / redefine** against OWL-Time (T4). |

## 7. Reused (external) — NOT HCMO-minted, do not move

- **SOSA/SSN**: `hasFeatureOfInterest`, `hasResult`, `madeBySensor`, `madeObservation`, `observedProperty`, `phenomenonTime`, `resultTime`, `usedProcedure`.
- **OWL-Time**: `TemporalEntity`, `hasBeginning`, `hasEnd`, `inXSDDateTime`.
- **semts**: `DataDimension`, `TimeSeriesSegment`, `during`, `generated`, `hasDimension`, `isPartOf`, `dimensionUnit`, `title`.

These are declared where used (or as core imports) and appear in alignment axioms (`docs/ALIGNMENTS.md`), not re-homed.

## 8. Junk → drop (T4)

`ns:Class2` *(already removed)* · `ns:objectProperty` · `xsd:boolean` / `xsd:integer` typed as properties ·
empty `…/hcm/obs#` property (blank label) · duplicate `UNKNOWN:hasName` (real `hcm:hasName` exists).

## 9. Placeholders → define or drop (T4/T5), grouped by likely target module

- **tech**: `hasSensors` `captures` `hasActuators`
- **core/enclosure**: `hasEnrichmentReq` `partOF`
- **obs/condition model**: `hasCondition`
- **bio**: none remaining
- **generic → redefine/drop**: `hasType`

> 7 placeholders remain after the v2 cleanup passes. All are `UNKNOWN:`/`ns:` today; each becomes a real term in the module above
> (with label + `rdfs:comment`, T5) or is dropped. Note the tech bucket dominates — the rationale for Q19
> (a `tech` module quarantines this debt).
