# Class audit working notes

Status: signed working evidence for accepted checklist item A06. This audit is
a decision gate. It does not authorize automatic class, definition, hierarchy,
mapping, or deprecation changes.

Reviewer: Cyril Gilbert (`https://orcid.org/0009-0008-2489-8106`)

Review started: 2026-07-24

Review branch: `cyril/c04-entailment-contract`

## Scope and method

The audit covers all 33 active local classes declared in the five active source
modules and 15 external classes used directly as superclass, restriction
filler, property domain/range, or contributor type. Deprecated compatibility
classes remain migration evidence and are not active hierarchy candidates.

For every local class, the source catalogue records the full IRI, label,
definition, module, asserted parents, and restrictions. The tables below record
the intended upper category, mapping status, provenance, relevant competency
questions, inferred-parent review, reviewer decision, and rationale.

Run the reproducible catalogue and coverage checks with:

```text
python tooling/class_audit.py --catalog
```

The active IRI, label, and definition baseline is checked against
`dist/profile.json`, as required by A06. Owning modules, parents, and
restrictions are then supplemented from `ontology/modules/*.ttl`; nothing is
copied from a diagram. Inferred parents below are limited to named consequences
of the asserted local hierarchy. HermiT remains the authoritative OWL DL
consistency check. `none beyond asserted` means no additional named parent is
currently entailed from HCMO's own class hierarchy; it is not a statement about
a fully imported external ontology.

All local rows have source provenance `HCMO 0.2.0, owning source module`.
External vocabulary versions are not pinned in the current release, so no
stronger mapping or hierarchy change is authorized until those sources and
versions are reviewed.

## Active local class decisions

Table columns:

- **Class** identifies the full IRI through the repository's namespace map.
- **Decision** uses the controlled A06 decision vocabulary.
- **Upper category / mapping** records the asserted or intended semantic anchor.
- **Restrictions / inferred parents** summarizes logical consequences requiring
  review; the executable catalogue retains the exact expressions.
- **CQ** names current competency-question evidence, or `none`.

### Core

| Class | Decision | Definition and intended upper category / mapping | Restrictions / inferred parents | CQ and review rationale |
| --- | --- | --- | --- | --- |
| `hcm:Enclosure` | `keep` | Physical housing enclosure; asserted BFO material entity. | No restriction; none beyond asserted. | `animals-by-enclosure`, `missing-dimensions`, `needs-provisioning`; meaning and use agree. |
| `hcm:EnclosureDimensions` | `keep` | Information record describing enclosure size; asserted IAO information content entity. | No restriction; none beyond asserted. | `missing-dimensions`; record semantics agree with values and unit fields. |
| `hcm:Enrichment` | `keep` | Material or structure supplied in an enclosure; asserted BFO material entity. | No restriction; none beyond asserted. | none; distinct from textual enrichment requirements. |
| `hcm:MonitoredEnclosure` | `keep` | Enclosure equipped for longitudinal monitoring; local specialization of `hcm:Enclosure`. | Universal fillers constrain dimensions, subjects, environment profiles, and sensors; inferred `hcm:Enclosure` and BFO material entity. | all five CQs; mandatory presence remains in SHACL rather than OWL. |
| `hcm:OperationalAssessment` | `keep` | Process that assesses an enclosure's operational state; asserted BFO process and PROV activity. | Generates an operational status record in the evidence pattern; none beyond asserted anchors. | `status-evidence-at-time`; separates the assessment event from its record. |
| `hcm:OperationalStatusRecord` | `keep` | Time-bounded information record of assessed operational status; asserted IAO information content entity. | SHACL requires a boolean value, validity interval, and generating assessment concerning the same enclosure. | `status-evidence-at-time`; replaces the deprecated timeless boolean. |

### Bio

| Class | Decision | Definition and intended upper category / mapping | Restrictions / inferred parents | CQ and review rationale |
| --- | --- | --- | --- | --- |
| `hcm-bio:ExperimentalGroup` | `keep` | Group of subjects sharing a study condition; exposed under BFO material entity in the end-user model. | The optional developer profile adds the more precise BFO object-aggregate parent. | `animals-by-enclosure`; material grouping is intuitive by default while the precise BFO refinement remains available to ontology developers. |
| `hcm-bio:HousingAssignment` | `keep` | Assignment record linking subjects/groups and enclosures; asserted IAO information content entity. | No restriction; none beyond asserted. | `animals-by-enclosure`, `needs-provisioning`; assignment is correctly reified for study context. |
| `hcm-bio:StudyFactors` | `needs evidence` | Independent variable represented as an information artifact; currently asserted IAO information content entity. | No restriction; none beyond asserted. | none; singular label/plural IRI and factor-versus-factor-specification meaning require domain evidence before definition or mapping changes. |
| `hcm-bio:Subject` | `keep` | Biological individual observed in HCM; asserted BFO material entity. | No observation shortcut restriction; observations identify the subject canonically with `sosa:hasFeatureOfInterest`. | `animals-by-enclosure`, `current-housing-at-time`; intended individual granularity and stable identity are explicit. |

### Environment

| Class | Decision | Definition and intended upper category / mapping | Restrictions / inferred parents | CQ and review rationale |
| --- | --- | --- | --- | --- |
| `hcm-env:EnvironmentProfile` | `keep` | Structured conditions/requirements record; asserted IAO information content entity. | Composes measurement specifications, gas specifications, and light cycles; none beyond asserted. | `environment-spec-observation`; profile/container role is distinct from specification and observation. |
| `hcm-env:EnvironmentalProperty` | `needs evidence` | Environmental property currently anchored to both BFO quality and SOSA Property. | No restriction; inferred parents depend on external ontologies not imported. | `sensors-behaviors`; BFO-quality versus SOSA-observable-property identity must be validated before retaining or weakening the dual parentage. |
| `hcm-env:GasConcentrationProfile` | `keep` | Gas-specific measurement specification; local specialization of `MeasurementSpecification`. | Inferred IAO information content entity. | `environment-spec-observation`; distinct from a gas observation and its result. |
| `hcm-env:LightCycle` | `keep` | Information description of light/dark timing; asserted IAO information content entity. | No restriction; none beyond asserted. | none; temporal values are profile fields, not the cycle individual itself being an OWL-Time interval. |
| `hcm-env:MeasurementSpecification` | `keep` | Information specification for measurement representation or constraints; asserted IAO information content entity. | No restriction; none beyond asserted. | none; specification remains distinct from observation and result. |
| `hcm-env:ThriveProfile` | `needs evidence` | Normative welfare/husbandry environment profile; local specialization of `EnvironmentProfile`. | Inferred IAO information content entity; linkage does not assert compliance or outcome. | none; broader content beyond environmental requirements still needs representative use cases. |

### Observations and results

| Class | Decision | Definition and intended upper category / mapping | Restrictions / inferred parents | CQ and review rationale |
| --- | --- | --- | --- | --- |
| `hcm-obs:BehaviorObservation` | `keep` | HCM behavior observation; direct SOSA Observation specialization. | Requires some behavior result and some subject feature of interest; no additional local named parent. | `systems-24h-limited`; observation/result/subject roles are explicit. |
| `hcm-obs:BehaviorResult` | `keep` | Detected or classified behavior result; local observation-result specialization. | Inferred `hcm-obs:ObservationResult`, SOSA Result, and IAO information content entity. | none; result remains with its observation module. |
| `hcm-obs:CategoricalResult` | `keep` | Observation result represented by a category. | Inferred `hcm-obs:ObservationResult`, SOSA Result, and IAO information content entity. | none; representation is distinct from numeric quantity. |
| `hcm-obs:EnvironmentObservation` | `keep` | Observation about an enclosure environmental property; direct SOSA Observation specialization. | Requires some monitored-enclosure feature of interest; observed values are limited to HCMO environmental properties through `sosa:observedProperty`. | none; the earlier SemTS dimension restriction was removed because dimensions belong to time-series segments, not observations. |
| `hcm-obs:GasConcentrationObservation` | `keep` | Environmental observation specialized for gas concentration. | Inferred `hcm-obs:EnvironmentObservation` and SOSA Observation. | none; specialization is coherent with environmental observation. |
| `hcm-obs:HealthStatusObservation` | `keep` | Health-status observation about a subject; direct SOSA Observation specialization. | Requires some subject feature of interest; no additional local named parent. | none; scope and feature of interest agree. |
| `hcm-obs:LocationResultTable` | `keep` | Tabular location observation result and SemTS time-series segment. | Uses canonical SemTS 1.2.0 `segmentDimension` only for `DataDimension` values; inferred ObservationResult, SOSA Result, IAO information content entity, and TimeSeriesSegment. | none; the knowledge-generation-specific `generated` relation was removed after semantic review. |
| `hcm-obs:ObservationResult` | `keep` | Information artifact produced by an HCM observation; dual SOSA Result and IAO information content entity anchor. | No restriction; none beyond asserted external parents. | none; accepted policy keeps results with observations. |
| `hcm-obs:QuantityValue` | `keep` | Quantitative observation result using the pinned QUDT value/unit pattern. | Inferred `hcm-obs:ObservationResult`, SOSA Result, IAO information content entity, and `qudt:QuantityValue`. | `environment-spec-observation`; numeric value and unit are validated by SHACL. |
| `hcm-obs:WeightObservation` | `keep` | Body-weight observation about a subject; direct SOSA Observation specialization. | Requires some subject feature and some quantity result; no additional local named parent. | none; observation/result structure is explicit. |

### Technology

| Class | Decision | Definition and intended upper category / mapping | Restrictions / inferred parents | CQ and review rationale |
| --- | --- | --- | --- | --- |
| `hcm-tech:Actuator` | `keep` | Physical HCM actuator affecting behavior, physiology, or environment; asserted BFO material entity and SOSA Actuator. | No restriction; external inferred hierarchy not bundled. | none; matches accepted A05 physical-device policy while actuation events remain future work. |
| `hcm-tech:CalibrationActivity` | `keep` | Process that calibrates a sensor; asserted BFO process and PROV activity. | Generates a calibration record in the evidence pattern; none beyond asserted anchors. | `status-evidence-at-time`; separates calibration execution from its status record. |
| `hcm-tech:CalibrationRecord` | `keep` | Time-bounded information record of sensor calibration status; asserted IAO information content entity. | SHACL requires a boolean value, validity interval, and generating activity concerning the same sensor. | `status-evidence-at-time`; replaces the deprecated timeless boolean. |
| `hcm-tech:Hardware` | `keep` | Physical computing component; asserted BFO material entity. | No restriction; none beyond asserted. | none; physical-device scope is clear. |
| `hcm-tech:Sensor` | `keep` | Physical sensing device; asserted BFO material entity and SOSA Sensor. | No installation restriction; no additional local named parent. | `sensors-behaviors`; rack-level and remote sensors are supported without asserting cage installation. |
| `hcm-tech:Software` | `needs evidence` | Software used in HCM workflows; currently asserted IAO information content entity. | No restriction; none beyond asserted. | none; executable artifact versus information-content representation needs an explicit upper-ontology policy. |
| `hcm-tech:TimeSeries` | `keep` | Ordered time-indexed measurement/output artifact; asserted IAO information content entity. | No restriction; none beyond asserted. | none; generic time-series artifacts remain broader than the reviewed SemTS specialization on location result tables. |

## Directly used external class anchors

These rows record the external source family and current release status.
Reviewed BFO/IAO labels and definitions for the five end-user anchors are
included in the checksummed `external-upper.ttl` presentation. Its direct
Entity links are source-entailed navigation shortcuts. The source-faithful
intermediate hierarchy and the object-aggregate refinement for Experimental
Group are retained in the optional
`ontology/profiles/external-upper-developer.ttl` profile. Other external terms
remain references rather than a bundled import closure. A `needs evidence`
decision blocks stronger mappings and new hierarchy axioms until the stated
issue is resolved.

| Anchor | Current direct use | Source/version status | Decision |
| --- | --- | --- | --- |
| `BFO:0000015` | Parent of operational assessments and calibration activities. | BFO 2020 source, commit and checksum pinned; exposed as the process anchor in the curated upper projection. | `keep` |
| `BFO:0000019` | Parent of `hcm-env:EnvironmentalProperty`. | BFO 2020 source, commit and checksum pinned; canonical definition included in the upper projection. | `keep` |
| `BFO:0000040` | Parent of material subjects, enclosures, enrichments, and devices. | BFO 2020 source, commit and checksum pinned; canonical definition included in the upper projection. | `keep` |
| `IAO:0000030` | Parent of records, profiles, results, software, and time series. | IAO 2026-03-30 source, commit and checksum pinned; canonical definition included in the upper projection. | `keep` |
| `sosa:Actuator` | Parent of `hcm-tech:Actuator`. | SOSA/SSN 2017 Recommendation artifact and checksum pinned. | `keep` |
| `sosa:Observation` | Parent/domain anchor for observation classes and properties. | SOSA/SSN 2017 Recommendation artifact and checksum pinned. | `keep` |
| `sosa:ObservableProperty` | Parent/range anchor for environmental and captured properties. | SOSA/SSN 2017 Recommendation artifact and checksum pinned at immutable W3C repository commit `6dc6059`. | `keep` |
| `sosa:Result` | Parent of `hcm-obs:ObservationResult`. | SOSA/SSN 2017 Recommendation artifact and checksum pinned. | `keep` |
| `sosa:Sensor` | Parent of `hcm-tech:Sensor`. | SOSA/SSN 2017 Recommendation artifact and checksum pinned. | `keep` |
| `prov:Activity` | Additional process/provenance anchor for operational assessments and calibration activities. | PROV-O W3C Recommendation 2013-04-30 artifact and checksum pinned. | `keep` |
| `qudt:QuantityValue` | Parent/range anchor for numeric values with explicit units. | QUDT 3.4.0 schema and unit vocabulary artifacts and checksums pinned. | `keep` |
| `schema:Person` | Contributor exchange type for ORCID-identified creators. | Schema.org; version not pinned. | `needs evidence` |
| `schema:Place` | Range of `hcm:locatedIn`. | Schema.org; version not pinned. | `needs evidence` |
| `semts:DataDimension` | Restriction filler for dimensions of location result tables. | Canonical unversioned entity IRI from checksummed SemTS 1.2.0; used with its declared `segmentDimension` relation. | `keep` |
| `semts:TimeSeriesSegment` | Parent of location result tables. | Canonical unversioned entity IRI from checksummed SemTS 1.2.0; semantic fit reviewed for time-indexed location tables. | `keep` |

The optional developer profile additionally restores
`hcm-bio:ExperimentalGroup rdfs:subClassOf BFO:0000027` and BFO's canonical
object-aggregate hierarchy. Because that axiom is excluded from the default
release graph, `BFO:0000027` is not counted as a directly used default anchor.

## Review outcome

The inventory records 29 local classes as `keep` and 4 as `needs evidence`.
No class is approved here for definition, axiom, mapping, or deprecation
changes. The next semantic implementation must be a separate, evidence-backed
item and must include examples, reasoning, validation, regenerated artifacts,
and changelog evidence.

Priority evidence gaps:

1. validate the dual BFO-quality/SOSA-property parentage of
   `hcm-env:EnvironmentalProperty`;
2. distinguish study factor from factor specification for
   `hcm-bio:StudyFactors`;
3. settle the upper-category treatment of software artifacts; and
4. resolve the invalid SemTS term references and pin Schema.org evidence for
   the contributor/place exchange anchors.
