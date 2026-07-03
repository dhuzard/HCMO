# HCMO v2 placeholder cleanup map

Status: working map for T4. This file records how each remaining
`UNKNOWN:`/placeholder term in `ontology/v2/modules/hcm-placeholders.ttl` should
be handled before promotion. The goal is to avoid silently minting weak terms.

## Already resolved in v2

| Placeholder | Resolution | Rationale |
|---|---|---|
| `UNKNOWN:isOccupied` | Replace with existing `hcm:isOccupied` | Exact duplicate in core. |
| `UNKNOWN:isOperational` | Mint as `hcm:isOperational` | Enclosure operational status is a core enclosure attribute and is already used by `MonitoredEnclosure`. |
| `UNKNOWN:hasSamplingRate` | Drop duplicate; use `hcm-tech:hasSamplingRate` | Exact device/data property already exists in `tech`. |

## Remaining placeholders by proposed action

### Mint in `tech`

| Placeholder | Proposed term | Kind | Notes |
|---|---|---|---|
| `UNKNOWN:communicatesWith` | `hcm-tech:communicatesWith` | ObjectProperty | Device-to-device/system communication relation. |
| `UNKNOWN:runsOn` | `hcm-tech:runsOn` | ObjectProperty | Software-to-hardware relation. |
| `UNKNOWN:supportsEnclosure` | `hcm-tech:supportsEnclosure` | ObjectProperty | Device/system support relation to enclosure. |
| `UNKNOWN:hasSensors` | `hcm-tech:hasSensor` or drop | ObjectProperty | Likely overlaps with `monitoredBy`; decide direction before minting. |
| `UNKNOWN:captures` | `hcm-tech:captures` or SOSA property | ObjectProperty | Currently typed datatype; likely a relation. Check against SOSA before minting. |
| `UNKNOWN:hasActuators` | `hcm-tech:hasActuator` | ObjectProperty | Currently typed datatype; plural suggests relation. |
| `UNKNOWN:hasFirmware` | `hcm-tech:hasFirmware` | DatatypeProperty | Literal firmware identifier/version unless a Firmware class is introduced. |
| `UNKNOWN:hasModelNumber` | `hcm-tech:hasModelNumber` | DatatypeProperty | Device metadata. |
| `UNKNOWN:hasProtocol` | `hcm-tech:hasProtocol` | DatatypeProperty | Communication protocol label/identifier. |
| `UNKNOWN:hasSensorIdentifier` | `hcm-tech:hasSensorIdentifier` | DatatypeProperty | Device identifier. |
| `UNKNOWN:hasSensorTechnology` | `hcm-tech:hasSensorTechnology` | DatatypeProperty | Technology label/category. |
| `UNKNOWN:hasSensorType` | `hcm-tech:hasSensorType` | DatatypeProperty | Sensor category; consider controlled vocabulary later. |
| `UNKNOWN:isCalibrated` | `hcm-tech:isCalibrated` | DatatypeProperty | Boolean calibration state. |

### Mint in `env`

| Placeholder | Proposed term | Kind | Notes |
|---|---|---|---|
| `UNKNOWN:hasCondition` | `hcm-env:hasCondition` | DatatypeProperty | General condition label; may later become object relation to a Condition class. |
| `UNKNOWN:hasDarkPhaseDuration` | `hcm-env:hasDarkPhaseDuration` | DatatypeProperty | Light-cycle parameter. |
| `UNKNOWN:hasDarkPhaseStart` | `hcm-env:hasDarkPhaseStart` | DatatypeProperty | Light-cycle parameter. |
| `UNKNOWN:hasDawnDuration` | `hcm-env:hasDawnDuration` | DatatypeProperty | Light-cycle transition parameter. |
| `UNKNOWN:hasDuskDuration` | `hcm-env:hasDuskDuration` | DatatypeProperty | Light-cycle transition parameter. |
| `UNKNOWN:hasLightPhaseDuration` | `hcm-env:hasLightPhaseDuration` | DatatypeProperty | Light-cycle parameter. |

### Mint in `core`

| Placeholder | Proposed term | Kind | Notes |
|---|---|---|---|
| `UNKNOWN:hasEnrichmentReq` | `hcm:hasEnrichmentRequirement` | ObjectProperty or DatatypeProperty | Decide whether requirements become modeled objects. |
| `UNKNOWN:hasEnrichmentType` | `hcm:hasEnrichmentType` | DatatypeProperty | Enclosure/enrichment attribute. |
| `UNKNOWN:hasFacilityType` | `hcm:hasFacilityType` | DatatypeProperty | Facility/location attribute. |
| `UNKNOWN:hasFloorArea` | `hcm:hasFloorArea` | DatatypeProperty | Enclosure/space dimension; later QUDT/OM candidate. |
| `UNKNOWN:hasFoodReq` | `hcm:hasFoodRequirement` | DatatypeProperty | Husbandry requirement; consider future needs profile. |
| `UNKNOWN:hasSafetyReq` | `hcm:hasSafetyRequirement` | DatatypeProperty | Husbandry/facility requirement. |
| `UNKNOWN:hasWaterReq` | `hcm:hasWaterRequirement` | DatatypeProperty | Husbandry requirement; consider future needs profile. |
| `UNKNOWN:partOF` | `hcm:partOf` or external relation | ObjectProperty | Typo/case issue; use a standard part-whole relation if one is adopted. |

### Mint in `bio`

| Placeholder | Proposed term | Kind | Notes |
|---|---|---|---|
| `UNKNOWN:hasSocialReq` | `hcm-bio:hasSocialRequirement` | DatatypeProperty | Subject/group husbandry requirement. |

### Drop or defer

| Placeholder | Proposed action | Notes |
|---|---|---|
| `UNKNOWN:hasType` | Drop/defer | Too generic; replace with more specific terms or controlled vocabularies. |

