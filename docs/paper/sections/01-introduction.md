# 1. Introduction & motivation

- What home-cage monitoring is: 24/7, automated, non-invasive observation of
  lab animals (esp. rodents) in their home cage; sensors for activity, weight,
  behaviour, environment.
- Why it matters: data quality & reproducibility in preclinical research; 3Rs
  (Reduction, Refinement); animal welfare; richer, less stressful phenotyping.
- The problem: each commercial system emits proprietary, heterogeneous,
  siloed data → comparison/aggregation/sharing across devices & labs is hard;
  undermines FAIR and open science.
- Gap: no shared semantic model covering the HCM domain end-to-end.
- **Scope (HITL R2): the resource = the ontology + SHACL shapes + competency-question
  SPARQL + JSON-LD context + examples.** The KGQA pipeline and authoring webapp are
  *outlook/potential uses* in §7, NOT claimed contributions.
- Contributions (bullet list):
  1. HCMO — the **first** modular, standards-aligned OWL ontology for HCM
     (modules bio/housing/env/tech); no direct HCM ontology exists (HITL R2).
  2. A tool-consumable, reproducible, FAIR resource package (manifest, dist,
     SHACL, CQs, JSON-LD, docs).
  3. Evaluation (pitfalls, FAIR, reasoning, SHACL, competency questions) with
     worked examples — synthetic ABoxes now; real **TEATIME** data as the
     validation path.
