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

## Deferred decisions

- Replace unit strings with a reviewed QUDT or OM pattern.
- Refine the target class for `hcm-obs:hasCondition`.
- Validate the ISA Process / LabProcess representation of cage allocation with
  ISA domain experts. See `ISA-RO-CRATE-MAPPING.md`.
