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
| `dataOutput.datasetLinks[]` | `dcterms:source` on system | datatype literal | Dataset links are not yet separate dataset nodes. |
| `contributor.*` | `schema:Person` linked with `dcterms:contributor` | object + schema literals | Submission provenance, not an HCMO domain claim. |

## Staging fields not yet projected to Turtle

These fields remain in JSON/Markdown until the ontology pattern is confirmed:

| Form field / JSON path | Reason |
|---|---|
| `contributor.consent` | Administrative consent, not a domain ontology fact. |
| `animals.*` | The form describes supported species/cohorts, not a concrete animal instance. |
| `measurements.parameters[]` | Needs a measurement-specification pattern before canonical RDF. |
| `measurements.behaviors` | Needs behavior term normalization or an observation/result pattern. |
| `measurements.circadian` | Current active ontology lacks a finalized circadian concept pattern. |
| `recording.*` | Duration is free text and needs normalization before `hcm:ObservationWindow`. |
| `dataOutput.sampling`, `dataOutput.volume`, `dataOutput.schema`, `dataOutput.license` | Dataset/profile metadata pattern still pending. |
| `extra.gaps`, `extra.notes` | Curation notes, not canonical ABox assertions. |

## Catalog distinction

`docs/hcm-systems/catalog.ttl` is a sparse reference graph generated from the
catalog table. It is useful for discovery and Fuseki lookup, but it is not a full
system-submission graph and is not expected to satisfy every `hcm:System` SHACL
constraint.
