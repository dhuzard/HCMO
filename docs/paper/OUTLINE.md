# HCMO Resource Paper — outline & page budget

Working title: **HCMO: An Ontology for Home-Cage Monitoring of Laboratory Animals**
Target: **ESWC 2027 Resources Track**, Springer LNCS, **15 pp + unlimited refs**
(decided, HITL Round 1). Canonical HCMO 0.2.0 structure: five active modules,
**core / bio / env / obs / tech**, plus a migration-only compatibility module.

| § | Section | Pages | Key content / evidence |
|---|---------|------:|------------------------|
| — | Title, authors, abstract | 0.5 | Named authors (single-anonymous). Abstract ≤ ~200 words. |
| — | **Resource metadata block** | 0.1 | Type / License / DOI / URL (CfP-mandated, right after abstract). |
| 1 | **Introduction & motivation** | 1.5 | Home-cage monitoring (24/7, non-invasive); preclinical reproducibility, 3Rs, FAIR; vendor data silos & interoperability gap; contributions (bulleted). |
| 2 | **Related work** | 1.0 | Existing HCM/animal data models; SOSA/SSN-based sensor ontologies; biomedical/animal ontologies (e.g. OBI, anatomy/taxonomy); why none cover HCM end-to-end. |
| 3 | **Requirements & competency questions** | 1.0 | Use cases; competency questions (cite `queries/`); design requirements driving the model. |
| 4 | **Resource description** | 2.5 | HCMO 0.2.0 modules **core/bio/env/obs/tech** plus compatibility; key classes and the sensor≠observation≠result split; SOSA, OWL-Time, BFO/IAO and SEMTS reuse; JSON-LD context. Figure: ontology overview. |
| 5 | **Engineering & availability** | 1.5 | Release manifest as a stable contract; modular Turtle → reproducible dist (TTL/OWL/JSON-LD); CI validation gate; SHACL; PURL (w3id) + DOI + CC BY 4.0; WIDOCO docs; FAIR mapping. Figure: architecture/build pipeline. |
| 6 | **Evaluation** | 1.5 | OOPS! pitfalls; FOOPS! FAIR score; reasoner consistency; SHACL validation on examples; competency-query results; coverage/completeness; comparison to alternatives. |
| 7 | **Impact, use cases & sustainability** | 1.0 | KGQA (NL querying) layer; authoring webapp; vendor-data mapping ambition; adoption path; welfare/3Rs/open-science impact; governance, versioning, maintenance plan. |
| 8 | **Conclusion & future work** | 0.5 | Honest limitations (early stage); roadmap (QUDT/OM units, bridge modules, more data). |
| — | References | 1.5 | LNCS bib. |

## Narrative spine (the argument)
1. HCM produces rich welfare/physiology data but it is **siloed and
   non-interoperable** across vendors → blocks comparison, aggregation, FAIR sharing.
2. **No existing ontology** covers the HCM domain end-to-end (enclosure ↔ subject
   ↔ environment ↔ observation ↔ device).
3. **HCMO** fills this with a modular, standards-aligned ontology shipped as a
   **tool-consumable, reproducible, FAIR** resource.
4. We **evaluate** it (pitfalls, FAIR, reasoning, SHACL, competency questions).
5. It has **impact** (welfare/3Rs/reproducibility) and a **sustainability** plan,
   with concrete reuse (KGQA, authoring app).

## Figures (T19)
- F1: HCMO architecture & reproducible build/release pipeline.
- F2: Ontology overview (modules + selected release-aligned classes/relations).
- F3: Worked example — minimal ABox as an RDF graph mapped to standards.
