# Legacy ontology (HCMO 1.0.0)

These files are the previous HCMO core (version 1.0.0), authored on the namespace
`https://w3id.org/hcmo/ontology/hcm#` with ontology IRI
`https://w3id.org/hcmo/ontology/hcm`. They are **retained, not deleted**, because
they are authored content.

The repository has been reorganized around the MAPP ontology (MAPP 0.0.1), whose
hand-authored sources live in `ontology/modules/`. MAPP **keeps the same base
namespace** `https://w3id.org/hcmo/ontology/hcm#` (sub-namespaces `…/hcm/bio#`,
`…/hcm/env#`, `…/hcm/obs#`) but defines a **different term set** (e.g.
`MonitoredEnclosure`, `Subject`, observation classes) than this legacy 1.0.0
file (e.g. `System`, `ObservationWindow`). Only `ontology/modules/` is merged
into `dist/`; these legacy files are not.

The SHACL shapes (`shapes/`), example A-boxes (`examples/`), SPARQL queries
(`queries/`) and JSON-LD context (`ontology/context.jsonld`) were written for the
legacy 1.0.0 term set and need re-authoring against the MAPP terms before they
validate the new modules.
