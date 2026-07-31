# ADR-0003: Environmental roles and temporal state evidence

- Status: accepted
- Date: 2026-07-31

## Context

Earlier HCMO properties used one relation for three different roles: an
environment profile containing a requirement, a measurement specification
identifying what is specified, and an observation identifying what was
observed. Timeless booleans also asserted occupancy, operational state, and
calibration without saying when or on what evidence the assertion depended.

## Decision

Environmental data use three explicit layers:

1. an `EnvironmentProfile` composes a `MeasurementSpecification` through
   `hcm-env:hasMeasurementSpec`;
2. the specification identifies an `EnvironmentalProperty` through
   `hcm-env:specifiesProperty` and may carry a target
   `hcm-env:hasSpecifiedValue`; and
3. an `EnvironmentObservation` uses the SOSA 2017
   `sosa:observedProperty`/`sosa:hasResult` pattern.

The former temperature, humidity, gas, and light predicates are retained as
deprecated IRIs because they conflate these roles. `ThriveProfile` is an
`EnvironmentProfile`; this hierarchy does not assert compliance, treatment, or
an animal outcome.

Housing history is authoritative in time-bounded `HousingAssignment` records.
Current enclosure membership and occupancy are query results evaluated at an
explicit reference time. `hasMonitoredAnimals` and `isOccupied` are deprecated.

Operational and calibration status use separate activities and information
records. Each record carries a validity interval, a status value, and
`prov:wasGeneratedBy` evidence. SHACL verifies that the generating activity
concerns the same enclosure or sensor. The timeless `isOperational` and
`isCalibrated` properties are deprecated.

Study factors specify independent variables in the study design; experimental
groups are named populations; executed treatments are activities. The
ambiguous `hasTreatment` string is deprecated. `hasCondition` remains only a
non-causal contextual observation link. Subject-to-observation shortcuts are
deprecated in favor of inverse navigation over `sosa:hasFeatureOfInterest`.

## Consequences

Users must provide a reference time for current-state questions. The model can
retain conflicting or changing historical evidence without overwriting an
enclosure or sensor. Existing IRIs remain parseable, but standard-profile
SHACL rejects the three timeless booleans in new data.

