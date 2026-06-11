# Legacy ontology (HCMO 1.0.0, namespace https://w3id.org/hcmo/ontology/hcm#)

These files are the previous HCMO core (version 1.0.0) built on the namespace
`https://w3id.org/hcmo/ontology/hcm#`. They are **retained, not deleted**, because
they are authored content.

The repository has been reorganized around the new MAPP ontology
(`https://w3id.org/hcm/mapp`, namespace `https://w3id.org/hcm/`, version 0.0.1),
whose hand-authored sources live in `ontology/modules/`. The two ontologies use
**different namespaces** and are not merged.

The SHACL shapes (`shapes/`), example A-boxes (`examples/`), SPARQL queries
(`queries/`) and JSON-LD context (`ontology/context.jsonld`) still target this
legacy namespace and need re-authoring before they validate the new MAPP modules.
