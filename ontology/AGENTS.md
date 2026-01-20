# AGENTS.md — Ontology Workspace (ontology/)

This folder contains the ontology source of truth. Generated files should not be edited by hand.

## Architecture (repo-specific)
- `hcm.ttl` : core ontology terms and axioms (authoritative source)
- `hcm-align.ttl` : external standards alignments
- `hcm-metadata.ttl` : ontology metadata and import declarations
- `hcm-bridge-*.ttl` : optional bridge modules for external domain ontologies
- `context.jsonld` : JSON-LD context for application developers

## Canonical modeling patterns (project-specific)
Authoritative notes live in `docs/MODEL.md`. Use ONLY these patterns unless you propose a change:
1) Behavior as process:
   - `hcm:BehaviorAndPhysiology` is a process (BFO-aligned)
2) Observation window:
   - `hcm:TimeInterval` with `hcm:durationHours` >= 24 and limited human interaction
3) System composition:
   - `hcm:System` uses `hcm:hasEnclosure`, `hcm:hasHardware`, `hcm:hasSoftware`,
     `hcm:hasSensor`, `hcm:hasActuator`
4) Needs:
   - simple boolean decomposition (upgrade to classes only if justified)
5) Dimensions:
   - simple datatype pattern; roadmap to QUDT/OM if needed

## Required annotations (per entity)
- label: rdfs:label
- definition: IAO:0000115 (or the project's definition property)
- editor note / provenance: project choice (keep lightweight)
- created/modified dates only if the repo already enforces them (avoid inventing metadata rules)

## Deprecation & replacements
When deprecating:
- keep the IRI
- mark deprecated = true
- add "replaced by" pointer (property depends on your profile)
- preserve old label as an exact synonym if appropriate

## Validation commands (repo scripts)
Preferred: run the repo script:
- `./tooling/validate.ps1`

Never claim validation passed unless you actually ran the command.
