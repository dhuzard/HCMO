# OOPS! evaluation report, 2026-07-10

Source tested: `ontology/v2/hcmo-v2-merged-clean.owl`

Tool: OOPS! OntOlogy Pitfall Scanner REST service, `https://oops.linkeddata.es/rest`.
The raw XML response is archived as `oops-v2-clean-2026-07-10.xml`.

Context: this run was performed after PR #14 was merged and after the FOOPS
metadata/definition/logo updates were merged into `main`. The tested file is
the clean Protege/BioPortal artifact with no active `UNKNOWN:` placeholders.

## Validation Context

- HermiT on `ontology/v2/hcmo-v2-merged-clean.owl`: 700 triples, 32 classes,
  0 `UNKNOWN:` IRIs, 0 inconsistent classes.
- `tooling/validate.py`: PASS.
- FOOPS: reported as 1.0 after metadata, definitions, and logo updates.

## Summary

| Code | Pitfall | Importance | Affected elements | Initial interpretation |
|---|---|---:|---:|---|
| P04 | Creating unconnected ontology elements | Minor | 10 | Partly real: several classes still need explicit links/restrictions. |
| P08 | Missing annotations | Minor | 20 | Mostly external SOSA, OWL-Time, and SEMTS terms after Damien's v2 definitions pass. |
| P10 | Missing disjointness | Important | n/a | Expected modeling decision; do not add broad disjointness without review. |
| P11 | Missing domain or range in properties | Important | 99 | Real but should be handled carefully; domain/range axioms affect inference. |
| P12 | Equivalent properties not explicitly declared | Important | 1 group | Review needed: `hcm-obs:hasResult` vs `sosa:hasResult`. |
| P13 | Inverse relationships not explicitly declared | Minor | 46 | Mostly optional; add inverses only when useful and semantically safe. |
| P22 | Using different naming conventions | Minor | 1 group | Low-priority warning from mixed local names. |
| P34 | Untyped class | Important | 1 | Real: `schema:Person` is used as a class but not declared locally. |

## What Changed After the FOOPS Work

The earlier OOPS baseline reported 131 missing annotations. After the FOOPS
definition pass on `main`, OOPS now reports 20 missing annotations. The remaining
P08 affected terms are primarily imported/reused vocabulary terms from SOSA,
OWL-Time, and SEMTS, not HCMO-local v2 classes/properties.

## Immediate Follow-up Candidates

1. P34: declare or import `schema:Person` consistently.
   OOPS reports `https://schema.org/Person` as an untyped class. The clean v2
   graph uses it, but the term is not declared as an `owl:Class` in the merged
   artifact. This is small and concrete.

2. P12: decide whether `hcm-obs:hasResult` duplicates `sosa:hasResult`.
   OOPS flags those two properties as possibly equivalent. Options are:
   explicitly align them, deprecate the local property, or document why both are
   needed.

3. P11: review domain/range policy before adding axioms.
   OOPS reports 99 affected properties. This should not be fixed mechanically:
   adding `rdfs:domain` and `rdfs:range` changes inference behavior. This should
   be a modeling pass, not a scanner-driven bulk edit.

4. P04: inspect the 10 unconnected elements.
   Some may be acceptable temporary draft terms, but each should either gain a
   relation/restriction or be explicitly justified.

## Lower-priority or Review-only Findings

- P08: remaining missing annotations are mostly external vocabulary terms. Avoid
  copying external definitions into HCMO unless we intentionally provide local
  annotations for reused terms.
- P10: missing disjointness is common in lightweight OWL ontologies. Add
  disjointness only where domain experts are certain.
- P13: inverse properties are not mandatory. Avoid adding inverse properties
  just to satisfy the scanner.
- P22: naming-convention warning is low priority unless it points to a real
  typo or inconsistent namespace policy.

## Recommended Next Task Split

- Cyril: address OOPS findings that are concrete and low risk first:
  `schema:Person`, the `hasResult`/SOSA decision, and inspection of the 10
  unconnected elements.
- Damien: FOOPS/FAIR has already reached 1.0; future FOOPS reruns can be used
  as regression checks after ontology changes.

