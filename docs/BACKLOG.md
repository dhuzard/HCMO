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

## 1. BFO / SOSA double hierarchy (ADR-0005 accepted 2026-10-12)

Source: BFO/SOSA decision sheet and work plan, PROV-BFO reading notes, the
2026-09-18 meeting, the 2026-09-24 co-author replies and the 2026-10-06 audit
([`decisions/ADR-0005-evidence-audit.md`](decisions/ADR-0005-evidence-audit.md)).
Position reached: option **(a)** preferred by all four respondents with **(d)** as
fallback; implemented as one-way links through the published SOSA→PROV-O and
PROV-O→BFO alignments, not as equivalences. **ADR-0005 is accepted (2026-10-12);
the opt-in profile is built on branch `feat/bfo-sosa-bridge`
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

- [x] **Co-author validation of ADR-0005 (accepted 2026-10-12):** Pierre Larmande and Cyril Gilbert
  agreed to the five points. Cyril Gilbert validated the carrier pattern on 2026-10-09 (sensor = deployed physical system,
  separate from the software and its execution). Pierre Larmande, replying to
  the replay update on 2026-10-12, considers all decisions validated (carrier
  pattern and feature-of-interest restriction included). No objection was
  received; Philippe and Antoine Toffano did not reply and Serge cannot reply.
  Accepted by the editor on 2026-10-12.
- [x] **Disjointness remark (closed 2026-10-12): likely a note-taking misunderstanding.**
  No written source from Philippe; the editor considers the sentence a probable
  misunderstanding of the 2026-09-18 call. Nothing depends on it (ADR-0005 rests on
  the tested artifacts). Investigation record: The pinned
  SOSA 2017 file has none; the 2023 Working Draft (2026-10-03) has none on the
  classes concerned, only among its four collection classes.
  *Source found (2026-10-12):* the 2026-09-18 co-author call (Cyril Gilbert,
  Philippe Rocca-Serra, Damien Huzard), recorded in
  `docs/meetings/CO-AUTHOR-MEETING-2026-09-18.md` §2 (removed from the tree in
  `0b1ccdb`; read it with `git show 0b1ccdb~1:docs/meetings/CO-AUTHOR-MEETING-2026-09-18.md`):
  "both hierarchies assert disjointness: BFO's top-level branches are disjoint,
  and the SOSA parents are disjoint as well". The meeting's action was to send
  "Philippe's original comment" to the co-authors. Gmail holds no written version
  of the remark (searched 2026-10-12); Philippe's 2026-09-15 email raises the
  underlying point (no explicit alignment between OBO resources and PROV-O/SOSA).
  *Philippe's emails checked (2026-10-12): none mentions disjointness.* The
  2026-07-15 review asks for top-level anchoring; the 2026-07-22 email proposes
  the five-heading presentation (Entity; Material Entity; Information Entity;
  Quality/Property; Process Entity/PROV-O Event); the 2026-09-15 email asks what
  bringing PROV-O or SOSA into an OBO stack means "when there is no explicit
  alignment between these distinct artefacts". His proposed SOSA-under-BFO
  axioms were already recorded on 2026-09-17 (paper TODO T20l/T20m, `19afee5`),
  after he wrote on 2026-09-16 that he would formalise his points that night, so
  they most likely come from his PLM manuscript comments. The disjointness
  sentence first appears in the call notes committed straight after the call
  (`e6744e9`, 2026-09-18 17:08), unquoted: an oral remark or a paraphrase, not a
  written source. Its BFO half holds; its SOSA half matches no SOSA artifact.
  Read as "placing SOSA under disjoint BFO branches would let BFO's disjointness
  constrain SOSA", it is covered by the ADR-0005 gates (every relevant
  disjointness axiom listed, no unsatisfiable class, examples consistent).
  The PLM manuscript comments were not searched; not needed once the editor
  identified the sentence as his own probable misreading.
- [ ] **Follow up the upstream fix for the unparseable PROV-to-BFO file:** reported
  as BFO-Mappings/PROV-to-BFO#44 with the prefix fix in #43 (both open as of
  2026-10-09; ROBOT evidence added to #44 the same day). The typo fix (#41) is
  already on upstream `main` but not in any tag. Exit condition: a tag that
  contains **both** the #41 typo fix and the #43 prefix declarations, and whose
  file parses unmodified. Then pin that tag in `external-vocabularies.yaml`,
  delete the repaired copy, the `repair` block (`prepended_lines`,
  `replaced_once`) and `check_vendor`'s repair checks in
  `tooling/bridge_profile.py`, update `third_party/bfo-sosa-bridge/README.md`,
  and re-run the matrix. A tag with only one of the two fixes does not satisfy
  this item.
- [x] **Production-stack replay (acceptance requirement):** done by Cyril
  Gilbert on 2026-10-09. Protégé 5.6.9 / HermiT 1.4.3.456: both presentations
  consistent, no unsatisfiable class, expected inferences and probe results.
  ROBOT 1.9.10 rejected the vendored PROV-to-BFO file on the `rdfs:comment:`
  typo; the repair now corrects that token and the checksum is re-pinned.
- [x] **RO/CCO mappings and SWRL location rules (closed 2026-10-12):** RO/CCO
  out of scope. SWRL rules come with the published alignment and have no effect
  on current HCMO data. Revisit if HCMO adopts `prov:atLocation`. (The eight
  rules sit inside the imported PROV-to-BFO file and fire only on
  `prov:atLocation`, `prov:hadRole` and `prov:entity`, which no HCMO module,
  shape or example uses.)
- [x] **BFO definition differences reviewed (closed 2026-10-12): keep our pin.**
  The pinned BFO (commit `dd89f4a…`, 2026-03) is newer than the alignment's
  target (`release-2024-01-29`) and corrects it: the material entity
  elucidation restores "that at all times at which it exists" (the target's
  sentence is garbled); the continuant part definition uses "part of" instead
  of the circular "continuant part of"; 16 scope notes give the real
  temporal-extensions URL instead of a `<Link>` placeholder (the target has one
  more such placeholder note, on BFO_0000055, absent from our pin); the version IRI
  ends in `.owl` instead of `.ttl`. No logical axiom differs (checked by
  `tooling/bridge_profile.py`, which fails on any non-annotation difference).
  HCMO copies none of these definitions, so nothing changes in HCMO.
- [x] **Split external-reuse reporting by reuse kind (done 2026-10-12).**
  `tooling/reuse_report.py` classifies every external term in `dist/hcmo.ttl`
  (semantic, metadata, replacement target) and writes the generated
  `docs/EXTERNAL-REUSE.md`; `build.py` regenerates it and `validate.py` fails
  when it is stale. Result: 20 semantic terms from 7 vocabularies, 23 metadata
  terms from 7 vocabularies, 2 QUDT replacement targets. This corrects the hand
  count of 2026-09-24 (25 semantic, 6 metadata vocabularies), which counted
  `schema:Person`/`name`/`logo` and QUDT `numericValue`/`hasUnit` as semantic.
  `ALIGNMENTS.md` and paper Table 1 updated. *Related: T20l.*
- [ ] **Release 0.4.1 checklist** (PR #42, branch `release/0.4.0`; procedure in
  `paper/RELEASE-GATE.md`):
  - [x] Default-versus-optional qualifiers in `ALIGNMENTS.md` (2026-10-12).
  - [x] Manuscript moved to 0.4.1: Table 1, availability statement, tag links,
    evaluation counts, bridge-profile sentence, `prudhomme2025` (2026-10-12).
  - [x] Dated default-versus-optional notes in `PHILIPPE-ROCCA-SERRA-FEEDBACK.md`
    and the B09 entry of the human-review checklist (2026-10-12).
  - [x] Version 0.4.1 in the ontology header, `hcmo.yaml`, `CITATION.cff`,
    competency-question index, contribution form and documentation; nine
    authors in paper order; ADR-0006 accepted; CHANGELOG cut (2026-10-12).
  - [x] ~~`v0.4.0`~~ published 2026-10-12 from the pre-release commit `ac37bef`
    (artifacts say 0.3.0); superseded by 0.4.1, see `paper/RELEASE-GATE.md`.
  - [x] Merge the release PR, tag `v0.4.1` on the merge commit, verify the tag
    and one asset, publish the GitHub release (2026-10-12).
  - [x] v0.4.0 GitHub release marked superseded (2026-10-12).
  - [ ] Add the superseded note to the v0.4.0 Zenodo description (needs the
    Zenodo account).
  - [x] Record the Zenodo 0.4.1 version DOI `10.5281/zenodo.23315766` (CITATION.cff, README, paper,
    resource-metadata sheet).
  - [x] Check PURL content negotiation and the redeployed WIDOCO site.
  - [ ] Re-run OOPS!/FOOPS! on 0.4.1 and update the paper's scan table.
  - [ ] If the upstream PROV-to-BFO tag (#41 + #43) exists, swap the pin (item
    above); otherwise ship the repaired copy as is.
  - If the profile later becomes default or SOSA 2023 is adopted, write a new ADR.
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

- [x] **ADR-0006 accepted (2026-10-12, editor) for release 0.4.1** (interacting
  groups and roles, loosened `BehaviorObservation` axiom).
- [ ] **ADR-0006 open point 2:** should group housing measured only at cage level
  use `InteractingGroup`, `ExperimentalGroup`, or the enclosure as feature of
  interest?
- [ ] **ADR-0006 open point 3:** co-author review of the LMT event table
  `event-mapping.csv`.
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
