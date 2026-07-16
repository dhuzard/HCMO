# Ontology architecture

HCMO 0.1.0 is authored as five domain modules plus one migration-only
compatibility module. The release manifest `hcmo.yaml` is the authoritative
module list; `dist/` is generated from that manifest.

## Active modules

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

## Dependency policy

HCMO reuses external classes and properties by reference and does not redeclare
them locally. The active ontology uses:

- BFO and IAO as upper-level anchors;
- SOSA for observation, result, sensor, actuator, observed-property, and
  feature-of-interest roles;
- OWL-Time for temporal intervals;
- Dublin Core Terms for ontology metadata and provenance.

The `bio` and `obs` modules intentionally have a small semantic cycle:
subject-side convenience properties live in `bio`, while observations point to
their subject with `sosa:hasFeatureOfInterest`. HCMO is released as one merged
graph, so this does not create an import-order dependency.

## Extension rules

- Keep the core module limited to enclosure concepts shared across use cases.
- Add each term to the module matching its namespace.
- Put application-specific cardinality and intake rules in `shapes/`, not in
  the domain class hierarchy.
- Prefer a bridge document or module for ISA, QUDT/OM, taxon, and anatomy
  mappings until an equivalence is justified.
- Never re-mint a published HCMO IRI. Deprecate it and map a replacement when a
  defensible replacement exists.
