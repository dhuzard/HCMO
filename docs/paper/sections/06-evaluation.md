# 6. Evaluation

- Pitfall scan: OOPS! (report + how pitfalls were addressed).
- FAIRness: FOOPS! score.
- Logical quality: Protege reasoner pass (ELK/HermiT) on
  `ontology/v2/hcmo-v2-merged.ttl` — consistency, no unsatisfiable classes, no
  unintended inferred placements. See `docs/paper/PROTEGE-REASONER.md`.
- Data validation: SHACL is deferred until the v2 terms are frozen/promoted;
  current `shapes/` and `examples/` still target the legacy/live term set.
- Competency-question results: each CQ → answer over the merged graph (T6).
- Coverage/completeness vs requirements (§3); comparison to alternatives.
- Archive all reports (figures/ or appendix) for reproducibility.
