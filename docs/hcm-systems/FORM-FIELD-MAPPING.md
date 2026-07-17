# HCMO contribution form field mapping

This document records the contribution form's HCMO 0.2.0 RDF projection. The
form emits JSON staging data, current-model Turtle, and a three-column CSV in
which every row is one RDF triple (`subject`, `predicate`, `object`). CSV terms
use N-Triples lexical form and absolute IRIs so prefixed names never depend on a
consumer's local prefix configuration. Turtle remains the directly loadable
Fuseki serialization.

## Resource and namespace policy

- Ontology terms use the stable HCMO namespaces
  `https://w3id.org/hcmo/ontology/hcm#` and the `bio#`, `env#`, `obs#`, and
  `tech#` module namespaces.
- `identifiers.baseIri` is the instance namespace. It defaults to
  `https://w3id.org/hcmo/id/`; form values are percent-encoded before minting.
- The former generic `hcm:System` compatibility node is no longer emitted. The
  submitted monitoring setup is projected as `hcm:MonitoredEnclosure`, with
  its technical components linked through current `hcm-tech` properties.

## Triple CSV

The CSV header is exactly `subject,predicate,object`. Subjects and predicates
are absolute IRIs enclosed in angle brackets. IRI objects use the same form;
literal objects retain their RDF lexical form and expanded datatype IRI, for
example:

```csv
"subject","predicate","object"
"<https://w3id.org/hcmo/id/cage-1>","<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>","<https://w3id.org/hcmo/ontology/hcm#MonitoredEnclosure>"
"<https://w3id.org/hcmo/id/cage-1>","<http://www.w3.org/2000/01/rdf-schema#label>","""Cage 1"""
```

CSV is intended for tabular ETL or a Fuseki bulk-load transformation. Use the
Turtle view when importing the submission directly into Fuseki.

## Current RDF projection

| Form data | RDF target | Semantic effect |
|---|---|---|
| `identifiers.systemId` | `hcm:MonitoredEnclosure` | Main submitted resource, minted below the selected instance base IRI. |
| `system.name` | `rdfs:label` | Human-readable enclosure/system name. |
| `system.vendor` | `hcm:hasManufacturer` | Manufacturer or developer literal; a `schema:Organization` provenance node is also emitted. |
| `enclosure.*` | `hcm:EnclosureDimensions` and current `hcm:hasWidth`, `hasLength`, `hasHeight`, `hasDimUnit` properties | Physical enclosure details. |
| `animals.*` | `hcm-bio:Subject` plus `hcm-bio:HousingAssignment` | Supported subject profile and its enclosure assignment. Biological sex is intentionally not collected. |
| `measurements.parameters[]` | `hcm-env:MeasurementSpecification` linked from `hcm-env:EnvironmentProfile` | A parameter/specification, not an observed result. Unit uses `hcm:hasUnit`; free-text rate uses `dcterms:frequency`. |
| `measurements.results[]` | `sosa:Observation` / `hcm-obs:BehaviorObservation` plus an explicit result node | A produced result, kept distinct from its measurement parameter. |
| quantitative result | `hcm-obs:QuantityValue`, `hcm-obs:hasNumericValue`, `hcm:hasUnit` | Numeric result pattern. |
| categorical result | `hcm-obs:CategoricalResult`, `hcm-obs:hasCategory` | Category result pattern. |
| behavioral result | `hcm-obs:BehaviorResult`, `hcm-obs:hasBehaviorType` | Behavior result pattern. |
| location-table result | `hcm-obs:LocationResultTable` | Tabular location result pattern. |
| `conditions.*` | Open `schema:Thing` condition node, attached with `hcm-obs:hasCondition` | Experimental, environmental, interaction, and interpretation context. HCMO intentionally leaves the condition class model open. |
| `recording.*` | Generic `sosa:Observation` profile with `hcm-obs:hasInterval` and `dcterms:type` | Recording duration and mode; recognized hour/day/week values become `xsd:duration`. |
| `dataOutput.*` | `hcm-tech:TimeSeries` | Data/time-series artifact. |
| `dataOutput.fileName` | `rdfs:label`, `dcterms:title` | File or series name. |
| `dataOutput.formats[]` | `hcm-tech:hasFileFormat` | Repeatable file formats. |
| `dataOutput.datasetLinks[]` | `hcm-tech:hasStoragePath` | Repeatable local paths or remote locators. |
| `dataOutput.sampling` | `hcm-tech:hasSamplingRate` | Time-series sampling rate or resolution. |
| `dataOutput.version` | `hcm-tech:hasVersion` | Data or pipeline version. |
| `dataOutput.volume` | `dcterms:extent` | Typical file/data volume. |
| `dataOutput.schema` | `rdfs:comment` | Example header or field list pending a reviewed schema model. |
| `dataOutput.license` | `dcterms:license` | License text pending normalization to license IRIs. |
| `sensors[]` | `hcm-tech:Sensor` linked with `hcm-tech:monitoredBy` / `installedIn` | Current sensor model, including identifier and functional type. |
| `actuators[]` | `hcm-tech:Actuator` linked with `hcm-tech:hasActuator` | Current actuator model. |
| `hardwareSoftware.*` | `hcm-tech:Hardware`, `hcm-tech:Software`, `supportsEnclosure`, and `runsOn` | Technical component graph. |

## Staging-only fields

Administrative consent and free curation notes remain in JSON/Markdown and are
not asserted as HCMO domain facts. Unparseable numeric or duration values are
also retained in the submission summary instead of being assigned a false RDF
datatype.
