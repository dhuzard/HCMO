# Modeling notes

## Central pattern

A `hcm:MonitoredEnclosure` is a physical enclosure that:

- has one `hcm:EnclosureDimensions` record through `hcm:hasDimensions`;
- houses one or more `hcm-bio:Subject` instances through
  `hcm:hasMonitoredAnimals`;
- is monitored by `hcm-tech:Sensor` instances through
  `hcm-tech:monitoredBy` (inverse: `hcm-tech:installedIn`); and
- may have an `hcm-env:EnvironmentProfile`.

Animal-to-cage allocation is modeled explicitly with
`hcm-bio:HousingAssignment`. This supports allocation metadata and avoids
treating a cage as a study factor. A cage should be represented as a study
factor only when cage identity or cage treatment is deliberately manipulated
as an independent variable.

## Observation pattern

HCMO specializes SOSA rather than duplicating it:

1. an HCMO observation is a `sosa:Observation`;
2. `sosa:hasFeatureOfInterest` identifies the observed subject;
3. `sosa:madeBySensor` identifies the sensor;
4. `sosa:hasResult` links the result; and
5. `hcm-obs:occursIn` identifies the monitored enclosure.

Time-series files use `hcm-tech:TimeSeries`; format and storage metadata use
`hcm-tech:hasFileFormat` and `hcm-tech:hasStoragePath`.

## Constraint strategy

OWL expresses semantic typing and inference. SHACL expresses intake rules such
as required identifiers, dimensions, housing assignments, sensor placement,
and observation-result cardinalities. The ontology does not encode those
application requirements as universal class definitions.

### Validation entailment contract

The canonical validation contract keeps ontology semantics and profile
validation distinct while making their interaction explicit:

1. the ontology graph is the offline union of the source modules listed in
   `hcmo.yaml`, including the compatibility module;
2. each example is validated as an isolated data graph, with the canonical
   ontology supplied separately to pySHACL as its ontology graph;
3. pySHACL applies RDFS inference, so shape targets and value classes include
   types inferred from intentional subclass, domain, and range axioms;
4. an explicitly typed instance and an instance receiving the same type by
   RDFS inference are subject to the same shape;
5. SHACL cardinality, datatype, pattern, and required-value failures do not
   become OWL axioms or imply that missing facts are false; and
6. HermiT remains the separate OWL DL consistency check. A successful SHACL
   run is not a proof of ontology consistency, and RDFS validation inference is
   not a replacement for HermiT classification.

Validation is offline and does not resolve live `owl:imports`. Positive
examples must conform. Files whose names contain `edge` or `invalid` are
negative fixtures and must be non-conformant. At least one negative fixture
must rely on ontology-inferred target typing, preventing a validator from
passing merely because it failed to select the intended focus node.

Competency questions run against the canonical ontology plus all positive
example graphs. Negative fixtures are excluded. Every indexed CQ records its
expected row count; successful parsing with an unreviewed empty result is not
considered sufficient evidence.

## Deferred decisions

- Replace unit strings with a reviewed QUDT or OM pattern.
- Refine the target class for `hcm-obs:hasCondition`.
- Validate the ISA Process / LabProcess representation of cage allocation with
  ISA domain experts. See `ISA-RO-CRATE-MAPPING.md`.
