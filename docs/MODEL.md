# Modeling notes

## Central pattern

A `hcm:MonitoredEnclosure` is a physical enclosure that:

- has one `hcm:EnclosureDimensions` record through `hcm:hasDimensions`;
- has time-bounded subject/group housing recorded through
  `hcm-bio:HousingAssignment`; `hcm:hasMonitoredAnimals` is only an optional
  derived snapshot at an explicitly stated evaluation time;
- is monitored by `hcm-tech:Sensor` instances through
  `hcm-tech:monitoredBy`; physical cage installation is represented separately
  with `hcm-tech:installedIn`; and
- may have an `hcm-env:EnvironmentProfile`.

Animal-to-cage allocation is modeled explicitly with
`hcm-bio:HousingAssignment`. This supports allocation metadata and avoids
treating a cage as a study factor. A cage should be represented as a study
factor only when cage identity or cage treatment is deliberately manipulated
as an independent variable. Assignment validity uses half-open `[start, end)`
intervals: adjacent re-housing records may share a boundary, while overlap,
zero-length/reversed intervals, and orphan records fail the standard profile.
Historical graphs use the assignment records rather than materializing the
time-dependent shortcut.

## Observation pattern

HCMO specializes SOSA rather than duplicating it:

1. an HCMO observation is a `sosa:Observation`;
2. `sosa:hasFeatureOfInterest` identifies the observed subject;
3. `sosa:madeBySensor` identifies the sensor;
4. `sosa:hasResult` links the result; and
5. `hcm-obs:occursIn` identifies the monitored enclosure.

For interval measurements, the observation enclosure must agree with the
subject's authoritative housing assignment throughout the phenomenon interval.

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
complete expected answer rows; the validator compares bindings, unbound values,
values, and multiplicity. A matching count or an unreviewed empty result is not
sufficient evidence.

The ISA/STATO bridge has a separate evidence shape. It constrains the pinned
Investigation/Study/Assay and LabProcess/File slice and includes an injected
process/data cycle that must be non-conformant. This profile is evidence for the
example boundary, not a claim of formal ISA RO-Crate conformance.

A second isolated profile validates the accepted housing, identity, 2 × 2
factor/group, repeated-observation, and statistical-result/file-fragment
invariants. Its canonical RDF and extended ISA RO-Crate JSON-LD graphs must be
isomorphic. Separate loss manifests describe ISA-JSON and ISA-Tab projections.
The executable native overlap covers only a distinct animal Source, specimen-
collection process, and genuine tissue Sample; HCMO IRIs are carried through
the Tab round trip as explicit comments. No Sample proxy is created for an
unchanged animal, so source-bound factor values and direct whole-animal assay
semantics remain explicit controlled losses.

## Deferred decisions

- Replace unit strings with a reviewed QUDT or OM pattern.
- Refine the target class for `hcm-obs:hasCondition`.
- Obtain an authoritative permanent ISA RO-Crate profile URI, base RO-Crate
  edition, and endorsed validator procedure before claiming formal conformance.
