# Archived HCMO v2 review workspace

The reviewed v2 source modules were promoted to `ontology/modules/` as HCMO
0.1.0 on 2026-07-16. The current release contract is `hcmo.yaml`; current
generated artifacts are under `dist/`.

The merged Turtle and RDF/XML files retained in this directory are historical
review snapshots. They are not inputs to the build and must not be edited or
used as the current HCMO release.

The obsolete v2 builder and reasoner were retired at promotion. Current
reasoning uses `tooling/reason.py` against `dist/hcmo.owl`.

Promotion added explicit BFO/IAO and SOSA anchors, property domain/range axioms,
canonical SOSA `hasResult` use, compatibility mappings for published 0.0.1 IRIs,
and re-authored SHACL/examples/competency queries. The pre-promotion modules were
moved rather than copied, so there is no second active source tree here.
