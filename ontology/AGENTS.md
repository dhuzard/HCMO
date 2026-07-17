# AGENTS.md — Ontology Workspace (ontology/)

This folder contains the ontology source of truth. Generated files (`../dist/`) must not be edited by hand.

## Architecture (repo-specific)
- `modules/hcm-core.ttl` : core terms, axioms, and the `owl:Ontology` header (incl. `dcterms:creator` attribution).
- `modules/hcm-bio.ttl`  : biological subjects/groups (namespace `…/hcm/bio#`).
- `modules/hcm-env.ttl`  : environment & measurement terms (namespace `…/hcm/env#`).
- `modules/hcm-obs.ttl`  : observations & results (namespace `…/hcm/obs#`).
- `modules/hcm-tech.ttl` : sensors, actuators, software, and data artifacts (namespace `…/hcm/tech#`).
- `modules/hcm-compat.ttl`: deprecated 0.0.1 HCMO IRIs and explicit replacements; no new concepts.
- `context.jsonld`       : JSON-LD context for application developers.
- `legacy/`              : the previous HCMO 1.0.0 ontology (retained, not merged).

The merged graph is the union of `modules/*.ttl`, produced by `../tooling/build.py` into `../dist/`.
Module load order and all paths are declared in `../hcmo.yaml`.

## Namespaces
- Base: `https://w3id.org/hcmo/ontology/hcm#` (ontology IRI `https://w3id.org/hcmo/ontology/hcm`).
- Sub-namespaces are path segments: `…/hcm/bio#`, `…/hcm/env#`, `…/hcm/obs#`, `…/hcm/tech#`.
- Put each new term in the module matching its namespace.

## Required annotations (per entity)
- label: `rdfs:label`
- definition: `rdfs:comment` and/or `IAO:0000115`
- provenance / editor note: lightweight, project choice
- Do not invent labels/definitions. Missing ones are listed in `../docs/MISSING-DEFINITIONS.md`.

## Known data-quality debt (see ../docs/MISSING-DEFINITIONS.md)
- Many terms still lack `rdfs:comment` definitions.
- Chowlk export artifacts are preserved as authored (e.g. `UNKNOWN:*`, `ns:Class2`,
  `xsd:boolean`/`xsd:integer` typed as properties) — review and re-map/remove at the source, do not silently delete.

## Deprecation & replacements
When deprecating: keep the IRI, mark `owl:deprecated true`, add a "replaced by" pointer, and preserve the old label as an exact synonym if appropriate.

## Validation (repo scripts)
From the repo root:
- `python ../tooling/build.py`    — regenerate `../dist/` (reproducible).
- `python ../tooling/validate.py` — parse + SHACL + competency queries.

Never claim validation passed unless you actually ran the command.
