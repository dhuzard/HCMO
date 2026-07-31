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
| SOSA 2017 terms | Implemented selective reuse/alignment | Reviewed sensor, actuator, observable-property, observation, result, and relation terms; immutable 2017 artifact pinned |
| Schema.org | Implemented selective reuse | Contributor, place, and exchange terms |
| OWL-Time | Implemented selective reuse plus validated interoperability evidence | Time-bounded housing, observation, operational-status, and calibration records with exact-answer queries |
| PROV-O | Implemented selective reuse plus validated interoperability evidence | `prov:Activity` and `prov:wasGeneratedBy` in evidence-backed operational and calibration patterns, plus workflow fixtures |
| OBI, STATO, and ISA/Bioschemas | Validated interoperability evidence | Pinned recording workflow plus lossless extended-crate 2 × 2, housing, Source/Sample, and statistical-result fixtures; no HCMO class mappings |
| SemTS 1.2.0 | Implemented selective reuse/alignment | Canonical `TimeSeriesSegment`, `DataDimension`, and `segmentDimension` terms for location result tables |
| QUDT 3.4.0 | Implemented selective reuse | Pinned QuantityValue, numericValue, hasUnit, and reviewed unit IRIs for dimensions, sampling rates, specifications, and observations |
| OM | Not implemented | QUDT was selected for the release; no OM terms are asserted |
| ISA RO-Crate | Validated interoperability evidence; no formal conformance claim | HCMO RDF/extended-crate graph round trip, RO-Crate 1.2 required validation, and ISA-specific required validation pass; permanent ISA profile URI/base-version decision remains external |

## Upper-level anchors

- The default readable upper hierarchy is a checksummed five-anchor
  presentation of BFO 2020 (`bfo/2020/bfo-core.owl`) and IAO 2026-03-30. It
  supplies canonical labels and definitions plus source-entailed shortcuts to
  Entity without a full `owl:imports` closure.
- Physical enclosures, subjects, sensors, actuators, and hardware are anchored
  under BFO material entities.
- Experimental groups appear under BFO material entity by default. The optional
  developer profile restores the more precise BFO object-aggregate parent.
- Environmental properties are BFO qualities and SOSA 2017
  `sosa:ObservableProperty` instances.
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

HCMO normatively uses the
[2017 W3C Recommendation](https://www.w3.org/TR/2017/REC-vocab-ssn-20171019/).
Its ontology artifact is pinned to W3C's historical repository commit and
checksum in `external-vocabularies.yaml`. Environmental and sensor-captured
properties use `sosa:ObservableProperty`. HCMO does not mix in
`sosa:Property` from the developing later edition. Adopting a later SOSA
edition requires a separate reviewed migration and an immutable source pin.

## SemTS

HCMO selectively reuses SemTS 1.2.0 with its canonical unversioned entity
namespace. A location result table is a `semts:TimeSeriesSegment` and may use
`semts:segmentDimension` values typed as `semts:DataDimension`. SemTS is not
used to describe an observation's observed property, and HCMO does not use
SemTS `generated`, whose knowledge-generation domain and range do not fit the
location-result relation. See ADR-0002 and the migration note.

## OWL-Time

The current example data represent observation intervals directly with
`time:Interval`, `time:hasBeginning`, and `time:hasEnd`; the duration competency
query consumes that pattern. These OWL-Time terms are not redeclared as HCMO
classes or properties. The former
`hcm:OWL-Timeintervaltable` artifact is deprecated without replacement.

## Quantities and units

HCMO uses the QUDT 3.4.0 `QuantityValue`/`numericValue`/`hasUnit` pattern.
The external contract pins both the schema and unit vocabulary. See ADR-0004
for scope and the migration guide for replacements of earlier literal fields.
