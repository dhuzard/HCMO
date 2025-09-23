# HCMO Ontology

A professional, reusable ontology for Home-Cage Monitoring (HCMO).

- Core: classes and properties for systems, animals, enclosures, behaviors, sensors/actuators, time intervals, and needs.
- Standards: aligns to SOSA/SSN, OWL-Time, PROV, BFO; optional QUDT/OM for units.
- Validation: SHACL shapes for key constraints.
- Examples: minimal ABox and edge-case dataset.
- Queries: competency-question SPARQL files.

Quickstart
- Load `ontology/hcm-metadata.ttl` (imports `hcm.ttl` and `hcm-align.ttl`) plus `shapes/hcm-shapes.ttl` into your triple store.
- Add `examples/abox-minimal.ttl` and run queries in `queries/`.
- Validate with pySHACL: see `tooling/validate.ps1`.

IRI and Prefix
- Base: `https://w3id.org/hcmo/ontology/hcm#`
- Version: `https://w3id.org/hcmo/ontology/hcm/1.0.0`

License
- CC BY 4.0

