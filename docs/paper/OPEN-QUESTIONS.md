# HITL improvement loop — open questions backlog

Purpose: aspects of the resource paper I am **< 90% confident** about. Each is
asked to the author in batched rounds (human-paced loop). Answers are applied to
the relevant doc and logged in `TODO.md`.

**Confidence legend:** 🔴 low (<60%) · 🟠 medium (60–90%) · 🟢 resolved (≥90%)
**Last updated:** 2026-06-29

## Round 1 — foundational ✅ RESOLVED (2026-06-29)
| # | Aspect | Conf. | Answer |
|---|--------|-------|--------|
| Q1 | Target venue + cycle | 🟢 | **ESWC 2027, Resources Track, 15 pp + unlimited refs.** |
| Q2 | Track | 🟢 | **Resources Track** (not In-Use). |
| Q3 | Canonical module structure | 🟢 | **bio/housing/env/tech** (report) → repo must be re-modularised (T3b). |
| Q4 | True current artifact state | 🟢 | **Needs audit → done.** Repo `dist/` is an OLD broken Chowlk export (143 terms, 0 defs, 43 placeholders); the report's clean V1 is **not committed**. See `AUDIT.md`. New blocker **T0**: obtain & commit the clean source. |

## Round 2 — scope & contribution ✅ RESOLVED (2026-06-29)
| # | Aspect | Conf. | Answer |
|---|--------|-------|--------|
| Q5a | Clean V1 source (blocker T0) | 🟢 | **Damien will provide** the diagrams.net/Turtle; Claude commits it. |
| Q5 | Contribution scope | 🟢 | **Ontology + SHACL + CQs + JSON-LD + examples only.** KGQA/webapp/vendor = outlook in §7. |
| Q7 | Novelty / competitors | 🟢 | **HCMO is first / none known.** Compare to SOSA/SSN + adjacent biomedical ontologies. (Can verify via LOV/BioPortal on request.) |
| Q8 | Real datasets | 🟢 | **Via TEATIME network** (needs coordination). Build synthetic ABoxes now; TEATIME data = validation path. |

> Q6 (HCMO vs MAPP branding) deferred to Round 3.

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
| 2026-06-29 | R1 | Resolved Q1–Q4: ESWC 2027 Resources, 15 pp, bio/housing/env/tech; audit done → AUDIT.md, blocker T0. |
| 2026-06-29 | R2 | Resolved Q5a/Q5/Q7/Q8: author provides clean V1; scope = ontology package only; HCMO is first; data via TEATIME (synthetic now). Applied to §1/§2/§7. |
