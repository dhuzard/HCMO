# 6. Evaluation

- Pitfall scan: OOPS! report archived at
  `docs/paper/evaluation/OOPS-REPORT-2026-07-10.md`; P04/P08/P12/P34 were
  addressed, P11 was reduced from 94 to 59 by conservative domain/range
  additions, including `owl:unionOf` domains for explicitly multi-context
  properties. A 2026-07-15 OOPS rerun from the public GitHub artifact reports
  no critical pitfalls; remaining findings are P11 domain/range gaps
  (31 properties), P13 missing inverse properties (45, minor), and P22 naming
  convention noise (1, minor). The XML output is archived at
  `docs/paper/evaluation/oops-v2-clean-2026-07-15.xml`.
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
