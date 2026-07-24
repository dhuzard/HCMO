# Class audit working notes

Status: signed working evidence for accepted checklist item A06. This audit is
a decision gate. It does not authorize automatic class, definition, hierarchy,
mapping, or deprecation changes.

Reviewer: Cyril Gilbert (`https://orcid.org/0009-0008-2489-8106`)

Review started: 2026-07-24

Review branch: `cyril/c04-entailment-contract`

## Scope and method

The audit covers all 29 active local classes declared in the five active source
modules and 13 external classes used directly as superclass, restriction
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

### Bio

| Class | Decision | Definition and intended upper category / mapping | Restrictions / inferred parents | CQ and review rationale |
| --- | --- | --- | --- | --- |
| `hcm-bio:ExperimentalGroup` | `keep` | Group of subjects sharing a study condition; asserted BFO object aggregate. | No restriction; none beyond asserted. | `animals-by-enclosure`; aggregate interpretation matches membership relations. |
| `hcm-bio:HousingAssignment` | `keep` | Assignment record linking subjects/groups and enclosures; asserted IAO information content entity. | No restriction; none beyond asserted. | `animals-by-enclosure`, `needs-provisioning`; assignment is correctly reified for study context. |
| `hcm-bio:StudyFactors` | `needs evidence` | Independent variable represented as an information artifact; currently asserted IAO information content entity. | No restriction; none beyond asserted. | none; singular label/plural IRI and factor-versus-factor-specification meaning require domain evidence before definition or mapping changes. |
| `hcm-bio:Subject` | `keep` | Biological individual observed in HCM; asserted BFO material entity. | Behavior-observation values restricted to `hcm-obs:BehaviorObservation`; none beyond asserted BFO parent. | `animals-by-enclosure`, `needs-provisioning`; intended individual granularity is explicit. |

### Environment

| Class | Decision | Definition and intended upper category / mapping | Restrictions / inferred parents | CQ and review rationale |
| --- | --- | --- | --- | --- |
| `hcm-env:EnvironmentProfile` | `keep` | Structured conditions/requirements record; asserted IAO information content entity. | Universal fillers for measurement, gas, and light profiles; none beyond asserted. | `needs-provisioning`; profile/container role is coherent. |
| `hcm-env:EnvironmentalProperty` | `needs evidence` | Environmental property currently anchored to both BFO quality and SOSA Property. | No restriction; inferred parents depend on external ontologies not imported. | `sensors-behaviors`; BFO-quality versus SOSA-observable-property identity must be validated before retaining or weakening the dual parentage. |
| `hcm-env:GasConcentrationProfile` | `keep` | Information profile for relevant gas concentrations; asserted IAO information content entity. | No restriction; none beyond asserted. | none; distinct from a gas observation and its result. |
| `hcm-env:LightCycle` | `keep` | Information description of light/dark timing; asserted IAO information content entity. | No restriction; none beyond asserted. | none; temporal values are profile fields, not the cycle individual itself being an OWL-Time interval. |
| `hcm-env:MeasurementSpecification` | `keep` | Information specification for measurement representation or constraints; asserted IAO information content entity. | No restriction; none beyond asserted. | none; specification remains distinct from observation and result. |
| `hcm-env:ThriveProfile` | `needs evidence` | Welfare/husbandry conditions record; asserted IAO information content entity. | No restriction; none beyond asserted. | none; scope and relationship to `EnvironmentProfile` need representative use cases before adding a hierarchy relation. |

### Observations and results

| Class | Decision | Definition and intended upper category / mapping | Restrictions / inferred parents | CQ and review rationale |
| --- | --- | --- | --- | --- |
| `hcm-obs:BehaviorObservation` | `keep` | HCM behavior observation; direct SOSA Observation specialization. | Requires some behavior result and some subject feature of interest; no additional local named parent. | `systems-24h-limited`; observation/result/subject roles are explicit. |
| `hcm-obs:BehaviorResult` | `keep` | Detected or classified behavior result; local observation-result specialization. | Inferred `hcm-obs:ObservationResult`, SOSA Result, and IAO information content entity. | none; result remains with its observation module. |
| `hcm-obs:CategoricalResult` | `keep` | Observation result represented by a category. | Inferred `hcm-obs:ObservationResult`, SOSA Result, and IAO information content entity. | none; representation is distinct from numeric quantity. |
| `hcm-obs:EnvironmentObservation` | `keep` | Observation about an enclosure environmental property; direct SOSA Observation specialization. | Requires some monitored-enclosure feature of interest; dimension values restricted to SemTS DataDimension. | none; observation is distinct from environment profile/specification. |
| `hcm-obs:GasConcentrationObservation` | `keep` | Environmental observation specialized for gas concentration. | Inferred `hcm-obs:EnvironmentObservation` and SOSA Observation. | none; specialization is coherent with environmental observation. |
| `hcm-obs:HealthStatusObservation` | `keep` | Health-status observation about a subject; direct SOSA Observation specialization. | Requires some subject feature of interest; no additional local named parent. | none; scope and feature of interest agree. |
| `hcm-obs:LocationResultTable` | `needs evidence` | Tabular location result with generated time-series segments; local observation-result specialization. | Generated values restricted to SemTS TimeSeriesSegment; inferred ObservationResult, SOSA Result, and IAO information content entity. | none; SemTS source/version and whether every location table uses that representation need evidence. |
| `hcm-obs:ObservationResult` | `keep` | Information artifact produced by an HCM observation; dual SOSA Result and IAO information content entity anchor. | No restriction; none beyond asserted external parents. | none; accepted policy keeps results with observations. |
| `hcm-obs:QuantityValue` | `keep` | Quantitative observation result with value and unit. | Inferred `hcm-obs:ObservationResult`, SOSA Result, and IAO information content entity. | none; numeric and unit properties support this representation. |
| `hcm-obs:WeightObservation` | `keep` | Body-weight observation about a subject; direct SOSA Observation specialization. | Requires some subject feature and some quantity result; no additional local named parent. | none; observation/result structure is explicit. |

### Technology

| Class | Decision | Definition and intended upper category / mapping | Restrictions / inferred parents | CQ and review rationale |
| --- | --- | --- | --- | --- |
| `hcm-tech:Actuator` | `keep` | Physical HCM actuator affecting behavior, physiology, or environment; asserted BFO material entity and SOSA Actuator. | No restriction; external inferred hierarchy not bundled. | none; matches accepted A05 physical-device policy while actuation events remain future work. |
| `hcm-tech:Hardware` | `keep` | Physical computing component; asserted BFO material entity. | No restriction; none beyond asserted. | none; physical-device scope is clear. |
| `hcm-tech:Sensor` | `needs evidence` | Physical sensing device; asserted BFO material entity and SOSA Sensor. | Requires installation in some monitored enclosure; no additional local named parent. | `sensors-behaviors`; portable/remote/not-yet-deployed sensors may invalidate the existential restriction. |
| `hcm-tech:Software` | `needs evidence` | Software used in HCM workflows; currently asserted IAO information content entity. | No restriction; none beyond asserted. | none; executable artifact versus information-content representation needs an explicit upper-ontology policy. |
| `hcm-tech:TimeSeries` | `keep` | Ordered time-indexed measurement/output artifact; asserted IAO information content entity. | No restriction; none beyond asserted. | none; artifact interpretation is coherent, pending separate SemTS mapping review. |

## Directly used external class anchors

These rows record the external source family and current release status. Their
definitions, versions, and imported hierarchy are not copied into HCMO 0.2.0.
All therefore remain `needs evidence` for A06: this does not reject their use,
but blocks stronger mappings and new hierarchy axioms until exact authoritative
versions and definitions are recorded.

| Anchor | Current direct use | Source/version status | Decision |
| --- | --- | --- | --- |
| `BFO:0000019` | Parent of `hcm-env:EnvironmentalProperty`. | BFO; exact release not pinned. | `needs evidence` |
| `BFO:0000027` | Parent of `hcm-bio:ExperimentalGroup`. | BFO; exact release not pinned. | `needs evidence` |
| `BFO:0000040` | Parent of material subjects, enclosures, enrichments, and devices. | BFO; exact release not pinned. | `needs evidence` |
| `IAO:0000030` | Parent of records, profiles, results, software, and time series. | IAO; exact release not pinned. | `needs evidence` |
| `sosa:Actuator` | Parent of `hcm-tech:Actuator`. | SOSA/SSN; exact release not pinned. | `needs evidence` |
| `sosa:Observation` | Parent/domain anchor for observation classes and properties. | SOSA/SSN; exact release not pinned. | `needs evidence` |
| `sosa:Property` | Parent/range anchor for environmental and captured properties. | SOSA/SSN; exact release not pinned. | `needs evidence` |
| `sosa:Result` | Parent of `hcm-obs:ObservationResult`. | SOSA/SSN; exact release not pinned. | `needs evidence` |
| `sosa:Sensor` | Parent of `hcm-tech:Sensor`. | SOSA/SSN; exact release not pinned. | `needs evidence` |
| `schema:Person` | Contributor exchange type for ORCID-identified creators. | Schema.org; version not pinned. | `needs evidence` |
| `schema:Place` | Range of `hcm:locatedIn`. | Schema.org; version not pinned. | `needs evidence` |
| `semts:DataDimension` | Restriction filler on environment observations. | SemTS namespace version `120`; authoritative release evidence not recorded. | `needs evidence` |
| `semts:TimeSeriesSegment` | Restriction filler on location result tables. | SemTS namespace version `120`; authoritative release evidence not recorded. | `needs evidence` |

## Review outcome

The inventory records 23 local classes as `keep` and 6 as `needs evidence`.
No class is approved here for definition, axiom, mapping, or deprecation
changes. The next semantic implementation must be a separate, evidence-backed
item and must include examples, reasoning, validation, regenerated artifacts,
and changelog evidence.

Priority evidence gaps:

1. validate the dual BFO-quality/SOSA-property parentage of
   `hcm-env:EnvironmentalProperty`;
2. test portable and remote sensors against the `hcm-tech:Sensor`
   installation existential;
3. distinguish study factor from factor specification for
   `hcm-bio:StudyFactors`;
4. settle the upper-category treatment of software artifacts; and
5. pin authoritative versions and definitions for every external anchor,
   especially the two SemTS restriction fillers.
