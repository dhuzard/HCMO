# HCMO contribution form field mapping

This document maps the static contribution form to RDF triples for Fuseki intake.
The form JSON remains staging data; the Turtle view is the first canonical ABox
projection.

## Core submission graph

| Form field / JSON path | RDF target | Triple kind | Notes |
|---|---|---|---|
| `identifiers.baseIri` | subject IRI base | IRI policy | Used to mint all submitted resources. |
| `identifiers.systemId` | `hcm:System` subject | `rdf:type` | Main submitted monitoring-system instance. |
| `system.name` | `rdfs:label` on system | annotation literal | Required for submission validation. |
| `system.description` | `rdfs:comment` on system | annotation literal | Free-text system description. |
| `system.type` | `dcterms:type` on system | datatype literal | UI-controlled but not yet a SKOS concept. |
| `system.modality[]` | `dcterms:type` on system | datatype literal | Temporary technology/modality literal. |
| `system.url` | `dcterms:source` on system | datatype literal | Valid URLs may be normalized later. |
| `system.vendor` | `hcm:producedBy` to `hcm:Supplier`; supplier `rdfs:label` | object + annotation | Required. |
| `hardwareSoftware.hardware` | `hcm:hasHardware` to `hcm:Hardware`; hardware `rdfs:label` | object + annotation | Hardware node is always minted. |
| `hardwareSoftware.software` | `hcm:hasSoftware` to `hcm:Software`; software `rdfs:label` | object + annotation | Software node is always minted. |
| `hardwareSoftware.interoperability` | `rdfs:comment` on hardware | annotation literal | Staging field until a specific interoperability property is modeled. |
| `enclosure.type` | enclosure `dcterms:type` | datatype literal | Enclosure is linked from system with `hcm:hasEnclosure`. |
| `enclosure.fit` | enclosure `rdfs:comment` | annotation literal | Free-text fit/replacement/retrofit note. |
| `enclosure.width` | `hcm:width` on `hcm:Dimensions` | datatype literal, `xsd:decimal` | Required and positive. |
| `enclosure.length` | `hcm:length` on `hcm:Dimensions` | datatype literal, `xsd:decimal` | Required and positive. |
| `enclosure.height` | `hcm:height` on `hcm:Dimensions` | datatype literal, `xsd:decimal` | Required and positive. |
| `enclosure.unit` | `hcm:unit` on `hcm:Dimensions` | datatype literal | Defaults to `cm`. |
| `sensors[].sensor_name` | `hcm:Sensor` subject `rdfs:label`; system `hcm:hasSensor` | object + annotation | At least one named sensor is required. |
| `sensors[].sensor_type` | sensor `dcterms:type` | datatype literal | Temporary type literal. |
| `actuators[].actuator_name` | `hcm:Actuator` subject `rdfs:label`; system `hcm:hasActuator` | object + annotation | Optional. |
| `actuators[].actuator_type` | actuator `dcterms:type` | datatype literal | Temporary type literal. |
| `dataOutput.formats[]` | `dcterms:format` on system | datatype literal | Repeatable output-format values. |
| `dataOutput.datasetLinks[]` | `dcterms:source` on system; `hcm:hasStoragePath` on data product | datatype literal | Also used to populate the `hcm:DataProduct` node. |
| `contributor.*` | `schema:Person` linked with `dcterms:contributor` | object + schema literals | Submission provenance, not an HCMO domain claim. |
| `animals.species` | `hcm-bio:Subject` + `hcm-bio:hasSpecies` | datatype literal | Modeled as a supported subject profile, not a concrete study animal. |
| `animals.strain` | `hcm-bio:hasStrain` | datatype literal | Free text until a strain vocabulary is chosen. |
| `animals.sex` | `hcm-bio:hasBiologicalSex` | datatype literal | UI controlled values, still literal. |
| `animals.housing` | subject-profile `rdfs:comment` | annotation literal | No precise housing-assignment object is minted yet. |
| `animals.perCage` | `hcm:hasCapacity` | datatype literal, `xsd:integer` when numeric | Non-numeric ranges stay out of the canonical triple. |
| `animals.cages` | `dcterms:extent` | datatype literal | Represents scale/cage count text. |
| `measurements.parameters[].param_name` | `hcm-env:MeasurementSpecification` + `rdfs:label` | object + annotation | One measurement-specification node per row. |
| `measurements.parameters[].param_unit` | `hcm-env:hasUnit` | datatype literal | Unit text is not normalized to QUDT/OM yet. |
| `measurements.parameters[].param_rate` | `hcm:hasSamplingRate` | datatype literal | Free text rate such as `4 Hz` or `30 fps`. |
| `measurements.behaviors` | `hcm:BehaviorAndPhysiology` + `rdfs:comment`; sensors `hcm:captures` behavior profile | object + annotation | Free-text behavior profile, not controlled behavior terms. |
| `measurements.circadian` | `hcm:CircadianRhythm` + `rdfs:label` | object + annotation | Linked from the behavior profile. |
| `recording.duration` | `hcm:ObservationWindow` + `hcm:durationHours` | object + `xsd:decimal` | Emitted only when duration is parseable and greater than 24 hours. |
| `recording.mode` | observation-window `dcterms:type` | datatype literal | UI controlled values, still literal. |
| `recording.extendable` | `hcm:isExtendable` | datatype literal, `xsd:boolean` | Emitted only for yes/no values. |
| `dataOutput.sampling` | `hcm:hasSamplingRate` on `hcm:DataProduct` | datatype literal | Free-text rate. |
| `dataOutput.volume` | `hcm:hasDescription` on `hcm:DataProduct` | datatype literal | Free-text volume description. |
| `dataOutput.schema` | `rdfs:comment` on `hcm:DataProduct` | annotation literal | Stores pasted header/field list pending schema modeling. |
| `dataOutput.license` | `dcterms:license` on `hcm:DataProduct` | datatype literal | Literal until licenses are normalized to IRIs. |

## Staging fields not yet projected to Turtle

These fields remain in JSON/Markdown until the ontology pattern is confirmed:

| Form field / JSON path | Reason |
|---|---|
| `contributor.consent` | Administrative consent, not a domain ontology fact. |
| non-numeric `animals.perCage` | Cannot safely cast to `xsd:integer`; retained in JSON/Markdown. |
| unparseable or <=24h `recording.duration` | Current SHACL requires `hcm:ObservationWindow` duration to be greater than 24 hours. |
| `extra.gaps`, `extra.notes` | Curation notes, not canonical ABox assertions. |

## Catalog distinction

`docs/hcm-systems/catalog.ttl` is a sparse reference graph generated from the
catalog table. It is useful for discovery and Fuseki lookup, but it is not a full
system-submission graph and is not expected to satisfy every `hcm:System` SHACL
constraint.
