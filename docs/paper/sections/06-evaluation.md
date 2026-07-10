# 6. Evaluation

- Pitfall scan: OOPS! report archived at
  `docs/paper/evaluation/OOPS-REPORT-2026-07-10.md`; P04/P08/P12/P34 were
  addressed, P11 was reduced from 94 to 87 by conservative domain/range
  additions, and P10/P11/P13/P22 remain documented modeling-policy findings.
- FAIRness: FOOPS! v0.4.0 on `ontology/v2/hcmo-v2-merged-clean.owl`
  improved from 0.49444446 to 1.0 after adding ontology-header FAIR metadata,
  v2 term definitions, and canonical logo metadata. See
  `docs/paper/FOOPS-REPORT-2026-07-09.md`.
- Logical quality: Protege/HermiT pass on
  `ontology/v2/hcmo-v2-merged-clean.owl` — 33 classes loaded, 0 inconsistent
  classes, no `UNKNOWN:` IRIs. See `docs/paper/PROTEGE-REASONER.md`.
- Data validation: SHACL is deferred until the v2 terms are frozen/promoted;
  current `shapes/` and `examples/` still target the legacy/live term set.
- Competency-question results: each CQ → answer over the merged graph (T6).
- Coverage/completeness vs requirements (§3); comparison to alternatives.
- Archive all reports (figures/ or appendix) for reproducibility.
