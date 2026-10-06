# ADR-0005: BFO/SOSA bridge policy

- Status: proposed (author decisions taken 2026-10-06; co-author validation pending, see "Vote record")
- Date: 2026-10-06
- Scope: an optional alignment profile; the default release, the normative
  modules and the SOSA edition policy of ADR-0002 are unchanged
- Evidence: [`ADR-0005-evidence-audit.md`](ADR-0005-evidence-audit.md)
  (recomputed facts, reasoning matrix, SOSA 2023 inspection)
- Implementation: [`../BFO-SOSA-BRIDGE-PROFILE.md`](../BFO-SOSA-BRIDGE-PROFILE.md)

## Context

HCMO reuses SOSA/SSN 2017 for observation, sensing and actuation terms and
places its other terms under BFO/IAO in the `external-upper` presentation. The
two hierarchies are not linked: the four HCMO observation classes (Behavior,
Weight, Health Status and Environment observations, plus the indirect
`GasConcentrationObservation`) have no BFO placement.

Declaring SOSA classes equivalent to BFO classes is rejected because SOSA is
deliberately broad: a `sosa:Sensor` may be a device, an agent or software, and a
`sosa:Result` may be a physical sample. Only one-way "is a kind of" links are
safe.

Two published alignments give such links without HCMO authoring statements about
W3C terms: the W3C one-way alignment of SOSA to PROV-O (SSN 2017 section 6.5,
non-normative), and the PROV-O to BFO alignment of Prudhomme et al. 2025
(Sci Data 12:282; tag `v2025-01-19`, CC0). For example,
`sosa:Observation ⊑ prov:Activity` and `prov:Activity ≡ BFO process`, so an
observation is inferred to be a BFO process. Options (a) link the hierarchies
without dropping either and (d) a fallback where strict equivalence fails were
preferred in the co-author discussion, with (a) first.

## Decision

1. **Reuse over authoring.** The bridge is an optional profile with its own
   ontology IRI that imports the two published alignments. HCMO adds a direct
   link only where the chain cannot provide it; none is needed so far. Each
   consequence is recorded with its source and rationale as SSSOM
   (`semapv:ManualMappingCuration`, review-only) in `mappings/semantic/`, and the
   sources are pinned in `external-vocabularies.yaml`.
2. **Unparseable upstream file: vendored, minimally patched copy.** The tagged
   PROV-to-BFO file (and `main`) does not parse: it uses the default prefix `:`
   and `xsd:` without declaring them. HCMO vendors the verbatim file (SHA-256
   recorded) together with a patch that only prepends the two missing prefix
   declarations, and a CI check proves the patched file differs from the original
   by exactly those lines. No axiom is changed and the `rdfs:comment:` typo in the
   pinned tag (already fixed on upstream `main`) is left as it is. The problem is
   reported upstream as BFO-Mappings/PROV-to-BFO issue #44 with the fix proposed in
   pull request #43 (same declarations, same default namespace); when a corrected
   immutable tag exists, HCMO pins it and removes the patch. Until then results are stated as "on the prefix-repaired
   chain", never as raw-source success.
3. **Opt-in.** The profile is not part of the default release manifest and the
   core modules take on no BFO commitment through it. `hcmo.yaml`, `dist/` and the
   merged graph are unchanged; CI checks that. This may be reconsidered once the
   profile has proved stable.
4. **Software sensors: carrier pattern.** The code stays `hcm-tech:Software`
   (an information content entity). The *deployed, running installation* is the
   Sensor, a material carrier that is distinct from the code and from the
   execution process. Accepted as an **optional documented pattern**: the sensor
   bears a quality, and that quality concretizes the code
   (`BFO:0000196` bearer of, `BFO:0000019` quality, `BFO:0000059` concretizes).
   A direct "sensor concretizes code" statement is inconsistent with the pinned
   BFO and is not allowed. The profile ships a SHACL check that flags an
   individual typed both as software and as a sensor. This is a commitment
   introduced by the BFO alignment, not by SOSA, and is documented as such.
5. **Duplicate terms are decided by meaning, not by name.**
   `hcm-tech:Actuator`, `hcm-tech:Sensor`, `hcm-obs:ObservationResult` and
   `hcm-env:EnvironmentalProperty` are each narrower than their SOSA counterpart,
   so all four are kept and what each adds is documented. No HCMO class is
   retired. `hcm-tech:Actuator` is kept for its authored scope (a device that
   elicits or perturbs behaviour, physiology or the monitored environment, typed
   as a material entity) and because three HCMO properties depend on it; the SOSA
   2017 definition is "a device" and is not claimed to cover software.
6. **SOSA edition: 2017 retained.** The chain is tested against the pinned SOSA
   2017 Recommendation artifact (ADR-0002) and the matching W3C alignment. The
   2023 edition is a W3C Working Draft (3 October 2026) that deprecates
   `sosa:Result` and `sosa:ObservableProperty`; moving to it would need a new ADR,
   a pinned immutable artifact and re-testing.
7. **Feature-of-interest guard.** The chain makes every `sosa:hasFeatureOfInterest`
   filler a continuant, so a process (behavioural bout, interaction, session) used
   as a feature of interest becomes inconsistent. Current data is unaffected (the
   audit found only subjects, groups and enclosures). The profile adds a modelling
   note (the feature of interest is what the observation is about; a bout or
   interaction is the observed phenomenon or result, as in ADR-0006), a
   profile-only SHACL warning, and a consistency probe. Default shapes are not
   touched. The restriction is documented as a consequence of the alignment, not
   of SOSA.
8. **ObservableProperty: no direct axiom.** The chain gives "continuant". A
   stronger specifically-dependent-continuant axiom would be a new HCMO statement
   about a W3C class, would add a sixth anchor to a presentation designed around
   five, is not supported by the pinned 2017 definition, and concerns a term the
   2023 draft deprecates. Revisit at an edition migration.
9. **Validation gates** (adopted from the PROV-BFO paper's own checks):
   - the vendored alignment is byte-identical to the recorded original plus the
     two prefix lines, and all pinned inputs match their SHA-256;
   - no class becomes unsatisfiable, over the full pinned BFO and IAO closure;
   - `examples/` stays consistent, plus probes (software sensor, carrier pattern,
     physical-sample result, observation result, process as feature of interest);
   - loading the alignment adds no named subsumption inside the HCMO, SOSA or BFO
     hierarchies (a finite taxonomy check, not a proof of conservative extension);
   - every disjointness axiom the combination makes relevant is listed;
   - default artifacts (`dist/`) are unchanged by the profile.

   All are run under the default presentation and the developer profile.
   Production-stack replay (Protégé / ROBOT) is an acceptance requirement.

## Expected consequences

Verified on the prefix-repaired chain with full pinned BFO and IAO (HermiT
1.3.8.1099; re-run by `tooling/bridge_profile.py`, 70 checks passing); not a general SOSA–BFO reading.

| Class | Placement under the chain |
| --- | --- |
| `sosa:Sensor`, `sosa:Actuator`, `sosa:Sampler` | material entity |
| `sosa:Observation`, `sosa:Actuation`, `sosa:Sampling` | process |
| `sosa:Result`, `sosa:ObservableProperty`, `sosa:FeatureOfInterest`, `sosa:Platform` | continuant (only) |
| `sosa:Procedure` | generically dependent continuant |
| Four HCMO observation classes and `GasConcentrationObservation` | process |

Physical-specimen results stay valid because Result is only a continuant.

## Per-axiom verdicts

Transcribed from the private decision sheet and work plan (`hcmo-internal-docs`)
and updated with the audit. Round 1 = the 2026-09-18 plan, which tested each axiom
*asserted directly by HCMO* against the pinned SOSA 2017 definitions. Round 2 =
the composed SOSA → PROV-O → BFO chain.

### A. The four axioms tabled by option (a)/(d)

| Axiom | Round 1: direct assertion | Round 2: via published chain | ADR verdict |
| --- | --- | --- | --- |
| `sosa:Actuator` under material entity | Sound: "a device". | Entailed. | **Accept via chain.** |
| `sosa:Observation` under process | Sound, valuable; repairs the unanchored observation classes. | Entailed; the HCMO observation classes become processes with no module edit. | **Accept via chain.** |
| `sosa:Sensor` under material entity | Unsound: SOSA includes agents and software; `hcm-tech:Software` is information. | Entailed. A Software+Sensor individual is inconsistent in both modes; the carrier pattern is consistent. | **Accept via chain, with the carrier pattern** (decision 4). **Rejected as a direct HCMO assertion.** |
| `sosa:Result` under information entity | Unsound: SOSA includes physical samples. | Not entailed: only "continuant"; specimen probe consistent. | **Reject.** Record information entity as a rejected review row only. |

### B. Axioms not on the original list

| Axiom | Verdict |
| --- | --- |
| `sosa:ObservableProperty` under specifically dependent continuant | **Not added** (decision 8). Chain continuant only. |
| `sosa:Procedure`, `FeatureOfInterest`, `Platform` | No direct HCMO axiom; chain placement only. `sosa:Sample` is not placed by the pinned alignment (see remaining risks). |
| `sosa:hasFeatureOfInterest` filler must be a continuant | **Guard required** (decision 7). |

### C. De-duplication

| HCMO class | Duplicate of the SOSA class? | Verdict |
| --- | --- | --- |
| `hcm-tech:Actuator` | No: authored HCM scope, material typing; 3 dependent properties (`hasActuator` range, `hasModelNumber` and `communicatesWith` via union domain/range). The earlier "retire" proposal is superseded. | **Keep.** |
| `hcm-tech:Sensor` | No: HCM device; SOSA's includes agents and software. Domain of 7 properties (+6 through union domains), range of 2 (+1), referenced by 3 shapes (1 targets it), explicit in 6 TTL example files (+ duplicate JSON serialisation). | **Keep.** |
| `hcm-obs:ObservationResult` | No: 4 direct subclasses, domain of `hasConfidenceScore`. | **Keep.** |
| `hcm-env:EnvironmentalProperty` | No: range of 8 properties (7 deprecated, 1 active). | **Keep.** |

No `hcm-compat` deprecation entry and no `### Renamed` changelog section follow.

### D. Scope and packaging

| Item | Verdict |
| --- | --- |
| Report reuse by kind (annotation properties versus classes/properties) in `ALIGNMENTS.md` and the paper | Adopt regardless of the vote. |
| Ship the bridge in the default release | **Rejected** (ontology-hijacking risk, version bump). Opt-in profile. |
| Direct HCMO axioms on `sosa:*` terms | **Rejected** as the default route. |
| Dropping SOSA or BFO (option c) | **Rejected**: breaks the observation machinery and ADR-0002. |
| Documentation only (option b) | Not chosen; the reconciliation rule is still written because Sensor, Result and EnvironmentalProperty stay double-parented. |
| PROV-O dual anchors (OperationalAssessment, CalibrationActivity) | Out of scope here. Under the opt-in equivalence the `BFO:0000015` / `prov:Activity` double parent becomes redundant, which is "already resolved by a published alignment", not "an orthogonal view". |

## Remaining risks

- The chain results hold on the prefix-repaired alignment, with one reasoner
  (HermiT). Production-stack replay (Protégé / ROBOT) is pending.
- The pinned BFO (commit `dd89f4a…`, 1014 triples) differs from the alignment's
  target (`release-2024-01-29`, 1015 triples) by 19 and 20 annotation-only
  triples (version IRI, definitions, scope notes); no BFO IRI the alignment uses
  is missing. The material-entity and continuant-part definitions differ in prose
  and need author review. The profile is tested against both BFO files.
- The W3C SOSA-to-PROV-O alignment is pinned at the immutable commit that matches the
  pinned SOSA 2017 file. The file served live at `https://www.w3.org/ns/sosa/prov/` adds one
  statement (`sosa:Sample ⊑ prov:Entity`), so the audit's continuant placement of `sosa:Sample`
  does not hold for the pinned file; the profile does not place `sosa:Sample`.
- The optional RO/CCO mappings are not part of the chain and are untested.
- The taxonomy comparison is finite; it is not a proof of conservative extension.
- Whether the carrier pattern suits real software toolchains (DeepLabCut, LMT) is
  a co-author judgement.

## Vote record

| Participant | Position | Date |
| --- | --- | --- |
| Konstantin, Cyril, Pierre, Gaoussou | Option (a) preferred; (d) as fallback (Pierre and Gaoussou) | before 2026-09-24 |
| Pierre Larmande | Agrees with all five points | by 2026-10-06 |
| Cyril Gilbert | Agrees with the approach; asks that reasoning consequences, notably for software sensors and process-like features of interest, be checked jointly during implementation and recorded in this ADR | by 2026-10-06 |
| Damien Huzard (editor) | Decisions 2, 4, 6 above (vendored patch plus upstream issue, carrier pattern as optional documented pattern, 2017 retained) | 2026-10-06 |
| Philippe | Not yet received as of 2026-10-06 (five points put to them 2026-09-24) | open |
| Serge Sonfack Sounchio, Antoine Toffano | Not yet received | open |

Open question for co-authors: which exact artifact motivated the earlier
disjointness remark? The pinned 2017 artifact has no disjointness; the 2023
Working Draft has none on the classes concerned (only among the four collection
classes), so the remark may concern an older draft, the BFO closure or an
optional alignment. This does not reopen ADR-0002.

## Consequences

- Status moves to accepted when the open replies are in, the carrier pattern and
  feature-of-interest restriction are validated by co-authors, and a production
  stack replay passes.
- Implementation (profile, vendored alignments, SSSOM rows, gates, documentation)
  is on branch `feat/bfo-sosa-bridge-profile`; remaining items stay in
  `docs/BACKLOG.md` section 1.
- Adopting SOSA 2023 as the basis for the bridge requires a new ADR.
