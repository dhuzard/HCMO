# 6. Evaluation

- Pitfall scan: OOPS! was run on the public v2 clean artifact and archived at
  `docs/paper/evaluation/OOPS-REPORT-2026-07-10.md`. The 2026-07-15 rerun
  (`docs/paper/evaluation/oops-v2-clean-2026-07-15.xml`) reports no critical or
  important pitfalls; the only remaining finding is P13 (minor) for 8 inverse
  relationships that were intentionally not asserted because OOPS classified the
  candidate inverses as P05. Pitfalls to re-confirm against the promoted 0.1.0
  release before submission.
- FAIRness: FOOPS! v0.4.0 on `ontology/v2/hcmo-v2-merged-clean.owl`
  improved from 0.49444446 to 1.0 after adding ontology-header FAIR metadata,
  v2 term definitions, and canonical logo metadata. See
  `docs/paper/FOOPS-REPORT-2026-07-09.md`.
- Logical quality: Protege/HermiT pass on
  `ontology/v2/hcmo-v2-merged-clean.owl` — 32 classes loaded, 0 inconsistent
  classes, no `UNKNOWN:` IRIs. See `docs/paper/PROTEGE-REASONER.md`.
- Data validation: SHACL is deferred until the v2 terms are frozen/promoted;
  current `shapes/` and `examples/` still target the legacy/live term set.
- Competency-question results: each CQ → answer over the merged graph (T6).
- Coverage/completeness vs requirements (§3); comparison to alternatives.
- Archive all reports (figures/ or appendix) for reproducibility.
