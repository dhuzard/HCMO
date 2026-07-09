# HCMO v2 placeholder cleanup map

Status: applied cleanup map for T4. This file records how each former
`UNKNOWN:`/placeholder term in `ontology/v2/modules/hcm-placeholders.ttl` was
handled on the v2 review branch. The goal is to make the semantic decisions
auditable before co-author sign-off.

## Already resolved in v2

| Placeholder | Resolution | Rationale |
|---|---|---|
| `UNKNOWN:isOccupied` | Replace with existing `hcm:isOccupied` | Exact duplicate in core. |
| `UNKNOWN:isOperational` | Mint as `hcm:isOperational` | Enclosure operational status is a core enclosure attribute and is already used by `MonitoredEnclosure`. |
| `UNKNOWN:hasSamplingRate` | Drop duplicate; use `hcm-tech:hasSamplingRate` | Exact device/data property already exists in `tech`. |
| `UNKNOWN:communicatesWith` | Mint as `hcm-tech:communicatesWith` | Straightforward device/system communication relation. |
| `UNKNOWN:runsOn` | Mint as `hcm-tech:runsOn` | Straightforward software-to-hardware relation. |
| `UNKNOWN:hasFirmware` | Mint as `hcm-tech:hasFirmware` | Device metadata literal. |
| `UNKNOWN:hasModelNumber` | Mint as `hcm-tech:hasModelNumber` | Device metadata literal. |
| `UNKNOWN:hasProtocol` | Mint as `hcm-tech:hasProtocol` | Device/procedure protocol label or identifier. |
| `UNKNOWN:hasSensorIdentifier` | Mint as `hcm-tech:hasSensorIdentifier` | Sensor identifier metadata. |
| `UNKNOWN:hasSensorTechnology` | Mint as `hcm-tech:hasSensorTechnology` | Sensor technology metadata. |
| `UNKNOWN:hasSensorType` | Mint as `hcm-tech:hasSensorType` | Sensor category metadata; controlled vocabulary can follow later. |
| `UNKNOWN:isCalibrated` | Mint as `hcm-tech:isCalibrated` | Boolean calibration state. |
| `UNKNOWN:hasDarkPhaseDuration` | Mint as `hcm-env:hasDarkPhaseDuration` | Light-cycle duration parameter. |
| `UNKNOWN:hasDarkPhaseStart` | Mint as `hcm-env:hasDarkPhaseStart` | Light-cycle start-time parameter. |
| `UNKNOWN:hasDawnDuration` | Mint as `hcm-env:hasDawnDuration` | Light-cycle transition duration. |
| `UNKNOWN:hasDuskDuration` | Mint as `hcm-env:hasDuskDuration` | Light-cycle transition duration. |
| `UNKNOWN:hasLightPhaseDuration` | Mint as `hcm-env:hasLightPhaseDuration` | Light-cycle duration parameter. |
| `UNKNOWN:hasSocialReq` | Mint as `hcm-bio:hasSocialRequirement` | Subject/group husbandry requirement. |
| `UNKNOWN:hasEnrichmentType` | Mint as `hcm:hasEnrichmentType` | Enclosure/enrichment attribute. |
| `UNKNOWN:hasFacilityType` | Mint as `hcm:hasFacilityType` | Facility/location attribute. |
| `UNKNOWN:hasFloorArea` | Mint as `hcm:hasFloorArea` | Enclosure/space dimension; later QUDT/OM candidate. |
| `UNKNOWN:hasFoodReq` | Mint as `hcm:hasFoodRequirement` | Husbandry requirement literal. |
| `UNKNOWN:hasSafetyReq` | Mint as `hcm:hasSafetyRequirement` | Husbandry/facility requirement literal. |
| `UNKNOWN:hasWaterReq` | Mint as `hcm:hasWaterRequirement` | Husbandry requirement literal. |
| `UNKNOWN:supportsEnclosure` | Mint as `hcm-tech:supportsEnclosure` | Device/system support relation to enclosure. |

## Former remaining placeholders by action

## Applied decisions for co-author review

These decisions have been applied to the v2 RDF modules on the review branch,
but should still be confirmed by co-authors before promotion. They are grounded
in the v2 module split, existing v2 terms, and legacy HCMO where a clear
precedent exists.

| Placeholder | Applied action | Target term | Module | Confidence | Rationale |
|---|---|---|---|---|---|
| `UNKNOWN:captures` | Restore/mint as a tech relation | `hcm-tech:captures` | `tech` | high | Legacy HCMO already had `hcm:captures` for a sensor capturing behaviour/physiology signals. In v2, sensors live in `tech`, so the relation belongs with the device layer. Keep separate from SOSA until we decide whether the object is a signal, behaviour, observed property, or observation. |
| `UNKNOWN:hasActuators` | Replace plural placeholder with singular relation and add/restore actuator class | `hcm-tech:hasActuator` + `hcm-tech:Actuator` | `tech` | high | Legacy HCMO had `hcm:Actuator` and `hcm:hasActuator`. In v2, hardware/sensors/software are in `tech`; actuator should follow the device-layer pattern. Use singular property naming. |
| `UNKNOWN:hasSensors` | Do not mint as-is; replace with existing direction where possible | prefer `hcm-tech:monitoredBy`; optionally add inverse `hcm-tech:hasSensor` later | `tech` | medium | v2 already uses `hcm-tech:monitoredBy` from enclosure/core toward `hcm-tech:Sensor`. Minting `hasSensors` would duplicate that unless we explicitly want an inverse convenience property. |
| `UNKNOWN:hasCondition` | Restore as an observation-side relation, pending condition class decision | `hcm-obs:hasCondition` | `obs` | medium | Legacy HCMO had `hcm:hasCondition`, including observation-window condition usage. In v2 this should not be an environment literal; it needs an object model for experimental/observation conditions. |
| `UNKNOWN:hasEnrichmentReq` | Mint a literal requirement property unless object requirements are adopted soon | `hcm:hasEnrichmentRequirement` | `core` | medium | Existing v2 cleanup already uses literal requirement properties for food, water, safety, and social requirement. Enrichment requirement can follow that pattern for now. |
| `UNKNOWN:partOF` | Do not keep typo; replace with a normal part-whole property only if still needed | `hcm:partOf` or an imported standard relation | `core` | medium | The placeholder is a casing/typo artifact. If no current class restriction needs it, drop it; otherwise use `hcm:partOf` for consistency or adopt a standard part-whole relation as a separate modeling decision. |
| `UNKNOWN:hasType` | Drop/defer; do not mint | none | none | high | Too generic to be semantically useful. Replace case-by-case with specific properties such as `hasSensorType`, `hasEnrichmentType`, controlled vocabulary links, or class membership. |

Implementation notes:

1. Safe tech restorations applied: `captures`, `hasActuator`, `Actuator`.
2. Duplicate sensor relation mapped to existing `hcm-tech:monitoredBy`.
3. Literal enrichment requirement added following the existing requirement
   pattern.
4. `hasCondition` restored in `obs`; its target condition model can still be
   refined later.
5. `hasType` and typo `partOF` were not minted as active terms.

### Mint in `tech`

| Placeholder | Proposed term | Kind | Notes |
|---|---|---|---|
| `UNKNOWN:hasSensors` | Prefer existing `hcm-tech:monitoredBy`; mint inverse `hcm-tech:hasSensor` only if needed | ObjectProperty | Likely overlaps with `monitoredBy`; avoid duplicate semantics unless inverse convenience is explicitly wanted. |
| `UNKNOWN:captures` | `hcm-tech:captures` | ObjectProperty | Legacy HCMO precedent exists; keep in tech with sensors. |
| `UNKNOWN:hasActuators` | `hcm-tech:hasActuator` + `hcm-tech:Actuator` | ObjectProperty + Class | Legacy HCMO precedent exists; singularize property name and keep in tech. |

### Defer: observation condition model

| Placeholder | Proposed term | Kind | Notes |
|---|---|---|---|
| `UNKNOWN:hasCondition` | `hcm-obs:hasCondition` | ObjectProperty | Legacy HCMO models conditions on observation windows; do not mint as an env literal. Needs target condition class/model. |

### Mint in `core`

| Placeholder | Proposed term | Kind | Notes |
|---|---|---|---|
| `UNKNOWN:hasEnrichmentReq` | `hcm:hasEnrichmentRequirement` | DatatypeProperty | Follows existing v2 literal requirement properties unless object requirements are adopted. |
| `UNKNOWN:partOF` | Drop if unused; otherwise `hcm:partOf` or external relation | ObjectProperty | Typo/case issue; use a standard part-whole relation if one is adopted. |

### Drop or defer

| Placeholder | Proposed action | Notes |
|---|---|---|
| `UNKNOWN:hasType` | Drop/defer | Too generic; replace with more specific terms or controlled vocabularies. |
