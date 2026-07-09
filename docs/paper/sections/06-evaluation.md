# 6. Evaluation

- Pitfall scan: OOPS! (report + how pitfalls were addressed).
- FAIRness: FOOPS! score.
- Logical quality: Protege/HermiT pass on
  `ontology/v2/hcmo-v2-merged-clean.owl` — 32 classes loaded, 0 inconsistent
  classes, no `UNKNOWN:` IRIs. See `docs/paper/PROTEGE-REASONER.md`.
- Data validation: SHACL is deferred until the v2 terms are frozen/promoted;
  current `shapes/` and `examples/` still target the legacy/live term set.
- Competency-question results: each CQ → answer over the merged graph (T6).
- Coverage/completeness vs requirements (§3); comparison to alternatives.
- Archive all reports (figures/ or appendix) for reproducibility.
