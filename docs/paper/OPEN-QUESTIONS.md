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

## Round 3 — branding, vocab, availability, governance ✅ RESOLVED (2026-06-29)
| # | Aspect | Conf. | Answer |
|---|--------|-------|--------|
| Q6 | HCMO vs MAPP branding | 🟢 | **Drop MAPP** — use HCMO only in the paper (repo reconcile = T7b). |
| Q12 | Reused vocabularies in V1 | 🟢 | **All real**: SOSA/SSN, OWL-Time, UO, PROV, BFO, schema, semts. |
| Q13 | SPARQL endpoint | 🟢 | **Yes — will host one** (T6b). |
| Q14 | Governance/maintenance | 🟢 | **Lab-maintained** (Huzard team, GitHub); TEATIME = feedback channel. |

## Round 4 — artifact-dependent (PARKED until clean V1 arrives, T0)
| # | Aspect | Conf. | Answer |
|---|--------|-------|--------|
| Q9 | Runnable competency-question SPARQL against the V1 terms | 🔴 | _parked: needs T0 artifact_ |
| Q10 | OOPS!/FOOPS!/reasoner/SHACL reports run? | 🔴 | _parked: needs T0 artifact_ |
| Q11 | Confirm counts (~45 classes / ~46 props / 6 reused / 17 reused / 12 prefixes) | 🟠 | _parked: verify against T0 artifact_ |
| Q15 | w3id PURL redirect resolves today? (availability hard gate) | 🟠 | _to verify (T2) — actionable without author_ |
| Q16 | Author affiliations + missing ORCIDs (Gilbert, Sanou, Sonfack, Tofano) | 🟠 | _pending (next round)_ |

## Change log
| Date | Round | Outcome |
|------|-------|---------|
| 2026-06-29 | — | Backlog created from Gilbert 2026 report + repo cross-check. |
| 2026-06-29 | R1 | Resolved Q1–Q4: ESWC 2027 Resources, 15 pp, bio/housing/env/tech; audit done → AUDIT.md, blocker T0. |
| 2026-06-29 | R2 | Resolved Q5a/Q5/Q7/Q8: author provides clean V1; scope = ontology package only; HCMO is first; data via TEATIME (synthetic now). Applied to §1/§2/§7. |
| 2026-06-29 | R3 | Resolved Q6/Q12/Q13/Q14: drop MAPP; all vocabs real; host SPARQL endpoint; lab-maintained. Applied to README/OUTLINE/§00/§04/§05/§07; T6b/T7/T7b added. Q9–Q11 parked on T0. |
