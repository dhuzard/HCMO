# ISWC Resources Track — manuscript sync, comment resolution, and migration plan

Date: 2026-09-24 · Owner: Damien · Status: **sync, comment pass, and first
migration pass done (§8); co-author review of the migrated draft pending.**

Decisions this plan implements (see
[`../meetings/CO-AUTHOR-EMAIL-REPLIES-2026-09-24.md`](../meetings/CO-AUTHOR-EMAIL-REPLIES-2026-09-24.md) §4.1):
D1 restructure, D2 "2 × 2 factorial design with repeated measures", D3
additional co-author. Target venue: **ISWC Resources Track** (was ESWC 2027 in
[`CALL-REQUIREMENTS.md`](CALL-REQUIREMENTS.md)).

---

## 1. Which version is the most advanced — sync record

Three versions of `docs/paper/overleaf/` existed:

| Version | Source | What it had |
| --- | --- | --- |
| **Base** | `HCMO.zip` (online project, 2026-09-04) *(archive since removed from the repository tree; kept in git history)* | Last common ancestor of the other two. |
| **Online** | `HCMO (1).zip` (online project, exported 2026-09-24) *(archive since removed from the repository tree; kept in git history)* | All co-author edits since 4 Sept: rewritten abstract, Olog/Bains related-work text, methodology moved into §3, representative CQ instead of the CQ table, resource statistics table, OOPS!/FOOPS!/AskWol citations and links, 7-module manifest wording, adoption caveat, authors with ORCIDs and full affiliations, updated CRediT (adds Philippe Rocca-Serra and Benoit Girard), updated acknowledgements, `todonotes` review comments, `\new{}` change-marking macro. |
| **Repo** | `HEAD` of this branch | Repo-only work never uploaded online: redesigned Figure 3, new Figure 4 (evidence layers), links to the fixture CSV/result files and `native-isa/`, OBI/STATO boundary sentence in §4, "authoritative PLMLatex" README. |

**Neither was a superset.** Online is the more advanced *manuscript*; repo is
the more advanced *figures and evidence links*. A three-way merge
(`git merge-file`, base = 4 Sept export) was applied per file:

- 12 of 15 files merged cleanly; 4 conflicts in 3 files were resolved by hand:
  - `main.tex` CRediT → **online** version (co-author edits), with `–`/`&`
    fixed to `--`/`\&` (the bare `&` would not compile) and CRediT role
    capitalisation normalised.
  - `main.tex` INITIUM thanks → **online** (adds Noelline Meslin).
  - `figures/f3.tex` caption → **repo** redesigned caption, prefixed with the
    D2 wording.
  - `sections/06-evaluation.tex` → **online** text (CQ table replaced by the
    representative question) **plus** the repo's data/fixture links, with the
    online draft's duplicated "2 × 2 … 2 × 2" phrase replaced by the D2 wording.
- `figures/f4.tex` exists only in the repo and is kept; the online project
  must receive it on the next upload.
- The repo README (PLMLatex is authoritative) is kept; the online README was
  stale.

Result: merged sources are in `docs/paper/overleaf/`, and
`docs/paper/hcmo-overleaf-upload.zip` was rebuilt with `tooling/build_paper.py`
(byte-reproducible on re-run). **Upload this zip to the online project before
anyone edits again**, otherwise figures 3–4 and the data links will be lost
there.

Compile check (TeX Live, `texlive/texlive:latest` Docker image, `latexmk -pdf`):
**no errors, no undefined references or citations, 22 pages** — sections 1–8
end on p. 17, back matter pp. 18–20, references from p. 20. Four minor
overfull boxes.

## 2. Review comments — resolution log

| # | Where | Comment | Resolution |
| --- | --- | --- | --- |
| 1 | §1 ¶1 | GS: "provide" → "capturing??" | **Fixed:** "Such protocols capture only a narrow window …" |
| 2 | §1 ¶3 | PRS: s/producing/relying/ | **Fixed:** "while relying on very different sensors …" |
| 3 | §1 contributions | PRS: "what about the separation with bio or env?" | **Fixed:** added "and keeps the monitored subject (bio) and its environmental conditions (env) distinct from the observations made about them (obs)". Matches the model: subjects are features of interest, `hcm-env:EnvironmentalProperty ⊑ sosa:ObservableProperty`, observations live in obs. |
| 4 | §1 contributions | KT: "all of the above are the contributions" | **Already done online** ("These four elements constitute the contributions"); note removed. |
| 5 | §1 end | KT: paper-structure paragraph + TEATIME link | **Already done online** (roadmap paragraph + footnote); note removed. The roadmap must be rewritten after migration. |
| 6 | §1 ¶5 | PRS: "featuring or characterised by?" + flow: move HCMO presentation to results, set the scene with SOSA/PROV/BFO/OBI and TEATIME earlier | **Resolved by migration:** TEATIME and its WG2 definition are introduced in §1 ¶4; the HCMO description moved to §4; the sentence now reads "which formalises HCM as an integrated system … Its contributions are:". |
| 7 | §2 | KT: "Standards reused" and "Ontology engineering" don't fit related work | **Resolved by migration:** both are now in §3 Methodology ("Development process"; "Selecting and reusing external resources"). |
| 8 | §3 | PL: one CQ in the manuscript, the rest in annex/GitHub | **Already done online** (representative CQ + pointer); note removed. |
| 9 | §4 | KT: missing statistics table and access links | **Already done online** (Table 1, values verified against `dist/profile.json`: 1,397 triples, 60 classes, 68 object and 75 datatype properties, 11 CQs). "Ratio of reused vocabulary" still missing → added in migration (§5.3). |
| 10 | §5 | KT: figures 1 and 2 not referenced | **Already done online** (refs to `fig:pipeline`, `fig:domain-model`, `fig:roundtrip`); note removed. `fig:evidence-layers` was already referenced. |
| 11 | §6 | PL: "is the capital here OK?" (`bioschemas:Sample`, `schema:MediaObject`) | **Answered — yes.** Class names are UpperCamelCase; both are the exact types used in `examples/isa-roundtrip/ro-crate-metadata.json`. Notes removed. |
| 12 | §6 | PL: "do you mean competency questions?" | **Fixed** (the heading had lost its first word; repo already had "Competency questions"). |
| 13 | back matter | KT: Funding should be a short unnumbered Acknowledgements section after the conclusion | **Fixed:** conclusion → *Resource Availability Statement* (ISWC requirement, replaces "Supplementary material") → `\section*{Acknowledgements}` (Funding, provenance, non-author contributions) → CRediT → Competing interests. Still long; shortened in migration. |
| 14 | §7 | KT: quantitative adoption measures | **Closed (2026-09-24, Damien):** figures are too preliminary to report. The online caveat ("adoption is presented as a pathway rather than a demonstrated outcome") is kept; note removed. |
| 15 | §5 | `\reviewcomment` "À confirmer avec Gaoussou et Konstantin" (hosted SPARQL service) | **Kept open — question to Gaoussou/Konstantin.** |
| 16 | CRediT | (new) Benoit Girard has CRediT roles but is not in the author list and is still thanked as a non-author | **Resolved:** added as co-author after Larmande; removed from the acknowledgements. Affiliation and ORCID still to be supplied (placeholder institute). |

All my text changes are wrapped in `\new{}` so they show in blue while
`\reviewtrue` is set.

## 3. ISWC Resources Track requirements (provisional)

The ISWC 2027 call is not published (checked 2026-09-24). The ISWC 2024–2026
Resources Track rules have been stable and are used as the baseline;
re-verify against the 2027 call (expected deadline around early May 2027 —
ISWC 2026 used abstract 2 May / paper 7 May).

- **Length:** 15 pages **plus** unlimited references; over-length papers are
  rejected. LNCS, English. Single-anonymous (authors named).
- **Resource Availability Statement — mandatory**, desk-rejection risk.
  At the end of the paper, **before references and acknowledgements**, italic
  run-in heading (`\paragraph*{Resource Availability Statement:}`); **counts
  toward the 15 pages**. Must list every resource presented, where it is,
  and justify anything not available.
- **Three mandatory checks:** persistent URI (w3id ✔), canonical citation
  (CITATION.cff + DOI ✔ — the paper should state it), licence (CC BY 4.0 ✔).
- **Resource available at submission time** and reviewed alongside the paper.
- **Review criteria:** *Impact* (novelty, gap filled, **comparison with
  similar resources**, community interest, societal relevance); *Reusability*
  (**evidence of use by a wider community**, ease of reuse, extensibility,
  documentation, stated limitations); *Design & technical quality* (best
  practice, appropriate reuse, fitness for task, FAIR); *Availability*
  (access routes, **discoverability through registries**, sustainability
  plan, open standards).

Consequences for HCMO:

1. The ESWC "resource metadata block" after the abstract is not required by
   ISWC. Keep a two-line version (URL + DOI) or drop it; the availability
   statement now carries the full list.
2. A **comparison with similar resources** is expected. Add a compact table
   (HCMO vs TEATIME Olog, Bains et al. model, OBI, MEDO, OLAM, ARRIVE) in §2.
3. **Registry discoverability** is currently not evidenced. Register HCMO in
   at least one of LOV, BioPortal, OLS or FAIRsharing before submission, and
   cite the entry.
4. **Community-use evidence** is the weakest criterion (see comment 14).

## 4. Target structure and page budget

Seven numbered sections, per [`OUTLINE.md`](OUTLINE.md) and decision D1,
aligned to the four ISWC criteria. Budget is 15 pages including the
availability statement and the back matter.

| § | Section | Budget | ISWC criterion served |
| --- | --- | ---: | --- |
| — | Title, authors, abstract (≤ 200 words), 2-line URL/DOI | 0.8 | — |
| 1 | Introduction and motivation (TEATIME introduced here) | 1.2 | Impact |
| 2 | Related work and positioning (incl. comparison table) | 1.3 | Impact |
| 3 | Methodology (requirements, CQs, **resource-selection criteria**, engineering workflow, evaluation design) | 1.8 | Design quality |
| 4 | The HCMO resource (IRIs, statistics + reuse ratio, modules, key modelling decisions, reuse, distribution, docs, sustainability) | 3.2 | Design quality, Availability |
| 5 | Interoperability use case: the 2 × 2 factorial fixture with repeated measures | 1.7 | Reusability |
| 6 | Evaluation and potential impact | 2.3 | Design quality, Impact |
| 7 | Discussion, limitations, future work, conclusion | 1.0 | Reusability |
| — | Resource Availability Statement | 0.3 | Availability (mandatory) |
| — | Acknowledgements, CRediT, competing interests | 0.9 | — |
| | **Total before references** | **14.5** (0.5 reserve) | |

**Current length ≈ 19 pages before references → about 4 pages must go.**
Sources of the cut: ~1.5 p from removing repetition (§5.2), ~1 p from
compressing evaluation prose into tables, ~0.7 p from the back matter, ~0.5 p
from merging §§7–8, and ~0.3 p from the abstract/metadata block.

## 5. Migration map

### 5.1 Paragraph-level source → target

Paragraph references are `file:line` in `docs/paper/overleaf/sections/`.

| Current | → Target | Action |
| --- | --- | --- |
| `01:2` behavioural testing | §1 | Keep, trim ~20%. |
| `01:4` what HCM is, 3Rs, bias shift | §1 | Keep. |
| `01:6` heterogeneity, FAIR, ethics | §1 | Keep; ethics sentence also serves §6 impact (single mention here). |
| `01:8` why an ontology | §1 | Keep, shorten. |
| — | §1 | **New** 2–3 sentences introducing COST TEATIME and its Working Group 2 early (PRS #6). |
| `01:10–25` HCMO + four contributions | §1 | Keep the list; replace item 2's vocabulary inventory with one clause; move the outlook sentence to §7. |
| `01:27` roadmap | §1 | Rewrite for the new seven sections. |
| `02:4` HCM field, Bains, Forrest, WellFAIR | §2 | Keep. |
| `02:6–10` Olog and Bains model | §2 | Merge into one paragraph (the provenance detail — who led what — moves to Acknowledgements only). |
| `02:12` formalisation gap | §2 | Keep as the closing gap statement. |
| `02:15` standards reused (KT #7) | §3.3 | Becomes the start of the resource-selection subsection. |
| `02:17` OBI/OLAM/MEDO/ARRIVE | §2 | Keep; feeds the **new comparison table**. |
| `02:19` ISA/RO-Crate | §2 | One sentence of positioning; the conformance caveat moves to §5. |
| `03:2` development methodology | §3.1 | Keep. |
| `03:4` stakeholders | §3.1 | Keep, shorten. |
| `03:6–32` R1–R8 | §3.2 | Convert to a compact two-column table (requirement → where addressed); saves ~0.3 p. |
| `03:34` CQs | §3.2 | Keep the representative CQ; results stay in §6. |
| — | §3.3 | **New** resource-selection criteria (T20c) + reuse-kind distinction (metadata vs semantic reuse, T20l) + mapping-strength policy (`04:35` "claim strength"). |
| `04:2` IRIs | §4.1 | Keep. |
| `04:4–23` Table 1 | §4.1 | Keep; **add** reuse rows (§5.3). |
| `04:25` modular organisation | §4.2 | Keep; delete the duplicate in `05:6`. |
| `04:27–29` two boundaries | §4.3 | Keep — core modelling decisions. |
| `04:31,33` BFO/IAO/SOSA/QUDT reuse | §4.4 | Keep as the **single home** for the vocabulary inventory. |
| `04:35` claim strength | §3.3 | Move. |
| `04:37` SOSA 2017/SemTS | §4.4 | Keep. |
| `04:37` OBI/STATO/ISA and 2 × 2 fixture | §5 | Move. |
| `04:39` Fig. 4 evidence layers | §5 | Move with its paragraph. |
| `04:41` distribution and application support | §4.5 | Merge with `05:4,6` (manifest, reproducible build). |
| `04:43` active inventory counts (33 classes, 69 properties) | §4.1 | Reconcile with Table 1 (release vs active counts) in the caption; delete the paragraph. |
| `04:45` Fig. 2 domain model | §4.2 | Keep. |
| `05:2–8` package, manifest, build, CI | §4.5 | Merge, shorten ~40%; keep Fig. 1. |
| `05:10–28` FAIR list | §4.6 | Compress to one paragraph; the vocabulary sentence (`05:23`) is a repeat and is deleted. |
| `05:30` WIDOCO docs | §4.6 | Keep one sentence. |
| `05:32` sustainability | §4.6 | Keep; add registry entry (§3 item 3). |
| `06:2` evaluation overview | §6 | Keep. |
| `06:4–10` OOPS!/FOOPS!/AskWol | §6.1 | Convert to a table (tool, date, artifact, outcome, triage link); saves ~0.4 p. |
| `06:12` logical consistency | §6.1 | Keep; delete the repeated counts (Table 1 has them). |
| `06:14` SHACL | §6.2 | Keep. |
| `06:16` fixture description | §5 | Move; plain-language introduction of the 2 × 2 design first (T20f). |
| `06:18–20` CQs | §6.3 | Keep. |
| `06:22` round-trip results | §5 | Move with Fig. 3. |
| `07:2` why HCMO matters | §6.4 | Keep as the potential-impact subsection. |
| `07:4–7` reasoning and data quality | §6.4 | Shorten; first level overlaps §6.2. |
| `07:9–21` outlook uses | §7 | Compress to one paragraph. |
| `07:23` adoption path | §6.4 | Keep; add real figures if the co-authors supply them. |
| `08:2` conclusion recap | §7 | Cut to 3–4 sentences (currently repeats the abstract). |
| `08:4` limitations | §7 | Keep; add experimental-unit heterogeneity (meeting 2026-09-18 §6). |
| `08:6` future work | §7 | Keep; add the BFO/SOSA alignment profile only once Philippe confirms. |
| `main` Resource Availability Statement | end | Rewrite to the ISWC template: one line per resource (ontology + distributions, shapes, CQs + expected answers, examples + fixture, tooling, documentation, evaluation reports) with location. |
| `main` Acknowledgements | end | Shorten the provenance history to ~3 lines; merge duplicated TEATIME/Olog acknowledgement with §2. |

### 5.2 Repetition inventory — one home per topic

| Topic | Currently stated in | Single home after migration |
| --- | --- | --- |
| Reused-vocabulary inventory (BFO, IAO, SOSA, OWL-Time, QUDT, SemTS, PROV, schema.org) | abstract, §1 item 2, §2 ¶15, §4 ¶31/33/37, §5 FAIR-I, §8 | **§4.4** (+ one clause in the abstract) |
| "Not HCMO class mappings / not formal ISA conformance" caveat | §1, §2 ¶19, §4 ¶35/37, §5 FAIR-I, §6 ¶20/22, §8 | **§5** (+ one line in §7 limitations) |
| Package contents (sources, distributions, SHACL, CQs, JSON-LD, PID, licence, docs) | abstract, §1 item 3, §5, §8 | **§4.5–4.6** (+ abstract) |
| Manifest / distributions / `profile.json` | §4 ¶41, §5 ¶4/6 | **§4.5** |
| Resource counts | Table 1, §4 ¶43, §6 ¶12 | **Table 1** |
| Sensor ≠ observation ≠ result | abstract, §1, R2, §4 ¶27, §8 | **§4.3** (+ abstract, R2) |
| TEATIME grounding | §1, §2, §5 ¶32, §7 ¶23, §8, acknowledgements | **§1** (introduced), **§6.4** (adoption) |
| 2 × 2 round-trip fixture | §3 ¶34, §4 ¶37, §6 ¶16/22, §8, Fig. 3 | **§5** |
| Eleven CQs | §3 ¶34, §6 ¶18 | Definition **§3.2**, results **§6.3** |
| Outlook uses (KGQA, authoring, vendor mapping) | §1 ¶25, §7, §8 | **§7** |
| Olog/Bains authorship history | §2 ¶6/8, acknowledgements | **Acknowledgements** |

### 5.3 New content required

1. **Comparison table** vs similar resources (§2) — ISWC Impact criterion.
2. **Resource-selection criteria** (§3.3, T20c) — must describe the criteria
   the authors actually used; do not invent retrospective justifications.
3. **Reuse ratio** in Table 1 (KT #9), with the metadata-vs-semantic split
   (T20l). Measured on `dist/hcmo.ttl` (0.3.0) on 2026-09-24:
   - HCMO-declared classes and properties: 203 (60 + 68 + 75, including
     deprecated compatibility terms);
   - external **semantic** terms referenced: **25** — SOSA 9, BFO 4,
     schema.org 4, SemTS 3, QUDT 3, IAO 1, PROV-O 1;
   - external **metadata** vocabularies: 6 — DCTERMS, DC, SKOS, VANN, BIBO,
     MOD.
   Example data additionally reuse OWL-Time, PROV-O, OBI, STATO, ISA and
   Bioschemas terms; report them separately as instance-level reuse.
4. Plain-language introduction to the 2 × 2 fixture (T20f) at the start of §5.
5. ISWC-format **Resource Availability Statement**.
6. Registry entry (LOV / BioPortal / OLS / FAIRsharing) cited in §4.6.
7. Experimental-unit heterogeneity (group-level vs individual measurements)
   in §7 limitations, per the 2026-09-18 meeting.

## 6. Inputs needed from co-authors

| Input | From | Needed for |
| --- | --- | --- |
| Confirm the additional co-author (Benoit Girard?), his affiliation and author position | Damien | author list, CRediT, acknowledgements |
| Hosted SPARQL service: yes/no for the submission | Gaoussou, Konstantin | §4.6, comment 15 |
| Any quantitative adoption figures (TEATIME WG members involved, labs or datasets mapped, GitHub/Zenodo usage) | all | §6.4, comment 14 |
| Selection criteria actually applied when choosing external vocabularies | Cyril, Gaoussou, Konstantin | §3.3 |
| Confirmation of the BFO/SOSA alignment profile | Philippe | §4.4 / §7 wording only (the paper describes 0.3.0) |

## 7. Execution steps

1. Upload `hcmo-overleaf-upload.zip` to the online project (keeps figures 3–4
   and the data links there). Ask co-authors to stop editing during step 3.
2. Resolve D3 (author list) and comment 15 (SPARQL service).
3. Migrate in LaTeX (the Markdown `sections/*.md` are history and are not
   regenerated): create the new section files, move paragraphs per §5.1,
   delete repetitions per §5.2, then write the new content in §5.3. Keep every
   moved or rewritten passage in `\new{}` for the co-author review.
4. Compile; check the page count against the 15-page budget with
   `\reviewfalse` and todos disabled.
5. Rebuild the upload zip, upload, circulate for a focused co-author read
   (T20k).
6. Update `CALL-REQUIREMENTS.md` against the ISWC 2027 call when it appears.

## 8. First migration pass (2026-09-24)

Done in `docs/paper/overleaf/` after co-authors stopped editing online and the
synced zip was uploaded.

**New section files** (old `03-requirements`, `04-resource`, `05-availability`,
`07-impact`, `08-conclusion` removed). The old online project is abandoned; a
new online project will be created from `hcmo-overleaf-upload.zip`:

| File | Section |
| --- | --- |
| `01-introduction.tex` | 1 Introduction — TEATIME introduced early; four contributions; new roadmap |
| `02-related-work.tex` | 2 Related work — HCM data/metadata; Olog + Bains model merged; adjacent resources; **new comparison table**; gap |
| `03-methodology.tex` | 3 Methodology — development process; stakeholders; **requirements table**; CQs; **resource-selection criteria** (orange todo: co-authors to confirm); claim-strength policy |
| `04-hcmo.tex` | 4 The HCMO resource — identity; **Table 1 with release/active counts and reuse ratio**; modules + Fig. 2; modelling decisions; reused standards (single home of the vocabulary inventory); engineering + Fig. 1; availability and sustainability (orange todo: registry entry) |
| `05-use-case.tex` | 5 Interoperability use case — evidence slice + Fig. 4; **plain-language 2 × 2 factorial design with repeated measures**; three projections + Fig. 3 |
| `06-evaluation.tex` | 6 Evaluation and potential impact — **scan table** (FOOPS!/OOPS!/AskWol); consistency; SHACL; CQs; impact; adoption (KT todo kept) |
| `07-discussion.tex` | 7 Discussion, limitations, future work, conclusion — adds the experimental-unit limitation |

**Back matter:** ISWC Resource Availability Statement (one line per resource
kind); Acknowledgements shortened to Funding / Provenance / Non-author
contributions, Benoit Girard removed (now an author), HCM-D (BioPortal, from
March 2025) added to the provenance per Leonardo Restivo; CRediT in author
order; competing interests.

**Corrections made while migrating:**

- Table 1's caption claimed the counts include "directly referenced external
  terms". They do not: all 60/68/75 are HCMO-namespace terms, of which 27/36/38
  are deprecated compatibility terms. The table now shows release and active
  counts (33/32/37, matching the "33 classes and 69 properties" sentence it
  replaces) and counts external reuse separately.
- Links to the fixture data now point to the immutable `v0.3.0` tag where the
  files exist there. `examples/isa-roundtrip/README.md` and `native-isa/` exist
  only after `v0.3.0` (commit `5826a4a`) and are **not on GitHub `main`**, so
  their links are broken for reviewers — orange todo in the availability
  statement: merge to `main` or cut a 0.3.1 release before submission.

**Length:** compiles with no errors or undefined references; **17 pages, body
plus back matter end on p. 15, references from p. 16** — exactly at the
15-page budget with no reserve. Any text added in review must be offset.

**Build tooling:** `tooling/build_paper.py` now takes the section list from
`main.tex` `\input` lines and fails on missing or orphan section files,
instead of requiring exactly nine sections.

**Follow-up (same day):** Benoit Girard's ORCID added
(0000-0002-3914-6483); registry requirement met by the existing BioPortal
entry <https://bioportal.bioontology.org/ontologies/HCMO>, now cited in §4 (to
be updated with the final release); adoption figures dropped as too
preliminary. **Version:** the submitted paper will describe the next release
(probably v0.4), so every 0.3.0-specific number, DOI, date, and link — and the
broken post-0.3.0 fixture links — is to be reconciled against that release,
not patched now.

**Second follow-up (same day):** the §3 selection criteria were approved by
Damien (orange note removed). A *Use of AI assistants* paragraph was added to
§3, based on the repository record: OpenAI Codex and Anthropic Claude Code
connected to the GitHub repository, working on branches under `AGENTS.md`
rules (20 commits authored by a Claude identity and 27 Claude co-author
trailers out of 190 commits; `codex/` and `claude/` branches; Codex and
Claude entries in the TODO log), with author review before merge, the same CI
gate, and modelling decisions taken by the authors. To stay within 15 pages,
the stakeholder and claim-strength paragraphs, one related-work sentence, the
§6 query/SHACL/impact wording, the §5 opening, the §7 opening, and the
provenance sentence were tightened. A review PDF is at
`docs/paper/review/HCMO-draft-v4-review.pdf` (new text in blue, notes in the
margin).

**Still open:** Benoit Girard's affiliation; hosted SPARQL question; v0.4
reconciliation. (AI-use paragraph validated by Damien on 2026-09-24.)
