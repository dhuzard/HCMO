# Alignments

## Claim-strength policy

HCMO uses three claim levels, accepted for the resource paper on 2026-07-31:

1. **Implemented semantic reuse/alignment** means that canonical, versioned,
   semantically reviewed external terms participate in normative HCMO
   semantics. The strength of each assertion—direct reuse, specialization,
   instance typing, or equivalence—must still be stated; this level never
   implies alignment with an entire vocabulary.
2. **Validated interoperability evidence** means that a pinned, executable
   example combines HCMO and external terms and is covered by validation and
   exact-answer competency questions. It demonstrates the tested workflow, not
   general class mappings, complete round trips, or profile conformance.
3. **Formal profile conformance** requires a pinned external profile and
   evidence that every applicable normative requirement is satisfied within a
   declared scope. HCMO currently makes no external formal-conformance claim.

“Provisional” is a review status, not a fourth achievement level. A provisional
reference is not counted as implemented reuse or alignment.

| Vocabulary or profile | Current classification | Scope |
| --- | --- | --- |
| BFO and IAO | Implemented selective alignment | Canonical upper anchors and the optional source-faithful developer hierarchy |
| SOSA 2017 terms | Implemented selective reuse/alignment | Reviewed sensor, actuator, observation, result, and relation terms |
| Schema.org | Implemented selective reuse | Contributor, place, and exchange terms |
| OWL-Time | Validated interoperability evidence | Supported example and duration-query pattern |
| PROV-O, OBI, STATO, and ISA/Bioschemas | Validated interoperability evidence | One pinned recording-to-statistical-result workflow; no HCMO class mappings |
| SemTS | Provisional; not implemented reuse | Canonical IRIs and semantic fit unresolved |
| `sosa:Property` from the developing 2023 Edition | Provisional; not stable alignment | Edition choice and exact semantics unresolved |
| QUDT/OM | Future work | No implemented alignment |
| ISA RO-Crate | No formal conformance claim | Evidence slice only; no complete profile validation or round trip |

## Upper-level anchors

- The default readable upper hierarchy is a checksummed five-anchor
  presentation of BFO 2020 (`bfo/2020/bfo-core.owl`) and IAO 2026-03-30. It
  supplies canonical labels and definitions plus source-entailed shortcuts to
  Entity without a full `owl:imports` closure.
- Physical enclosures, subjects, sensors, actuators, and hardware are anchored
  under BFO material entities.
- Experimental groups appear under BFO material entity by default. The optional
  developer profile restores the more precise BFO object-aggregate parent.
- Environmental properties are BFO qualities and `sosa:Property` instances.
- Profiles, specifications, assignments, software, and recorded result/data
  resources are anchored under the IAO information-content hierarchy.

The optional `ontology/profiles/external-upper-developer.ttl` profile retains
the canonical BFO intermediate distinctions for ontology developers. The
default headings “Material Entity,” “Information Entity,”
“Quality / Property,” and “Process Entity” are a presentation view, not new
HCMO classes or equivalence mappings across upper ontologies. PROV-O remains a
separate provenance view.

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
