# Alignments

## Upper-level anchors

- Physical enclosures, subjects, sensors, actuators, and hardware are anchored
  under BFO material entities.
- Experimental groups are BFO object aggregates.
- Environmental properties are BFO qualities and `sosa:Property` instances.
- Profiles, specifications, assignments, software, and recorded result/data
  resources are anchored under the IAO information-content hierarchy.

## SOSA

- `hcm-tech:Sensor` is a subclass of `sosa:Sensor`.
- `hcm-tech:Actuator` is a subclass of `sosa:Actuator`.
- HCMO observation classes are subclasses of `sosa:Observation`.
- HCMO result classes are subclasses of `sosa:Result`.
- `hcm-tech:captures` is a subproperty of `sosa:observes`.
- HCMO uses canonical `sosa:hasResult`, `sosa:madeBySensor`, and
  `sosa:hasFeatureOfInterest`; it does not duplicate those relations.

SOSA roles are applied selectively. A domain class is not made a subclass of
`sosa:FeatureOfInterest` merely because one of its instances can be observed.

## OWL-Time

Observation intervals are represented directly with `time:Interval` and
`time:hasBeginning` / `time:hasEnd`. The former
`hcm:OWL-Timeintervaltable` artifact is deprecated without replacement.

## Units roadmap

HCMO 0.2.0 retains datatype values plus explicit unit strings. Adopting QUDT or
OM quantity-value patterns remains an open, separately reviewed modeling
decision.
