# 4. Resource description

- MAPP framework overview; namespace policy (w3id base + module sub-namespaces).
- Modular structure: hcm-core / hcm-bio / hcm-env / hcm-obs.
- Key classes: MonitoredEnclosure, Subject, ExperimentalGroup, observation
  classes (Weight/Behavior/Health/Environment), ObservationResult, Sensor,
  Hardware, Software, QuantityValue, EnclosureDimensions, TimeSeries(Segment).
- Key properties & restrictions (composition, monitoring, temporal, results).
- Standards reuse & alignment axioms (cite `docs/ALIGNMENTS.md`):
  Sensor ⊑ sosa:Sensor; System ⊑ sosa:Platform; ObservationWindow ⊑
  time:TemporalEntity; producedBy ⊑ prov:wasAttributedTo;
  BehaviorAndPhysiology ⊑ bfo:process.
- JSON-LD context for application developers.
- Figure F2: ontology overview (WebVOWL).
