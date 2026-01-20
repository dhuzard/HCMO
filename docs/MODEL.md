# Modeling Notes

Scope
- System composition (enclosure, hardware, software), animals, behaviors, sensors/actuators, time intervals, needs.

Key Choices
- Behavior as process: `hcm:BehaviorAndPhysiology` treated as an occurrence (aligns to BFO process).
- Observation window: `hcm:ObservationWindow` with `durationHours` > 24 and optional extendability; conditions modeled via `hcm:hasCondition`.
- Composition: `hcm:hasEnclosure`, `hcm:hasHardware`, `hcm:hasSoftware` plus property-chain-derived `hcm:hasSensor`/`hcm:hasActuator` from hardware components.
- Needs: object-based 5-tuple via `hcm:AnimalNeedProfile`; deprecated boolean needs remain for legacy data.
- Enclosure vs space: `hcm:Enclosure` is an artifact linked to a `hcm:PhysicalSpace` via `hcm:hasSpaceRegion`.
- Dimensions: simple datatype pattern; roadmap to QUDT/OM for quantity values and units.

Alternatives
- N-ary relations for System composition with provenance.
- SOSA Observation: add `sosa:Observation` instances linked to `sosa:FeatureOfInterest` (animals) if measurement semantics are required.

Constraints Strategy
- OWL gives typing/inference; SHACL enforces data-quality rules (cardinality, numeric thresholds).
