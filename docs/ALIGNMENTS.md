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
Likewise, `hcm-tech:monitoredBy` is a monitoring association rather than an
installation relation. Rack-level, portable, or remote sensors may monitor an
enclosure without an `hcm-tech:installedIn` assertion.

### Edition policy

Most SOSA terms reused by HCMO occur in the
[2017 W3C Recommendation](https://www.w3.org/TR/vocab-ssn/).
`sosa:Property`, however, follows the developing
[SOSA/SSN 2023 Edition](https://www.w3.org/TR/vocab-ssn-2023/), currently
published as a W3C Working Draft; the 2017 edition uses
`sosa:ObservableProperty` instead. The current `sosa:Property` reference is
therefore provisional. A dated SOSA source and its exact semantics must be
pinned before HCMO treats this choice as a stable alignment.

## SemTS

SemTS alignment remains provisional. HCMO currently contains references derived
from an earlier SemTS model, but their canonical IRIs and semantic fit have not
yet been validated. These references are not counted as implemented
external-vocabulary reuse.

## OWL-Time

The current example data represent observation intervals directly with
`time:Interval`, `time:hasBeginning`, and `time:hasEnd`; the duration competency
query consumes that pattern. These OWL-Time terms are not redeclared as HCMO
classes or properties. The former
`hcm:OWL-Timeintervaltable` artifact is deprecated without replacement.

## Units roadmap

HCMO 0.2.0 retains datatype values plus explicit unit strings. Adopting QUDT or
OM quantity-value patterns remains an open, separately reviewed modeling
decision.
