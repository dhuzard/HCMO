# HCMO Resource Paper — TODO & change tracking

**Status legend:** ☐ todo · ◐ in progress · ☑ done · ⚠ blocked
**Last updated:** 2026-06-29

This is the single source of truth for paper progress. Update the **status**
column and append to the **Change log** whenever something moves.

---

## Phase 0 — Decide & set up

| ID | Task | Owner | Status | Notes |
|----|------|-------|--------|-------|
| T0 | **🔴 BLOCKER (awaiting author): commit the clean V1 artifact** — Damien will provide the diagrams.net/Chowlk + exported Turtle (HITL R2) | Damien → Claude | ⚠ | Repo `dist/` is an old, broken export — see `AUDIT.md`. Everything depends on this. |
| T1 | ~~Lock venue~~ → **ESWC 2027 Resources Track, 15 pp** (HITL R1) | — | ☑ | Re-confirm dates/template when CfP opens. |
| T2 | **Create the w3id PURL redirect** (CHANGELOG says it's not set up yet) so the ontology IRI dereferences | — | ☐ | **Availability hard gate** — submit a PR to perma-id/w3id.org. |
| T3 | Create Overleaf project from **LNCS** template; mirror `sections/` | — | ☐ | Keep authors **named** (single-anonymous). |
| T3b | **Re-modularise** ontology to **bio/housing/env/tech** (HITL R1) | — | ☐ | Repo currently core/bio/env/obs. |

## Phase 1 — Make the resource paper-ready (ontology work)

> These are prerequisites: the paper can only claim quality the artifact has.

| ID | Task | Status | Notes |
|----|------|--------|-------|
| T4 | Replace/remove **Chowlk placeholders** (`UNKNOWN:*`, `ns:Class2`, `ns:objectProperty`, `xsd:boolean/integer` as properties) | ☐ | 43 terms. See `docs/MISSING-DEFINITIONS.md`. |
| T5 | Add **labels + `rdfs:comment`/IAO definitions** for all terms | ☐ | 143 terms lack comments; 1 lacks a label. |
| T6 | **Re-author SHACL shapes, examples & competency queries** against the clean V1 term set | ☐ | Currently legacy → CQs return 0 rows. |
| T6b | **Host a public SPARQL endpoint** (HITL R3) | ☐ | Strongest availability story; depends on T0. |
| T7 | Write **lab-maintained** governance/versioning policy (Huzard team, GitHub, SemVer+versionIRI; TEATIME = feedback channel) | ☐ | HITL R3. Feeds §7. |
| T7b | **Drop MAPP branding** in paper docs (done) + reconcile repo branding (`hcmo.yaml` title, README) separately | ◐ | HITL R3. Repo rename is a bigger change — confirm before touching core files. |
| T8 | Run **quality evaluation**: OOPS!, FOOPS! (FAIR), reasoner (HermiT/ELK), pySHACL, CQ results — archive reports | ☐ | Evidence for §Evaluation. |
| T9 | Cut a **tagged release** (e.g. `v0.x`) + refreshed Zenodo DOI matching the paper | ☐ | Canonical citation. |

## Phase 2 — Write the paper

| ID | Section | File | Status |
|----|---------|------|--------|
| T10 | Abstract + resource-metadata block | `metadata/resource-metadata.md`, `sections/00-abstract.md` | ☐ |
| T11 | Introduction & motivation — **drafted** (Gilbert 2026) | `sections/01-introduction.md` | ☑ |
| T12 | Related work — **drafted** (OBI/OLAM/MEDO/ARRIVE positioned) | `sections/02-related-work.md` | ☑ |
| T13 | Requirements & competency questions — **drafted** (R1–R8 + CQ1–CQ6; results deferred T6) | `sections/03-requirements.md` | ☑ |
| T14 | Resource description (modules, classes/properties, standards reuse) | `sections/04-resource.md` | ☐ |
| T15 | Engineering & availability (build, CI, manifest, FAIR, license, PURL/DOI) | `sections/05-availability.md` | ☐ |
| T16 | Evaluation (OOPS!/FOOPS!/reasoner/SHACL/CQs + completeness) | `sections/06-evaluation.md` | ☐ |
| T17 | Impact, use cases & sustainability (KGQA, webapp, vendor mapping, 3Rs/welfare) | `sections/07-impact.md` | ☐ |
| T18 | Conclusion & future work (limitations stated honestly) | `sections/08-conclusion.md` | ☐ |
| T19 | Figures: architecture, ontology overview (WebVOWL), example ABox graph | `figures/` | ☐ |
| T20 | Bibliography | `references.bib` | ☐ |

## Phase 3 — Polish & submit

| ID | Task | Status |
|----|------|--------|
| T21 | Complete **CALL-REQUIREMENTS.md** checklist — all ✔ | ☐ |
| T22 | Internal review pass (co-authors) + proofread, page-count check | ☐ |
| T23 | Confirm affiliations + ORCIDs of all 7 authors (Gilbert lead, Huzard corresponding — see `metadata/authors.md`) | ☐ |
| T24 | Submit **abstract** by pre-submission deadline | ☐ |
| T25 | Submit **full paper** (+ supplementary material link) | ☐ |

---

## Change log

| Date | Change | By |
|------|--------|----|
| 2026-06-29 | Created paper folder, requirements checklist, outline, section stubs, metadata block. | Claude |

<!-- Append new rows above this line. One row per meaningful change/decision. -->
