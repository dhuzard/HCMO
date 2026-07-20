# HITL improvement loop — open questions backlog

Purpose: aspects of the resource paper I am **< 90% confident** about. Each is
asked to the author in batched rounds (human-paced loop). Answers are applied to
the relevant doc and logged in `TODO.md`.

**Confidence legend:** 🔴 low (<60%) · 🟠 medium (60–90%) · 🟢 resolved (≥90%)
**Last updated:** 2026-07-20

## Round 1 — foundational ✅ RESOLVED (2026-06-29)
| # | Aspect | Conf. | Answer |
|---|--------|-------|--------|
| Q1 | Target venue + cycle | 🟢 | **ESWC 2027, Resources Track, 15 pp + unlimited refs.** |
| Q2 | Track | 🟢 | **Resources Track** (not In-Use). |
| Q3 | Canonical module structure | 🟢 | **Five active modules: core/bio/env/obs/tech**, plus a migration-only compatibility module. Promoted in HCMO 0.2.0. |
| Q4 | True current artifact state | 🟢 | **Audit and remediation complete.** The old Chowlk export is archived; the reviewed model is active in `ontology/modules/`. See `AUDIT.md`. |

## Round 2 — scope & contribution ✅ RESOLVED (2026-06-29)
| # | Aspect | Conf. | Answer |
|---|--------|-------|--------|
| Q5a | Clean V1 source (blocker T0) | 🟢 | **Provided, reviewed, and promoted.** T0 is closed in HCMO 0.2.0. |
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

## Round 4 — authorship, novelty, availability ✅ RESOLVED (2026-06-29)
| # | Aspect | Conf. | Answer |
|---|--------|-------|--------|
| Q15 | w3id PURL redirect resolves today? (availability hard gate) | 🟢 | **YES — resolved.** `https://w3id.org/hcmo/ontology/hcm#` returns 303 → docs site (verified 2026-07-03; w3id PR #6261 merged 2026-06-30). **T2 done.** |
| Q16 | Authorship / order | 🟢 | **Gilbert first author; Todorov & Huzard co-lead / co-corresponding (contact).** TEATIME = acknowledgement. See `metadata/authors.md`. |
| Q17 | Affiliations + missing ORCIDs | 🟠 | **ORCIDs provided** (2026-06-29) → CITATION.cff, README, authors.md; names fixed (Sonfack **Sounchio**, To**ff**ano). **Affiliations still pending.** Fold ORCIDs into V1 ontology header at T0. |
| Q18 | Novelty verification | 🟢 | **Search run** → no HCM ontology exists; adjacents = OBI/OLAM/MEDO + ARRIVE. See `NOVELTY.md`; applied to §2. |

## Round 5 — ontology architecture ◐ (Q19–Q20 RESOLVED 2026-07-03 · Q21 open)
| # | Aspect | Conf. | Decision / status |
|---|--------|-------|-------------------|
| Q19 | Should `tech` be its own module? Device layer (Sensor / Hardware / Software / TimeSeries + all sensor properties). | 🟢 | **YES — full `tech` module ("for now").** Final shape: **5 modules `hcm` core · `bio` · `obs` · `env` · `tech`.** Quarantines the 34 `UNKNOWN:` tech placeholders; mirrors SOSA/SSN's Observation ‖ System split; matches report fig10. `Sensor/Hardware/Software/TimeSeries` IRIs move `…/hcm#` → `…/hcm/tech#` **before** the T9 release. |
| Q20 | Where do results live? (Decision 0 vs 1 conflict.) | 🟢 | **Drop results from core entirely → `core = enclosure only`; all result/value classes (`ObservationResult`, `QuantityValue`, `CategoricalResult`, `Structural&LocationTable`) move to `obs`.** Reference scan confirmed: once Chowlk cruft (`MonitoredEnclosure ⊑ ObservationResult`) is cleaned, all result usage is obs-internal → zero cross-module edges. Core reduces to the single hub concept: **MonitoredEnclosure**. |
| Q21 | Adopt **QUDT/OM** for units & quantities? | 🟠 | **Roadmap decision, not implemented in 0.2.0.** The release consolidates unit strings under `hcm:hasUnit`; the choice of QUDT vs OM and the quantity-value pattern still require review. |

## Formerly parked — resolved or narrowed after promotion
| # | Aspect | Conf. | Answer |
|---|--------|-------|--------|
| Q9 | Runnable competency-question SPARQL against the active terms | 🟠 | Five queries execute on 0.2.0, but expected-answer tests over ontology-plus-example data remain to be added. |
| Q10 | OOPS!/FOOPS!/reasoner/SHACL reports run? | 🟢 | HermiT and SHACL pass on 0.2.0; OOPS!/FOOPS! evidence is archived from the promoted v2 lineage and must be rerun on the final paper-matching release. |
| Q11 | Confirm release counts | 🟢 | Active modules: 29 classes, 32 object properties, 49 datatype properties. Full graph with compatibility: 56/57/73 and 1,252 triples. |

## Change log
| Date | Round | Outcome |
|------|-------|---------|
| 2026-06-29 | — | Backlog created from Gilbert 2026 report + repo cross-check. |
| 2026-06-29 | R1 | Resolved Q1–Q4: ESWC 2027 Resources, 15 pp, bio/housing/env/tech; audit done → AUDIT.md, blocker T0. |
| 2026-06-29 | R2 | Resolved Q5a/Q5/Q7/Q8: author provides clean V1; scope = ontology package only; HCMO is first; data via TEATIME (synthetic now). Applied to §1/§2/§7. |
| 2026-06-29 | R3 | Resolved Q6/Q12/Q13/Q14: drop MAPP; all vocabs real; host SPARQL endpoint; lab-maintained. Applied to README/OUTLINE/§00/§04/§05/§07; T6b/T7/T7b added. Q9–Q11 parked on T0. |
| 2026-06-29 | R4 | Resolved Q15/Q16/Q17/Q18: Gilbert lead + Huzard corresponding (authors.md); affiliations later; w3id redirect missing (T2); novelty search done (NOVELTY.md, §2). Q9–Q11 remain parked on T0 (author: V1 in days). |
| 2026-07-03 | — | **Q15 closed**: w3id PURL verified live (303 → docs site); T2 done, availability hard gate cleared. |
| 2026-07-03 | R5 | **Ontology architecture opened (to vote)**: Q19 tech-as-own-module (suggest YES → 5 modules), Q20 results placement (suggest core = enclosure only, results → obs). Cross-ref TODO T3b/T3c. |
| 2026-07-03 | R5 | **Q19 + Q20 RESOLVED**: tech = own module (5 modules); results dropped from core (core = enclosure only, all results → obs). **Q21 opened**: adopt QUDT/OM for units — to discuss. Final shape recorded in TODO T3b. |
| 2026-07-03 | R5 | **7 micro-decisions resolved** (`MODULE-MAP.md` §6): StudyFactors→bio, TimeSeries→tech, dim-props→core, hasUnit→QUDT/OM (**Q21 units decided**), manufacturer/version split, monitoredBy/installedIn→tech, OWL-Timeintervaltable dropped. Spec now implementation-ready. |
