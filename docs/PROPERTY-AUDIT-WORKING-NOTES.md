# Property audit working notes

Status: working evidence for checklist item C01. This document is not the
approved C03 property inventory and does not authorize ontology changes.

Reviewer: Cyril Gilbert (`https://orcid.org/0009-0008-2489-8106`)

Review started: 2026-07-22

Review branch: `cyril/property-audit`

## Scope and method

The audit covers the 69 active, non-deprecated local object and datatype
properties plus 25 newly deprecated properties declared in the five active
source modules. The 49 deprecated
properties in `hcm-compat.ttl` will be reviewed separately. External
properties directly used in HCMO axioms, shapes, examples, or competency
queries remain in scope.

For each priority case, the review will distinguish:

- asserted domain, range, parent, inverse, and class restrictions;
- consequences inferred from isolated positive and edge-case assertions;
- use in examples, SHACL shapes, and competency questions;
- the intended domain meaning and a reviewer decision; and
- any later implementation item, which must have separate approval and tests.

`python tooling/property_audit.py` verifies the current `81 + 49` source
snapshot and executes the first rule-level entailment test with OWL RL. The
normal HermiT check remains the ontology-wide OWL DL consistency gate. OWL RL
is used here only to expose concrete inverse and domain/range consequences; it
does not replace HermiT.

The exact C03 TSV fields are still awaiting co-author validation. These notes
therefore must not be converted automatically into ontology edits or treated
as the final inventory.

## C01-01: monitoredBy and installedIn

Review status: `revise axiom` — implemented after review

Owning module: `ontology/modules/hcm-tech.ttl`

### Reviewed semantics

| Property | Definition summary | Domain | Range | Other axiom |
| --- | --- | --- | --- | --- |
| `hcm-tech:monitoredBy` | enclosure to a sensor that monitors it, regardless of physical installation | `hcm:MonitoredEnclosure` | `hcm-tech:Sensor` | no inverse |
| `hcm-tech:installedIn` | sensor to an enclosure in which it is physically installed | `hcm-tech:Sensor` | `hcm:MonitoredEnclosure` | no inverse |

`hcm-tech:Sensor` no longer has an `installedIn` existential restriction.
Portable, remote, rack-level, and not-yet-deployed sensors can therefore be
represented without inventing an enclosure-level installation.

### Evidence and use

- Positive examples assert both properties in `abox-minimal.ttl`,
  `isa-hcmo-bridge.ttl`, and `user-submission.ttl` where both relations are
  independently known.
- The DVC example includes a rack environmental monitor connected only through
  `monitoredBy`, demonstrating conforming monitoring without cage installation.
- `hcm-shapes.ttl` requires at least one `monitoredBy` value for a monitored
  enclosure. When `installedIn` is present, its value must be a
  `MonitoredEnclosure`, but installation is optional and has no timeless
  cardinality.
- competency question `sensors-behaviors` navigates from an enclosure through
  `monitoredBy` and then through `captures`.

### Verified inference

The executable property audit starts from each relation separately. With the
reviewed axioms:

1. `cage monitoredBy sensor` does not entail `sensor installedIn cage`;
2. `sensor installedIn cage` does not entail `cage monitoredBy sensor`; and
3. each assertion also entails the declared subject and object types through
   domain and range.

Reverse query navigation can use a SPARQL inverse path where needed. A future
deployment or monitoring-assignment model may add temporal context, but it must
not restore a context-free equivalence between monitoring and installation.

## Active local property decisions

The following tables cover all 94 authored local properties: 69 active and 25
deprecated by the accepted environmental, temporal, and quantity policies. Asserted type,
domain, range, parent, inverse, restrictions, examples, shapes, and CQ usage
are reproduced directly from the sources by:

```text
python tooling/property_audit.py --catalog
```

`keep` means that this review found no current evidence for a semantic change;
it is not a claim that the property is mandatory in every data profile.
`needs evidence` identifies a concrete unresolved meaning or inference and
blocks an ontology edit until the stated evidence is available.

### Core: 30 properties

| Property | Decision | Review rationale |
| --- | --- | --- |
| `hcm:hasCapacity` | `keep` | Enclosure capacity with a non-negative integer range is intentional; cardinality remains a profile concern. |
| `hcm:hasDescription` | `keep` | Generic descriptive metadata has no class-specific inference beyond `owl:Thing`. |
| `hcm:hasDimUnit` | `deprecate` | Replaced by a unit on each QUDT quantity value. |
| `hcm:hasDimensions` | `keep` | The enclosure-to-dimensions-record relation has aligned domain, range, examples, and shape use. |
| `hcm:hasEnclosureIdentifier` | `keep` | Identifier semantics and string range are aligned with enclosure examples and SHACL. |
| `hcm:hasEnrichment` | `keep` | Relates an enclosure to a material enrichment; requirement text remains a separate property. |
| `hcm:hasEnrichmentRequirement` | `keep` | Records a requirement rather than asserting the presence of an enrichment. Controlled values belong to a later profile. |
| `hcm:hasEnrichmentType` | `keep` | Type text is scoped to an enrichment resource and creates the intended domain inference. |
| `hcm:hasFacilityType` | `keep` | A descriptive enclosure-location category is distinct from the `locatedIn` place relation. |
| `hcm:hasFloorArea` | `deprecate` | Replaced by `hasFloorAreaQuantity` so value and unit remain inseparable. |
| `hcm:hasFoodRequirement` | `keep` | Requirement semantics are distinct from actual provisioning and are used by the provisioning CQ. |
| `hcm:hasHeight` | `deprecate` | Replaced by `hasHeightQuantity`. |
| `hcm:hasLength` | `deprecate` | Replaced by `hasLengthQuantity`. |
| `hcm:hasManufacturer` | `keep` | Manufacturer text is scoped to the enclosure; organization linking can be reviewed as a separate enhancement. |
| `hcm:hasMonitoredAnimals` | `deprecate` | Membership is derived at an explicit time from authoritative HousingAssignment intervals. |
| `hcm:hasName` | `keep` | Generic display metadata has no class-specific inference beyond `owl:Thing`. |
| `hcm:hasSafetyRequirement` | `keep` | Requirement text is distinct from an assertion that a safety condition is satisfied. |
| `hcm:hasUnit` | `deprecate` | Replaced by canonical `qudt:hasUnit` on a QUDT QuantityValue. |
| `hcm:hasWaterRequirement` | `keep` | Requirement semantics are distinct from actual provisioning and are used by the provisioning CQ. |
| `hcm:hasWidth` | `deprecate` | Replaced by `hasWidthQuantity`. |
| `hcm:isOccupied` | `deprecate` | Occupancy is derived at an explicit time from HousingAssignment intervals. |
| `hcm:isOperational` | `deprecate` | Replaced by a time-bounded, evidence-backed operational status record. |
| `hcm:locatedIn` | `keep` | The broad `schema:Place` exchange range matches accepted decision A04; physical/site distinctions remain in the place value. |
| `hcm:assessesEnclosure` | `keep` | Connects an operational assessment to the enclosure it evaluates. |
| `hcm:hasOperationalStatusRecord` | `keep` | Links an enclosure to its evidence-backed, time-bounded status record. |
| `hcm:hasOperationalStatusValue` | `keep` | Boolean value is scoped to the time-bounded record rather than the enclosure. |
| `hcm:hasFloorAreaQuantity` | `keep` | QUDT quantity preserves the numeric floor area and unit together. |
| `hcm:hasHeightQuantity` | `keep` | QUDT quantity preserves the numeric height and unit together. |
| `hcm:hasLengthQuantity` | `keep` | QUDT quantity preserves the numeric length and unit together. |
| `hcm:hasWidthQuantity` | `keep` | QUDT quantity preserves the numeric width and unit together. |

### Biology: 13 properties

| Property | Decision | Review rationale |
| --- | --- | --- |
| `hcm-bio:assignedToEnclosure` | `keep` | Assignment record to enclosure is the stable direction and preserves room for assignment metadata and time. |
| `hcm-bio:belongsToGroup` | `keep` | Subject-to-group membership is coherent; an inverse remains deferred until membership temporality is agreed. |
| `hcm-bio:hasBehaviorObservation` | `deprecate` | Query the inverse of canonical `sosa:hasFeatureOfInterest`; do not maintain duplicate subject links. |
| `hcm-bio:hasBiologicalSex` | `keep` | The property is subject-scoped; controlled values and external vocabulary alignment are separate review items. |
| `hcm-bio:hasDateOfBirth` | `keep` | The OWL-compatible literal range plus SHACL `xsd:date` enforcement is intentional. |
| `hcm-bio:hasHealthStatusObservation` | `deprecate` | Query the inverse of canonical `sosa:hasFeatureOfInterest`. |
| `hcm-bio:hasHousingAssignment` | `keep` | Subject or group to assignment is intentional; a union domain avoids incorrectly inferring one named disjunct. |
| `hcm-bio:hasMember` | `keep` | Group-to-subject membership is coherent; exact inverse status with `belongsToGroup` remains evidence-dependent. |
| `hcm-bio:hasSocialRequirement` | `needs evidence` | Subject/group scope is plausible, but requirement ownership and assignment-time variation need examples. |
| `hcm-bio:hasSpecies` | `keep` | Subject scope is correct; taxon-IRI migration is a separate mapping decision. |
| `hcm-bio:hasStrain` | `keep` | Subject scope is correct; strain registry alignment is a separate mapping decision. |
| `hcm-bio:hasTreatment` | `deprecate` | Planned factor assignment and executed treatment require distinct explicit patterns. |
| `hcm-bio:hasWeightObservation` | `deprecate` | Query the inverse of canonical `sosa:hasFeatureOfInterest`. |

### Environment: 21 properties

| Property | Decision | Review rationale |
| --- | --- | --- |
| `hcm-env:AmbientTemperature` | `deprecate` | Role-conflating shortcut replaced by profile composition, specification property, and SOSA observation links. |
| `hcm-env:AmmoniaConcentration` | `deprecate` | Role-conflating shortcut replaced by the three-layer pattern. |
| `hcm-env:CarbonDioxideConcentration` | `deprecate` | Role-conflating shortcut replaced by the three-layer pattern. |
| `hcm-env:LightIntensity` | `deprecate` | Role-conflating shortcut replaced by the three-layer pattern. |
| `hcm-env:LightState` | `deprecate` | Role-conflating shortcut replaced by the three-layer pattern. |
| `hcm-env:OxygenConcentration` | `deprecate` | Role-conflating shortcut replaced by the three-layer pattern. |
| `hcm-env:RelativeHumidity` | `deprecate` | Role-conflating shortcut replaced by the three-layer pattern. |
| `hcm-env:hasDarkPhaseDuration` | `keep` | Light-cycle duration with SHACL datatype validation follows the accepted OWL/SHACL boundary. |
| `hcm-env:hasDarkPhaseStart` | `keep` | Light-cycle start time with SHACL datatype validation follows the accepted OWL/SHACL boundary. |
| `hcm-env:hasDawnDuration` | `keep` | Transition duration is correctly scoped to `LightCycle`. |
| `hcm-env:hasDuskDuration` | `keep` | Transition duration is correctly scoped to `LightCycle`. |
| `hcm-env:hasEnvironment` | `keep` | Enclosure-to-profile relation is distinct from an individual observation. |
| `hcm-env:hasGasConcentrationProfile` | `keep` | Profile composition has aligned domain and range. |
| `hcm-env:hasGasType` | `deprecate` | Gas identity is represented by the environmental property resource specified. |
| `hcm-env:hasLightCycle` | `keep` | Profile composition has aligned domain and range. |
| `hcm-env:hasLightPhaseDuration` | `keep` | Light-cycle duration with SHACL datatype validation follows the accepted OWL/SHACL boundary. |
| `hcm-env:hasMeasurementSpec` | `keep` | Profile-to-specification composition is distinct from recording an observed result. |
| `hcm-env:hasThriveProfile` | `keep` | Monitored-enclosure to husbandry profile is coherent and does not imply compliance. |
| `hcm-env:hasValue` | `deprecate` | Replaced by `hasSpecifiedValue` with a QUDT QuantityValue. |
| `hcm-env:specifiesProperty` | `keep` | Gives a measurement specification one explicit environmental-property role. |
| `hcm-env:hasSpecifiedValue` | `keep` | Carries the target or required value as a QUDT quantity. |

### Observation: 8 properties

| Property | Decision | Review rationale |
| --- | --- | --- |
| `hcm-obs:hasBehaviorType` | `needs evidence` | The same predicate spans observation and result layers; representative data must establish whether the value describes the procedure, event, or result. |
| `hcm-obs:hasCategory` | `keep` | Category text is limited to `CategoricalResult`, avoiding the earlier misplaced observation restriction. |
| `hcm-obs:hasCondition` | `keep` | Retained only as a non-causal contextual link; it does not assert a study factor, treatment, or execution. |
| `hcm-obs:hasConfidenceScore` | `keep` | Decimal confidence is scoped to an observation result; bounds are profile constraints. |
| `hcm-obs:hasHealthStatusTerm` | `keep` | Text/coded value is scoped to health-status observations; vocabulary alignment remains separate. |
| `hcm-obs:hasInterval` | `needs evidence` | A literal duration overlaps the richer `sosa:phenomenonTime`/OWL-Time pattern and needs a clear retained use case. |
| `hcm-obs:hasNumericValue` | `deprecate` | Replaced by canonical `qudt:numericValue` on QUDT QuantityValue. |
| `hcm-obs:occursIn` | `keep` | Observation-to-enclosure context is distinct from `sosa:hasFeatureOfInterest` and has aligned direction and range. |

### Technology: 22 properties

| Property | Decision | Review rationale |
| --- | --- | --- |
| `hcm-tech:captures` | `keep` | Sensor-to-property meaning is narrower than `sosa:observes`; the parent axiom remains provisionally supported by C02. |
| `hcm-tech:communicatesWith` | `needs evidence` | The broad component union is plausible, but direction, protocol context, and any symmetry must be demonstrated by examples. |
| `hcm-tech:hasActuator` | `keep` | Enclosure-to-physical-actuator association follows accepted actuator decision A05. |
| `hcm-tech:hasFileFormat` | `keep` | Software/time-series format metadata is intentionally descriptive; no stronger media-type semantics are inferred. |
| `hcm-tech:hasFirmware` | `keep` | Firmware identifier is correctly limited to hardware and sensors. |
| `hcm-tech:hasModelNumber` | `keep` | Manufacturer model metadata applies coherently to physical technical components. |
| `hcm-tech:hasProtocol` | `needs evidence` | Communication, acquisition, and processing protocols are different notions currently collapsed into one string property. |
| `hcm-tech:hasSamplingRate` | `deprecate` | Replaced by `hasSamplingRateQuantity` with a QUDT QuantityValue. |
| `hcm-tech:hasSensorIdentifier` | `keep` | Identifier string is correctly scoped to sensors. |
| `hcm-tech:hasSensorTechnology` | `keep` | Sensing technology/modality is correctly scoped to sensors pending vocabulary alignment. |
| `hcm-tech:hasSensorType` | `keep` | Functional category is correctly scoped to sensors, distinct from model and technology. |
| `hcm-tech:hasStoragePath` | `keep` | Locator metadata is intentionally non-inferential; URI/path normalization belongs to a profile. |
| `hcm-tech:hasVersion` | `keep` | Version text applies coherently to hardware, software, and time-series artifacts. |
| `hcm-tech:installedIn` | `keep` | Physical placement is retained as an optional relation independent of monitoring; it has no inverse or timeless SHACL cardinality. |
| `hcm-tech:isCalibrated` | `deprecate` | Replaced by an evidence-backed, time-bounded calibration record. |
| `hcm-tech:monitoredBy` | `keep` | Monitoring association is retained independently of physical installation; the incorrect inverse axiom was removed. |
| `hcm-tech:runsOn` | `keep` | Software-to-hardware execution direction and domain/range are coherent. |
| `hcm-tech:supportsEnclosure` | `needs evidence` | “Supports” is underspecified and may overlap installation, monitoring, acquisition, or software processing. |
| `hcm-tech:calibratesSensor` | `keep` | Connects a calibration activity to the sensor calibrated. |
| `hcm-tech:hasCalibrationRecord` | `keep` | Links a sensor to a time-bounded calibration status record. |
| `hcm-tech:hasCalibrationStatusValue` | `keep` | Boolean value is scoped to the evidence record, not the sensor. |
| `hcm-tech:hasSamplingRateQuantity` | `keep` | Represents sampling rate as a comparable QUDT quantity. |

Coverage total: **30 core + 13 bio + 21 env + 8 obs + 22 tech = 94**.

## Directly used external properties

This supplement covers external predicates used as logical properties,
example-data predicates, query predicates, or release annotations. SHACL's own
constraint vocabulary and RDF/RDFS/OWL syntax predicates are implementation
languages rather than domain relations and are not treated as audit targets.
External source/version pinning remains governed by B01.

| Property group | Properties | Decision and effect |
| --- | --- | --- |
| SOSA observation pattern | `sosa:hasFeatureOfInterest`, `sosa:hasResult`, `sosa:madeBySensor`, `sosa:observedProperty`, `sosa:phenomenonTime` | `keep`; these are the canonical observation links used by restrictions, shapes, examples, or CQs. Confirm their pinned SOSA version under B01. |
| SOSA sensor capability | `sosa:observes` | `keep`; `hcm-tech:captures` is narrower and has the SOSA 2017-compatible `ObservableProperty` range. |
| SemTS time-series structure | `semts:segmentDimension` | `keep`; canonical SemTS 1.2.0 relation used only from a location `TimeSeriesSegment` to `DataDimension`. The ill-fitting `semts:generated` and nonexistent `semts:hasDimension` references were removed. |
| OWL-Time temporal pattern | `time:hasTime`, `time:hasBeginning`, `time:hasEnd`, `time:inXSDDateTime`, `time:numericDuration`, `time:unitType` | `keep`; housing, status, calibration, and observation intervals are validated and queried at explicit times. |
| PROV evidence pattern | `prov:wasGeneratedBy`, plus workflow `prov:generated` and `prov:used` | `keep`; status records identify their evidence-generating activity and the ISA/STATO fixture retains execution provenance. |
| QUDT quantity pattern | `qudt:numericValue`, `qudt:hasUnit` | `keep`; QUDT 3.4.0 is pinned and SHACL validates one value/unit pair per QuantityValue. |
| Schema.org exchange examples | `schema:about`, `schema:additionalType`, `schema:affiliation`, `schema:email`, `schema:encodingFormat`, `schema:hasPart`, `schema:name`, `schema:object`, `schema:result`, `schema:roleName` | `keep outside canonical HCMO inference`; these support ISA/RO-Crate-style exchange examples and do not assert OWL mappings. |
| Dublin Core example metadata | `dcterms:contributor`, `dcterms:license`, `dcterms:relation`, `dcterms:source`, `dcterms:type` | `keep as metadata`; these predicates must not be interpreted as HCMO domain-property mappings. |
| Release annotations | `bibo:authorList`, `dcterms:bibliographicCitation`, `dcterms:created`, `dcterms:creator`, `dcterms:identifier`, `dcterms:issued`, `dcterms:license`, `dcterms:modified`, `dcterms:publisher`, `dcterms:source`, `mod:createdWith`, `schema:logo`, `schema:name`, `vann:preferredNamespacePrefix`, `vann:preferredNamespaceUri` | `keep as annotations`; no domain/range inference is intended from release metadata. |

`schema:Place` is used as the range class of `hcm:locatedIn`, not as a
property, and is therefore handled in A04 and the `locatedIn` row above.

## Deprecated compatibility property audit

All 49 compatibility properties remain excluded from the active vocabulary.
The decision `keep deprecated` means preserving the published IRI and its
migration annotation without restoring active domain, range, inverse, or
subproperty axioms. A dash means that no exact context-free replacement is
currently asserted.

| Deprecated property | Replacement | Decision |
| --- | --- | --- |
| `hcm:captures` | `hcm-tech:captures` | `keep deprecated` |
| `hcm:collectsInfoOn` | - | `keep deprecated` |
| `hcm:communicatesWith` | `hcm-tech:communicatesWith` | `keep deprecated` |
| `hcm:displays` | - | `keep deprecated` |
| `hcm:durationHours` | - | `keep deprecated` |
| `hcm:elicits` | - | `keep deprecated` |
| `hcm:extendsEnoughToCapture` | - | `keep deprecated` |
| `hcm:followsProtocol` | - | `keep deprecated` |
| `hcm:hasActuator` | - | `keep deprecated` |
| `hcm:hasCategory` | `hcm-obs:hasCategory` | `keep deprecated` |
| `hcm:hasCircadianRhythm` | - | `keep deprecated` |
| `hcm:hasEnclosure` | - | `keep deprecated` |
| `hcm:hasEnvironment` | `hcm-env:hasEnvironment` | `keep deprecated` |
| `hcm:hasEnvironmentalEnrichment` | - | `keep deprecated` |
| `hcm:hasFileFormat` | `hcm-tech:hasFileFormat` | `keep deprecated` |
| `hcm:hasFood` | - | `keep deprecated` |
| `hcm:hasHardware` | - | `keep deprecated` |
| `hcm:hasNumericValue` | `hcm-obs:hasNumericValue` | `keep deprecated` |
| `hcm:hasProperty` | - | `keep deprecated` |
| `hcm:hasResult` | - | `keep deprecated` |
| `hcm:hasSafetyFromThreat` | - | `keep deprecated` |
| `hcm:hasSamplingRate` | `hcm-tech:hasSamplingRate` | `keep deprecated` |
| `hcm:hasSensor` | - | `keep deprecated` |
| `hcm:hasSocialContacts` | - | `keep deprecated` |
| `hcm:hasSoftware` | - | `keep deprecated` |
| `hcm:hasSpaceRegion` | - | `keep deprecated` |
| `hcm:hasStoragePath` | `hcm-tech:hasStoragePath` | `keep deprecated` |
| `hcm:hasThriveProfile` | `hcm-env:hasThriveProfile` | `keep deprecated` |
| `hcm:hasVersion` | `hcm-tech:hasVersion` | `keep deprecated` |
| `hcm:hasWater` | - | `keep deprecated` |
| `hcm:height` | `hcm:hasHeight` | `keep deprecated` |
| `hcm:installedIn` | `hcm-tech:installedIn` | `keep deprecated` |
| `hcm:isDisplayedInside` | - | `keep deprecated` |
| `hcm:isExtendable` | - | `keep deprecated` |
| `hcm:length` | `hcm:hasLength` | `keep deprecated` |
| `hcm:livesIn` | - | `keep deprecated` |
| `hcm:monitoredBy` | `hcm-tech:monitoredBy` | `keep deprecated` |
| `hcm:producedBy` | - | `keep deprecated` |
| `hcm:protocolReference` | - | `keep deprecated` |
| `hcm:provides` | - | `keep deprecated` |
| `hcm:requiresToThrive` | - | `keep deprecated` |
| `hcm:unit` | `hcm:hasDimUnit` | `keep deprecated` |
| `hcm:width` | `hcm:hasWidth` | `keep deprecated` |
| `hcm-env:hasDimUnit` | `hcm:hasDimUnit` | `keep deprecated` |
| `hcm-env:hasHeight` | `hcm:hasHeight` | `keep deprecated` |
| `hcm-env:hasLength` | `hcm:hasLength` | `keep deprecated` |
| `hcm-env:hasUnit` | `hcm:hasUnit` | `keep deprecated` |
| `hcm-env:hasWidth` | `hcm:hasWidth` | `keep deprecated` |
| `hcm-obs:assignedToEnclosure` | `hcm-bio:assignedToEnclosure` | `keep deprecated` |

Compatibility coverage total: **49 deprecated properties**. The automated
check confirms that all have labels, definitions, source, and deprecation
markers; 22 have declared replacements. One migration deliberately changes
property kind: legacy datatype property `hcm:hasEnvironment` points to active
object property `hcm-env:hasEnvironment`. Consumers must transform the old
literal into an `EnvironmentProfile` resource rather than copy the triple.
Every dash remains an explicit "no exact replacement" decision, not a mapping
inferred from label similarity.

## Priority inference evidence

The executable audit now verifies these consequences independently of the
positive examples:

- `locatedIn` infers `Enclosure` for its subject and `schema:Place` for its
  object;
- a shared environmental predicate infers membership in its anonymous union
  domain but does not choose `EnvironmentProfile`, `MeasurementSpecification`,
  or `EnvironmentObservation`;
- `hasCondition` infers `sosa:Observation` for its subject but adds no useful
  condition type;
- `hasMonitoredAnimals` infers `MonitoredEnclosure` and `Subject` but carries no
  housing validity time;
- `hasBehaviorObservation` infers its local subject/object classes but does not
  entail `sosa:hasFeatureOfInterest`; and
- `captures` entails `sosa:observes` plus the intended sensor/property types.

## Open decision queue

The property-by-property pass is complete, but `needs evidence` decisions are
not implementation approvals. The next semantic work should resolve, in this
order:

1. temporal occupancy, operation, calibration, and housing assignment;
2. profile/specification/observation separation for environmental properties;
3. SOSA consistency for subject-to-observation shortcuts;
4. the condition model and literal interval overlap with OWL-Time;
5. unit and sampling-rate representation; and
6. underspecified technical relations and protocol categories.

Each resolved item must become a separate semantic change with a positive
example, an edge or invalid example, a CQ where applicable, and reasoner plus
SHACL evidence. The group-membership inverse candidate remains deferred under
C02; no inverse is added merely for navigation.
