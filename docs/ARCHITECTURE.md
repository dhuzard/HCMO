# Ontology architecture

HCMO 0.2.0 is authored as a checksummed end-user upper-level presentation, five
domain modules, and one migration-only compatibility module. The release
manifest `hcmo.yaml` is the authoritative module list; `dist/` is generated
from that manifest.

## Active modules

- `ontology/modules/external-upper.ttl`: a flattened presentation of five
  canonical BFO 2020 / IAO 2026-03-30 anchors—Entity, Material entity,
  Information content entity, Quality, and Process. Its direct links to Entity
  are source-entailed navigation shortcuts. It does not mint HCMO terms or
  replace either source ontology.
- `ontology/modules/hcm-core.ttl` (`hcm:`): monitored enclosures, enclosure
  dimensions, enrichment, and stable enclosure relations.
- `ontology/modules/hcm-bio.ttl` (`hcm-bio:`): subjects, experimental groups,
  study factors, and housing assignments.
- `ontology/modules/hcm-env.ttl` (`hcm-env:`): environmental profiles,
  environmental properties, light cycles, and measurement specifications.
- `ontology/modules/hcm-obs.ttl` (`hcm-obs:`): SOSA observations and results.
- `ontology/modules/hcm-tech.ttl` (`hcm-tech:`): sensors, actuators, hardware,
  software, and time-series resources.
- `ontology/modules/hcm-compat.ttl`: deprecated 0.0.1 HCMO IRIs and explicit
  replacement mappings. New data must not use this vocabulary.

The former `ontology/v2/` draft has been promoted into the active module set.
Its old generated review artifacts remain only as historical evidence.

## End-user and developer upper views

The default generated release deliberately hides BFO's continuant, occurrent,
independent-continuant, and dependent-continuant intermediates. This implements
Philippe Rocca-Serra's pragmatic end-user layer while retaining canonical
BFO/IAO IRIs, source definitions, and compatibility.

Ontology developers can load
`ontology/profiles/external-upper-developer.ttl` alongside `dist/hcmo.owl`.
That optional, non-manifest profile restores the pinned source-faithful
intermediate hierarchy and refines `hcm-bio:ExperimentalGroup` from the default
Material entity category to BFO object aggregate. The default and developer
views make no equivalence assertions between BFO, IAO, SOSA, PROV-O, SIO, SULO,
or ONTOP.

See [UPPER-LEVEL-VIEW.md](UPPER-LEVEL-VIEW.md) for the user-facing tree,
placement examples, and instructions for loading the optional profile.

## Dependency policy

HCMO reuses external classes and properties by reference and does not redeclare
them as local HCMO terms. The end-user presentation copies reviewed source
annotations and adds only source-entailed navigation shortcuts. The active
ontology modules use:

- BFO and IAO as upper-level anchors;
- SOSA for observation, result, sensor, actuator, observed-property, and
  feature-of-interest roles;
- Schema.org for contributor and place exchange types;
- SemTS 1.2.0 for the reviewed time-series-segment and segment-dimension
  pattern; and
- Dublin Core Terms for ontology metadata and provenance.

The current example data and competency queries reuse OWL-Time for observation
and housing-validity intervals. Pinned evidence uses particular PROV-O, OBI,
STATO, and ISA/Bioschemas instances without asserting ontology mappings. A
lossless HCMO RDF/extended ISA RO-Crate fixture is validated separately, but
formal ISA profile conformance remains deferred. Quantity/unit alignment
remains roadmap work.
The normative sensing policy is pinned to SOSA 2017 and uses
`sosa:ObservableProperty`; no developing-edition `sosa:Property` term is mixed
into the release. SemTS reuse is limited to canonical 1.2.0
time-series-segment and segment-dimension terms.

`external-vocabularies.yaml` is the external-source contract. It records the
authoritative version, canonical term namespace, used-term allowlist, immutable
artifact URL, and SHA-256 for the upper anchors and the sensing, temporal, OBI,
PROV-O, STATO, SemTS, and ISA RO-Crate evidence sources. It is deliberately
separate from `hcmo.yaml`; validation asserts that the public manifest's key
shape is unchanged. The build remains offline and does not follow
`owl:imports`. Network checksum verification is an explicit audit command:
`python tooling/external_vocab.py --verify-network`.

The `bio` and `obs` modules intentionally have a small semantic cycle:
subject-side convenience properties live in `bio`, while observations point to
their subject with `sosa:hasFeatureOfInterest`. HCMO is released as one merged
graph, so this does not create an import-order dependency.

## Monitoring and physical installation

Monitoring association and physical installation are intentionally distinct.
`hcm-tech:monitoredBy` links an enclosure to a sensor that monitors it, including
remote and rack-level sensors. `hcm-tech:installedIn` records physical
installation in a particular monitored enclosure. Neither property is the
inverse of the other, and being a sensor does not require installation in an
individual enclosure. SHACL validates the target class when `installedIn` is
present but does not require the relation or impose a timeless cardinality.

## Validation architecture

The release has seven separate validation layers:

- `tooling/build.py` creates deterministic release artifacts from the module
  list in `hcmo.yaml` without network access;
- pySHACL validates each isolated example against `shapes/hcm-shapes.ttl`, with
  the merged ontology supplied as a separate ontology graph and RDFS inference
  enabled;
- a dedicated ISA/STATO evidence profile validates
  `examples/isa-hcmo-bridge.ttl` and rejects an injected cyclic process/data
  graph;
- a dedicated round-trip profile validates graph isomorphism, housing/identity,
  factor/group, observation, result-fragment, mapping-registry, and controlled-
  loss invariants;
- pinned `isatools` executes the native animal Source → genuine tissue Sample
  overlap through ISA-JSON → ISA-Tab → ISA-JSON and checks the explicit HCMO
  identity comments;
- `roc-validator` independently checks RO-Crate 1.2 and the pinned ISA-specific
  rules; and
- HermiT checks OWL DL consistency on the generated release artifact.

The pySHACL data graph is never the ontology graph alone. Supplying the
ontology graph ensures that an instance typed through a reviewed subclass,
domain, or range axiom is selected by the same `sh:targetClass` as an explicitly
typed instance. Shapes define intake/profile requirements and must not be
copied into OWL existential restrictions.

Competency queries run over a separate evaluation graph containing the merged
ontology and all positive examples declared in `hcmo.yaml`. Negative examples
remain isolated and never contribute answers. Complete expected answer rows
live beside the stable CQ identifiers in `queries/competency_questions.yaml`;
the validator fails on a missing query, an unindexed query, or any answer-value,
binding, multiplicity, or row mismatch.

## Extension rules

- Keep the core module limited to enclosure concepts shared across use cases.
- Add each term to the module matching its namespace.
- Put application-specific cardinality and intake rules in `shapes/`, not in
  the domain class hierarchy.
- Prefer a bridge document or module for ISA, taxon, and anatomy
  mappings until an equivalence is justified.
- Never re-mint a published HCMO IRI. Deprecate it and map a replacement when a
  defensible replacement exists.
