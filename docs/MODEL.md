# Modeling Notes

Scope
- System composition (enclosure, hardware, software), animals, behaviors, sensors/actuators, time intervals, needs.

Key Choices
- Behavior as process: `hcm:BehaviorAndPhysiology` treated as an occurrence (aligns to BFO process).
- Observation window: `hcm:TimeInterval` with `durationHours` ≥ 24 and limited human interaction.
- Composition: `hcm:hasEnclosure`, `hcm:hasHardware`, `hcm:hasSoftware`, `hcm:hasSensor`, `hcm:hasActuator` (n-ary alternative possible via event pattern).
- Needs: simple boolean decomposition; may be upgraded to classes for richer modeling.
- Dimensions: simple datatype pattern; roadmap to QUDT/OM for quantity values and units.

Alternatives
- N-ary relations for System composition with provenance.
- SOSA Observation: add `sosa:Observation` instances linked to `sosa:FeatureOfInterest` (animals) if measurement semantics are required.

Constraints Strategy
- OWL gives typing/inference; SHACL enforces data-quality rules (cardinality, numeric thresholds).

