# Reading notes — Prudhomme et al. 2025, PROV-O → BFO alignment

**Status:** reading notes plus one reasoner experiment. No HCMO axiom has been
changed. These notes feed the open decisions in
[`BFO-SOSA-DECISIONS-TO-TAKE.md`](BFO-SOSA-DECISIONS-TO-TAKE.md). Sent by
Philippe Rocca-Serra on 2026-09-23.

## Citation

Prudhomme T, De Colle G, Liebers A, Sculley A, Xie PK, Cohen S, Beverley J.
*A semantic approach to mapping the Provenance Ontology to Basic Formal
Ontology.* Scientific Data 12, 282 (2025).
[doi:10.1038/s41597-025-04580-1](https://doi.org/10.1038/s41597-025-04580-1)
· PMID 39962095 · PMCID PMC11833102

- Alignment files: <https://github.com/BFO-Mappings/PROV-to-BFO>, tag
  `v2025-01-19`, CC0-1.0. Files: `prov-bfo-directmappings.ttl`,
  `prov-cco-directmappings.ttl`, `prov-ro-directmappings.ttl`.
- Archive: Zenodo 10.5281/zenodo.14692262 (cited in the paper); the repository
  README cites 10.5281/zenodo.11338700.
- Target versions: PROV-O 2013-04-30, BFO 2020 `release-2024-01-29`, CCO
  2024-11-06, RO 2024-04-24.

## Why it matters for HCMO

This paper is a peer-reviewed BFO interpretation of PROV-O. It also states
(Methods, Evaluation) that combining it with the W3C SOSA→PROV alignment
**gives a SOSA→BFO alignment**, and that this combination was checked against
the SOSA documentation examples with no inconsistencies. The authors leave a
fuller SOSA discussion "for another time".

So there is already a published, citable route from SOSA terms to BFO. HCMO
would not have to author one itself. We ran that route against HCMO (see
[Experiment](#experiment-the-composed-sosa--prov--bfo-chain-against-hcmo)).
It supports some of the recommendations in the decision sheet and challenges
others.

## What the paper does

### Method: four criteria for an alignment

1. **Mapping relation types.** Use only relations with logical force:
   `owl:equivalentClass`, `rdfs:subClassOf`, `rdfs:subPropertyOf`, property
   chains, and SWRL rules. SKOS (`skos:relatedMatch`, …) is used only as
   non-binding commentary, because a reasoner draws nothing from it.
2. **Coherence and consistency.** The union O1 ∪ O2 ∪ alignment has no
   unsatisfiable classes (coherence). With instance data it entails no
   contradiction (consistency).
3. **Conservativity.** The alignment must not add or remove a subsumption
   between two terms of the same source ontology. Tested as the "approximate
   deductive difference" (Solimando et al.).
4. **Scope.** *Total*: every PROV term maps to something. *Interpretable*:
   O2 ∪ Δ ⊨ O1. *Synonymous*: interpretability in both directions. They reach
   total, not full interpretation. Their slogan: "interpretability enhances
   interoperability".

They also avoid redundant mappings. A subclass inherits its parent's mapping,
so it is not mapped explicitly; inverse properties are not mapped either. A
separate derived file holds the reasoner-materialised mappings.

### Evaluation pipeline (ROBOT + GNU Make + GitHub Actions)

- **Totality query.** A SPARQL query lists every PROV term not connected to
  BFO/RO/CCO by an equivalence, a subsumption, a property chain, or a SWRL
  rule. Transitive paths are allowed, and inverses are materialised first with
  HermiT. The query runs in CI and reports the terms still unmapped.
- **Consistency on canonical instances.** All 312 example individuals from the
  W3C PROV documentation are loaded with the ontologies and alignments, then
  checked with HermiT.
- **Conservativity.** Materialise subsumptions and equivalences with and
  without the alignment. A SPARQL CONSTRUCT keeps only the relations within one
  ontology, and `robot diff` compares the two outputs. They found no
  difference. The alignment does add new *disjointness* between PROV terms.
- **Candidate property matching.** A SPARQL query finds BFO/RO/CCO properties
  whose domain and range match a PROV property's mapped domain and range.
  Curators then choose among the candidates.

### Packaging

- Alignments are kept in separate, versioned OWL 2 DL Turtle files. They
  deliberately do not `owl:import` PROV-O or BFO; a separate wrapper file
  imports everything for viewing and testing. This follows the PROV Dublin
  Core extension, and it leaves both source ontologies unchanged.
- Each mapping is a reified `owl:Axiom` carrying `sssom:object_label`, an
  `rdfs:comment` justification, and version provenance. A SPARQL query exports
  them to an SSSOM CSV with `mapping_justification`
  `semapv:ManualMappingCuration`. The authors chose OWL over native SSSOM
  because SSSOM does not yet define a standard for complex mappings.
- The paper does not use confidence scores, since every mapping was curated by
  hand.

### Results

The paper maps all 153 PROV-O classes and object properties, including
PROV-AQ, -Dictionary, -Links, -Inverses and -DC. Explicit mappings:

| Target | Explicit mappings |
| --- | --- |
| BFO | 35 terms: 6 equivalences, 24 subsumptions, 8 SWRL rules |
| CCO | 37 terms: 5 equivalences, 23 subsumptions, 1 property chain, 6 SWRL rules |
| RO | 25 terms: 26 subsumptions |

Four terms also carry SKOS commentary. **Data properties are not mapped**
(`prov:startedAtTime` etc.). In BFO these need a whole pattern: the process
occupies a temporal region, which has an identifier, and so on. The authors
suggest SPARQL CONSTRUCT as a future route.

## The class mappings (from `prov-bfo-directmappings.ttl`, v2025-01-19)

| PROV term | Relation | BFO target | Their justification (abridged) |
| --- | --- | --- | --- |
| `prov:Activity` | ≡ | process `BFO:0000015` | Happens over time and is not itself a temporal region |
| `prov:InstantaneousEvent` | ≡ | process boundary `BFO:0000035` | The start or end of an activity |
| `prov:Location` | ≡ | site `BFO:0000029` | A 3-D immaterial entity bounded by material entities |
| `prov:Entity` | ⊑ | (independent continuant ⊓ ¬spatial region) ⊔ GDC ⊔ SDC | Exists entirely at different times; spatial regions cannot participate in processes |
| `prov:Agent` | ⊑ | material entity ⊓ ∃participates in (at some time).Activity ⊓ ∃bearer of.(role ⊓ ∃realized in.Activity) | Always has a material part. `prov:SoftwareAgent` is *running* software, i.e. a material carrier, not source code |
| `prov:Role` | ⊑ | role `BFO:0000023` | Externally determined, so a role and not a function; narrower than BFO role |
| `prov:Plan`, `prov:Bundle`, `prov:Dictionary`, `prov:KeyEntityPair` | ⊑ | GDC `BFO:0000031` | Can exist as multiple copies |
| `prov:Influence` | ⊑ | process ⊔ process boundary, not both | Contradicts PROV's "capacity" wording on purpose: every subclass occurs in time |
| `prov:DictionaryInvolvement` | ⊑ | occurrent | Undefined in PROV; inferred from its examples |

CCO adds equivalences for `prov:Agent`, `prov:Person` (CCO Person ⊓
prov:Agent), `prov:Organization`, `prov:Start` (Process Beginning) and
`prov:End` (Process Ending). It adds `prov:Plan` ⊑ Information Content Entity,
deliberately **not** CCO Plan, because a PROV plan can prescribe more than
intentional acts.

Key property mappings to BFO:

- `used`, `generated`, `wasAssociatedWith`, `wasStartedBy`, `wasEndedBy`,
  `invalidated` ⊑ has participant (at some time) `BFO:0000057`
- `wasGeneratedBy`, `wasInvalidatedBy` ⊑ participates in (at some time)
  `BFO:0000056`
- `qualifiedStart`, `qualifiedEnd`, `qualifiedUsage`, `hadGeneration`,
  `hadUsage` ⊑ has temporal part `BFO:0000121`
- `hadMember` ⊑ has continuant part `BFO:0000178`
- `atLocation` is mapped by SWRL rules: to occurs in `BFO:0000066` for
  activities and instantaneous events, and to located in `BFO:0000171` for
  entities and agents.

In RO, `wasDerivedFrom`, `wasAttributedTo` and `alternateOf` ⊑ causally
influenced by `RO:0002559`; `influenced`/`influencer` ⊑ causally related to
`RO:0002410`.

### Modelling positions worth knowing

- **Continuant/occurrent disjointness wins over PROV's Rationale.** The Rationale's
  Requirement V14 allows an agent to be an activity. The authors reject this
  on purpose, so the alignment makes `prov:Agent` and `prov:Activity`
  disjoint. They argue no documented PROV example needs the overlap.
- **Influences are events, not capacities.** A generation happens at an
  instant; a capacity (a BFO disposition) is a continuant.
- **Qualified generation/invalidation have no sound subsumption**, because the
  range is a process boundary and the candidate BFO/CCO properties have
  `process` as range. SKOS is used only as a last resort.
- **Reuse over minting.** "We do not recommend adding terms … for the sole
  purpose of creating equivalence mappings … existing terms should be reused."

### Errors found in the W3C documentation

- Two PROV examples contradict PROV-O itself: a publication activity used as
  the subject of a property whose domain is Entity, and the `prov:Revision`
  example.
- Two examples contradict only the BFO alignment. In the first, the
  `prov:hadGeneration`/`prov:entity` subject is the digested protein sample
  instead of the Derivation. In the second, `prov:atTime` is used on an
  Activity where `prov:startedAtTime` was meant.

The authors call this "a feature, not a bug": the added axioms expose modelling
mistakes that PROV-O alone accepts.

---

## Experiment: the composed SOSA → PROV → BFO chain against HCMO

**Setup (2026-09-23, run locally, nothing committed to the build):**

- HCMO `dist/hcmo.ttl` (0.3.0).
- The pinned BFO core (`external-vocabularies.yaml`, commit `dd89f4a`) and
  pinned SOSA 2017 (`6dc6059`).
- PROV-O `prov-o.owl`.
- `prov-bfo-directmappings.ttl` v2025-01-19, with SWRL rules dropped. They
  only concern `atLocation`.
- The W3C SOSA→PROV alignment from SSN Recommendation §6.5.2–6.5.3,
  transcribed by hand because it is not served as a standalone file (see the
  appendix).

The reasoner was HermiT via owlready2 0.51. Runs were made with and without
`ontology/profiles/external-upper-developer.ttl`.

### Inferred BFO placement of SOSA terms

| SOSA term | Inferred BFO ancestor | Compare: decision sheet proposal |
| --- | --- | --- |
| `sosa:Observation`, `Actuation`, `Sampling` | **process** | Statement 3 (Observation ⊑ process): **same** |
| `sosa:Actuator` | **material entity** | Statement 1: **same** |
| `sosa:Sensor` | **material entity** | Statement 2: **same**. The sheet rejected this one. |
| `sosa:Result` | continuant (only) | Statement 4 was ICE. The chain is weaker and **physical samples stay valid** |
| `sosa:ObservableProperty` | continuant | Decision 4 (SDC): compatible, and the chain is weaker |
| `sosa:Procedure` | generically dependent continuant | — |
| `sosa:FeatureOfInterest`, `Platform`, `Sample` | continuant | — |
| `hcm-obs:BehaviorObservation`, `WeightObservation`, `HealthStatusObservation`, `EnvironmentObservation` | **process** | Decision 7 gap: **closed** |

### Consistency results

| Test | Default presentation | With developer profile | Without the bridge |
| --- | --- | --- | --- |
| TBox coherence (unsatisfiable classes) | none | none | — |
| All six `examples/*.ttl` | consistent | consistent | — |
| Probe: an individual typed both `hcm-tech:Software` and `sosa:Sensor` | consistent ⚠ | **inconsistent** | consistent |
| Probe: `hcm-tech:Software` individual plus a separate running-instance `sosa:Sensor` ⊓ material entity | consistent | consistent | — |
| Probe: physical specimen typed `sosa:Sample`, `sosa:Result`, material entity | consistent | consistent | — |
| Probe: `hcm-obs:ObservationResult` as `sosa:hasResult` value | consistent | consistent | — |
| Probe: `sosa:hasFeatureOfInterest` pointing at a BFO process | **inconsistent** | **inconsistent** | consistent |

The ⚠ row is consistent only because the default presentation places
`IAO:0000030` directly under `BFO:0000001`. The source-faithful path
ICE ⊑ GDC appears only in the developer profile. So the same data passes for a
default user and fails for a developer-profile user.

### What this means for the open decisions

- **Decisions 2 and 5: there is a new option.** Instead of HCMO authoring
  axioms about W3C terms, an opt-in profile could import two external
  artifacts: the CC0 PROV-to-BFO files and the W3C's own SOSA→PROV alignment.
  HCMO itself would then assert nothing about `sosa:*`, which removes the
  "ontology hijacking" concern from HCMO. The paper also argues for reuse over
  minting.
- **Decision 3: the chain includes Sensor.** The published route entails
  `sosa:Sensor ⊑ material entity`, which is the statement the sheet rejected,
  and it cannot be cherry-picked out. The paper answers the software-sensor
  objection with *running* software: the sensor is the executing, material
  realisation, and the software (an ICE) is what it concretises. The probe
  shows this pattern is consistent in HCMO. Adopting the chain therefore means
  adopting that pattern for HCM video-tracking pipelines. The sheet's
  objection remains valid for data that types a `hcm-tech:Software`
  individual as a sensor. The two rejected statements now differ:
  - **Sensor:** the paper argues the case, and the result depends on how we
    model software sensors.
  - **Result:** the chain supports the sheet. It entails only *continuant*,
    which is sound, so the ICE claim should stay rejected.
- **Decision 4:** the chain gives `ObservableProperty ⊑ continuant`, which is
  compatible with the proposed SDC bucket and with HCMO's current `quality`
  parent.
- **Decision 7:** closed by the chain with no change to HCMO modules, as
  predicted.
- **Decision 8: the stated rationale is contradicted.** The sheet calls PROV-O
  "an orthogonal view … not a competing classification". The paper treats
  PROV-O as interpretable in BFO, with `prov:Activity ≡ process`. Under this
  alignment, the double parent of Operational Assessment and Calibration
  Activity (`BFO:0000015`, `prov:Activity`) is simply redundant: both parents
  are the same class. The recommendation (out of scope) can stand, but the
  reason should become "already resolved by a published alignment", not
  "orthogonal".
- **Decision 9:** not settled by the paper. The SOSA→PROV alignment it relies
  on is in the 2017 Recommendation, which matches our pin.
- **New constraint surfaced:** `sosa:hasFeatureOfInterest ⊑ prov:used ⊑ has
  participant` makes every feature of interest a non-spatial-region continuant
  that participates in the observation. HCMO's own restrictions use
  `hcm-bio:Subject`, which is fine. But data that sets a behavioural *bout* (a
  process) as the feature of interest would become inconsistent. This is worth
  a SHACL check or a modelling note before any bridge ships.
- **Default vs. developer profile divergence.** Any bridge should be tested
  under the developer profile, because the default presentation hides
  ICE/material-entity clashes.

### Method ideas to adopt, whatever is decided

1. Add a **conservativity check** to `tooling/validate.py` for any bridge
   profile. It would verify that no new subsumption appears between two HCMO
   terms or two SOSA terms.
2. Add **example consistency under the bridge**. The paper's 312-instance check
   corresponds to running `examples/` plus targeted probes like the ones above.
3. Give each bridge axiom the **paper's annotation pattern**: a reified
   `owl:Axiom` with `sssom:object_label`, an `rdfs:comment` justification and
   target versions. Export it to `mappings/semantic/` as SSSOM with
   `semapv:ManualMappingCuration`.
4. A **totality/coverage query** could report which SOSA terms used by HCMO
   still lack a BFO anchor.

### Caveats

- The SOSA→PROV alignment is **non-normative** in the SSN Recommendation.
- PROV-to-BFO targets BFO release 2024-01-29, while we pin a different BFO
  commit. The IRIs are the same, but the axioms were not diffed.
- SWRL location rules were dropped. HermiT ran via owlready2, not ROBOT. Only
  the BFO file was loaded, not the CCO or RO files.
- The probes are illustrative individuals, not HCMO shapes.

## Appendix: SOSA → PROV axioms used (SSN Rec. §6.5)

Shorthand, not valid Turtle: comma-separated subjects share the axiom.

```text
sosa:Observation, sosa:Actuation, sosa:Sampling  rdfs:subClassOf prov:Activity .
sosa:Sensor, sosa:Actuator, sosa:Sampler         rdfs:subClassOf prov:Agent , prov:Entity .
sosa:Procedure                                   rdfs:subClassOf prov:Plan .
sosa:FeatureOfInterest, sosa:ObservableProperty,
sosa:Platform, sosa:Result, sosa:Sample          rdfs:subClassOf prov:Entity .
sosa:madeBySensor, sosa:madeByActuator,
sosa:madeBySampler, sosa:invokedBy               rdfs:subPropertyOf prov:wasAssociatedWith .
sosa:hasFeatureOfInterest                        rdfs:subPropertyOf prov:used .
sosa:hasResult                                   rdfs:subPropertyOf prov:generated .
sosa:isResultOf                                  rdfs:subPropertyOf prov:wasGeneratedBy .
sosa:isSampleOf                                  rdfs:subPropertyOf prov:wasDerivedFrom .
# (sosa:resultTime ⊑ prov:endedAtTime and the sp:eventAssociation /
#  sp:hadProcedure property chain were not used in the experiment.)
```
