# 4. Resource description

> **Status:** full draft for HCMO 0.2.0. ~2.5 pp before figures.

HCMO represents Home-Cage Monitoring as a connected system in which biological
subjects, their enclosure and environment, technical devices, observations, and
results remain distinct but queryable together. The ontology IRI is
`https://w3id.org/hcmo/ontology/hcm`; terms in the core use the corresponding
hash namespace, while domain modules use the `bio#`, `env#`, `obs#`, and `tech#`
sub-namespaces. Published IRIs are retained across releases. Terms superseded by
the reorganisation are deprecated and mapped in a compatibility module rather
than deleted or silently re-minted.

## 4.1 Modular organisation

Version 0.2.0 is authored in five domain modules and one migration-only module.
The release manifest (`hcmo.yaml`) defines their load order and is the
authoritative description of the distributed ontology.

- **Core (`hcm`)** contains the enclosure hub: `Enclosure`,
  `MonitoredEnclosure`, `EnclosureDimensions`, and `Enrichment`, together with
  stable relations for dimensions, occupancy, enrichment, and location. Keeping
  this module small prevents device- or assay-specific concepts from becoming
  dependencies of every HCM dataset.
- **Biology (`hcm-bio`)** describes `Subject`, `ExperimentalGroup`,
  `StudyFactors`, and the explicit `HousingAssignment` that connects a subject or
  group to an enclosure. A housing assignment is an information record, rather
  than a permanent class-level statement that an animal always lives in one cage.
- **Environment (`hcm-env`)** represents `EnvironmentProfile`,
  `EnvironmentalProperty`, `MeasurementSpecification`, `LightCycle`, gas
  profiles, and husbandry-oriented thrive profiles. It separates the property of
  interest, such as temperature or humidity, from a specification or observed
  value.
- **Observation (`hcm-obs`)** specialises the SOSA observation pattern for
  behaviour, body weight, health status, gas concentration, and other
  environmental observations. Observation results, including quantitative,
  categorical, behavioural, and location-table results, remain in this module so
  that the event and its output are not split across unrelated namespaces.
- **Technology (`hcm-tech`)** describes `Sensor`, `Actuator`, `Hardware`,
  `Software`, and `TimeSeries`, with relations for installation, monitoring,
  acquisition, communication, execution, calibration, formats, and sampling
  rates. This device layer is separate from the biological interpretation of the
  data it produces.
- **Compatibility (`hcm-compat`)** preserves deprecated HCMO 0.0.1 IRIs and
  records replacements where an exact or defensible mapping exists. It is loaded
  in the merged release for migration, but new data should use only the five
  active namespaces.

The five active modules define 29 HCMO classes, 32 object properties, and 49
datatype properties. The generated distribution additionally contains the
deprecated compatibility vocabulary; consequently `profile.json` reports 56
HCMO classes, 57 object properties, and 73 datatype properties in the complete
1,252-triple release graph.

## 4.2 Central modelling patterns

The central entity is `hcm:MonitoredEnclosure`, a physical enclosure equipped for
longitudinal observation. It links to an `hcm:EnclosureDimensions` record, the
subjects housed or tracked within it, an environmental profile, and the sensors
installed in or monitoring it. Device placement is expressed by the inverse pair
`hcm-tech:monitoredBy` and `hcm-tech:installedIn`. Animal allocation is represented
separately through `hcm-bio:HousingAssignment`, allowing assignment-specific
metadata and avoiding the assumption that cage membership is timeless.

HCMO deliberately keeps **sensor, observation, and result** separate. A
`hcm-tech:Sensor` is a physical device and a subclass of `sosa:Sensor`; an HCMO
observation is a measurement or classification event and a subclass of
`sosa:Observation`; and an HCMO result is the information artifact produced by
that event and a subclass of `sosa:Result`. Canonical SOSA properties connect the
pattern: `sosa:madeBySensor` identifies the device,
`sosa:hasFeatureOfInterest` identifies what was observed,
`sosa:observedProperty` identifies the measured property, and `sosa:hasResult`
identifies the output. `hcm-obs:occursIn` adds the monitored enclosure context.
This structure supports both direct sensor readings and outputs derived later by
software, without treating an algorithmic classification as if it were the
sensor itself.

Technical data products are represented independently of observation results.
`hcm-tech:TimeSeries` describes an ordered sequence of time-indexed outputs and
can carry format and storage metadata. Location-oriented results may reference
SEMTS data dimensions and generated time-series segments. This keeps file-level
provenance available while preserving the semantic identity of the observation
and result.

## 4.3 Reuse and alignments

HCMO reuses external vocabularies by reference and adds a local term only when
the HCM domain requires a specialisation. SOSA provides the observation, result,
sensor, actuator, observed-property, and feature-of-interest pattern. OWL-Time is
used in example data and constraints for observation intervals, beginnings, and
ends. BFO anchors material entities, object aggregates, and qualities; IAO anchors
profiles, specifications, assignments, software, and recorded information
artifacts. Dublin Core Terms, Schema.org, VANN, BIBO, and MOD describe ontology
identity, creators, citation, namespace, status, and release metadata. SEMTS is
reused selectively for data dimensions and time-series segments.

These alignments are intentionally conservative. HCMO does not declare every
possible observed entity to be a `sosa:FeatureOfInterest`, nor does it assert
equivalence merely because two labels appear similar. QUDT or OM quantity-value
patterns remain a roadmap decision; version 0.2.0 retains numeric literals with
explicit unit strings. PROV and additional biomedical bridge ontologies may be
introduced in reviewed bridge modules, but are not claimed as active semantic
dependencies of this release.

## 4.4 Application-facing representations

The hand-authored Turtle modules are merged reproducibly into Turtle, RDF/XML,
and JSON-LD distributions. A JSON-LD context exposes stable compact terms for
application developers, while `profile.json` provides a flat inventory of IRIs,
labels, definitions, and counts. SHACL shapes define intake requirements without
turning application-level completeness rules into universal OWL axioms. The
minimal example demonstrates the complete path from an enclosure and subject to
an installed sensor, a SOSA observation, its temporal interval, and its result.

*Figure F2: overview of the five active HCMO modules and the enclosure-subject-
sensor-observation-result path. Figure F3: the minimal example ABox as an RDF
graph.*
