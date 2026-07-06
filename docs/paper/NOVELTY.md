# Novelty & related-resources search (HITL Round 4)

**Date:** 2026-06-29 · **Method:** web search of ontology registries (BioPortal/LOV
context) + literature. To be deepened with direct BioPortal/LOV queries before
submission.

## Headline finding
**No ontology dedicated to Home-Cage Monitoring was found.** Searches for an HCM
ontology return only HCM *systems/technical/application* papers, not semantic
models. → The claim "**HCMO is the first ontology for the HCM domain**" is
defensible, **but must be stated precisely** and positioned against adjacent
resources below (reviewers will check these).

## Adjacent resources to cite & differentiate in §2

| Resource | What it is | Relation to HCMO |
|----------|------------|------------------|
| **OBI** — Ontology for Biomedical Investigations | Models investigations: design, protocols, instruments, materials, data, analysis. | Upper/adjacent. HCMO can **align/bridge** (investigation, device, assay) but OBI does **not** model the HCM enclosure↔subject↔sensor↔observation chain. |
| **OLAM** — Ontology of Laboratory Animal Medicine (BioPortal, upd. 2024) | Lab-animal medicine terminology. | Adjacent vocabulary for subjects/health; **not** an HCM data/observation model. |
| **MEDO** — Mouse Experimental Design Ontology (BioPortal) | Standard language for experimental design in mouse studies. | Overlaps on experimental groups/study factors (HCMO-housing); **not** sensor/observation acquisition. |
| **ARRIVE** guidelines | Reporting standard for in-vivo experiments (not an ontology). | Requirements source for metadata completeness; **not** a machine-readable ontology. |
| **SOSA/SSN, OWL-Time, UO, PROV, BFO** | W3C/community standards. | **Reused** by HCMO (not competitors) — the sensor/observation/temporal/units/provenance/upper layers. |

## Honest framing for the paper
> "To our knowledge, HCMO is the first ontology specifically modelling home-cage
> monitoring as an integrated system (animal subject, housing, environment,
> acquisition devices, observations, and provenance). Existing biomedical and
> laboratory-animal ontologies (OBI, OLAM, MEDO) and reporting guidelines (ARRIVE)
> address adjacent concerns but do not cover the HCM acquisition chain; HCMO
> reuses W3C standards (SOSA/SSN, OWL-Time, UO, PROV, BFO) rather than competing
> with them."

## Sources
- HCM systematic review — PMC10642068; bioRxiv 2023.03.07.531465.
- HCM (Kiryk et al.) — Springer 978-3-032-19781-8_1 (report ref [12]).
- OBI — PLOS One 10.1371/journal.pone.0154556; BioPortal/NCBO.
- OLAM — BioPortal `OLAM`.
- MEDO — BioPortal (Mouse Experimental Design Ontology).
- ARRIVE — PLOS Biology 10.1371/journal.pbio.1002151.

## TODO (deepen before submission)
- [ ] Direct BioPortal + **LOV** queries; record exact versions/IRIs.
- [ ] Check for any HCM/animal-sensor vocabularies in agri/veterinary domains.
- [ ] Decide which adjacencies to **bridge** (OBI/MEDO) vs merely cite.
