# HITL improvement loop — open questions backlog

Purpose: aspects of the resource paper I am **< 90% confident** about. Each is
asked to the author in batched rounds (human-paced loop). Answers are applied to
the relevant doc and logged in `TODO.md`.

**Confidence legend:** 🔴 low (<60%) · 🟠 medium (60–90%) · 🟢 resolved (≥90%)
**Last updated:** 2026-06-29

## Round 1 — foundational (asked first)
| # | Aspect | Conf. | Why it matters | Answer |
|---|--------|-------|----------------|--------|
| Q1 | **Target venue + cycle** (ISWC vs ESWC; which year) | 🔴 | Sets page limit, dates, template. Both 2026 closed. | _pending_ |
| Q2 | **Paper authorship & lead** (who leads; author order; is this Resources vs In-Use track) | 🔴 | Affects framing & credit; Resources≠In-Use. | _pending_ |
| Q3 | **Canonical module structure** — report says `bio/housing/env/tech`; repo ships `core/bio/env/obs` | 🔴 | The paper must present ONE consistent structure. | _pending_ |
| Q4 | **True current artifact state** — committed `dist/` has 43 `UNKNOWN:*` placeholders + 143 undefined terms, but the report's diagrams are clean | 🔴 | Determines what we can honestly claim; is there a newer Turtle? | _pending_ |

## Round 2 — scope & contribution
| # | Aspect | Conf. | Answer |
|---|--------|-------|--------|
| Q5 | **Contribution scope**: ontology only, or ontology + KGQA pipeline + authoring webapp? | 🟠 | _pending_ |
| Q6 | **HCMO vs MAPP branding** — title/abstract should foreground which? | 🟠 | _pending_ |
| Q7 | **Novelty / competitors** — are there existing HCM ontologies to position against? | 🔴 | _pending_ |
| Q8 | **Real datasets** — any HCM datasets / vendor exports to demonstrate reuse & mapping? | 🔴 | _pending_ |

## Round 3 — evaluation evidence
| # | Aspect | Conf. | Answer |
|---|--------|-------|--------|
| Q9 | **Competency-question SPARQL** — do runnable CQs against the MAPP terms exist (repo's return 0 rows)? | 🔴 | _pending_ |
| Q10 | **Quality reports** — have OOPS!/FOOPS!/reasoner/SHACL been run? results available? | 🔴 | _pending_ |
| Q11 | **Counts to report** — confirm ~45 classes / ~46 props / 6 reused classes / 17 reused props / 12 prefixes vs repo | 🟠 | _pending_ |
| Q12 | **Reused vocabularies in V1** — report: SOSA, OWL-Time, UO; repo also: PROV, BFO, schema, semts. Which are real vs roadmap? | 🟠 | _pending_ |

## Round 4 — availability & sustainability
| # | Aspect | Conf. | Answer |
|---|--------|-------|--------|
| Q13 | **SPARQL endpoint** — will one be provided (CfP values LOD/API availability)? | 🟠 | _pending_ |
| Q14 | **Governance & maintenance** — maintainer, release cadence, role of COST TEATIME network | 🟠 | _pending_ |
| Q15 | **w3id PURL** — does the redirect resolve today? (availability hard gate) | 🟠 | _pending_ |
| Q16 | **Author affiliations + missing ORCIDs** (Gilbert, Sanou, Sonfack, Tofano) | 🟠 | _pending_ |

## Change log
| Date | Round | Outcome |
|------|-------|---------|
| 2026-06-29 | — | Backlog created from Gilbert 2026 report + repo cross-check. |
