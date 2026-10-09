# ADR-0005 evidence audit

Audit date: 2026-10-06 (Europe/Paris). Status: evidence for a proposed ADR, not acceptance or implementation. The current working tree is audited, not the historical v0.3.0 tag; its manifest still says 0.3.0. Only this uncommitted report was created in the repository.

**Evidence convention:** VERIFIED FACT means inspected source, parsed assertions or a specified experiment. JUDGMENT means interpretation/recommendation. UNVERIFIED means the experiment does not establish the claim. Repository paths are relative; `scratch:` denotes `C:/Users/damie/AppData/Local/Temp/hcmo-adr0005-audit-20261006`. Source hashes, scripts and detailed inventories follow. Anonymous RDF identifiers are parse-local, not new ontology terms. Probe IRIs are disposable individuals only.

## 1. Executive summary

1. **VERIFIED FACT:** four source pins match; dependency counts need corrections; scratch-copy build/validation pass (A, D, G).
2. **VERIFIED FACT:** published PROV–BFO TTL fails parsing; successful chain tests require a disclosed scratch-only prefix repair (E).
3. **VERIFIED FACT:** repaired chains with full pinned BFO/IAO have no unsatisfiable classes; all nine TTL examples are consistent; within-vocabulary named subsumption deltas are zero (E).
4. **JUDGMENT — Actuator:** retain local specialisation; accept material placement via a repaired, pinned opt-in chain; **high** conditional confidence (A/E).
5. **JUDGMENT — Observation:** accept opt-in process placement after artifact repair is governed; **high** confidence (E).
6. **JUDGMENT — Sensor:** accept only after authors approve a material-carrier/code pattern; **medium** suitability confidence, high confidence in the clash (B/E).
7. **JUDGMENT — Result:** reject global information placement; retain local ObservationResult and generic chain continuant placement; **high** confidence (C/E).
8. **JUDGMENT — ObservableProperty:** keep chain continuant consequence; defer stronger SDC axiom; **medium** confidence (E/F).
9. **UNVERIFIED:** unmodified-chain execution, production import portability and full optional RO/CCO composition (D/E).
10. **JUDGMENT:** keep ADR proposed pending artifact, modelling and author decisions; retain 2017 edition policy (F/G).

## 2. Recomputed facts versus ADR claims

Counts are graph counts unless labelled lexical. Domain/range counts include object and datatype properties. Membership in a union does not entail membership in each union class.

| ADR claim | Recomputed result | Evidence |
|---|---|---|
| Sensor domain: 7 | 7 direct; **plus 6 union-domain dependencies = 13** | Appendix A; `hcm-tech.ttl:75–169,188` |
| Sensor range: 2 | 2 direct; **plus 1 union-range dependency = 3** | Appendix A; `hcm-tech.ttl:140,164,183` |
| Sensor: 3 SHACL shapes | 3 named shapes reference the class; **only 1 targets it** | `shapes/hcm-shapes.ttl:15,26,230,231,278,310` |
| Sensor: 7 example graphs | **6 TTL files explicitly name the class: 5 root examples + canonical fixture. Seven files only if duplicate JSON serialisation is counted.** Property-expanded use adds `abox-inferred-invalid.ttl` | Appendices A/B |
| EnvironmentalProperty range: 7 | **8: seven deprecated properties plus active specifiesProperty** | `hcm-env.ttl:17–75,171–175`; Appendix A |
| ObservationResult: 4 subclasses | Confirmed, 4 direct named subclasses | `hcm-obs.ttl:32,37,66,149` |
| Actuator: several dependent properties | Confirmed: 3 distinct properties | `hcm-tech.ttl:81,163,164,173–177` |
| Four observations have no BFO parentage | Confirmed in current default/developer source hierarchy | Appendices A/B |
| Software already information | Direct Software subclass of IAO:0000030 | `hcm-tech.ttl:32–35` |
| Developer profile exposes Software/Sensor clash | **Both modes expose it when full BFO/IAO are loaded**, as required by this audit | E probe table |
| SOSA 2017: 345 triples, zero disjointness | Confirmed: 345, disjointWith 0, AllDisjointClasses 0 | D/F, checksum and reproduction command |
| BFO drift / potentially missing terms | 1014 vs 1015 triples; **no BFO IRI absent**; graph differences only versionIRI, definitions, scope notes | D; BFO diff outputs |
| Published chain ready to import | **Tagged and main PROV–BFO TTL fail on undeclared `:`; `xsd:` also missing; `rdfs:comment:` typo obstructs RDF/XML serialization** | E; upstream lines 147,319,323 |
| SOSA 2017 Actuator explicitly covers software/other systems | **Not stated by its device definition**; don't attribute later-edition wording to 2017 | `scratch:sosa-2017.ttl:177`; ADR:47,113 |
| ObservableProperty definition establishes dispositions/functions | **Not established by pinned definition**, which speaks of quality/property/characteristic | `scratch:sosa-2017.ttl:56`; ADR:105 |
| 2023 disjointness unknown | Inspected current core has **none on requested classes**; SSN aggregate has 12 directed collection-disjoint triples | F / Appendix F |
| No local process class | **False already:** OperationalAssessment and CalibrationActivity have BFO process parents | `docs/UPPER-LEVEL-VIEW.md:34`; `hcm-core.ttl:108–111`; `hcm-tech.ttl:42–45` |

## 3. Findings A–G

### A. Parents, dependencies and specialisations

**VERIFIED FACT:** named direct parents are identical under default and additive developer presentations:

| Class | Named direct parents | Developer ancestor refinement |
|---|---|---|
| hcm-tech:Sensor | BFO:0000040, sosa:Sensor | independent continuant → continuant → entity |
| hcm-tech:Actuator | BFO:0000040, sosa:Actuator | same |
| hcm-obs:ObservationResult | IAO:0000030, sosa:Result | generically dependent continuant → continuant → entity |
| hcm-env:EnvironmentalProperty | BFO:0000019, sosa:ObservableProperty | specifically dependent continuant → continuant → entity |
| Behavior/Weight/HealthStatus/EnvironmentObservation | sosa:Observation each | none gains BFO ancestry |

Evidence: `ontology/modules/hcm-tech.ttl:22–35`, `hcm-obs.ttl:18–77,157–161`, `hcm-env.ttl:48–52`; developer profile:26–92. Appendices A/B include exact traversal output and **all anonymous restriction parents**. “Observation is the only parent” would be incomplete if intended to include OWL superexpressions. GasConcentrationObservation is an additional indirect subclass (`hcm-obs.ttl:50–53`) and also becomes a process under the chain.

**VERIFIED FACT:** Appendix A individually lists all direct and union-domain/range properties. Actuator depends on `hasActuator` (range), `hasModelNumber` (union domain), `communicatesWith` (both union domain/range). It has no subclass, exact target shape or explicit typed example. DVC uses the shared `communicatesWith` relation (`examples/dvc-tecniplast.ttl:37`), which does not type its endpoints as Actuator.

**VERIFIED FACT:** ObservationResult's direct subclasses are BehaviorResult, CategoricalResult, LocationResultTable, QuantityValue. Its direct-domain property is `hasConfidenceScore`; no direct/union range uses the superclass. Exact superclass absence from examples is not absence of inferred instances: subclasses are used extensively. QuantityValueShape targets a subclass; BehaviorObservationShape and EnvironmentObservationShape constrain result subclasses (`shapes/hcm-shapes.ttl:227,313,327`). EnvironmentalProperty has no exact target; MeasurementSpecificationShape and EnvironmentObservationShape constrain it as a value class (`:213–224`).

**VERIFIED FACT:** Appendices A/B separate exact mentions from dependency-expanded references (descendants and dependent-property uses). Sensor's CQ dependencies are `isa-recording-provenance`, `status-evidence-at-time`, `sensors-behaviors`; EnvironmentalProperty's is `environment-spec-observation`; ObservationResult's includes `social-interaction-partners` through descendant-domain property use. Generic `hasResult` queries also retrieve local results without naming their superclass (`queries/cq-environment-spec-observation.rq:14`, `cq-social-interaction-partners.rq:9`). The fixture query `examples/isa-roundtrip/queries/repeated-observation-counts.rq:7` uses generic feature links. Appendix C inventories these data-pattern dependencies separately; they are not extra explicit class occurrences.

**JUDGMENT — definition-grounded draft specialisation paragraphs:**

- **Sensor:** HCMO's Sensor is a device capturing signals about behaviour, physiology or the enclosure environment. Its material parent restricts it to physical devices; generic SOSA also admits agents/software. Retain that device and subject-matter scope. Evidence: `hcm-tech.ttl:27–30`; pinned SOSA:152.
- **Actuator:** HCMO's Actuator is a device eliciting or perturbing behaviour, physiology or the monitored environment. It adds that scope and explicit material typing to SOSA's general actuation-procedure device definition. Its current definition does not explicitly say “home-cage”; don't substitute future checklist wording for authored content. Evidence: `hcm-tech.ttl:22–25`; pinned SOSA:177.
- **ObservationResult:** HCMO's ObservationResult is an information artifact produced by a home-cage monitoring observation. It adds information-content typing and the HCM context to generic Result; its subclasses refine recorded output forms. A physical specimen can be a generic Result without being ObservationResult. Evidence: `hcm-obs.ttl:157–161,32,37,66,149`; pinned SOSA:344.
- **EnvironmentalProperty:** HCMO's EnvironmentalProperty is an environmental parameter measured, specified or controlled in home-cage monitoring. It adds that environmental/HCM scope and explicit BFO quality placement to the generic observable-property pattern. Evidence: `hcm-env.ttl:48–52`; pinned SOSA:56.

### B. Software sensors and running instances

**VERIFIED FACT:** Software directly subclasses IAO:0000030. The developer projection restores its GDC ancestry, while full IAO supplies it in both chain modes (`hcm-tech.ttl:35`; developer profile:85–89; Appendix A).

**VERIFIED FACT:** one explicitly typed current Software individual occurs in the recursive TTL examples: DVC Analytics. It `runsOn` a separate rack controller, which communicates with physical electrode sensors. No Software individual is also typed Sensor; no explicit running-software Sensor is linked to code. Hardware/analytics separation is not itself the proposed running-instance pattern (`examples/dvc-tecniplast.ttl:28–52`; Appendices A/D). ISA canonical/crate contain no Software assertion; their sensor is a separate device (`canonical.ttl:1928`; crate:4088).

**VERIFIED FACT:** `docs/hcm-systems/CATALOG.md:99–120` distinguishes software layers from cage hardware and lists DeepLabCut/3D, DeeperCut, SLEAP, YOLO, SAM, OpenCV, Anipose, DANNCE/s-DANNCE, B-SOiD, VAME, BehaviorFlow, Keypoint-MoSeq, DeepSqueak, LMT USV Toolbox and EzTrack. These descriptions assert neither code/Sensor co-typing nor running instances. Generated systems are SKOS concepts, e.g. Live Mouse Tracker (`vocabularies/systems.ttl:166–173`), not deployed Software/Sensor individuals. Shapes have no Software target (Appendix D searches; source shapes in Appendix A). A catalogue description is not an ABox assertion.

**VERIFIED FACT:** `runsOn` exists, domain Software, range Hardware (`hcm-tech.ttl:191–195`); it does not mean concretization. No deployed-instance class or concretization predicate is authored in active modules. No RO entry is pinned. Full pinned BFO contains `BFO_0000059` concretizes, domain `(process OR specifically dependent continuant)`, range GDC; it is absent from HCMO's used_terms, as is `BFO_0000196` bearer of. Evidence: pin inventory, Appendix D, graph-domain check and `linked_probes.py`.

**JUDGMENT — proposal only:** review an existing-term pattern: material sensor bears a quality, that quality concretizes separate Software/code. If adopted, allowlist the selected existing BFO predicates and govern their source. Direct `material-sensor concretizes code` is inconsistent with this pin; don't introduce that shortcut. If RO is preferred, first choose/pin an RO release and inspect its actual constraints. This audit does not infer RO semantics from BFO labels. Whether a material carrier is the scientifically intended software Sensor is an author decision, not a reasoner result.

### C. Feature-of-interest and Result guards

**VERIFIED FACT:** nine TTL example files contain 62 hasFeatureOfInterest triples and 60 hasResult triples. Appendix A lists every subject/object and asserted filler type. Appendix C inventories all lexical occurrences across examples, JSON fixture, shapes, queries and notes. Canonical contributes 56 of each; JSON repeats exactly the same subject/object IRIs (`scratch:crate-comparison.txt`). Do not count duplicate serialisation as an independent dataset.

**VERIFIED FACT:** asserted features are subjects, enclosures or interacting groups, never a typed bout/interaction process/session. Multi-animal observation-2 concerns dyad-mouse-1-mouse-2; “approach” belongs to its BehaviorResult (`examples/abox-minimal.ttl:102–123`). Social-negative data still uses a material interacting group (`abox-social-invalid.ttl:22–31`). ADR-0006:29–41 chooses group features plus roles. InteractingGroup is material and developer-refined to object aggregate; transience does not make it a process (`hcm-bio.ttl`; developer profile:96–97).

**JUDGMENT:** no present asserted feature is a process, but generic `?foi` queries and cage/group-level modelling notes do not enforce the bridge requirement. Future imported data could use a session/bout. Existing BehaviorObservationShape checks subject/group requirements (`shapes/hcm-shapes.ttl:280–303`), not a universal opt-in guard. Add a profile-scoped guard plus inferred consistency probe; retain subject/group/enclosure versus observed-process distinctions. E's process-feature probe fails in both modes.

**VERIFIED FACT:** all 60 explicit result fillers are BehaviorResult and/or QuantityValue, hence information-content entities. None is an ISA/Bioschemas Sample. Tissue is output through schema:result and prov:generated, not sosa:hasResult (`canonical.ttl:1166–1167,1609`). Some animals also carry Bioschemas Sample typing (`:1834–1911`), but are features, not results. Appendix A enumerates every filler. “Information only” means information-typed and not explicitly material in these data; it is not closed-world completeness of all types.

**JUDGMENT:** no physical result in current examples does not justify making generic Result information-only. The independent physical-Sample probe passes (E).

**VERIFIED FACT — prose-only modelling notes:** the broader phrase search also finds group/subject feature mappings in `docs/MODEL.md:38`, `docs/hcm-systems/systems/live-mouse-tracker/lmt-system-profile.md:132–133`, enclosure/animal choices in `docs/ISA-RO-CRATE-MAPPING.md:35`, and cage/group-level DVC notes (`docs/hcm-systems/systems/DVC_Tecniplast/README.md:65`). None chooses an interaction event or bout as an asserted feature. The old class-audit note (`docs/CLASS-AUDIT-WORKING-NOTES.md:91`) still describes subject-only behaviour features; **JUDGMENT:** qualify that historical note or update its pointer to ADR-0006 so it does not erase the new group case. Full prose search is added in Appendix C; `rg -n -i 'feature.of.interest|behavio.ral bout|social interaction|running software|software sensor' docs README.md -g '*.md' -g '*.tex' -g '!ADR-0005-evidence-audit.md'` reproduces it.

### D. Pins, downloads and BFO comparison

**VERIFIED FACT:** the pin inventory below comes directly from `external-vocabularies.yaml`. Downloaded BFO, IAO, SOSA 2017 and PROV-O all match their expected SHA-256. RO has no contract entry/version/checksum/allowlist. Whole BFO and IAO artifacts have no owl:imports. PROV-O was included explicitly to resolve the W3C alignment's import, as was full pinned SOSA (not SSN's additional axioms). Evidence: download ledger and assembly script.

**VERIFIED FACT:** HCMO pins BFO 2020 ISO projection `bfo/2020/bfo-core.owl`, at commit `dd89f4a193038b66ef0e891d546c05a5b477f40f` (commit date 2026-03-01, metadata in ledger). Do not call this the 2024-01-29 tag. Authors' CC0 mapping version v2025-01-19 names `release-2024-01-29/src/owl/bfo-core.ttl` as source (`scratch:prov-bfo.ttl:14–18`). The target has 1015 triples vs pinned 1014. Canonical graph diff: 995 shared, 19 pin-only, 20 target-only. Differences use only owl:versionIRI, skos:definition, skos:scopeNote; material-entity and continuant-part definitions differ. Structural logical compatibility does not make prose differences irrelevant. Evidence: `compare_reasoning.py`, `bfo-only-pin.nt`, `bfo-only-target.nt`.

**VERIFIED FACT:** all 18 BFO IRIs mentioned by PROV–BFO occur in the pin; none is absent. W3C SOSA–PROV uses no BFO IRI. Appendix E gives the full list. Full-file availability is different from membership in HCMO's short used_terms allowlist; a production profile needs a governed expanded dependency surface.

**VERIFIED FACT:** the [authors' tagged mapping](https://raw.githubusercontent.com/BFO-Mappings/PROV-to-BFO/v2025-01-19/prov-bfo-directmappings.ttl) declares CC0 at line 16. The [W3C alignment](https://www.w3.org/ns/sosa/prov/) is linked from [2017 SSN §6.5](https://www.w3.org/TR/2017/REC-vocab-ssn-20171019/#PROV_Alignment), a non-normative section (`scratch:ssn2017.html:6776`). URLs/date/hashes are in the ledger. Separate authors' RO/CCO mappings and editor file were downloaded for scope inspection, not added silently to the two-alignment chain. Full optional RO/CCO composition is **UNVERIFIED**; it requires an explicitly selected artifact set and repeat tests. There is no full RO pin to add under the question's “if pinned” condition.

### E. Reasoning experiments and limits

**VERIFIED FACT — tooling:** Python 3.12 environment; RDFLib 7.2.1; Owlready2 0.51; bundled HermiT implementation version **1.3.8.1099** (JAR manifest); Java 23.0.2; 2048 MB heap. This reuses `tooling/reason.py:61–65`'s Owlready2/HermiT mechanism, extended in scratch for isolated worlds, ancestry and probes. No ROBOT was used. The paper's ROBOT/HermiT versions are not this audit's versions. Owlready's `--ignoreUnsupportedDatatypes` appears in command logs; this is not general datatype certification.

**VERIFIED FACT — raw artifact blocker:** tagged and main PROV–BFO TTL both fail at line 319: `Prefix ":" not bound`. `xsd:` is also undeclared at line 323. `rdfs:comment:` at line 147 is a distinct IRI that obstructs RDF/XML serialization. No successful unmodified-chain reasoning result exists. Parse failure is not logical inconsistency. Reproduce with RDFLib Graph.parse on the raw download.

**VERIFIED FACT — tested repair:** prepend default-namespace (file base + `#`, for SWRL variables) and xsd declarations, in scratch only. Keep every rule/axiom and the misspelled annotation predicate; serialize N-Triples to avoid the XML QName issue. Load HCMO manifest union + entire pinned SOSA/BFO/IAO/PROV + W3C alignment + prefix-repaired PROV–BFO. Remove the two imports only after explicitly resolving them to pinned inputs, preventing uncontrolled network imports. All six SWRL rule nodes remain in the input. Add the developer projection for mode two. Scripts and hashes identify each variant.

**VERIFIED FACT:** 27 mappings are encoded as owl:Axiom annotations, with no explicit RDF subclass/equivalence mapping triples in the authors' file. The OWL reasoner parsing nevertheless reconstructs their consequences: prefix-only tests infer material Sensor/process Observation. A separate diagnostic asserts missing annotated base triples across the entire assembled graph (29, not 27) and yields identical named ancestor dictionaries. This diagnostic is not silently substituted for the published file and is not needed for the reported prefix-only probes. Raw RDF/SPARQL consumers need a separately reviewed representation strategy. Evidence: `download4.py`, `assemble.py`, `compare_reasoning.py`, result JSONs.

**VERIFIED FACT:** baseline = HCMO plus full pinned BFO/IAO/SOSA/PROV, no alignment; chain = same plus both alignments with disclosed repair. Both modes' baselines/chains have zero named unsatisfiable classes (excluding owl:Nothing). All nine TTL examples individually, including four expected SHACL-negative fixtures, and the positive-example union are OWL-consistent in each mode. SHACL-negative is not synonymous with OWL-inconsistent. Complete per-run table follows.

| Probe | Default + full BFO/IAO | Developer + full BFO/IAO | Interpretation |
|---|---|---|---|
| Same individual Software and SOSA Sensor | inconsistent | inconsistent | information/material clash |
| Separate Software and Sensor, explicitly different | consistent | consistent | separation possible, no link asserted |
| Sensor bears quality concretizing separate code | consistent | consistent | candidate linked pattern |
| Material sensor directly concretizes code | inconsistent | inconsistent | invalid shortcut for this pin |
| Material specimen, SOSA Sample, hasResult filler | consistent | consistent | physical results possible |
| ObservationResult as hasResult filler | consistent | consistent | local information result possible |
| Process as hasFeatureOfInterest filler | inconsistent | inconsistent | continuant guard needed |

**VERIFIED FACT:** within each of HCMO, SOSA and BFO there are **zero new named-class subsumptions** in both modes. Cross-vocabulary placements are intentionally excluded: they are the bridge's purpose. Equal full imports in baseline/chain prevent misattributing import effects to alignment. This meets the finite taxonomy gate; it is **not proof of unrestricted logical conservative extension** (`compare_reasoning.py`, `reasoning-review.txt`).

| Class | Most specific named BFO placement in both modes |
|---|---|
| SOSA Sensor, Actuator, Sampler | material entity 0000040 |
| SOSA Observation, Actuation, Sampling | process 0000015 |
| SOSA Result, ObservableProperty, FeatureOfInterest, Platform, Sample | continuant 0000002 |
| SOSA Procedure | generically dependent continuant 0000031 |
| Four named HCMO observation classes | process 0000015 |
| HCMO GasConcentrationObservation | process 0000015 via EnvironmentObservation |

Evidence: ancestor JSONs and placement appendix. ADR:69–107 placements match this **repaired** graph. Differences/qualifications: raw artifact cannot run; Software clash occurs in both full-closure modes; additional GasConcentrationObservation also gains process placement; existing OperationalAssessment/CalibrationActivity dual anchors become redundant only with the opt-in equivalence. Continuant placement is not equivalence to every continuant: PROV Entity's mapping has a further union excluding spatial-region-only interpretations (`prov-bfo.ttl:24–42`).

**VERIFIED FACT — disjointness:** neither alignment asserts disjointWith/AllDisjointClasses; they activate inherited BFO/IAO/PROV partitions. Appendix E lists **every explicit disjoint axiom** in the input artifacts, including anonymous restrictions/all-disjoint lists. Key partitions are continuant/occurrent; independent/SDC/GDC; material/immaterial; quality/realizable entity; process versus other disjoint occurrent categories; PROV Activity/Entity. Sensor/Actuator/Sampler become disjoint with information Software/results and environmental qualities. Observations become disjoint with continuant features/results. Agent-role existentials also make role/disposition distinctions relevant. IAO prohibits continuants with occurrent parts and conversely. `scratch:reasoning-review.txt` records named descendant-side mappings; listing all explicit axioms does not claim enumeration of every inferred anonymous disjoint expression.

**UNVERIFIED:** production Protege/ROBOT import behaviour, another reasoner version, unrestricted SWRL semantics beyond HermiT's supported interpretation, full optional CCO/RO composition, and the identity of a future corrected upstream release. Verify by locking intended inputs and rerunning this matrix on the production stack. Add explicit location-rule entailment tests if those rules are part of the accepted contract. This audit does not certify an unselected future profile.

### F. SOSA 2017 and the inspected 2023 edition

**VERIFIED FACT:** pinned 2017: 345 triples, disjointWith 0, AllDisjointClasses 0. Sensor definition fragment: “Device, agent (including humans), or software (simulation)” (`sosa-2017.ttl:154`). Result fragment: “The Result of an Observation, Actuation, or act of Sampling.” (`:346`). Actuator is described as a device implementing/used by an actuation procedure; ObservableProperty as observable quality/property/characteristic (`:177,56`). None of those definitions formally equates a class with a BFO category.

**VERIFIED FACT:** the [dated 2023-edition publication](https://www.w3.org/TR/2026/WD-vocab-ssn-2023-20261003/) is a **W3C Working Draft, 3 October 2026**, not a 2023 Recommendation. The primary W3C source snapshot is commit `f657014a0e11e2278d85faba029896a283bafdc3`, dated 2026-10-03. Twelve files under `ssn/rdf/ontology/core/` were fetched with individual hashes. Editor source and published HTML are distinct artifacts; exact release provenance is not assumed beyond recorded identities.

**VERIFIED FACT:** negotiated `/ns/sosa/2023/` returned 345 triples, `/ns/ssn/2023/` 520 importing unversioned SOSA. These are not the modular core files described by the draft; preserve their bytes as sosa2023.ttl/ssn2023.ttl, not evidence that editions are identical. Source aggregate SOSA has 63 triples and SSN 55; their module imports matter (`download3.py`, `external_inspect.py`, ledger).

**VERIFIED FACT:** six SOSA core files and five SSN submodules have zero explicit disjointness. Aggregate `2023-ssn.ttl:78–92` has 12 directed triples: all six unordered pairs among ActuationCollection, ObservationCollection, SampleCollection, SamplingCollection. For **each** requested class—Sensor, Actuator, Sampler, Platform, Observation, Result, ObservableProperty, Property, FeatureOfInterest, Sample, Procedure—explicit disjointness mentioning it is zero across those files. No AllDisjointClasses occurs. This does not claim the same for every older draft, extension or optional alignment. Appendix F lists counts/lines.

**VERIFIED FACT:** new Sensor subclasses System, with definition beginning “System that implements an ObservingProcedure to determine the value of an observable Property” (`2023-sosa-observation.ttl:118–130`). Following prose covers infrastructure, agents and software-based systems/simulations. Result is in the deprecated module, owl:deprecated true (`2023-sosa-deprecated.ttl:87–99`), beginning “outcome of an Observation, Actuation, or act of Sampling.” (`:92`). ObservableProperty is also deprecated (`:62–85`). These changes don't support a Sensor/Result disjointness claim about 2017.

**JUDGMENT:** retain ADR-0002's pin. Ask which exact artifact the co-author's earlier disjointness remark meant; this source inspection cannot establish an unspecified older draft's contents.

### G. Packaging, documentation and quality gates

**VERIFIED FACT:** `hcmo.yaml:22–29` lists seven modules; the developer profile is excluded. `tooling/build.py:55–62` merges only that list, writing the manifest's dist paths (`:166–191`). `tooling/validate.py:53–58` merges the same list; optional-profile parsing/checks do not add it to the canonical union (`tooling/external_vocab.py`). No BFO–SOSA bridge profile exists to certify as isolated. These boundaries permit isolation if a future profile remains outside the manifest.

**JUDGMENT — proposal only:** leave hcmo.yaml shape **and values** unchanged. Give the new profile its own reviewed ontology IRI under the existing profile namespace; do not mint it in this audit. Govern expanded source/term dependencies in external-vocabularies.yaml and resolve imports with a locked local catalogue. Prefer a separate profile build/reason entry point, or an opt-in argument whose outputs cannot collide with dist. Normal build.py need not change; any optional path must preserve its no-argument behaviour. Add separately selected profile validation/reasoning checks in validate.py or a companion, preserving default SHACL/CQ expectations. CI must test both presentations, probes, finite taxonomy deltas and default artifact invariance. SSSOM remains review evidence, not automatically merged axioms.

**VERIFIED FACT:** ALIGNMENTS.md and UPPER-LEVEL-VIEW.md do not exist at root; applicable files are under docs. Recorded searches cover docs, README, CHANGELOG and recursive Overleaf .tex sources. Findings and proposed corrections:

| Location | Finding | Suggested correction (JUDGMENT; not applied) |
|---|---|---|
| `docs/UPPER-LEVEL-VIEW.md:33–35` | No local process class | Name existing OperationalAssessment/CalibrationActivity; distinguish four currently unanchored observation classes |
| Same `:5–6` | No PROV equivalence, unqualified | Scope to default release; optional proposed chain imports an external equivalence |
| `docs/ALIGNMENTS.md:55–56` | Separate provenance view | Qualify default/selective reuse; optional alignment makes Activity/process equivalence executable |
| `docs/PHILIPPE-ROCCA-SERRA-FEEDBACK.md:72` | Cross-cutting PROV | Add default-versus-optional qualifier, preserving historical feedback |
| Review checklist `:390,749,1294` | Provisional cross-cutting provenance | Preserve provisional/historical status; pointer to bridge commitments |
| Review checklist `:99,299` | Retains physical local Actuator, future wording | Consistent retention; distinguish future definition from current source; qualify software breadth by edition |
| ADR-0005 `:47,105,113–116,134–136` | Unsupported definition breadth, stale totals, undifferentiated drift | Exact edits listed at report end |
| `docs/BACKLOG.md:59–72` | Future guard/redundancy work | Keep future tense; cite repaired-input matrix, not raw import success |
| `docs/paper/TODO.md:15,107` | Historical retirement error and correction | Preserve history, mark old retirement proposal superseded |
| `docs/paper/overleaf/sections/04-hcmo.tex:30` | Device/event/result separation | Compatible; added software example needs explicit code/carrier distinction |
| Same `:32` | Selective reuse, 2017 pin, not full imports | Correct for default; any bridge description must remain separate/proposed |
| `docs/paper/overleaf/sections/07-discussion.tex:6` | Bridge modules future work | Keep proposed/future until accepted and implemented |
| README, CHANGELOG, remaining .tex search hits | No current instruction to retire local Actuator or implemented unconditional SOSA/BFO bridge found | No bridge-driven rewrite justified by these searches |

The review-checklist path above abbreviates `docs/PHILIPPE-ROCCA-SERRA-HUMAN-REVIEW-CHECKLIST.md`. Historical TODOs are not current axiom instructions. Source search outputs are retained in scratch; exact commands below.

**VERIFIED FACT:** tracked files were copied outside the repo. Build ran twice then validation there: exit 0/0/0; PASS. All four dist hashes match each other across builds **and the original repository bytes**. Ontology union 1454 triples; CQ graph 1860. No original-worktree build or commit was made. Logs/hashes follow.

**JUDGMENT — PR-ready CHANGELOG entry, not applied:** under `### Documentation`: “Audit the proposed optional BFO/SOSA bridge against pinned sources, recomputed dependencies and isolated reasoning probes; record artifact blockers, software-carrier and feature-of-interest constraints, and edition evidence. No ontology axioms, IRIs or release artifacts changed.” No Renamed section: nothing moved/renamed.

## 4. Decision table

| Decision | Options (2–3) | Recommendation (JUDGMENT) | Evidence | What changes it |
|---|---|---|---|---|
| Artifact | Raw import; corrected upstream pin; governed local normalization | Obtain corrected immutable pin; normalization only explicitly governed | E parse failure/diagnostic | Valid upstream release on production stack |
| Actuator | Retain local; generic only; deprecate with migration | Retain and conditional material chain placement | A/E | Definition-level equivalence plus migration coverage |
| Observation | Opt-in chain; direct reviewed bridge; documentation only | Chain after artifact gate | A/E | Process-incompatible real case or failed inference |
| Sensor | Carrier reading; separately named curated profile omitting mapping; defer | Conditional carrier acceptance, otherwise defer | B/E | Author-approved real software example |
| Result | Generic continuant; generic information; only local information without chain | Chain continuant plus retained local information class | C/E | Approved scope excludes all physical generic Results |
| ObservableProperty | Chain continuant; stronger SDC; quality | Chain only; defer stronger axiom | E/F | Source justification and agreed semantics |
| Feature guard | SHACL plus OWL; note only; revise mapping scope for process features | Guard, note and consistency probe | C/E | Accepted real process-feature requirement |
| Code link | runsOn only; BFO bearer/quality/concretizes; independently pinned RO | Review BFO pattern; runsOn isn't concretization | B/E | Better existing relation with verified constraints |
| Edition | 2017; separate 2023 migration; mixed editions | Keep 2017, never mix accidentally | D/F | New ADR and migration tests |
| Packaging | Separate profile/companion; isolated opt-in CLI; manifest merge | Separate locked profile and gates | G | Accepted release-scope/version change |

## 5. Blockers and risks before acceptance

- **VERIFIED:** raw PROV–BFO artifact does not parse; repaired success must not be presented as raw-source success (E).
- **JUDGMENT:** authors must accept material carrier distinct from code and execution process; no domain-approved linked software-sensor example exists (B/E).
- **VERIFIED:** no current concretization allowlist/pattern or universal feature guard; direct material-concretizes shortcut fails (B/C/E).
- **JUDGMENT:** review changed BFO definitions despite matching structural axioms/IRIs. IAO embeds its own BFO/RO-namespaced axioms, included whole here; that is not a separately pinned full RO release (D/E).
- **UNVERIFIED:** full optional CCO/RO composition and production-stack portability; decide whether they are required profile dependencies (D/E).
- **VERIFIED:** 2023-resolving URLs don't supply the inspected modular source graphs; lock immutable inputs (F).
- **UNVERIFIED:** private decision sheets and exact older disjointness artifact were not supplied; obtain actual file/hash rather than reconstructing private results (ADR:83–91; F).
- **JUDGMENT:** technical results cannot replace remaining author votes; preserve vote record and explicitly settle scope (ADR:140–155).

## 6. Reproduction

The original audit appendices (property inventories, download ledger, per-run
reasoner output, embedded scripts, line-level search hits) are not kept in the
repository; they are long and regenerable. References to "Appendix A–F" in
sections 2–5 point to that material. The checks are re-run by
`tooling/bridge_profile.py` (branch `feat/bfo-sosa-bridge-profile`), which
downloads the pinned inputs, verifies their SHA-256, builds the chain graphs and
runs the probes, taxonomy comparison and disjointness inventory.

The audit ran in a scratch directory outside the repository; all 253 tracked
files were byte-identical afterwards (HEAD `535120d`).


## Proposed ADR-0005 edits (applied to the ADR on 2026-10-06)

1. **Context / Decision 1:** retain reuse/opt-in intent; replace implied ready-to-import status with the raw TTL parse blocker. Specify tagged artifact/hash, W3C alignment hash, full pinned BFO/IAO/PROV/SOSA closure and corrected-upstream or explicitly governed normalization policy. Keep W3C non-normative status next to the commitment.
2. **Decision 3:** replace loose “running software (a material entity)” with a conditional material-carrier commitment, distinct from code and execution process. Add the tested bearer/quality/concretizes candidate, pending scientific approval and allowlisting; reject direct material concretizes code under this pin. Do not change Software's IRI/parent.
3. **Decision 4 / table C:** retain all four classes; replace unsupported 2017 Actuator-software breadth with authored behavioural/physiological/environmental device scope. Insert A's four definition-grounded paragraphs. Correct Sensor to direct 7/2 plus union 6/1, three referencing shapes but one target, six explicit-class TTL files plus duplicate JSON; report the seventh dependency-bearing TTL separately. Correct EnvironmentalProperty to eight ranges, seven deprecated and one active.
4. **Decision 5 / open question:** replace “2023 still to be checked” with the dated 2026-10-03 Working Draft/source commit, zero disjointness on requested classes and collection-disjointness finding. Record deprecations/URL ambiguity. Preserve ADR-0002 and ask which earlier artifact motivated the remark.
5. **Decision 6:** specify equal full-closure aligned/unaligned baselines, finite within-namespace named-taxonomy comparison and parse/import integrity gate. State Software clash occurs in both full-closure modes. Distinguish SHACL-negative from inconsistent OWL probes; lock production tool versions/configuration.
6. **Expected consequences / tables A–B:** label placements verified only on disclosed prefix-repaired graph. Keep Observation process, Sensor/Actuator material, generic Result/ObservableProperty continuant, Procedure GDC; add indirect GasConcentrationObservation. Remove unsupported assertion that the pinned ObservableProperty definition establishes dispositions/functions. Leave SDC open pending source/author rationale. Replace “mouse the feature” with subject/group/enclosure as appropriate, distinct from process/bout.
7. **Discrepancies:** replace vague BFO drift with commit/tag comparison, zero missing BFO IRIs and annotation/version differences. State full IAO inclusion and the untested optional CCO/RO configuration; decide whether those are acceptance requirements. Cite this variant matrix instead of raw-source test success.
8. **Packaging / consequences:** require separate reviewed profile IRI/import lock and default-artifact invariance; preserve hcmo.yaml shape/values. Add source repair, software pattern, feature guard and production-stack replay as technical acceptance gates. Preserve recorded votes; this audit supplies none. Link this report.

## Questions only the co-authors can settle

- Is the intended software Sensor a particular material carrier, abstract code/algorithm, or execution process? Is the tested linked pattern scientifically acceptable for an actual HCM software toolchain?
- Which exact edition/file/hash motivated the disjointness concern: an older working draft, SSN, optional alignment or BFO closure?
- Must external process/bout/session features remain usable, or can the profile require continuant subjects/groups/enclosures and keep the observed process distinct?
- Is the intended chain only SOSA–PROV plus PROV–BFO, or also separate RO/CCO mappings and location-rule commitments? What production reasoning stack is normative?
- What source and intended semantics justify a global SDC ObservableProperty commitment beyond the verified continuant consequence?
- Once technical gates are met, do the remaining authors accept these opt-in commitments and the distinction between physical specimens and local information results? No votes are inferred here.
