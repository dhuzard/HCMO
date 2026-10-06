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
2026-09-18 meeting, the 2026-09-24 co-author replies and the 2026-10-06 audit
([`decisions/ADR-0005-evidence-audit.md`](decisions/ADR-0005-evidence-audit.md)).
Position reached: option **(a)** preferred by all four respondents with **(d)** as
fallback; implemented as one-way links through the published SOSA→PROV-O and
PROV-O→BFO alignments, not as equivalences. **ADR-0005 is drafted as *proposed*;
the opt-in profile is built on branch `feat/bfo-sosa-bridge-profile`
([`BFO-SOSA-BRIDGE-PROFILE.md`](BFO-SOSA-BRIDGE-PROFILE.md)); no ontology module
and no `dist/` artifact changed.**

Done on 2026-10-06 (author decisions): vendored patched copy of the unparseable
PROV-to-BFO file; carrier pattern for software sensors as an optional documented
pattern with a profile SHACL check; SOSA 2017 retained; Actuator, Sensor,
ObservationResult and EnvironmentalProperty all kept; no direct ObservableProperty
axiom; feature-of-interest guard (note, profile SHACL warning, probe); BFO drift
tested against both BFO files; `tooling/bridge_profile.py` gates; SSSOM review rows;
pins in `external-vocabularies.yaml`; `UPPER-LEVEL-VIEW.md` correction.

Open:

- [ ] **Co-author validation of ADR-0005:** Pierre Larmande and Cyril Gilbert
  agreed to the five points; **Philippe's answers are still missing**, and
  Serge Sonfack Sounchio and Antoine Toffano have not replied. The carrier pattern
  and the feature-of-interest restriction need explicit co-author validation.
- [ ] **Ask which exact artifact motivated the disjointness remark.** The pinned
  SOSA 2017 file has none; the 2023 Working Draft (2026-10-03) has none on the
  classes concerned, only among its four collection classes.
- [ ] **Follow up the upstream fix for the unparseable PROV-to-BFO file:** reported
  as BFO-Mappings/PROV-to-BFO#44 with the fix in #43 (both open). When the pull
  request is merged and a tag is published, pin that tag in
  `external-vocabularies.yaml`, delete the prefix-fixed copy and its repair check in
  `tooling/bridge_profile.py`, and re-run the matrix.
- [ ] **Production-stack replay (acceptance requirement):** ask Cyril Gilbert to
  open the bundle from `python tooling/bridge_profile.py package` in Protégé
  (HermiT) and ROBOT, and report load errors, consistency, inferred placements and
  probe outcomes. Decide whether the optional RO/CCO mappings and the SWRL
  location rules are part of the contract.
- [ ] **Review the BFO definition differences** between the pinned BFO and the
  alignment target (material entity, continuant part; annotation-only).
- [ ] **Split external-reuse reporting by reuse kind** (annotation properties for
  ontology metadata versus classes and properties used in HCM semantics) in
  `docs/ALIGNMENTS.md` and the paper ("adopt regardless of the vote"). *Related: T20l.*
- [ ] **After acceptance:** add default-versus-optional qualifiers to
  `ALIGNMENTS.md`, update the WIDOCO pages, the manuscript's SOSA section and the
  historical notes that still describe provenance as an "orthogonal view", then
  changelog and release. If the profile later becomes default or SOSA 2023 is
  adopted, write a new ADR.
- [ ] **Revisit `sosa:ObservableProperty ⊑ BFO:0000020`** only at an edition
  migration (decision 8 of ADR-0005).

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
