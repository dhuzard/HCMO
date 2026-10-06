# ADR-0005: BFO/SOSA bridge policy

- Status: proposed (co-author vote incomplete; see "Vote record")
- Date: 2026-10-06
- Scope: an optional alignment profile; the default release, the normative
  modules and the SOSA edition policy of ADR-0002 are unchanged

## Context

HCMO reuses SOSA/SSN 2017 for observation, sensing and actuation terms and
places its other terms under BFO/IAO in the `external-upper` presentation. The
two hierarchies are not linked: the four HCMO observation classes
(`hcm-obs` Behavior, Weight, Health Status and Environment observations) have
no BFO placement.

Declaring SOSA classes equivalent to BFO classes is rejected because SOSA is
deliberately broad: a `sosa:Sensor` may be a device or a piece of software, and
a `sosa:Result` may be a physical sample. Only one-way "is a kind of" links are
safe.

Two published alignments give such links without HCMO authoring statements about
W3C terms: the W3C one-way alignment of SOSA to PROV-O, and the PROV-O to BFO
alignment of Prudhomme et al. 2025 (Sci Data 12:282). For example,
`sosa:Observation ⊑ prov:Activity`, `prov:Activity ≡ BFO process`, so an
observation is inferred to be a BFO process. Options (a) link the hierarchies
without dropping either and (d) a fallback where strict equivalence fails were
preferred in the co-author discussion, with (a) first.

## Decision

1. **Reuse over authoring.** The bridge is an optional profile with its own
   ontology IRI that imports the two published alignments. HCMO adds a direct
   link only where the chain cannot provide it. Each link is recorded with its
   source and rationale as SSSOM (`semapv:ManualMappingCuration`) in
   `mappings/semantic/`, and the sources are added to
   `external-vocabularies.yaml`.
2. **Opt-in.** The profile is not part of the default release manifest and the
   core modules take on no BFO commitment through it. This may be reconsidered
   once the profile has proved stable.
3. **Software sensors.** A software sensor is modelled as the running software
   (a material entity in the alignment's reading), with the code a separate
   information entity. This is a commitment introduced by the BFO alignment,
   not by SOSA, and is documented as such.
4. **Duplicate terms are decided by meaning, not by name.** `hcm-tech:Actuator`,
   `hcm-tech:Sensor`, `hcm-obs:ObservationResult` and
   `hcm-env:EnvironmentalProperty` are each narrower than their SOSA
   counterpart (for example `hcm-tech:Actuator` is a physical home-cage device,
   whereas `sosa:Actuator` also covers software and other systems), so all four
   are kept and what each adds is documented. No HCMO class is retired.
5. **SOSA edition.** The chain is tested against the pinned SOSA 2017
   Recommendation artifact (ADR-0002) and the matching W3C alignment. Nothing is
   carried over from SOSA 2023 work without re-testing.
6. **Validation gates** (adopted from the PROV-BFO paper's own checks):
   - no class becomes unsatisfiable, over the full pinned BFO and IAO closure;
   - `examples/` stays consistent, plus negative probes (software sensor,
     physical-sample result);
   - loading the alignment adds no subsumption inside the HCMO, SOSA or BFO
     hierarchies;
   - any new disjointness the alignment adds is listed and reviewed.

   These are also run under the developer profile, because the default
   presentation hides material-entity/information-entity clashes. The pinned
   BFO is diffed against the release the PROV-BFO alignment targets rather than
   assumed to match.

## Expected consequences (to be verified by the profile's tests)

These follow from the two alignments; they are not a general SOSA–BFO reading.

- Observation and Actuator receive the placements agreed in discussion; the four
  HCMO observation classes become BFO processes without any module edit.
- `sosa:Result` is placed only as a continuant, so physical samples remain valid.
- `sosa:Sensor` is placed under material entity (see decision 3).
- The chain makes every `sosa:hasFeatureOfInterest` filler a participating
  continuant, so data that sets a process (for example a behavioural bout) as
  the feature of interest would become inconsistent. A SHACL check or modelling
  note is required before the profile ships.

## Per-axiom verdicts

**Draft for discussion.** Transcribed from the private decision sheet and work
plan (`hcmo-internal-docs`: `BFO-SOSA-DECISIONS-TO-TAKE.md`,
`BFO-SOSA-DOUBLE-HIERARCHY-PLAN.md` section 2.2,
`PROV-BFO-ALIGNMENT-PAPER-NOTES.md`). Two rounds of evidence exist and they
disagree on two axioms, so both are shown. Nothing here has been implemented.

### A. The four axioms tabled by option (a)/(d)

Round 1 = the 2026-09-18 plan, which tested each axiom *asserted directly by
HCMO* against the pinned SOSA 2017 definitions. Round 2 = the composed
SOSA to PROV-O to BFO chain, run through HermiT against HCMO 0.3.0
(`PROV-BFO-ALIGNMENT-PAPER-NOTES.md`).

| Axiom | Round 1: direct assertion | Round 2: via published chain | Proposed ADR verdict |
| --- | --- | --- | --- |
| `sosa:Actuator` under material entity | **Sound.** SOSA defines it as "a device". | Entailed (material entity). | **Accept via chain.** |
| `sosa:Observation` under process | **Sound, valuable.** Repairs the four unanchored HCMO observation classes. | Entailed (process); the four HCMO observation classes inferred as processes, no module edit. | **Accept via chain.** |
| `sosa:Sensor` under material entity | **Unsound.** SOSA says "device, agent (including humans), or software (simulation)"; software is information, disjoint from material entity; `hcm-tech:Software` is already information. | Entailed (material entity), on the paper's reading that a software agent is the *running* software. Direct probe (individual typed both `hcm-tech:Software` and `sosa:Sensor`) is inconsistent under the developer profile; the running-instance pattern is consistent. | **Accept via chain, with the running-software pattern** (decision 3); document it as a BFO-alignment commitment, not a SOSA one. **Rejected as a direct HCMO assertion.** |
| `sosa:Result` under information entity | **Unsound.** SOSA says a Result includes the result of sampling, and physical samples ("specimens") are material. | Not entailed: only "continuant". Physical-specimen probe consistent. | **Reject** as stated. Only "continuant" follows; record information-entity as an SSSOM `skos:closeMatch` note at most. |

### B. Axioms not on the original list

| Axiom | Round 1 | Round 2 | Proposed ADR verdict |
| --- | --- | --- | --- |
| `sosa:ObservableProperty` under specifically dependent continuant (BFO:0000020), not under quality | Missing from the tabled list; quality would be wrong because SOSA's property also covers dispositions and functions. Not one of the five default-presentation anchors. | Chain gives "continuant" only (weaker, compatible). | **Open.** Either developer-only, or not added (a sixth default anchor is a presentation decision). |
| `sosa:Procedure`, `sosa:FeatureOfInterest`, `sosa:Platform`, `sosa:Sample` | Not proposed. | Placed as generically dependent continuant (Procedure) and continuant (others). | **No direct HCMO axiom.** Placement is a chain consequence only. |
| `sosa:hasFeatureOfInterest` filler must be a continuant | Not examined. | Consequence of the chain (`hasFeatureOfInterest` under `prov:used` under has participant). A behavioural bout (a process) as feature of interest becomes inconsistent. | **Guard required:** SHACL check or modelling note before the profile ships (the bout is the observed phenomenon, the mouse the feature of interest). |

### C. De-duplication (decision 4)

| HCMO class | Duplicate of the SOSA class? | Evidence | Verdict |
| --- | --- | --- | --- |
| `hcm-tech:Actuator` | Round 1: "essentially yes", recommended deprecating in favour of `sosa:Actuator` (no subclasses, only range of `hasActuator`). **Superseded:** narrower than SOSA's (physical home-cage device; SOSA's also covers software and other systems), and several properties depend on it. | Co-author correction of 2026-09-24. | **Keep**; document what it adds. |
| `hcm-tech:Sensor` | No: HCM device, whereas SOSA's includes humans and software. 7 relations (domain), 2 (range), 3 SHACL shapes, 7 example graphs, the ISA package. | Plan section 2.4. | **Keep.** |
| `hcm-obs:ObservationResult` | No: 4 HCMO subclasses, domain of `hasConfidenceScore`. | Plan section 2.4. | **Keep.** |
| `hcm-env:EnvironmentalProperty` | No: range of 7 HCMO properties. | Plan section 2.4. | **Keep.** |

No `hcm-compat` deprecation entries and no `### Renamed` changelog section
follow from this ADR.

### D. Scope and packaging verdicts

| Item | Verdict |
| --- | --- |
| Report reuse by kind (annotation properties versus classes/properties) in `ALIGNMENTS.md` and the paper | Adopt regardless of the vote (decision sheet 1). |
| Ship the bridge in the default release | **Rejected** (ontology-hijacking risk, version bump needed). Opt-in profile instead. |
| Direct HCMO axioms on `sosa:*` terms | **Rejected** as the default route; only where the chain cannot provide a needed link. |
| Dropping SOSA or BFO (option c) | **Rejected**: breaks the `sosa:hasResult` / `hasFeatureOfInterest` / `observedProperty` machinery and contradicts ADR-0002. |
| Documentation only (option b) | **Not chosen**, but the reconciliation rule it requires is still written, because Sensor, Result and Environmental Property stay double-parented. |
| PROV-O dual anchors (Operational Assessment, Calibration Activity) | Out of scope for this ADR in the sheet. Round 2 changes the rationale: the `BFO:0000015` / `prov:Activity` double parent becomes redundant under a published alignment, not "an orthogonal view". Wording to be settled. |

**Discrepancies to resolve before accepting.** (1) Round 1 rejected Sensor, and
the chain entails it; the acceptance rests entirely on the running-software
reading. (2) Round 1 recommended retiring `hcm-tech:Actuator`; this was
corrected. (3) The BFO release pinned by HCMO differs slightly from the one the
PROV-BFO alignment targets (2024-01-29), and the chain was tested with the BFO
file only, without CCO/RO files or the SWRL location rules; both must be
re-checked. (4) The W3C SOSA to PROV-O alignment is non-normative.

## Vote record

| Participant | Position | Date |
| --- | --- | --- |
| Konstantin, Cyril, Pierre, Gaoussou | Option (a) preferred; (d) as fallback (Pierre and Gaoussou) | before 2026-09-24 |
| Pierre Larmande | Agrees with all five points | by 2026-10-06 |
| Cyril Gilbert | Agrees with the approach; asks that reasoning consequences, notably for software sensors and process-like features of interest, be checked jointly during implementation and the final decisions recorded in this ADR | by 2026-10-06 |
| Philippe | Not yet received as of 2026-10-06 (five points put to them 2026-09-24) | open |
| Serge Sonfack Sounchio, Antoine Toffano | Not yet received | open |

Open question (point 5): whether the earlier disjointness remark concerned the
2017 Recommendation or the 2023 edition. If it concerned 2023, that is a
separate decision reopening ADR-0002. We are trying to settle this from the
published sources (SOSA 2017 pinned artifact has zero `owl:disjointWith` and
zero `owl:AllDisjointClasses`; the 2023 edition is still to be checked) while
waiting for Philippe.

## Consequences

- Status moves to accepted when the open replies are in, and decisions 3 and 5
  are settled.
- Implementation (profile, SSSOM records, CI gates, documentation updates) is
  tracked in `docs/BACKLOG.md` section 1 and starts in a new branch.
- Adopting SOSA 2023 as the basis for the bridge would require a new ADR.
