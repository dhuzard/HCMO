# OOPS! evaluation report, 2026-07-10

Source tested: `ontology/v2/hcmo-v2-merged-clean.owl`

Tool: OOPS! OntOlogy Pitfall Scanner REST service, `https://oops.linkeddata.es/rest`.
The raw XML response is archived as `oops-v2-clean-2026-07-10.xml`.

Context: this run was performed after PR #14 was merged and after the FOOPS
metadata/definition/logo updates were merged into `main`. The tested file is
the clean Protege/BioPortal artifact with no active `UNKNOWN:` placeholders.

## Validation Context

- HermiT on `ontology/v2/hcmo-v2-merged-clean.owl`: 966 triples, 33 named
  classes loaded, 0 `UNKNOWN:` IRIs, 0 inconsistent classes.
- `tooling/validate.py`: PASS.
- FOOPS: reported as 1.0 after metadata, definitions, and logo updates.

## Summary

| Code | Pitfall | Importance | Affected elements | Initial interpretation |
|---|---|---:|---:|---|
| P10 | Missing disjointness | Important | n/a | Expected modeling decision; do not add broad disjointness without review. |
| P11 | Missing domain or range in properties | Important | 59 | Real but should be handled carefully; domain/range axioms affect inference. |
| P13 | Inverse relationships not explicitly declared | Minor | 46 | Mostly optional; add inverses only when useful and semantically safe. |
| P22 | Using different naming conventions | Minor | 1 group | Low-priority warning from mixed local names. |

## OOPS Progress

The earlier OOPS baseline reported 131 missing annotations. After the FOOPS
definition pass on `main`, OOPS reported 20 missing annotations. This OOPS pass
adds local annotations for the reused SOSA, OWL-Time, and SEMTS scaffolding
terms, so P08 is no longer reported.

## Corrections Applied in This OOPS Pass

This pass made only semantically defensible changes rather than adding scanner-
driven filler axioms.

- P04 reduced from 10 to 0 by connecting previously isolated local classes
  through existing HCMO relations and by typing `schema:Person`/`schema:name`
  used in contributor metadata.
- P08 reduced from 20 to 0 by adding local annotations for reused SOSA,
  OWL-Time, and SEMTS scaffolding terms in the clean artifact.
- P12 removed by explicitly aligning `hcm-obs:hasResult` with `sosa:hasResult`
  using `owl:equivalentProperty`.
- P34 removed by declaring `schema:Person` as an `owl:Class` and declaring
  `schema:name` as the metadata property used for contributors.
- P11 reduced from 94 to 59 by adding conservative domain/range axioms only
  where they do not distort HermiT classification. Multi-context properties use
  `owl:unionOf` domains when a single domain would be too restrictive.

## Remaining Findings and Why They Are Not Bulk-fixed

- P10: missing disjointness is common in lightweight OWL ontologies. Add
  disjointness only where domain experts are certain that classes cannot
  overlap. Adding broad disjointness just to satisfy OOPS would make the model
  brittle.
- P11: OOPS still reports 59 properties without both domain and range. This is
  a real modeling task, but it should be handled in a dedicated domain/range
  policy pass. Adding generic `owl:Thing` domains/ranges would make OOPS quieter
  without improving HCMO.
- P13: inverse properties are not mandatory. Avoid adding inverse properties
  just to satisfy the scanner; add them only where they improve expected data
  authoring or querying.
- P22: naming-convention warning is low priority unless it points to a real
  typo or inconsistent namespace policy. The current warning reflects mixed
  property/class local-name shapes, not a known semantic error.

## Recommended Next Task Split

- Treat the current OOPS state as the clean v2 baseline.
- Next safe ontology-quality task: define a domain/range policy for v2 and apply
  it term-by-term, with HermiT checks after each batch.
- Keep P10/P13 as documented modeling choices unless a concrete use case
  requires disjointness or inverse properties.

## Follow-up local pass, 2026-07-15

After the archived OOPS REST run above, a further local pass added:

- minimal disjointness already present in the legacy ontology
  (`Sensor` disjoint with `Actuator`; `Hardware` disjoint with `Software`);
- `owl:SymmetricProperty` on `hcm-tech:communicatesWith`;
- additional conservative domain/range axioms for environmental, SEMTS, and
  technical relations.

An attempted `owl:inverseOf` assertion between the SOSA `madeBySensor` and
`madeObservation` properties was rejected by the OOPS REST scanner as P05
(`Defining wrong inverse relationships`) and was removed again. Follow-up work
added named context classes, completed conservative domain/range axioms, and
normalized v2 environmental property names. The resulting clean v2 artifact
contains 1926 triples. HermiT still reports 0 inconsistent classes and
`tooling/validate.py` passes. A local rdflib check for properties without both
`rdfs:domain` and `rdfs:range` reports 0 remaining properties.

## Official public-artifact rerun, 2026-07-15

OOPS was then rerun against the clean OWL file fetched from the public
`cyril/oops-evaluation` GitHub branch. The XML output is archived as
`docs/paper/evaluation/oops-v2-clean-2026-07-15.xml`.

| Code | Name | Severity | Affected | Status |
|---|---|---:|---:|---|
| P13 | Inverse relationships not explicitly declared | Minor | 8 | Remaining inverses were intentionally not asserted because OOPS classifies the candidate inverse pairs as P05 critical. |

No critical or important OOPS pitfalls remain in this rerun. P11 and P22 are
closed.
