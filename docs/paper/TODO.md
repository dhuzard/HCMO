# HCMO Resource Paper — TODO & change tracking

**Status legend:** ☐ todo · ◐ in progress · ☑ done · ⚠ blocked
**Last updated:** 2026-07-09

This is the single source of truth for paper progress. Update the **status**
column and append to the **Change log** whenever something moves.

---

## Phase 0 — Decide & set up

| ID | Task | Owner | Status | Notes |
|----|------|-------|--------|-------|
| T0 | **Clean ontology artifact for paper/release** — v2 draft now exists in `ontology/v2/`; official promotion still waits on co-author sign-off and cleanup gates. | Damien/Cyril/Codex | ◐ | `ontology/v2/` is the reviewed path forward. Live `ontology/modules/`, `dist/`, shapes/examples/queries still point to the old export until promotion. |
| T1 | ~~Lock venue~~ → **ESWC 2027 Resources Track, 15 pp** (HITL R1) | — | ☑ | Re-confirm dates/template when CfP opens. |
| T2 | ~~Create the w3id PURL redirect~~ → **live**: `https://w3id.org/hcmo/ontology/hcm#` resolves (303 → docs site) | — | ☑ | **Availability hard gate cleared.** [w3id PR #6261](https://github.com/perma-id/w3id.org/pull/6261) merged 2026-06-30; verified 2026-07-03. Re-check with the paper-matching release (T9). |
| T2b | **Update w3id for the promoted v2 ontology** while keeping the base ontology IRI stable. | — | ☐ | After v2 promotion/release, update the perma-id redirect/content negotiation targets to the v2 documentation and distributions; do not re-mint term IRIs. |
| T3 | Create Overleaf project from **LNCS** template; mirror `sections/` | — | ☐ | Keep authors **named** (single-anonymous). |
| T3b | **Re-modularise** to the **DECIDED** R5 shape (2026-07-03): **5 modules — `hcm` core = enclosure only · `bio` · `obs` (observations + results) · `env` · `tech`**. `HousingAssignment` → bio (out of obs); `EnclosureDimensions` → core; all result/value classes → obs; `Sensor/Hardware/Software/TimeSeries` → new `tech` (`…/hcm/tech#`). Supersedes bio/housing/env/tech. | — | ◐ | **Draft built and lightly cleaned in `ontology/v2/`** (parallel, not yet wired to build/CI). Commits `d1fd21e` + `3fc46a4` apply co-author-review cleanup and figure-label alignment. Awaiting Damien validation before replacing `ontology/modules/`. Spec: `docs/paper/MODULE-MAP.md`. |
| T3c | **Decide which module owns the bio↔obs linking properties** (Subject→observation vs Observation→subject). The two modules are mutually dependent; **accept the bio/obs cycle for V1 knowingly** (harmless in the merged graph; blocks strict `owl:imports` layering only). | — | ☑ | Decision applied in v2 and documented in `docs/ARCHITECTURE.md`/`MODEL.md`: subject-to-observation convenience links stay in `bio`; observation-to-subject semantics use SOSA `hasFeatureOfInterest` in `obs`. |

## Phase 1 — Make the resource paper-ready (ontology work)

> These are prerequisites: the paper can only claim quality the artifact has.

| ID | Task | Status | Notes |
|----|------|--------|-------|
| T4 | Replace/remove **Chowlk placeholders** (`UNKNOWN:*`, `ns:Class2`, `ns:objectProperty`, `xsd:boolean/integer` as properties) | ☑ | v2 active placeholders reduced from 32 to 0 on the review branch. Former ambiguous placeholders were mapped, restored from legacy precedent, or dropped/deferred with rationale in `docs/paper/PLACEHOLDER-MAP.md`. Co-author sign-off still needed before promotion. |
| T5 | Add **labels + `rdfs:comment`/IAO definitions** for all terms | ◐ | v2 now has `rdfs:comment` definitions for all 111 FOOPS-assessed terms; FOOPS `VOC4` passes. Live `ontology/modules/` still needs reconciliation/promotion, and co-authors should review definition wording. |
| T6 | **Re-author SHACL shapes, examples & competency queries** against the clean V1 term set | ☐ | Deferred after the 2026-07-06 meeting: SHACL waits until v2 terms are frozen/promoted; current shapes target legacy terms. |
| T6b | **Host a public SPARQL endpoint** (HITL R3) | ☐ | Strongest availability story; depends on T0. |
| T7 | Write **lab-maintained** governance/versioning policy (Huzard team, GitHub, SemVer+versionIRI; TEATIME = feedback channel) | ☐ | HITL R3. Feeds §7. |
| T7b | **Drop MAPP branding** in paper docs (done) + reconcile repo branding (`hcmo.yaml` title, README) separately | ◐ | HCMO branding applied to v2 ontology header and `version_rapport` figure sources. Live manifest/README/dist still need reconciliation at promotion. |
| T8 | Run **quality evaluation**: OOPS!, FOOPS! (FAIR), reasoner (HermiT/ELK), pySHACL, CQ results — archive reports | ◐ | Protege 5.6.9 opens `ontology/v2/hcmo-v2-merged-clean.owl`; HermiT passes with 38 named classes and 0 inconsistent classes. FOOPS v0.4.0 improved from 0.49444446 to 1.0 after metadata, definition, and logo fixes. OOPS! was rerun post-FOOPS on the 966-triple clean v2 artifact; P04/P08/P12/P34 are fixed. A 2026-07-15 public-artifact OOPS rerun on the 1926-triple clean v2 artifact reports no critical or important pitfalls: P11 and P22 are closed; only P13 remains for 8 inverses intentionally not asserted because OOPS classifies those candidate inverses as P05 critical. SHACL/CQ deferred until v2 promotion. See `docs/paper/PROTEGE-REASONER.md`, `docs/paper/FOOPS-REPORT-2026-07-09.md`, and `docs/paper/evaluation/OOPS-REPORT-2026-07-10.md`. |
| T9 | Cut a **tagged release** (e.g. `v0.x`) + refreshed Zenodo DOI matching the paper | ☐ | Canonical citation. |

## Phase 2 — Write the paper

| ID | Section | File | Status |
|----|---------|------|--------|
| T10 | Abstract — **drafted** (~190 w) + resource-metadata block ready | `metadata/resource-metadata.md`, `sections/00-abstract.md` | ☑ |
| T11 | Introduction & motivation — **drafted** (Gilbert 2026) | `sections/01-introduction.md` | ☑ |
| T12 | Related work — **drafted** (OBI/OLAM/MEDO/ARRIVE positioned) | `sections/02-related-work.md` | ☑ |
| T13 | Requirements & competency questions — **drafted** (R1–R8 + CQ1–CQ6; results deferred T6) | `sections/03-requirements.md` | ☑ |
| T14 | Resource description (modules, classes/properties, standards reuse) | `sections/04-resource.md` | ☐ |
| T15 | Engineering & availability — **drafted** (manifest, build, CI, FAIR, license, endpoint, governance; pending items marked) | `sections/05-availability.md` | ☑ |
| T16 | Evaluation (OOPS!/FOOPS!/reasoner/SHACL/CQs + completeness) | `sections/06-evaluation.md` | ☐ |
| T17 | Impact, use cases & outlook — **drafted** (reasoning, KGQA/authoring/vendor as outlook, TEATIME adoption) | `sections/07-impact.md` | ☑ |
| T18 | Conclusion & future work — **drafted** (honest limitations + roadmap) | `sections/08-conclusion.md` | ☑ |
| T19 | Figures: architecture, ontology overview (WebVOWL), example ABox graph | `figures/` | ◐ |
| T20 | Bibliography | `references.bib` | ☐ |

## Phase 3 — Polish & submit

| ID | Task | Status |
|----|------|--------|
| T21 | Complete **CALL-REQUIREMENTS.md** checklist — all ✔ | ☐ |
| T22 | Internal review pass (co-authors) + proofread, page-count check | ☐ |
| T23 | Confirm affiliations + ORCIDs of all 7 authors (Gilbert lead, Huzard corresponding — see `metadata/authors.md`) | ☐ |
| T23b | **Confirm the license with all co-authors** (CC BY 4.0 vs CC0 for an ontology) — currently asserted but unconfirmed. See OPEN-QUESTIONS Q19. Pre-submission gate. | ☐ |
| T24 | Submit **abstract** by pre-submission deadline | ☐ |
| T25 | Submit **full paper** (+ supplementary material link) | ☐ |

---

## Change log

| Date | Change | By |
|------|--------|----|
| 2026-07-15 | **OOPS public rerun** — added legacy-backed disjointness, symmetric `communicatesWith`, normalized v2 environmental property names, and completed conservative domain/range axioms; HermiT and repo validation pass on the 1926-triple clean v2 artifact; public OOPS rerun reports no critical or important pitfalls, with only P13 8 minor archived. | Codex |
| 2026-07-09 | **FOOPS logo metadata closed** — added `HCMO-logo3.png` to the README and `schema:logo` to the v2 ontology header; regenerated v2 artifacts and FOOPS now scores 1.0 on the clean OWL artifact. | Codex |
| 2026-07-10 | **OOPS post-FOOPS evaluation archived** — rebased the OOPS evaluation branch on the FOOPS/logo `main`, corrected safe OOPS findings, added conservative domain/range and union-domain axioms, reran OOPS on the 966-triple clean v2 artifact, and archived the XML plus a triaged Markdown report. | Codex |
| 2026-07-09 | **FOOPS VOC4 definition gap closed for v2** — added conservative `rdfs:comment` definitions to all 111 FOOPS-assessed v2 terms, regenerated v2 artifacts, and raised FOOPS from 0.92222226 to 0.9888889; only logo metadata remains. | Codex |
| 2026-07-09 | **FOOPS FAIR assessment applied to v2** — ran FOOPS v0.4.0 on `ontology/v2/hcmo-v2-merged-clean.owl`, raised the score from 0.49444446 to 0.92222226 by adding ontology-header metadata, regenerated v2 artifacts, and archived baseline/post-fix reports. | Codex |
| 2026-07-09 | **Checklist/RDF intake update** — mirrored the merged HermiT + placeholder status, added FOOPS! and the w3id-v2 follow-up to tracking, made form Turtle emit explicit `rdf:type`, and added a DVC profile ABox organized as class, object-property, and literal triples. | Codex |
| 2026-07-09 | **Applied final v2 placeholder cleanup** — replaced the remaining active v2 `UNKNOWN:` placeholders with proposed module terms or existing relations, regenerated v2 merged/clean artifacts, and confirmed HermiT still reports 0 inconsistent classes. | Codex |
| 2026-07-09 | **Placeholder decision proposal** — expanded `PLACEHOLDER-MAP.md` with recommended actions for the 7 remaining v2 `UNKNOWN:` placeholders, including confidence levels and rationale grounded in v2 modules and legacy HCMO precedent. | Codex |
| 2026-07-09 | **Figure placeholder alignment** — refreshed `version_rapport.drawio` and `.drawio.xml` labels again after the final cleanup, so the diagram no longer presents active v2 `UNKNOWN:` placeholders. | Codex |
| 2026-07-08 | **Protege Desktop open check** — installed Protege 5.6.9 portable, opened `ontology/v2/hcmo-v2-merged-clean.owl`, and recorded successful ontology/imports-closure loading from the Protege log; only network auto-update/cache warnings observed. | Codex |
| 2026-07-08 | **Clean v2 reasoner automation** — added reproducible HermiT tooling/CI for `hcmo-v2-merged-clean.owl`, regenerated clean BioPortal files from modules, and confirmed consistency; post-cleanup result at that point was 33 classes loaded with 0 inconsistent classes. | Codex |
| 2026-07-06 | **Meeting follow-up** — main is now the working branch; Cyril task captured as Protege reasoner check on v2, with SHACL deferred until v2 terms are frozen/promoted. | Codex |
| 2026-07-06 | **Protege pre-check** — parsed v2 merged TTL and recorded OWL typing sanity checks; no obvious restriction/property typing errors found, with `hcm:Enclosure`, OWL-Time beginning/end, and `hasCondition` flagged for manual Protege inspection. | Codex |
| 2026-07-06 | **Protege debug pass** — restored `hcm:Enclosure` as a class from legacy HCMO and corrected OWL-Time `hasBeginning`/`hasEnd` to object properties. | Codex |
| 2026-07-06 | **Protege notes cleanup** — marked environmental measured-property terms as intentionally object properties per `MODULE-MAP.md`; kept `hasCondition` as the main unresolved modeling check. | Codex |
| 2026-07-06 | **HermiT reasoner pass** — ran HermiT through `owlready2` on the v2 merged TTL converted to RDF/XML; 31 classes loaded, 0 inconsistent classes. | Codex |
| 2026-07-06 | **T4 tech support pass** — minted `UNKNOWN:supportsEnclosure` as `hcm-tech:supportsEnclosure`; reclassified `hasCondition` as an observation-condition modeling decision rather than an env literal; normalized remaining relation-like placeholders to `owl:ObjectProperty`. | Codex |
| 2026-07-06 | **T4 core facility pass** — minted safe core placeholders as `hcm:*` (`hasEnrichmentType`, `hasFacilityType`, `hasFloorArea`, food/water/safety requirements); left requirement-object, part-whole, generic type, and ambiguous tech relations deferred. | Codex |
| 2026-07-06 | **T4 bio pass** — minted `UNKNOWN:hasSocialReq` as `hcm-bio:hasSocialRequirement`; no bio placeholders remain. | Codex |
| 2026-07-06 | **T4 env pass** — minted light-cycle placeholders as `hcm-env:*` (`hasDarkPhaseStart`, dark/light phase durations, dawn/dusk durations); kept generic `hasCondition` deferred. | Codex |
| 2026-07-06 | **T4 tech pass** — minted obvious tech placeholders as `hcm-tech:*` (`communicatesWith`, `runsOn`, firmware/model/protocol/sensor metadata, calibration), leaving only ambiguous tech relations in the placeholder queue. | Codex |
| 2026-07-03 | **T4 started** — resolved safe v2 placeholder cases: `UNKNOWN:isOccupied` → `hcm:isOccupied`, `UNKNOWN:isOperational` → new `hcm:isOperational`, and duplicate `UNKNOWN:hasSamplingRate` dropped in favour of `hcm-tech:hasSamplingRate`. Added `PLACEHOLDER-MAP.md` for the remaining 29 placeholders. | Codex |
| 2026-07-03 | **T3c closed** — documented the accepted `bio`↔`obs` cycle and ownership rule: subject-side observation links live in `bio`; observation classes/results and SOSA feature-of-interest semantics live in `obs`. | Codex |
| 2026-07-03 | **Figure source labels refreshed** — `version_rapport.drawio`, `.drawio.xml`, and source TTL now use HCMO branding and `LocationResultTable`; only labels/IRIs were touched, not diagram structure. | Codex |
| 2026-07-03 | **v2 cleanup pass after co-author review** — HCMO branding applied to the v2 ontology header; `LocationResultTable` legacy label fixed; relation-like properties corrected from datatype to object properties; obvious Chowlk-inherited wrong-direction restrictions removed or retargeted. v2 modules + merged TTL parse with rdflib. | Codex |
| 2026-07-03 | **v2 draft built** — re-modularised 5-module ontology generated in `ontology/v2/` (parallel; live `ontology/modules/` untouched). `Structural&LocationTable`→`LocationResultTable`. All files parse; sanity checks pass. Awaiting co-author validation before promotion. | Claude |
| 2026-07-03 | **MODULE-MAP.md finalised** — all 7 term-placement micro-decisions resolved (StudyFactors→bio, TimeSeries→tech, dim-props→core, hasUnit→QUDT/OM, manufacturer/version split, monitoredBy/installedIn→tech, OWL-Timeintervaltable dropped). Spec is now implementation-ready for T3b. No ontology code changed yet. | Claude |
| 2026-07-03 | **Module shape FINALISED (R5)**: 5 modules — hcm core = **enclosure only** / bio / obs (observations+results) / env / **tech** (own module). HousingAssignment → bio; EnclosureDimensions → core; all results → obs. Q19/Q20 resolved; Q21 (QUDT/OM) open. Spec → `MODULE-MAP.md`. No ontology code changed yet. | Claude |
| 2026-07-03 | **Module shape proposed (R5)**: initial enclosure+tech+results core; superseded same day by the finalised 5-module shape above. | Claude |
| 2026-07-03 | **T23b added** — open license question (Q19): confirm CC BY 4.0 vs CC0 with all co-authors before submission. | Claude |
| 2026-07-03 | Updated ontology header attribution — all 7 co-authors now carry ORCID IRIs (Sonfack Sounchio, Toffano, Gilbert, Sanou added); rebuilt `dist/`. Feeds WIDOCO docs. | Claude |
| 2026-07-03 | **T2 done** — w3id PURL `https://w3id.org/hcmo/ontology/hcm#` verified live (303 → docs site); availability hard gate cleared. Updated OPEN-QUESTIONS Q15, §5 availability, FAIR table. | Claude |
| 2026-06-29 | Created paper folder, requirements checklist, outline, section stubs, metadata block. | Claude |

<!-- Append new rows above this line. One row per meaningful change/decision. -->
