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

## Remaining placeholders by proposed action

### Mint in `tech`

| Placeholder | Proposed term | Kind | Notes |
|---|---|---|---|
| `UNKNOWN:supportsEnclosure` | `hcm-tech:supportsEnclosure` | ObjectProperty | Device/system support relation to enclosure. |
| `UNKNOWN:hasSensors` | `hcm-tech:hasSensor` or drop | ObjectProperty | Likely overlaps with `monitoredBy`; decide direction before minting. |
| `UNKNOWN:captures` | `hcm-tech:captures` or SOSA property | ObjectProperty | Currently typed datatype; likely a relation. Check against SOSA before minting. |
| `UNKNOWN:hasActuators` | `hcm-tech:hasActuator` | ObjectProperty | Currently typed datatype; plural suggests relation. |

### Mint in `env`

| Placeholder | Proposed term | Kind | Notes |
|---|---|---|---|
| `UNKNOWN:hasCondition` | `hcm-env:hasCondition` | DatatypeProperty | General condition label; may later become object relation to a Condition class. |

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

### Drop or defer

| Placeholder | Proposed action | Notes |
|---|---|---|
| `UNKNOWN:hasType` | Drop/defer | Too generic; replace with more specific terms or controlled vocabularies. |
