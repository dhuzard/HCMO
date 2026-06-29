# 2. Related work

> **Positioning (HITL R2): HCMO is the first ontology for the HCM domain** — no
> direct competitor known. Compare to general standards we reuse and to adjacent
> biomedical/animal ontologies, and show none model HCM end-to-end.
> (Optional: I can verify via LOV/BioPortal search on request — not yet done.)

- HCM / laboratory-animal data models & standards efforts (and their limits).
- Sensor/observation ontologies: SOSA/SSN — what HCMO reuses and extends.
- Temporal modelling: OWL-Time.
- Provenance: PROV.
- Upper ontology: BFO (process modelling for behaviour/physiology).
- **Adjacent ontologies (found in novelty search — see `NOVELTY.md`):**
  - **OBI** (Ontology for Biomedical Investigations) — investigations/protocols/
    instruments; bridge candidate, but no HCM acquisition chain.
  - **OLAM** (Ontology of Laboratory Animal Medicine) — lab-animal terminology.
  - **MEDO** (Mouse Experimental Design Ontology) — experimental design (overlaps
    HCMO-housing groups/study factors).
  - **ARRIVE** guidelines — in-vivo reporting standard (not an ontology) → a
    metadata-completeness requirements source.
- Units: **UO** (reused), QUDT/OM (roadmap).
- Conclusion: **no ontology models HCM end-to-end** → HCMO is the first; it
  **reuses** SOSA/SSN, OWL-Time, UO, PROV, BFO (not competitors) and can bridge to
  OBI/MEDO.

> TODO: deepen with direct BioPortal/LOV queries; cite 15–25 refs in references.bib.
