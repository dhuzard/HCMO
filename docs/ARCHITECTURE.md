# Ontology Architecture (Modular Plan)

This document defines a modular architecture for HCMO so the core ontology
stays stable while allowing optional, domain-specific extensions (e.g., animal
taxa, anatomy, devices) to be connected safely.

## Goals
- Keep the core stable and minimal.
- Isolate alignments and domain extensions in separate modules.
- Enable optional bridge modules to connect to external ontologies without
  forcing those imports on all users.

## Current state
- Core terms and axioms live in `ontology/hcm.ttl`.
- External alignments live in `ontology/hcm-align.ttl`.
- Metadata and imports live in `ontology/hcm-metadata.ttl`.

## Target modular architecture
### 1) Core module (authoritative, minimal)
File: `ontology/hcm.ttl`
Scope:
- System composition (`hcm:System`, `hcm:hasEnclosure`, `hcm:hasSensor`, ...)
- Physical space and dimensions
- Time interval model
- Behavior/physiology process
- Needs (boolean decomposition)

### 2) Alignment module (standards mapping only)
File: `ontology/hcm-align.ttl`
Scope:
- SOSA/SSN, OWL-Time, PROV, BFO alignments
- No local constraints or domain extensions

### 3) Metadata module (ontology metadata + imports)
File: `ontology/hcm-metadata.ttl`
Scope:
- Ontology identity, version IRI, licensing, and import list

### 4) Bridge modules (optional, domain-specific alignments)
Pattern: `ontology/hcm-bridge-<domain>.ttl`
Scope:
- Connect HCMO assets to external ontologies (taxa, anatomy, devices)
- Keep all external imports and equivalences in these files
Examples:
- `ontology/hcm-bridge-animal.ttl` (animal taxa/anatomy)
- Future: `ontology/hcm-bridge-device.ttl` (device registries)

## Bridge module rules
- Each bridge module must import `https://w3id.org/hcmo/ontology/hcm`.
- External ontology imports must live ONLY in bridge modules.
- Prefer `rdfs:subClassOf` or `skos:exactMatch` over `owl:equivalentClass`
  unless the equivalence is defensible under reasoning.
- Do not move or re-mint HCM IRIs when bridging.

## Migration notes (future)
If the core grows, consider splitting by domain:
- `hcm-system.ttl`, `hcm-observation.ttl`, `hcm-assets.ttl`, `hcm-needs.ttl`
This should be done with explicit import wiring and a single released entry
point (metadata module).
