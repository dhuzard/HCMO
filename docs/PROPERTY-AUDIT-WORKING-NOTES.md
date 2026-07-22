# Property audit working notes

Status: working evidence for checklist item C01. This document is not the
approved C03 property inventory and does not authorize ontology changes.

Reviewer: Cyril Gilbert (`https://orcid.org/0009-0008-2489-8106`)

Review started: 2026-07-22

Review branch: `cyril/property-audit`

## Scope and method

The audit covers the 81 active, non-deprecated local object and datatype
properties declared in the five active source modules. The 49 deprecated
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

Review status: `needs evidence`

Owning module: `ontology/modules/hcm-tech.ttl`

### Asserted semantics

| Property | Definition summary | Domain | Range | Other axiom |
| --- | --- | --- | --- | --- |
| `hcm-tech:monitoredBy` | enclosure to a sensor installed in or monitoring it | `hcm:MonitoredEnclosure` | `hcm-tech:Sensor` | inverse of `hcm-tech:installedIn` |
| `hcm-tech:installedIn` | sensor to the enclosure in which it is installed | `hcm-tech:Sensor` | `hcm:MonitoredEnclosure` | inverse entailed from the declaration above |

`hcm-tech:Sensor` also has an existential restriction requiring installation
in some monitored enclosure. This restriction is relevant to the same
portable, remote, and not-yet-deployed sensor cases, but it is a distinct axiom
that requires its own decision.

### Current use

- Positive examples assert both properties in `abox-minimal.ttl`,
  `isa-hcmo-bridge.ttl`, and `user-submission.ttl`; the DVC example also uses
  both relations.
- `hcm-shapes.ttl` requires at least one `monitoredBy` value for a monitored
  enclosure and exactly one `installedIn` value for a sensor.
- competency question `sensors-behaviors` navigates from an enclosure through
  `monitoredBy` and then through `captures`.
- no current edge-case fixture represents remote or portable monitoring.

Because the positive examples explicitly assert both directions, they do not
test whether the inverse axiom itself is correct or necessary.

### Observed inference

The executable test starts from each relation separately. With the current
axioms:

1. `cage monitoredBy sensor` entails `sensor installedIn cage`;
2. `sensor installedIn cage` entails `cage monitoredBy sensor`; and
3. each assertion also entails the declared subject and object types through
   domain and range.

The first entailment is too strong if a remote or portable sensor can monitor
an enclosure without being physically installed in it. HermiT can confirm that
the ontology is consistent, but consistency alone cannot establish that this
domain claim is true.

### Preliminary decision

Decision: `needs evidence` from domain experts and representative systems.

The definitions currently differ: `monitoredBy` explicitly permits monitoring
without installation, whereas `installedIn` is a physical placement relation.
Under the accepted C02 inverse policy, that wording does not justify an exact
inverse.

Candidate resolutions for review:

1. Keep the relations distinct and remove the inverse axiom. Reverse query
   navigation can use a SPARQL inverse path where needed.
2. Narrow `monitoredBy` to installed sensors and retain the inverse, only if all
   intended HCM systems satisfy that stronger meaning.
3. Introduce a separately justified deployment or monitoring-assignment model
   if installation and monitoring vary over time or by recording session.

No candidate is implemented by this audit note. Before a change, the project
needs at least one portable or remote sensor example, an agreed competency
question, and explicit decisions for both the inverse and the Sensor
existential restriction.

## Active local property decisions

The following tables cover all 81 active local properties. Asserted type,
domain, range, parent, inverse, restrictions, examples, shapes, and CQ usage
are reproduced directly from the sources by:

```text
python tooling/property_audit.py --catalog
```

`keep` means that this review found no current evidence for a semantic change;
it is not a claim that the property is mandatory in every data profile.
`needs evidence` identifies a concrete unresolved meaning or inference and
blocks an ontology edit until the stated evidence is available.

### Core: 23 properties

| Property | Decision | Review rationale |
| --- | --- | --- |
| `hcm:hasCapacity` | `keep` | Enclosure capacity with a non-negative integer range is intentional; cardinality remains a profile concern. |
| `hcm:hasDescription` | `keep` | Generic descriptive metadata has no class-specific inference beyond `owl:Thing`. |
| `hcm:hasDimUnit` | `needs evidence` | The dimension-unit string is coherent temporarily, but the QUDT/OM decision may revise its range and representation. |
| `hcm:hasDimensions` | `keep` | The enclosure-to-dimensions-record relation has aligned domain, range, examples, and shape use. |
| `hcm:hasEnclosureIdentifier` | `keep` | Identifier semantics and string range are aligned with enclosure examples and SHACL. |
| `hcm:hasEnrichment` | `keep` | Relates an enclosure to a material enrichment; requirement text remains a separate property. |
| `hcm:hasEnrichmentRequirement` | `keep` | Records a requirement rather than asserting the presence of an enrichment. Controlled values belong to a later profile. |
| `hcm:hasEnrichmentType` | `keep` | Type text is scoped to an enrichment resource and creates the intended domain inference. |
| `hcm:hasFacilityType` | `keep` | A descriptive enclosure-location category is distinct from the `locatedIn` place relation. |
| `hcm:hasFloorArea` | `keep` | Decimal value is correctly scoped to the dimensions record; its unit is supplied separately. |
| `hcm:hasFoodRequirement` | `keep` | Requirement semantics are distinct from actual provisioning and are used by the provisioning CQ. |
| `hcm:hasHeight` | `keep` | Decimal dimension value is consistently scoped to `EnclosureDimensions`. |
| `hcm:hasLength` | `keep` | Decimal dimension value is consistently scoped to `EnclosureDimensions`. |
| `hcm:hasManufacturer` | `keep` | Manufacturer text is scoped to the enclosure; organization linking can be reviewed as a separate enhancement. |
| `hcm:hasMonitoredAnimals` | `needs evidence` | The direct current-state shortcut may disagree with time-bounded `HousingAssignment`; validity-time behavior needs a CQ and edge case. |
| `hcm:hasName` | `keep` | Generic display metadata has no class-specific inference beyond `owl:Thing`. |
| `hcm:hasSafetyRequirement` | `keep` | Requirement text is distinct from an assertion that a safety condition is satisfied. |
| `hcm:hasUnit` | `needs evidence` | The shared result/specification string pattern is explicitly temporary pending QUDT or OM. |
| `hcm:hasWaterRequirement` | `keep` | Requirement semantics are distinct from actual provisioning and are used by the provisioning CQ. |
| `hcm:hasWidth` | `keep` | Decimal dimension value is consistently scoped to `EnclosureDimensions`. |
| `hcm:isOccupied` | `needs evidence` | “Currently” has no reference time or validity interval and may conflict with housing-assignment history. |
| `hcm:isOperational` | `needs evidence` | Operational state is time-dependent but the property currently carries no temporal context. |
| `hcm:locatedIn` | `keep` | The broad `schema:Place` exchange range matches accepted decision A04; physical/site distinctions remain in the place value. |

### Biology: 13 properties

| Property | Decision | Review rationale |
| --- | --- | --- |
| `hcm-bio:assignedToEnclosure` | `keep` | Assignment record to enclosure is the stable direction and preserves room for assignment metadata and time. |
| `hcm-bio:belongsToGroup` | `keep` | Subject-to-group membership is coherent; an inverse remains deferred until membership temporality is agreed. |
| `hcm-bio:hasBehaviorObservation` | `needs evidence` | The shortcut does not entail the canonical `sosa:hasFeatureOfInterest` assertion and can drift from it. |
| `hcm-bio:hasBiologicalSex` | `keep` | The property is subject-scoped; controlled values and external vocabulary alignment are separate review items. |
| `hcm-bio:hasDateOfBirth` | `keep` | The OWL-compatible literal range plus SHACL `xsd:date` enforcement is intentional. |
| `hcm-bio:hasHealthStatusObservation` | `needs evidence` | The shortcut duplicates subject navigation without enforcing the SOSA feature-of-interest relation. |
| `hcm-bio:hasHousingAssignment` | `keep` | Subject or group to assignment is intentional; a union domain avoids incorrectly inferring one named disjunct. |
| `hcm-bio:hasMember` | `keep` | Group-to-subject membership is coherent; exact inverse status with `belongsToGroup` remains evidence-dependent. |
| `hcm-bio:hasSocialRequirement` | `needs evidence` | Subject/group scope is plausible, but requirement ownership and assignment-time variation need examples. |
| `hcm-bio:hasSpecies` | `keep` | Subject scope is correct; taxon-IRI migration is a separate mapping decision. |
| `hcm-bio:hasStrain` | `keep` | Subject scope is correct; strain registry alignment is a separate mapping decision. |
| `hcm-bio:hasTreatment` | `needs evidence` | A treatment may be a plan, assignment, or executed intervention and may vary over time; a string on subject/group loses that distinction. |
| `hcm-bio:hasWeightObservation` | `needs evidence` | The shortcut does not guarantee the canonical SOSA feature-of-interest assertion. |

### Environment: 19 properties

| Property | Decision | Review rationale |
| --- | --- | --- |
| `hcm-env:AmbientTemperature` | `needs evidence` | One predicate spans profile, specification, and observation layers; split relations may be needed. |
| `hcm-env:AmmoniaConcentration` | `needs evidence` | One predicate spans profile, specification, and observation layers; split relations may be needed. |
| `hcm-env:CarbonDioxideConcentration` | `needs evidence` | One predicate spans profile, specification, and observation layers; split relations may be needed. |
| `hcm-env:LightIntensity` | `needs evidence` | One predicate spans profile, specification, and observation layers; split relations may be needed. |
| `hcm-env:LightState` | `needs evidence` | One predicate spans profile, specification, and observation layers; split relations may be needed. |
| `hcm-env:OxygenConcentration` | `needs evidence` | One predicate spans profile, specification, and observation layers; split relations may be needed. |
| `hcm-env:RelativeHumidity` | `needs evidence` | One predicate spans profile, specification, and observation layers; split relations may be needed. |
| `hcm-env:hasDarkPhaseDuration` | `keep` | Light-cycle duration with SHACL datatype validation follows the accepted OWL/SHACL boundary. |
| `hcm-env:hasDarkPhaseStart` | `keep` | Light-cycle start time with SHACL datatype validation follows the accepted OWL/SHACL boundary. |
| `hcm-env:hasDawnDuration` | `keep` | Transition duration is correctly scoped to `LightCycle`. |
| `hcm-env:hasDuskDuration` | `keep` | Transition duration is correctly scoped to `LightCycle`. |
| `hcm-env:hasEnvironment` | `keep` | Enclosure-to-profile relation is distinct from an individual observation. |
| `hcm-env:hasGasConcentrationProfile` | `keep` | Profile composition has aligned domain and range. |
| `hcm-env:hasGasType` | `keep` | Gas-type text is scoped to a gas-concentration profile; vocabulary alignment can follow later. |
| `hcm-env:hasLightCycle` | `keep` | Profile composition has aligned domain and range. |
| `hcm-env:hasLightPhaseDuration` | `keep` | Light-cycle duration with SHACL datatype validation follows the accepted OWL/SHACL boundary. |
| `hcm-env:hasMeasurementSpec` | `keep` | Profile-to-specification composition is distinct from recording an observed result. |
| `hcm-env:hasThriveProfile` | `keep` | Monitored-enclosure to husbandry profile is coherent and does not imply compliance. |
| `hcm-env:hasValue` | `needs evidence` | A generic literal across measurement specifications and gas profiles lacks explicit quantity/unit semantics. |

### Observation: 8 properties

| Property | Decision | Review rationale |
| --- | --- | --- |
| `hcm-obs:hasBehaviorType` | `needs evidence` | The same predicate spans observation and result layers; representative data must establish whether the value describes the procedure, event, or result. |
| `hcm-obs:hasCategory` | `keep` | Category text is limited to `CategoricalResult`, avoiding the earlier misplaced observation restriction. |
| `hcm-obs:hasCondition` | `needs evidence` | `owl:Thing` deliberately leaves the condition model open but provides no useful range inference or condition identity policy. |
| `hcm-obs:hasConfidenceScore` | `keep` | Decimal confidence is scoped to an observation result; bounds are profile constraints. |
| `hcm-obs:hasHealthStatusTerm` | `keep` | Text/coded value is scoped to health-status observations; vocabulary alignment remains separate. |
| `hcm-obs:hasInterval` | `needs evidence` | A literal duration overlaps the richer `sosa:phenomenonTime`/OWL-Time pattern and needs a clear retained use case. |
| `hcm-obs:hasNumericValue` | `keep` | Decimal value is correctly scoped to `QuantityValue`; unit representation is reviewed separately. |
| `hcm-obs:occursIn` | `keep` | Observation-to-enclosure context is distinct from `sosa:hasFeatureOfInterest` and has aligned direction and range. |

### Technology: 18 properties

| Property | Decision | Review rationale |
| --- | --- | --- |
| `hcm-tech:captures` | `keep` | Sensor-to-property meaning is narrower than `sosa:observes`; the parent axiom remains provisionally supported by C02. |
| `hcm-tech:communicatesWith` | `needs evidence` | The broad component union is plausible, but direction, protocol context, and any symmetry must be demonstrated by examples. |
| `hcm-tech:hasActuator` | `keep` | Enclosure-to-physical-actuator association follows accepted actuator decision A05. |
| `hcm-tech:hasFileFormat` | `keep` | Software/time-series format metadata is intentionally descriptive; no stronger media-type semantics are inferred. |
| `hcm-tech:hasFirmware` | `keep` | Firmware identifier is correctly limited to hardware and sensors. |
| `hcm-tech:hasModelNumber` | `keep` | Manufacturer model metadata applies coherently to physical technical components. |
| `hcm-tech:hasProtocol` | `needs evidence` | Communication, acquisition, and processing protocols are different notions currently collapsed into one string property. |
| `hcm-tech:hasSamplingRate` | `needs evidence` | Sensor and time-series scope is plausible, but a string cannot support numeric/unit comparison or conversion. |
| `hcm-tech:hasSensorIdentifier` | `keep` | Identifier string is correctly scoped to sensors. |
| `hcm-tech:hasSensorTechnology` | `keep` | Sensing technology/modality is correctly scoped to sensors pending vocabulary alignment. |
| `hcm-tech:hasSensorType` | `keep` | Functional category is correctly scoped to sensors, distinct from model and technology. |
| `hcm-tech:hasStoragePath` | `keep` | Locator metadata is intentionally non-inferential; URI/path normalization belongs to a profile. |
| `hcm-tech:hasVersion` | `keep` | Version text applies coherently to hardware, software, and time-series artifacts. |
| `hcm-tech:installedIn` | `needs evidence` | Its physical placement meaning is narrower than monitoring, so exact inverse status is unresolved. |
| `hcm-tech:isCalibrated` | `needs evidence` | Calibration is time- and procedure-dependent; a timeless boolean may only be suitable for an intake snapshot. |
| `hcm-tech:monitoredBy` | `needs evidence` | Current inverse semantics incorrectly equate all monitoring with physical installation unless the intended scope is narrowed. |
| `hcm-tech:runsOn` | `keep` | Software-to-hardware execution direction and domain/range are coherent. |
| `hcm-tech:supportsEnclosure` | `needs evidence` | “Supports” is underspecified and may overlap installation, monitoring, acquisition, or software processing. |

Coverage total: **23 core + 13 bio + 19 env + 8 obs + 18 tech = 81**.

## Directly used external properties

This supplement covers external predicates used as logical properties,
example-data predicates, query predicates, or release annotations. SHACL's own
constraint vocabulary and RDF/RDFS/OWL syntax predicates are implementation
languages rather than domain relations and are not treated as audit targets.
External source/version pinning remains governed by B01.

| Property group | Properties | Decision and effect |
| --- | --- | --- |
| SOSA observation pattern | `sosa:hasFeatureOfInterest`, `sosa:hasResult`, `sosa:madeBySensor`, `sosa:observedProperty`, `sosa:phenomenonTime` | `keep`; these are the canonical observation links used by restrictions, shapes, examples, or CQs. Confirm their pinned SOSA version under B01. |
| SOSA sensor capability | `sosa:observes` | `keep`, parent evidence pending; it is inferred from `hcm-tech:captures` and must retain compatible domain/range consequences. |
| SEMTS structure | `semts:generated`, `semts:hasDimension` | `needs evidence`; local restrictions depend on these external meanings, but source version and intended entailments are not yet pinned. |
| OWL-Time example/query | `time:hasBeginning`, `time:hasEnd`, `time:inXSDDateTime`, `time:numericDuration`, `time:unitType` | `keep`; confined to temporal example/query behavior. Pin the OWL-Time source and keep execution, phenomenon, and assignment times distinct. |
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

1. installation versus monitoring and the Sensor existential restriction;
2. temporal occupancy, operation, calibration, and housing assignment;
3. profile/specification/observation separation for environmental properties;
4. SOSA consistency for subject-to-observation shortcuts;
5. the condition model and literal interval overlap with OWL-Time;
6. unit and sampling-rate representation; and
7. underspecified technical relations and protocol categories.

Each resolved item must become a separate semantic change with a positive
example, an edge or invalid example, a CQ where applicable, and reasoner plus
SHACL evidence. The group-membership inverse candidate remains deferred under
C02; no inverse is added merely for navigation.
