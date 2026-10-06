# HCMO backlog

One place for the open items that were scattered across the working notes and
meeting records now kept in the private `dhuzard/hcmo-internal-docs` repository
(to be moved out at the end of the release clean-up; see the last section).
It is a **backlog to be cleaned later**, not a plan: items are copied from those
notes as they stood on **2026-09-24** (the date of the last of them), cross-checked
against the open GitHub issues and `docs/paper/TODO.md` on 2026-10-01. Anything
marked "check" may already be done.

How to read it: each item names where it came from, where it is already
tracked (if anywhere), and the next step. Tracked elsewhere means that tracker is
authoritative; this file only points to it.

Abbreviations: **T…/P…** are rows in [`paper/TODO.md`](paper/TODO.md);
**#…** are GitHub issues or pull requests in `dhuzard/HCMO`.

---

## 1. BFO / SOSA double hierarchy (decision provisional)

Source: BFO/SOSA decision sheet and work plan, PROV-BFO reading notes, the
2026-09-18 meeting and the 2026-09-24 co-author replies. Position reached: option
**(a)** preferred by all four respondents with **(d)** as fallback; implemented
as one-way links through the published SOSA→PROV-O and PROV-O→BFO alignments, not
as equivalences. **Nothing is implemented and no module changed.**

- [ ] **Get Philippe's answers to the five points** put to him on 2026-09-24:
  (1) accept the software-sensor pattern (a software sensor is the *running*
  software, with the code a separate information entity); (2) reuse the published
  alignments rather than author new SOSA→BFO axioms; (3) keep the alignment
  profile opt-in, outside the default release; (4) duplicate terms are decided by
  meaning, not name (corrected the same day: keep `hcm-tech:Actuator`,
  `hcm-tech:Sensor`, `hcm-obs:ObservationResult`, `hcm-env:EnvironmentalProperty`;
  retire none); (5) was the disjointness remark about SOSA 2017 or the 2023
  edition. *Tracked: P1 (Actuator correction), T20m.*
- [ ] **Ask Serge Sonfack Sounchio and Antoine Toffano for their replies** on the
  BFO/SOSA thread (they had not replied by 2026-09-24).
- [ ] **Finish ADR-0005** (draft written 2026-10-06 as *proposed*; Pierre Larmande
  and Cyril Gilbert agreed to the five points; still to fill: per-axiom verdicts
  table, Philippe's answers, and point 5). Original scope: (`docs/decisions/ADR-0005-BFO-SOSA-BRIDGE-POLICY.md`,
  shaped like ADR-0002): per-axiom verdicts including the rejected ones, scope of
  de-duplication, default-versus-opt-in, and the vote (date, participants,
  outcome). Blocks every implementation step below.
- [ ] **Build the opt-in alignment profile** in its own ontology IRI, importing the
  published alignments; add a direct HCMO link only where the chain cannot give
  it. Record each mapping with source and rationale as SSSOM
  (`semapv:ManualMappingCuration`) in `mappings/semantic/`, and add the sources to
  `external-vocabularies.yaml`. Pin the exact SOSA 2017 artifact and matching W3C
  alignment.
- [ ] **Add CI gates for the profile:** satisfiability over the full pinned BFO and
  IAO closure; consistency of `examples/` plus negative probes (software sensor,
  physical-sample result); conservativity (no new subsumption inside the HCMO,
  SOSA or BFO hierarchies); review of any new cross-derived disjointness. Test under
  the developer profile too, because the default presentation hides
  material-entity/information-entity clashes. Diff the pinned BFO against the
  release the PROV-BFO alignment targets (2024-01-29) instead of assuming they match.
- [ ] **Guard the feature-of-interest constraint:** the chain makes every
  `sosa:hasFeatureOfInterest` filler a participating continuant, so data that sets a
  behavioural bout (a process) as the feature of interest would become inconsistent.
  Add a SHACL check or a modelling note before any profile ships.
- [ ] **Document the four narrower-than-SOSA classes** as specialisations and what
  each adds; document the software-sensor choice as a commitment introduced by the
  BFO alignment, not by SOSA.
- [ ] **Split external-reuse reporting by reuse kind** (annotation properties for
  ontology metadata versus classes and properties used in HCM semantics) in
  `docs/ALIGNMENTS.md` and the paper (Decision 1 of the sheet; "adopt regardless of
  the vote"). *Related: T20l.*
- [ ] **Smaller open decisions:** whether `sosa:ObservableProperty ⊑ BFO:0000020`
  is added (a sixth anchor in a presentation designed around five); restate the
  PROV-O rationale as "already resolved by a published alignment" rather than
  "orthogonal view" (the `BFO:0000015` / `prov:Activity` double parent becomes
  redundant); if the disjointness remark was about SOSA 2023, that reopens
  ADR-0002 as a separate decision.
- [ ] **After the decision:** update `UPPER-LEVEL-VIEW.md`, `ALIGNMENTS.md`, WIDOCO
  pages, shapes/examples/competency questions, the manuscript's SOSA section, then
  changelog and release. The plan estimates about 6 to 7.5 days of work for the
  narrowed bridge (documentation only about 2.5 to 3 days).

## 2. Manuscript and evidence (from the 2026-09-18 meeting and 2026-09-24 replies)

- [ ] **OBI/STATO class examples and the TBox / ABox / CBox distinction** in the
  paper. *Tracked: #36; T20n.*
- [ ] **2 × 2 fixture: explain what is tested and carry the data through to STATO.**
  Philippe planned a PR for the chain `data/dark-phase-activity.csv → ISA-Tab →
  STATO`; this touches the controlled losses declared in
  `examples/isa-roundtrip/loss/isa-tab.yaml`. The wording "2 × 2 factorial with
  repeated measures, seven daily observations per animal (56 in total)" is settled
  and applied. If the group wants day fitted as a seven-level factor, that changes
  the generator, the reported contrast and the expected answers in
  `examples/isa-roundtrip/competency_questions.yaml`. *Tracked: T20f, T20g, T20q, T20r.*
- [ ] **HCMO–ISA JSON-LD context and ISA→JSON-LD build**; decide whether to deposit
  the result on Zenodo. *Tracked: #34.*
- [ ] **Hasse diagram of the experimental design**, to be evaluated as a figure.
  *Tracked: #35.*
- [ ] **Discussion: heterogeneity and the experimental unit.** Some systems measure
  only at group (cage) level, others resolve the individual subject; HCMO cannot yet
  define the experimental unit unambiguously, which also drives how either case
  links to ISA. To be explained clearly, not compressed. *Not tracked anywhere:
  consider a GitHub issue.*
- [ ] **Validate the SPARQL queries**; ask Gaoussou Sanou for a PR (to be
  confirmed). *Not tracked.*
- [ ] **SKOS collection of file formats by system and provider.** Delivered in
  #38 (`vocabularies/file-formats.ttl`, `data-access-methods.ttl`, vendors and
  systems); close #31 and #33 when it merges, if they are fully covered. *Tracked:
  #31, #33.*
- [ ] **Benoit Girard's affiliation** is still a placeholder ("to be confirmed") in
  `paper/overleaf/main.tex` and `paper/metadata/authors.md`.
- [ ] **Check the section restructure against the settled layout** (D1: seven-section
  resource-paper layout). *Tracked: T20b (in progress), T20i, T20k, T20s.*
- [ ] **Check the venue:** the meeting notes and some TODO rows still say ESWC 2027
  while the paper now targets ISWC. *Tracked: T20a.*

## 3. ISA exchange profile (brainstorm of 2026-09-18, nothing decided)

Provisional recommendation recorded there: generalise and document the existing
SHACL constraints as an HCMO-maintained exchange profile, keep the native
Source-to-Sample round trip and its loss manifests, and promote an ISA
configuration only after a whole-animal feasibility test shows it enables a real
native workflow without inventing a Sample proxy. *Tracked: T20r, T20o.*

Decisions deferred to the co-authors:

- [ ] What real consumer or exchange scenario makes ISA useful for HCMO?
- [ ] Is ISA an optional exchange profile or an intended normative dependency?
- [ ] Must native ISA represent the whole-animal behavioural assay, or is the
  Source-to-tissue-Sample overlap enough for the paper?
- [ ] Must study-factor values stay directly attached to animal Sources?
- [ ] Which tool must consume an ISA configuration, and who maintains its version
  and controlled terminology?
- [ ] Generalise the existing shapes into a supported application profile, or keep
  them as evaluation-fixture checks?
- [ ] Which claim is intended: tested interoperability, conformance to an
  HCMO-maintained profile, or formal conformance to an externally governed ISA
  profile?
- [ ] Who owns updates when ISA, ISA RO-Crate, RO-Crate or the validators change?
- [ ] Review the candidate manuscript paragraph in the brainstorm (a drafting
  proposal, not approved text).

## 4. Multi-animal model, LMT and SKOS vocabularies (PR #38)

- [ ] **Co-author review of the multi-animal model and ADR-0006** (interacting
  groups and roles; status "proposed"). A tracking row (T20t) existed on the
  feature branch but was left out of #38 so as not to touch the paper TODO; add it
  to `paper/TODO.md` or track it here.
- [ ] **`catalog.ttl` emits deprecated `hcm:System` / `hcm:Supplier`:** adopt a
  `schema:Product` + SKOS vendor catalogue pattern. *Tracked: #32.*

## 5. Repository clean-up (from the release / OSS audit, PR #39)

- [ ] **Move the remaining working notes out of the public tree at the end**, once
  everything above is fixed: the Philippe Rocca-Serra review record, human-review
  checklist and meeting notes, and the class/property audit working notes. First
  rewire what still depends on them: `A02-ISA-STATO-COMPATIBILITY.md` links into
  the checklist, and `tooling/class_audit.py` and `tooling/property_audit.py` read
  and write the audit notes. The files already moved are listed in the internal
  repository's README.
- [ ] **Licence for code:** the repository is CC BY 4.0 throughout; consider MIT or
  Apache-2.0 for `tooling/` (maintainer decision).
- [ ] **Rights check** on the French internship report (kept by decision; it is a
  historical source) and confirm the DVC real dataset's sharing terms.
- [ ] **Tidy `docs/`:** it still mixes user docs with notes; decide whether
  `ontology/v2/` stays; move `HCMO-logo3.png` (1.1 MB) to `docs/assets/`;
  remove the absolute local path in `paper/PROTEGE-DRY-RUN-2026-07-06.md`;
  add `mappings/` and `external-vocabularies.yaml` to the README repository map;
  drop generated reports from version control (`tooling/robot-report.*`).
- [ ] **Confirm the contact address** in `SECURITY.md` and `CODE_OF_CONDUCT.md`
  (taken from `CITATION.cff`).
