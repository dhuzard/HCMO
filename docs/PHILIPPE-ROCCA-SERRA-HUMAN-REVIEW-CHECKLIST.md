# Philippe Rocca-Serra feedback: human review checklist

Source: [meeting notes](meetings/PHILIPPE-ROCCA-SERRA-HCMO-NOTES.md)

Related existing records:
[feedback implementation record](PHILIPPE-ROCCA-SERRA-FEEDBACK.md) and
[ISA/RO-Crate design note](ISA-RO-CRATE-MAPPING.md)

Prepared against: HCMO 0.2.0 on 2026-07-20

## Purpose and review rule

This checklist converts the meeting notes into reviewable decisions and exact
repository work. It is not authority to add, rename, merge, or reclassify an
ontology term. A reviewer must record an accepted decision and its semantic
rationale before an ontology action is implemented.

Use these marks:

- `[ ]` not reviewed;
- `[?]` needs source material or expert decision;
- `[x]` accepted and verified; and
- `[~]` rejected or deferred, with the reason recorded.

For each item, record the reviewer, date, decision, rationale, evidence link,
and follow-up issue or pull request in the review record at the end of this
document.

## Current repository facts

These facts prevent the meeting observations from being applied mechanically to
an ontology that has changed since the reviewed file was produced.

- The active source is `ontology/modules/*.ttl`; `ontology/legacy/` and
  `ontology/v2/` are historical and are not merged by `hcmo.yaml`.
- The active graph has 29 HCMO classes, 32 HCMO object properties, and 49 HCMO
  datatype properties.
- The generated profile audit reports no missing active labels, definitions,
  property domains, property ranges, or class anchors. The human task is to
  verify semantic correctness, not merely presence.
- The active graph has no `owl:imports`. It references BFO, IAO, SOSA, and
  Schema.org terms by IRI.
- The external axiom targets currently lacking labels in the merged graph are
  `BFO_0000019`, `BFO_0000027`, `BFO_0000040`, `IAO_0000030`,
  `sosa:Actuator`, `sosa:Observation`, `sosa:Property`, `sosa:Result`,
  `sosa:Sensor`, `sosa:observes`, and `schema:Place`.
- HCMO has no active local `Person` class. `schema:Person` is used only for
  contributor instances in the ontology header.
- HCMO has no active local `Place` class. `hcm:locatedIn` currently has
  `schema:Place` as its range.
- There is one active actuator class, `hcm-tech:Actuator`, anchored to
  `BFO_0000040` and `sosa:Actuator`. `hcm:Actuator` is retained in
  `hcm-compat.ttl` as a deprecated 0.0.1 IRI with an explicit replacement. It
  must not be deleted as a supposed duplicate.
- The existing ISA RO-Crate work is a design note and an RDF bridge example;
  it is not yet a declared, validated ISA RO-Crate profile.
- No active HCMO mappings to OBI, PROV-O, STATO, SKOS, or Wikidata were found.

## A. Architecture and class hierarchy

| Done | ID | Item and description | Human review action | What and where to change after approval | Acceptance evidence |
| --- | --- | --- | --- | --- | --- |
| [?] | A01 | **Readable upper-level presentation: provisionally accepted; co-author review pending.** Reuse authoritative external upper-level classes directly and include a curated, versioned annotation and hierarchy subset so Protégé renders readable names. Create a local HCMO upper class only when it is narrower than, or meaningfully different from, the external class. | Co-authors must validate or challenge the proposed structure below, identify the exact external IRIs and versions, and approve each asserted hierarchy or mapping relation. | No ontology implementation is authorized yet. After approval, add the curated external subset through the reviewed module/import strategy; document it in `docs/ARCHITECTURE.md` and `docs/ALIGNMENTS.md`; update owning modules only for approved hierarchy changes; regenerate `dist/`. | Co-author decision record; source and version for every external term; readable Protégé hierarchy; reasoner result with no unintended equivalences or unsatisfiable classes. |
| [?] | A02 | **Provisional process architecture; external review pending.** Reuse authoritative process classes directly when their meaning matches HCMO and keep semantic, provenance, and exchange layers distinct. | Co-authors and external reviewers must validate or challenge the proposed architecture below, identify exact external IRIs and versions, approve mapping strengths, and settle the ISA round-trip policy for housing assignments and non-file statistical results. | No ontology implementation is authorized yet. After approval, record the policy in `docs/ARCHITECTURE.md` and `docs/ALIGNMENTS.md`; put any approved HCMO specialization in its owning module; add examples, shapes, and competency questions; regenerate `dist/`. | Reviewer-approved term/mapping table; acyclic example workflow with explicit inputs and outputs; resolved ISA extension policy; at least one process competency question. |
| [x] | A03 | **Separate person identity, provenance responsibility, and contributor credit: accepted.** Use `schema:Person` for ISA/Bioschemas exchange, `prov:Person` and `prov:Agent` for provenance, and CRediT through qualified PROV relations for contributor credit. Do not create a local `hcm:Person`. | Preserve the distinctions in the accepted decision below. Before implementation, pin the external versions and identifiers and review every operational role whose meaning is narrower than CRediT. | No ontology class change is authorized. Current Schema.org contributor metadata remains in `ontology/modules/hcm-core.ttl`. Future provenance and contribution examples belong in `examples/`; approved mappings in `docs/ALIGNMENTS.md` or the mapping registry; requirements in `shapes/` and `queries/`; paper attribution guidance in `docs/paper/`. | Decision record below; no active `hcm:Person`; a future example distinguishes person, agent, association/attribution, CRediT contribution role, and any precise operational role. |
| [x] | A04 | **Broad exchange-level Place with separate material, spatial, and identifier semantics: accepted.** Do not create `hcm:Place`. Retain `schema:Place` as the broad range of `hcm:locatedIn`, without equating it to a BFO site, spatial region, or material entity. Keep institutes/organizations, physical facilities, spatial sites, and geometries distinct. | Preserve the accepted distinctions below. Select authoritative facility/site/geospatial classes only after definition review. Use a globally resolvable organization identifier, preferably ROR where eligible, and a GeoNames IRI for the corresponding geographic place where an appropriate record exists; never treat those identifiers as identifying the same entity. | No immediate ontology axiom change is authorized. Record identifier and mapping rules in `docs/ALIGNMENTS.md` or the mapping registry; add organization/place/facility examples and competency questions before specializing `hcm:locatedIn`; update `ontology/modules/hcm-core.ttl`, shapes, context, and generated artifacts only if the approved examples demonstrate a need. | Decision record below; examples distinguish organization, physical facility, BFO site/spatial entity, and geometry; ROR and GeoNames identifiers resolve to the correct separate entities; no unintended type inference from `hcm:locatedIn`. |
| [x] | A05 | **Retain the local physical HCM actuator specialization and model actuations and triggers explicitly: accepted.** `hcm-tech:Actuator` remains the physical, home-cage-specific subclass of BFO Material entity and `sosa:Actuator`; the broader SOSA class may also cover software and other systems. Keep the deprecated migration IRI. | Preserve the device/action/property/execution distinctions below. Before implementation, approve competency questions for physical state change, system reconfiguration, and triggering; pin the SOSA version; and select an explicit relation for each triggered execution rather than treating the actuator as the event. | The accepted future definition belongs in `ontology/modules/hcm-tech.ttl` without changing its IRI. Retain `hcm:Actuator` in `ontology/modules/hcm-compat.ttl`. Add approved SOSA actuation relations, physical and software-controller examples, shapes, queries, documentation, and regenerated `dist/` only in an implementation change. | Decision record below; active and deprecated IRIs remain distinguishable; examples distinguish physical actuator, software controller, actuation, acted-on property, and triggered execution; reasoner and SHACL tests reject physical typing of software-only controllers. |
| [x] | A06 | **Require an evidence-based inventory review before implementing further hierarchy or mapping changes: accepted.** Audit every active HCMO class and every external class directly used as an anchor. The audit is a decision gate, not authorization for bulk changes. | For each term, record IRI, label, definition, module, asserted and inferred parents, restrictions, intended upper category, external source/version, mapping status, provenance, competency questions, and reviewer decision. Classify it as `keep`, `revise definition`, `revise axiom`, `map`, `deprecate`, or `needs evidence`. | Generate the active-term review source from `dist/profile.json` and supplement it with directly referenced external anchors. Store the signed audit under `docs/` or another approved review path. Apply each accepted semantic change separately in its owning source module with examples, reasoning, validation, generated artifacts, and changelog evidence. | Complete signed inventory; separate decision/evidence for every non-`keep` row; no bulk label, hierarchy, equivalence, or deprecation edit; external anchors included despite their intentional exclusion from `dist/profile.json`. |
| [?] | A07 | **Preserve historical ontology artifacts as immutable evidence and exclude them from the active release: accepted; reviewed artifact identification pending.** `ontology/legacy/` and `ontology/v2/` remain historical and must not be edited to resemble the active ontology or used as the canonical Protégé entry point. | Obtain and record the exact file/version Philippe reviewed, its checksum, and the tool/view used; reproduce each finding against the current generated release and classify it as active, compatibility-only, or historical. | No historical ontology edit is authorized. Keep `ontology/modules/*.ttl` as the hand-authored source and `dist/hcmo.owl` / `dist/hcmo.ttl` as generated load targets. Put corrections in the owning active module or, for published migration IRIs, `ontology/modules/hcm-compat.ttl`; clarify canonical load instructions and preserve the historical inventory. | Accepted preservation policy; exact reviewed artifact and checksum; finding-classification table; historical paths remain excluded from `hcmo.yaml`; current release rebuild and validation pass. |

### A01 provisional decision and discussion structure

Status: provisional direction recorded on 2026-07-21; final approval is deferred
until co-authors have validated, challenged, or revised it. This record does not
authorize new classes, mappings, or hierarchy axioms.

Provisional decision:

> Reuse authoritative external upper-level classes directly. Include a curated,
> versioned subset of their labels, definitions, hierarchy, synonyms, and
> provenance in the HCMO release so Protégé renders readable names. Create a
> local HCMO upper class only when it is narrower than, or meaningfully
> different from, the external class.

Suggested structure to discuss, validate, or challenge:

```text
owl:Thing
├── Material entity
│   ├── Subject
│   ├── Enclosure
│   ├── Facility
│   ├── Building
│   ├── Rack
│   ├── Sensor
│   └── Actuator
├── Process entity
│   ├── Housing process
│   ├── Recording process
│   └── Data-processing process
├── Information entity
│   ├── Housing assignment
│   ├── Dataset
│   ├── Specification
│   └── Result
├── Quality / property entity
│   ├── Temperature
│   ├── Humidity
│   └── Light intensity
└── Immaterial / spatial entity
    ├── Site
    └── Spatial region

Exchange typing (not an upper-ontology branch)
└── schema:Place
```

Co-author validation must settle the following before implementation:

1. Select the authoritative external class and ontology version represented by
   each displayed upper-level label.
2. Confirm whether each HCMO class is a direct subclass of the external class or
   needs a more specific intermediate class.
3. Distinguish exact class equivalence (`owl:equivalentClass`), narrower meaning
   (`rdfs:subClassOf`), and non-logical correspondence (`skos:exactMatch` or
   `skos:closeMatch`). Do not use `owl:sameAs` for class equivalence.
4. Validate whether observation and recording entities are processes and how
   planned protocols differ from executed processes.
5. Validate which datasets, specifications, assignments, and results qualify as
   information-content entities.
6. Distinguish BFO qualities from SOSA observable properties before approving
   the Quality / property branch.
7. Apply the accepted A04 distinction: Facility, Building, and Rack are material;
   Site and Spatial region are immaterial/spatial; `schema:Place` is a broad
   exchange type rather than their shared upper-ontology class.
8. Confirm that the selected curated subset renders the proposed hierarchy in
   Protégé without requiring full external-ontology imports.

### A02 provisional decision and compatibility review

Status: provisional direction recorded on 2026-07-21; final approval is deferred
until co-authors and relevant external experts have validated, challenged, or
revised it. This record does not authorize new process classes, imports,
mappings, or hierarchy axioms.

Provisional decision:

> **A02 — provisional process architecture; external review pending.**
> Reuse authoritative process classes directly when their meaning matches HCMO.
> Use BFO as the upper process anchor; OBI for protocol-driven processes,
> specified inputs/outputs, data transformations, study design, and experimental
> assignment; SOSA for sensing procedures and executions; STATO for specific
> statistical methods, variables, models, and statistical outputs; and PROV-O
> for execution provenance.
>
> Treat ISA Process / Bioschemas LabProcess as the exchange representation of an
> executed process, not as HCMO's upper ontology. Keep protocol or plan, executed
> process, and generated record/data/result as distinct entities. Create a local
> HCMO process class only when it describes a narrower home-cage-specific process.
>
> ISA/STATO compatibility must be demonstrated with an acyclic workflow
> containing explicit inputs and outputs. Housing-assignment records and non-file
> statistical result entities require an HCMO extension and an agreed ISA
> round-trip policy before conformance is claimed.

The standards audit, compatibility findings, unresolved boundaries, candidate
mappings, and repository work proposed for later implementation are recorded in
[`A02-ISA-STATO-COMPATIBILITY.md`](A02-ISA-STATO-COMPATIBILITY.md). They remain
future work and are not ontology assertions.

### A03 accepted decision and implementation boundary

Status: accepted by Damien Huzard on 2026-07-21. This is a modeling and reuse
policy. It does not authorize a local Person class, external imports, mapping
axioms, or new operational-role terms.

Decision:

> **A03 — separate person identity, provenance responsibility, and contributor
> credit.**
> Represent a human contributor with `schema:Person` for ISA/Bioschemas exchange
> and `prov:Person` for provenance; `prov:Person` is a kind of `prov:Agent`. Use
> qualified PROV associations and attributions to connect the person to executed
> processes and generated entities.
>
> Use official CRediT roles through `prov:hadRole` when describing contributions
> to the study, dataset, software, analysis, or publication. Do not treat CRediT
> roles as person classes or substitutes for `prov:Agent`, and do not use them
> for precise operational responsibilities when their definitions are too broad.
>
> Do not create a local `hcm:Person` class. Create or reuse narrower operational
> role terms only when required by an approved competency question.

Implementation must preserve these distinctions:

- [`schema:Person`](https://schema.org/Person) is the ISA/Bioschemas exchange
  type; it is not asserted as an HCMO material-entity superclass.
- [`prov:Person`](https://www.w3.org/TR/prov-o/#Person) identifies a person in
  provenance and is a subclass of `prov:Agent`.
- `prov:qualifiedAssociation` relates an executed activity to an agent and may
  carry `prov:hadRole`; `prov:qualifiedAttribution` provides the corresponding
  qualified attribution for a generated entity.
- [CRediT](https://credit.niso.org/contributor-roles/) supplies scholarly
  contribution categories, not person classes and not automatically the precise
  operational role performed in an HCM workflow.
- The external source/version, official CRediT role identifier, mapping status,
  reviewer, and evidence must be recorded before an RDF example or application
  profile treats a role mapping as approved.

### A04 accepted decision and identifier boundary

Status: accepted by Damien Huzard on 2026-07-21. The category and identifier
policy is settled; exact external facility/site classes and any property
specializations remain subject to competency questions and mapping review. No
ontology axiom change is authorized by this record.

Decision:

> **A04 — retain a broad exchange-level Place while separating material
> containment, immaterial sites, and geometry.**
> Do not create a local `hcm:Place` class. Retain `schema:Place` as the broad
> range of `hcm:locatedIn` for exchange and metadata, but do not assert that
> `schema:Place` is equivalent to a BFO site, spatial region, or material entity.
>
> Represent a facility, building, rack, or other physical container as a
> material entity using an authoritative external class selected after review.
> Represent an interior space or occupied site with an appropriate BFO
> site/spatial term. Represent coordinates and geometry separately using a
> geospatial vocabulary when required.
>
> A Facility must not be placed beneath Spatial entity merely for display: the
> facility is physical, while its site or spatial region is immaterial. One
> real-world location resource may have an exchange type such as `schema:Place`
> alongside a more precise semantic type. Split or specialize `hcm:locatedIn`
> only when an approved competency question requires distinctions that the
> current broad relation cannot answer.
>
> An institute should have a globally unique, resolvable organization identifier,
> preferably a [ROR](https://ror.org/) identifier when the organization is in
> ROR. Its corresponding geographic place should use a
> [GeoNames](https://www.geonames.org/ontology/documentation.html) identifier
> where a record exists at the required granularity.

The institute and its place are different entities. ROR identifies the research
organization; a GeoNames IRI such as `https://sws.geonames.org/{id}/` identifies
a geographic feature or place. Link the organization to the place rather than
attaching both identifiers to one undifferentiated resource. Likewise, do not
assume that a ROR organization whose registry type is `facility` identifies a
particular building, room, BFO site, or geometry. The mapping registry must
record identifier scheme, target entity, source/version, status, and evidence.

### A05 accepted actuator and actuation boundary

Status: accepted by Damien Huzard on 2026-07-21. This decision approves the
future semantic scope and modeling pattern, but does not itself change the
current class definition or add SOSA actuation terms to the active ontology.

Decision:

> **A05 — retain the local physical HCM actuator specialization and model
> actuations and triggers explicitly.**
> Retain `hcm-tech:Actuator` as a subclass of both BFO Material entity and
> `sosa:Actuator`. It represents a physical device in a home-cage monitoring
> system that implements an actuating procedure to change a property or state of
> a subject, enclosure, environmental condition, device, or monitoring system.
>
> An HCM actuator may stimulate or perturb behavior or physiology, modify an
> environmental condition, change an enclosure or system configuration, enable
> or disable a function, or initiate, stop, or reconfigure a defined HCM
> execution.
>
> Model the physical device as `hcm-tech:Actuator`, the performed action as
> `sosa:Actuation`, the property that may be changed through `sosa:actsOn`, and
> the property actually acted upon through `sosa:actsOnProperty`. Represent any
> resulting or triggered recording, alert, feeding, lighting, or control
> execution separately; do not treat the actuator itself as the event.
>
> A software-only controller may be a `sosa:Actuator` and an appropriate software
> entity, but must not be typed as the physical `hcm-tech:Actuator`. Create a
> narrower local software-actuator class only if an approved competency question
> requires one.
>
> Retain the deprecated `hcm:Actuator` migration IRI and its replacement mapping.
> Do not delete it or assert equivalence between the local physical class and the
> broader SOSA class.

Implementation must preserve the existing `hcm-tech:Actuator` IRI. The revised
definition is a semantic expansion beyond its current behavior/physiology/
environment wording and therefore requires an explicit source-module change,
examples, competency questions, reasoning review, regenerated artifacts, and a
changelog entry when implemented. A relation between an actuation and a
triggered execution must be selected and justified separately; neither the
device nor `sosa:actsOn` alone expresses that execution dependency.

### A06 accepted active-class audit gate

Status: accepted by Damien Huzard on 2026-07-21. This is a required review gate
and does not authorize any class, definition, hierarchy, mapping, or deprecation
change by itself.

Decision:

> **A06 — require an evidence-based inventory review before implementing further
> hierarchy or mapping changes.**
> Review every active HCMO class and every external class directly used as an
> anchor. For each term, record its IRI, label, definition, owning module,
> asserted and inferred parents, restrictions, intended upper category,
> external source and version, mapping status, provenance, relevant competency
> questions, and reviewer decision.
>
> Classify each term as `keep`, `revise definition`, `revise axiom`, `map`,
> `deprecate`, or `needs evidence`. Do not make bulk label, hierarchy, or
> equivalence changes directly from the audit. Each accepted semantic change
> must become a separate implementation item with reasoning and validation
> evidence.
>
> Use `dist/profile.json` for the active HCMO inventory, supplemented by a
> separate inventory of referenced external anchors because the generated
> profile intentionally excludes external terms.

The inventory-generation step may be automated, but review classifications and
semantic rationales are human decisions. A generated table must never be used
as an unattended ontology-rewrite input.

### A07 accepted historical-artifact policy

Status: accepted by Damien Huzard on 2026-07-21. Verification remains open until
the exact artifact reviewed by Philippe is identified and checksummed.

Decision:

> **A07 — preserve historical ontology artifacts as immutable evidence and
> exclude them from the active release.**
> Treat `ontology/legacy/` and `ontology/v2/` as historical sources. Do not edit
> them to resemble the current ontology, merge them into the active release, or
> use them as the canonical Protégé entry point.
>
> The hand-authored source of truth remains `ontology/modules/*.ttl`; users
> should open the generated `dist/hcmo.owl` or `dist/hcmo.ttl`. Record the exact
> historical file, version, and checksum reviewed by Philippe, then classify
> each observation as active, compatibility-only, or historical.
>
> Preserve externally referenced IRIs through the active compatibility module
> and documented deprecation/replacement mappings. Corrections belong in active
> source modules or `hcm-compat.ttl`, never as retrospective edits to archived
> files.

This accepted preservation rule does not by itself complete A07. Completion
requires the reviewed-file evidence and comparison report described in the A07
checklist row.

## B. External labels, imports, and mappings

| Done | ID | Item and description | Human review action | What and where to change after approval | Acceptance evidence |
| --- | --- | --- | --- | --- | --- |
| [?] | B01 | **Use `ontology/external/` with a Python-controlled, pinned ROBOT extraction pipeline: provisionally accepted; co-author validation pending.** Keep approved source locks and selections separate from committed, generated per-source subsets. The canonical build remains offline. | Co-authors must validate the directory boundary, per-source artifact strategy, Python/ROBOT responsibilities, MIREOT default, conditions for locality extraction, upstream versions, selected annotations, licenses, and refresh procedure. | No implementation is authorized until co-author validation. After approval, add `ontology/external/`, `tooling/extract_external.py`, the external subset entries in `hcmo.yaml` without changing its shape, validation checks, repo-map updates, architecture/alignment documentation, and regenerated `dist/`. | Co-author sign-off; reviewed source and selection manifests; checksum-pinned reproducible extraction; offline canonical build; readable external hierarchy in Protégé; license and source/version provenance retained. |
| [x] | B02 | **Keep the canonical HCMO release self-contained and free of live full-ontology imports: accepted.** No unversioned or network-dependent `owl:imports` may enter the canonical release. Merge the approved, pinned B01 subset into generated HCMO artifacts for readable offline use. | Preserve only the reviewed upstream annotations and logical axioms selected for the subset. Record source/version, extraction boundary, checksum, and license. Treat any future full-import reasoning profile as optional and separate from the canonical release. | After B01 is approved, update the authoritative repo map, `hcmo.yaml` module values without changing its shape, extraction/validation tooling, `docs/ARCHITECTURE.md`, and release documentation. Canonical `tooling/build.py` must remain offline and deterministic. | Offline build, parse, reasoner, and OLS dry run; no live import resolution; generated external subset has pinned provenance and license; optional profile cannot silently alter canonical reasoning or downstream manifest behavior. |
| [?] | B03 | **Separate logical equivalence, individual identity, conceptual mapping, cross-reference, and exchange transformation: informed co-author feedback required.** The recommendation below is not accepted policy. | Give co-authors definitions and worked HCMO examples for `rdfs:subClassOf`, OWL equivalence, `owl:sameAs`, SKOS matches, references, and ISA/Bioschemas/RO-Crate transformation rules. Obtain explicit answers on evidence thresholds, review requirements, mapping-graph separation, SSSOM, and whether SKOS assertions may enter canonical reasoning. | Do not add mappings or a mapping module yet. After approval, record the policy in `docs/ALIGNMENTS.md`; implement the B04-approved mapping registry separately from exchange transformations; materialize only explicitly approved logical axioms in owning modules; extend validation for evidence and conflicting strengths. | Co-author review record with rationale for every policy question; ontology and domain reviewer approval; worked examples for class equivalence, narrower classes, individual identity, conceptual matches, cross-references, and exchange fields. |
| [?] | B04 | **Maintain separate semantic-mapping and exchange-transformation registries: provisionally accepted, subject to B03.** Use SSSOM/TSV for semantic mappings and a separate structured registry for ISA/Bioschemas/RO-Crate/ISA-JSON/ISA-Tab transformations. Neither enters the canonical reasoning graph by default. | Co-authors must first decide B03 mapping strengths and review thresholds. Then validate the proposed `mappings/semantic/` and `mappings/exchange/` split, required fields, SSSOM extensions, source format, generated products, and release boundary. | No registry is created yet. After B03/B04 approval, update the repo map; add the reviewed mapping sources and narrowly scoped validation/generation tooling; keep semantic RDF, if generated, separate from `dist/hcmo.*`; do not overload `tooling/build.py` with exchange keys. | B03-compatible schema; multiple mappings per HCMO IRI; deterministic validation rejects malformed CURIEs, missing justification/version/reviewer data, duplicate mapping identities, and contradictory strengths; exchange rules record direction, cardinality, transformation, and loss. |
| [?] | B05 | **Source-material register: partially resolved.** The ARC Workflow Run RO-Crate article and ISA-term-to-Schema.org/Bioschemas mapping file are confirmed below; the ISA model/profile, FAIR Cookbook recipe, and STATO source are located. Philippe's earlier ISA-OBO-PROV mapping resources remain unlocated. | Confirm the exact versions/commits and licenses of the listed sources and obtain Philippe's earlier ISA-OBO-PROV mappings or record that they are unavailable. Distinguish design evidence from normative profile requirements. | Add confirmed bibliography to `docs/paper/references.bib`; retain the audited versions in `docs/A02-ISA-STATO-COMPATIBILITY.md`; cite design evidence and mapping constraints in `docs/ISA-RO-CRATE-MAPPING.md` and `docs/ALIGNMENTS.md`. Do not derive ontology axioms directly from an article figure or field-mapping table. | Stable citations and reviewed versions for every used source; license/attribution recorded; missing-resource status explicit; each resulting mapping identifies the exact supporting source and section. |
| [?] | B06 | **Initial HCMO-to-ISA export architecture recorded for validation by Philippe.** Keep biological subjects/materials, physical enclosures, protocols, executions, sensors, files, and study factors distinct as specified below. Source/Sample round-trip identity and non-File assignment/statistical outputs remain unresolved. | Philippe or another ISA-profile expert must validate every row, assay/process granularity, direction, cardinality, transformation rule, allowed extension, and round-trip loss. Explicitly resolve the two open mappings below before any conformance claim. | No ontology or example change is authorized. After validation, extend `docs/ISA-RO-CRATE-MAPPING.md`; add B04 exchange-registry rows; update `examples/isa-hcmo-bridge.ttl`, fixtures, and validation tooling. Add ontology axioms only through a separate B03/A06-approved semantic item. | Signed ISA mapping table; acyclic Investigation -> Study -> Assay -> Process -> Material/Data example; Source/Sample roles survive round trip; housing assignment and non-File STATO result policies are explicit; controlled loss is tested. |
| [?] | B07 | **Adapt the ARC Workflow Run RO-Crate prospective/retrospective pattern for HCMO: co-author review required.** Use Ott et al. and its Figure 2 as design expertise, not as an automatically applicable HCMO profile or conformance claim. Multi-type computational specifications and executions only where all type meanings apply. | Co-authors must review the candidate adaptation below, especially which HCM processes are laboratory versus computational, where `ComputationalWorkflow`/`LabProtocol` and `CreateAction`/`LabProcess` multi-typing is valid, how HCMO/SOSA/OBI/PROV semantics remain distinct, and which RO-Crate/profile versions and validation rules apply. | No profile implementation is authorized. After approval, revise `docs/ISA-RO-CRATE-MAPPING.md`; create a minimal profile fixture and constraints; update the bridge example and JSON-LD context only for stable terms; document the profile URI/version and paper claims. | Co-author decision matrix; one physical acquisition and one computational-processing chain; prospective and retrospective entities remain distinct; base and extension profile validation pass; no ARC-specific type is reused without an HCMO requirement. |
| [?] | B08 | **Reuse current OBI classes selectively for experimental plans and executed processes: provisional architecture; co-author and OBI-expert validation required.** Keep ISA exchange resources, HCMO records, protocols, and executions distinct. Do not use deprecated `OBI_0000011`. | Validate the candidate protocol, investigation, assay, study-design execution, group-assignment, data-transformation, statistical-test, and specified-input/output terms below against current definitions and real HCM workflows. Decide mapping strength separately under B03. | No mapping or ontology implementation is authorized. After approval, add reviewed B04 mappings and `docs/ALIGNMENTS.md`; add process axioms only for justified HCMO specializations; add examples and competency questions. | Signed term matrix against pinned OBI `v2026-05-08`; every accepted mapping has a semantic-strength rationale and valid RDF use case; deprecated terms are absent from active mappings. |
| [?] | B09 | **Use PROV-O as a cross-cutting execution-provenance view: provisionally accepted, subject to B03/B04 and an end-to-end provenance example.** It does not replace BFO/OBI/SOSA domain process semantics. | Validate activity/entity/agent typing, actual usage and generation, derivation, timing, qualified plans, associations, attributions, and roles. Confirm that equipment is not made an agent merely because it participates. | No ontology implementation is authorized. After approval, add reviewed mappings and alignment documentation, a provenance example, SHACL profile requirements, and competency queries; add local specializations only if justified. | A query reconstructs subject/enclosure and sensor through recording, raw data, transformation, derived output, and STATO result, with responsibility and timing but no false agent or subject attribution. |
| [?] | B10 | **Use STATO for statistical-analysis variables, models, methods, and semantic results: provisional architecture; ISA/STATO (Philippe) expert validation required.** Keep study-design factors, factor levels, statistical variables, groups, result entities, and files distinct. | Validate every candidate and rejected term below against STATO and ISA definitions. Resolve the upstream `STATO_0000299` dependency on deprecated `OBI_0000011` without locally rewriting STATO. Decide mapping strength separately under B03. | No mapping or ontology implementation is authorized. After approval, update `hcm-bio.ttl` only for approved study-design semantics, the appropriate process/result module only for justified local specializations, B04 mappings, examples, queries, and `docs/ALIGNMENTS.md`. | Signed ISA/STATO matrix against pinned STATO `v2026-04-20`; factor/variable and analysis/output examples round-trip without treating a group as a factor or a semantic result as necessarily identical to a file. |
| [ ] | B11 | **Wikidata fallback.** Wikidata should not replace an available stable ontology term without a policy. | Define allowed use cases, identifier stability checks, mapping predicate, and review cadence. | Mapping policy and registry only; ontology modules change only for an approved semantic relation. | Each Wikidata mapping documents why no suitable maintained ontology term was selected. |

### B01 provisional external-subset directory and extraction pipeline

Status: accepted as a provisional direction by Damien Huzard on 2026-07-21;
co-author validation is required before implementation. This record does not
create a directory, extraction script, external subset, manifest entry, or
ontology axiom.

Provisional decision:

> **B01 — use a dedicated external-source area and a hybrid extraction
> pipeline.**
> Keep curated external ontology material under `ontology/external/`, separate
> from the hand-authored HCMO modules. Record pinned upstream sources and human-
> approved term selections separately from generated, committed per-source
> subsets. Use a Python controller for source locking, checksum and license
> verification, ROBOT invocation, boundary validation, deterministic output,
> and reporting.
>
> Use ROBOT MIREOT by default for the labels, definitions, synonyms, provenance,
> and named ancestor hierarchy needed for readable Protégé navigation. Use a
> syntactic locality extraction such as BOT or STAR only where A06 review has
> explicitly approved preservation of additional upstream entailments. The
> canonical build consumes committed subsets and performs no download or live
> import resolution.

Proposed layout for co-author validation:

```text
ontology/external/
|-- README.md
|-- sources.lock.yaml
|-- selection.yaml
`-- generated/
    |-- bfo-subset.ttl
    |-- iao-subset.ttl
    |-- obi-subset.ttl
    |-- sosa-subset.ttl
    |-- stato-subset.ttl
    `-- prov-subset.ttl

tooling/extract_external.py
```

The source lock records ontology and version IRIs, exact retrieval locations,
checksums, retrieval dates, licenses, and extraction-tool versions. The
selection manifest records each approved IRI, rationale, required annotations,
hierarchy boundary, extraction method, and A06 review reference. Generated
files remain separated by upstream source so their provenance, license, and
diffs can be reviewed independently.

Co-authors must validate:

1. whether `ontology/external/` is the correct stable directory name;
2. whether generated subsets should remain separated by upstream ontology;
3. whether MIREOT is the correct default and which cases justify BOT or STAR;
4. the pinned upstream versions, annotation allowlist, hierarchy boundaries,
   licensing, and update cadence; and
5. whether the refresh command may retrieve a checksum-pinned ROBOT executable
   into a local cache, while canonical build and validation remain offline.

### B02 accepted canonical import policy

Status: accepted by Damien Huzard on 2026-07-21. Implementation remains blocked
on co-author validation of the provisional B01 directory and extraction
pipeline. No `owl:imports`, external subset, or manifest entry is added by this
record.

Decision:

> **B02 — keep the canonical HCMO release self-contained and free of live
> full-ontology imports.**
> Do not add unversioned or network-dependent `owl:imports` to the canonical
> release. Merge the approved, version-pinned external subset from B01 into the
> generated HCMO release so Protégé, CI, OLS, and offline users see the required
> labels and hierarchy without downloading full external ontologies.
>
> Preserve the upstream logical axioms selected for the subset, but do not imply
> that HCMO republishes or endorses the complete external ontology. Document the
> extraction boundary and licenses.
>
> A separate optional full-import reasoning profile may be considered later,
> but it must not replace the canonical release or silently alter `hcmo.yaml`,
> reasoning results, or downstream API behavior.

The canonical build consumes a committed subset and performs no network fetch.
Refreshing that subset is a separate, explicit maintenance operation with
source-version and checksum verification.

### B03 mapping-strength policy for informed co-author review

Status: recommendation recorded by Damien Huzard on 2026-07-21; educated
co-author feedback is required before a decision. No mapping assertion,
registry, ontology axiom, or release artifact is authorized by this text.

Recommendation to review:

> **B03 — separate logical equivalence, individual identity, conceptual
> mapping, cross-reference, and exchange transformation.**
> Reuse an authoritative external IRI directly when its meaning matches HCMO.
> Use `rdfs:subClassOf` or `rdfs:subPropertyOf` when the HCMO entity is
> demonstrably narrower. Use `owl:equivalentClass` or
> `owl:equivalentProperty` only when the intended extensions and logical
> consequences agree in both directions under pinned source versions.
>
> Use `owl:sameAs` only when two IRIs identify the same individual. Never use
> it to relate classes, properties, identifier strings, or merely similar
> resources. Record non-logical conceptual correspondence with an appropriate
> SKOS match predicate in a separately versioned mapping product; do not
> automatically translate a SKOS match into an OWL equivalence axiom.
>
> Treat `rdfs:seeAlso`, `dcterms:source`, and identifier metadata as navigation,
> evidence, provenance, or identification rather than semantic mappings. Treat
> ISA, Bioschemas, and RO-Crate field mappings and round-trip rules as exchange
> transformations rather than ontology equivalence.
>
> Every mapping must record its entities and labels, predicate, source and
> target versions, justification, evidence, author, reviewer, date, status,
> scope, and decision reference. Require both ontology and domain review for
> OWL equivalence and `owl:sameAs` assertions.

The following examples should be used to educate and test the policy rather
than asking co-authors to approve predicates in the abstract:

| Claim | Recommended representation | Reason to review |
| --- | --- | --- |
| HCMO reuses BFO Material entity with the same meaning | Use the BFO class IRI directly | No duplicate HCMO class or identity assertion is needed. |
| An HCMO class is narrower than an external class | `rdfs:subClassOf` | Every HCMO instance must satisfy the external parent definition. |
| Two independently named classes have the same extension | `owl:equivalentClass`, only after bidirectional logical review | This is a reasoner-visible identity of class extensions, not label similarity. |
| Two IRIs identify the same person, organization, device, or other individual | `owl:sameAs`, only with identity evidence | It merges all facts about the two individuals and therefore requires strong evidence. |
| Two ontology concepts are exact, close, broader, or narrower conceptual matches | SKOS match predicate in the separate mapping product | The correspondence supports discovery or transformation without silently asserting OWL equivalence. |
| A publication or source supports a definition | `dcterms:source` or another approved provenance relation | Evidence is not a semantic mapping. |
| An HCMO entity becomes an ISA or RO-Crate field/value | Transformation rule in the exchange mapping registry | Serialization direction, cardinality, and round-trip loss are not captured by class equivalence. |

Co-authors are asked to answer explicitly:

1. Should direct reuse of the authoritative IRI be the default when meanings
   match?
2. Should `owl:sameAs` be forbidden for classes and properties and restricted
   to evidenced individual identity?
3. Should OWL equivalence and `owl:sameAs` require both a domain reviewer and
   an ontology reviewer?
4. Should SKOS mappings remain outside the canonical HCMO reasoning graph by
   default?
5. Should SSSOM be the preferred mapping exchange model, while B04 decides the
   authoritative serialization and generation process?
6. Which concrete counterexamples or interoperability requirements would need
   an exception to these defaults?

### B04 provisional mapping-registry architecture

Status: provisionally accepted by Damien Huzard on 2026-07-21, subject to the
B03 co-author decision. This records the intended separation and does not
authorize a directory, registry, generated mapping graph, or ontology axiom.

Provisional decision:

> **B04 — maintain separate registries for semantic mappings and exchange
> transformations.**
> Store ontology-to-ontology mappings in an authoritative SSSOM/TSV mapping set.
> Store ISA, Bioschemas, RO-Crate, ISA-JSON, and ISA-Tab field transformations
> separately because their direction, cardinality, formatting, and controlled
> information loss are not ontology-mapping predicates.
>
> Do not merge either registry into the canonical HCMO reasoning graph.
> Generate RDF, JSON, or other publication views only as separate release
> products. Deterministically validate identifiers, versions, predicates,
> justifications, reviewers, decision status, duplicate records, contradictory
> mapping strengths, and exchange round-trip declarations.

Proposed layout, to be finalized only after B03:

```text
mappings/
|-- README.md
|-- semantic/
|   `-- hcmo.sssom.tsv
`-- exchange/
    |-- isa-ro-crate.yaml
    |-- isa-json.yaml
    `-- isa-tab.yaml
```

The semantic mapping set uses standard SSSOM fields where available and
declared `ext_hcmo_*` extensions only for HCMO-specific workflow metadata that
SSSOM does not represent. The exchange registry records the HCMO IRI, target
profile and version, target entity/property or field path, direction,
cardinality, transformation, vocabulary handling, round-trip status, known
loss, evidence, reviewer, and decision status.

### B05 partially resolved source-material register

Status: partially resolved by Damien Huzard on 2026-07-21. The following
article and field-mapping source were confirmed by Damien; other listed sources
were located during the A02 audit. Earlier ISA-OBO-PROV mappings attributed to
Philippe remain an open evidence request.

Confirmed source for computational/experimental provenance design:

- Caroline Ott et al., [*Fusion of computational and experimental provenance
  in RO-Crate*](https://doi.org/10.1515/jib-2025-0050), especially
  [Figure 2 and its surrounding profile description](https://www.degruyterbrill.com/document/doi/10.1515/jib-2025-0050/html#j_jib-2025-0050_fig_002).

Confirmed ISA field-mapping source:

- [ISA RO-Crate `ISA term - schema term` mapping](https://github.com/nfdi4plants/isa-ro-crate-profile/blob/release/profile/isa_ro_crate_mapping.md).

Already located, with the ISA and STATO versions audited in
`docs/A02-ISA-STATO-COMPATIBILITY.md`:

- the ISA abstract model and pinned ISA RO-Crate draft/profile repository;
- the STATO source and audited commit; and
- the [FAIR Cookbook recipe FCB066, *Packaging ISA as a Research
  Object*](https://faircookbook.elixir-europe.org/content/recipes/maturity/isa-as-RO.html),
  whose exact reviewed revision and retrieval date still need to be recorded.

Still required:

1. Philippe's earlier ISA-OBO-PROV mapping tables, repository, or publication;
2. confirmation of the exact commits/releases and licenses to cite for B06-B10;
   and
3. a record of any source that cannot be recovered, so its alleged mappings are
   not treated as evidence.

The ISA-to-Schema.org table is an exchange mapping, and the article is design
evidence. Neither is, by itself, evidence for an OWL class or property axiom.

### B06 provisional HCMO-to-ISA architecture for Philippe's validation

Status: provisional architecture recorded by Damien Huzard on 2026-07-21.
Validation by Philippe Rocca-Serra or another designated ISA-profile expert is
required. No mapping or ontology implementation is authorized.

Initial mapping to validate:

| HCMO concern | Initial ISA/Bioschemas/RO-Crate representation |
| --- | --- |
| HCMO subject at study entry | ISA Source role and Bioschemas Sample exchange type |
| Derived tissue or specimen | Separate ISA Sample; never the same entity as the animal |
| Physical enclosure | HCMO material/equipment entity; never ISA Source or Sample |
| Acquisition protocol | ISA Protocol / Bioschemas LabProtocol |
| Recording execution | ISA Process / Bioschemas LabProcess |
| Sensor | Protocol equipment or HCMO/SOSA participant |
| Raw and derived files | ISA Data and RO-Crate File/MediaObject |
| Study factor | Only a deliberately manipulated variable, not a cage identifier or ordinary characteristic |

Two mappings remain explicitly unresolved:

1. The draft maps ISA Source and Sample to the same Bioschemas Sample type, so
   an additional rule is needed to preserve their distinct ISA roles during a
   round trip.
2. A `hcm-bio:HousingAssignment` record and a non-File STATO result are not
   permitted `LabProcess` outputs under the draft's Sample/File result
   restriction. They remain HCMO extensions until ISA experts approve a
   representation and round-trip policy.

Philippe is asked to validate or revise the entity mapping, assay and process
granularity, explicit inputs and outputs, extension boundary, and controlled
loss for ISA-Tab, ISA-JSON, and ISA RO-Crate.

### B07 ARC Workflow Run RO-Crate expertise to adapt for HCMO

Status: design source selected by Damien Huzard on 2026-07-21; HCMO adaptation
requires co-author review. The selected source is Ott et al., [*Fusion of
computational and experimental provenance in
RO-Crate*](https://doi.org/10.1515/jib-2025-0050), especially Figure 2. No
profile conformance or ontology change is authorized.

Relevant design pattern:

- keep prospective provenance (a protocol or workflow specification) distinct
  from retrospective provenance (an actual laboratory or computational
  execution);
- let a computational workflow specification satisfy both workflow-aware and
  ISA-aware views through justified multi-typing;
- let a computational workflow invocation satisfy both run-aware and ISA-aware
  views through justified multi-typing; and
- connect concrete inputs, outputs, parameters, characteristics, and factors in
  one queryable provenance graph.

Candidate HCMO adaptation for co-author review:

| HCMO case | Candidate exchange representation | Boundary requiring review |
| --- | --- | --- |
| Physical acquisition or recording protocol | `LabProtocol`, with an appropriate HCMO/OBI/SOSA protocol or procedure type | It is not a `ComputationalWorkflow` merely because software or a sensor is involved. |
| Physical acquisition or recording execution | `LabProcess`, with appropriate HCMO/OBI/SOSA execution semantics and PROV provenance | It is not automatically a Schema.org `CreateAction`; the article's computational multi-typing must not be generalized silently. |
| Data-processing or statistical workflow specification | `LabProtocol` plus `ComputationalWorkflow` and the required File/Software types when all profile definitions apply | The executable artifact, abstract plan, and protocol record may need distinct resources rather than forced identity. |
| Data-processing or statistical execution | `LabProcess` plus `CreateAction` when the same execution satisfies both definitions; PROV records provenance responsibility | Co-authors must confirm identity, input/output roles, agent, timing, status, and failure semantics. |
| Subject, specimen, enclosure, sensor, data, and statistical output | Retain precise HCMO/external semantic types alongside the required ISA/Schema.org/Bioschemas exchange types | Multi-typing must not collapse biological materials, physical devices, information entities, files, or statistical results. |
| Characteristics, factors, and parameters | Characteristics describe inherent input properties; factors describe deliberately varied study conditions; parameters describe execution settings | Placement and round-trip behavior must agree with ISA/STATO decisions and the B06 review. |

Questions for the co-authors:

1. Should the article's multi-typing pattern be adopted only for computational
   HCM workflows and invocations, while physical recording uses the ISA
   `LabProtocol`/`LabProcess` view without Workflow Run RO-Crate types?
2. When are the executable workflow artifact, protocol/plan information entity,
   and reusable procedure the same resource, and when must they be separate?
3. Which HCMO, OBI, SOSA, STATO, and PROV types and relations must coexist with
   the exchange types in each example?
4. Does the proposed placement of characteristics, factors, and parameters
   preserve the intended ISA/STATO meaning for home-cage studies?
5. Which base RO-Crate, ISA RO-Crate, Bioschemas, and Workflow Run RO-Crate
   versions will be pinned, and what validator establishes each conformance
   claim?
6. What is the smallest physical-acquisition plus computational-analysis
   example that demonstrates the adaptation without importing ARC-specific
   concepts that HCMO does not need?

### B08 provisional OBI architecture for expert validation

Status: provisional OBI architecture selected by Damien Huzard on 2026-07-21;
co-author and OBI-expert validation is required. No mapping, source-module
axiom, external subset, or generated release change is authorized.

The reviewed source is [OBI `v2026-05-08`](https://github.com/obi-ontology/obi/releases/tag/v2026-05-08),
commit
[`a7aeec49057d9f9ba03d14977576d064f3fa6825`](https://github.com/obi-ontology/obi/tree/a7aeec49057d9f9ba03d14977576d064f3fa6825).
The B01 subset must also retain the selected IAO and COB dependencies needed to
interpret these OBI terms.

Candidate reuse for definition-level review:

| Concern | Candidate | Required interpretation |
| --- | --- | --- |
| Reproducible protocol | [`OBI_0000272` protocol](http://purl.obolibrary.org/obo/OBI_0000272) | A sufficiently detailed `IAO_0000104` plan specification, distinct from its execution. |
| Executed investigation | [`OBI_0000066` investigation](http://purl.obolibrary.org/obo/OBI_0000066) | The executed scientific investigation, not automatically the ISA metadata container carrying the same label. |
| Study-design execution | [`OBI_0000471` study design execution](http://purl.obolibrary.org/obo/OBI_0000471) | An execution that carries out a study design. |
| Assay | [`OBI_0000070` assay](http://purl.obolibrary.org/obo/OBI_0000070) | Use only when the process examines a material entity to produce information about it. |
| Experimental-group assignment | [`OBI_0600015` group assignment](http://purl.obolibrary.org/obo/OBI_0600015) | Use when an organism is assigned a study role; do not infer that every cage allocation is group assignment. |
| Random assignment | [`OBI_0302900` group randomization](http://purl.obolibrary.org/obo/OBI_0302900) | Use only when assignment relies on chance to avoid experimental bias. |
| Data transformation | [`OBI_0200000` data transformation](http://purl.obolibrary.org/obo/OBI_0200000) | An executed process producing output data from input data. |
| Statistical test | [`OBI_0000673` statistical hypothesis test](http://purl.obolibrary.org/obo/OBI_0000673) | Use this or a more specific reviewed STATO method only when the analysis meets the definition. |
| Specified process roles | [`OBI_0000293` has specified input](http://purl.obolibrary.org/obo/OBI_0000293) and [`OBI_0000299` has specified output](http://purl.obolibrary.org/obo/OBI_0000299) | Express OBI process semantics; do not declare them equivalent to ISA exchange fields or actual PROV usage/generation. |

`OBI_0000011` is labelled `obsolete planned process` and is deprecated in the
reviewed OBI release. It must not be selected as HCMO's active process anchor.
Current selected OBI process classes use
[`COB_0000035` completely executed planned process](http://purl.obolibrary.org/obo/COB_0000035)
beneath the BFO process hierarchy.

A recording execution may receive both an appropriate OBI assay type and
SOSA execution/observation semantics only when all definitions apply. An ISA
Investigation, Assay, or Process resource is an exchange representation; it may
be multi-typed as the same OBI execution only after identity and semantic fit
are demonstrated. `hcm-bio:HousingAssignment` remains an information-content
record. A narrower HCM housing-allocation process may be created only after an
approved competency question establishes the requirement.

### B09 provisional PROV-O execution-provenance architecture

Status: provisionally accepted by Damien Huzard on 2026-07-21, subject to the
B03/B04 decisions and validation with an end-to-end provenance example. No
mapping, ontology axiom, shape, example, or query is implemented by this
decision.

Use PROV-O as a cross-cutting account of what happened, not as HCMO's upper
domain process ontology:

- an executed OBI, SOSA, or narrower HCM process may also be a `prov:Activity`
  when the same instance satisfies both meanings;
- use `prov:used` for entities actually used and `prov:wasGeneratedBy` for data,
  records, and results actually generated;
- use `prov:wasDerivedFrom` for derivation between entities, not merely as a
  replacement for process output;
- record execution time with `prov:startedAtTime` and `prov:endedAtTime`;
- connect an activity, responsible agent, and protocol or plan through a
  qualified `prov:Association` and `prov:hadPlan`;
- use qualified associations and attributions with `prov:hadRole`, including
  the CRediT policy accepted under A03; and
- use `prov:wasAssociatedWith` for responsibility for an activity and
  `prov:wasAttributedTo` for responsibility for an entity.

A protocol may also be a `prov:Plan` when the same resource meets the PROV
definition, but no class equivalence is implied. OBI specified inputs/outputs
and PROV actual usage/generation may coexist on the same execution; their
properties must not be declared equivalent. Do not globally assert that every
SOSA observation or OBI process is a `prov:Activity`; begin with reviewed
instance-level multi-typing.

A sensor, actuator, enclosure, or other piece of equipment is not a
`prov:Agent` merely because it participates in an execution. Type software or
an autonomous system as an agent only when it bears the intended provenance
responsibility. The required validation example and query must reconstruct:

`subject/enclosure and sensor -> recording activity -> raw data -> transformation activity -> derived data and STATO result`.

The example must also demonstrate responsible agents, plans, timing, and no
subject-level attribution inferred solely from cage occupancy.

### B10 provisional STATO architecture for Philippe's validation

Status: provisional STATO architecture selected by Damien Huzard on
2026-07-21; ISA/STATO validation by Philippe Rocca-Serra or a designated expert
is required. No mapping, ontology axiom, external subset, or generated release
change is authorized.

The reviewed source is [STATO `v2026-04-20`](https://github.com/ISA-tools/stato/releases/tag/v2026-04-20),
commit
[`a5910e6115217a88ee86e2666e12983ef2ef2a42`](https://github.com/ISA-tools/stato/tree/a5910e6115217a88ee86e2666e12983ef2ef2a42).

Initial candidate and rejection matrix:

| Concern | Candidate or rejected term | Required interpretation |
| --- | --- | --- |
| HCMO Study Factor | [`OBI_0000750` study design independent variable](http://purl.obolibrary.org/obo/OBI_0000750) | Review this study-design specification before any mapping; do not automatically equate a study factor with a STATO analysis variable. |
| ISA Factor Value | [`STATO_0000265` factor level](http://purl.obolibrary.org/obo/STATO_0000265) | Use when the value belongs to a deliberately manipulated independent variable. |
| Analysis variable | [`STATO_0000258` variable](http://purl.obolibrary.org/obo/STATO_0000258) or a specific quantitative/categorical subtype | Represents the variable in statistical analysis or a model; preserve its distinction from the study-design factor specification and observed value. |
| Statistical model | [`STATO_0000107` statistical model](http://purl.obolibrary.org/obo/STATO_0000107) | Represent the model separately from its fitting execution, parameters, estimates, and containing file. |
| Model fitting | [`STATO_0000218` model fitting](http://purl.obolibrary.org/obo/STATO_0000218) | A specific data transformation; prefer it to a new generic HCMO statistical-analysis class when it fits. |
| Parameter estimation | [`STATO_0000119` model parameter estimation](http://purl.obolibrary.org/obo/STATO_0000119) | Use for the transformation that determines model parameter estimates. |
| Model selection | [`STATO_0000328` statistical model selection](http://purl.obolibrary.org/obo/STATO_0000328) | Use for a transformation comparing model quality to select a model. |
| Statistical output | [`STATO_0000039` statistic](http://purl.obolibrary.org/obo/STATO_0000039), [`STATO_0000471` estimate](http://purl.obolibrary.org/obo/STATO_0000471), [`STATO_0000599` point estimate](http://purl.obolibrary.org/obo/STATO_0000599), [`STATO_0000600` interval estimate](http://purl.obolibrary.org/obo/STATO_0000600), or [`STATO_0000700` p-value](http://purl.obolibrary.org/obo/STATO_0000700) | A semantic information/data entity is not necessarily identical to the ISA or RO-Crate File in which it is serialized. |
| Experimental group | Candidate [`STATO_0000193` study group population](http://purl.obolibrary.org/obo/STATO_0000193) | Consider only when the population, membership, sampling, and measurement conditions fit; do not assert blanket equivalence. |
| Generic animal cohort | Reject [`STATO_0000203` cohort](http://purl.obolibrary.org/obo/STATO_0000203) | Its definition requires human beings in a longitudinal design. |
| Statistical sample versus biological sample | No automatic mapping to [`STATO_0000651` statistical sample](http://purl.obolibrary.org/obo/STATO_0000651) | A statistical draw or sample must not be conflated with an ISA biological Sample. |

An experimental group is neither a Study Factor nor a factor level. A group
may instead be characterized by combinations of factor levels. The B06
round-trip issue remains open because a non-File STATO result is not directly
permitted by the reviewed ISA RO-Crate draft's restricted `LabProcess` result
representation.

The reviewed STATO release still asserts deprecated `OBI_0000011` as a parent
of `STATO_0000299` statistical inference. HCMO must not silently repair that
upstream axiom. Exclude the generic term from the initial subset, or include it
with its exact upstream deprecation context, until Philippe and the STATO/OBI
maintainers validate a resolution. Mapping predicates and strengths for every
accepted candidate remain governed by B03 and B04.

## C. Object properties and reasoning

| Done | ID | Item and description | Human review action | What and where to change after approval | Acceptance evidence |
| --- | --- | --- | --- | --- | --- |
| [ ] | C01 | **Domain/range semantic review.** All active local object and datatype properties currently have a domain and range, but OWL domains/ranges infer types and may still be too narrow or too broad. | For every property, test intended and edge-case triples and inspect inferred types. Pay particular attention to union domains/ranges, `hcm:locatedIn`, environmental measured-property relations, `hcm-obs:hasCondition`, and housing assignment relations. | Edit axioms only in the owning `ontology/modules/*.ttl`. Put closed-world requirements in `shapes/hcm-shapes.ttl`, not narrower OWL axioms. Add positive/negative examples and regenerate `dist/`. | Property-by-property sign-off and automated reasoner/SHACL evidence. |
| [ ] | C02 | **Inverse and parent relations.** Only relations with justified semantics should receive inverses or superproperties. | Identify query-driven candidates; confirm direction and external parent definitions. Do not add inverses merely to silence quality tools. | Owning ontology modules; `docs/ALIGNMENTS.md` for reused parents; `queries/` for demonstrated utility; update `docs/paper/evaluation/` if OOPS findings change. | Every added inverse or parent is used by an example/query and introduces no unintended inference. |
| [ ] | C03 | **Property documentation and provenance.** Labels, definitions, domains, and ranges exist, but source/provenance, usage examples, and CQ links are not systematically attached. | Choose an annotation pattern and whether CQ links are RDF annotations or documentation-only references. | Ontology modules for lightweight provenance annotations; `docs/ALIGNMENTS.md` for sources; `queries/competency_questions.yaml` for CQ coverage; generated documentation templates if used. | Inventory showing label, definition, source, domain, range, optional inverse/parent, example, and CQ for every active object property. |
| [ ] | C04 | **OWL versus SHACL boundary.** The current design states that OWL provides semantics and SHACL provides intake constraints. | Confirm this policy for the new process, factor, provenance, and ISA profile requirements. | `docs/MODEL.md`, `docs/ARCHITECTURE.md`, and `shapes/hcm-shapes.ttl`; preserve the scalar `shapes` contract in `hcmo.yaml` unless a backward-compatible extension is approved. | Each proposed constraint is classified as inference, validation, or both, with tests. |

## D. Processes, inputs, outputs, and provenance

| Done | ID | Item and description | Human review action | What and where to change after approval | Acceptance evidence |
| --- | --- | --- | --- | --- | --- |
| [ ] | D01 | **Process scope and granularity.** Candidate processes include allocation, acclimatization, recording, measurement, detection, acquisition, preprocessing, feature extraction, analysis, annotation, and QC. | Select a minimal first-release subset based on competency questions and available datasets. For each, distinguish planned protocol, executed process/activity, and assignment or result record. | Architecture and alignment docs first. Approved local specializations go in the namespace-owning module; do not repurpose `hcm-bio:HousingAssignment`, which is currently an IAO information-content record, as a process without a migration design. | Approved process table with inputs, outputs, participants, agent, time, and external mappings. |
| [ ] | D02 | **Input/output relation pattern.** HCMO does not yet define a general input/output model. | Choose OBI, PROV-O, or ISA/Bioschemas relations and decide when local subproperties are necessary. Verify directionality against definitions. | Mapping artifact and owning modules; `examples/isa-hcmo-bridge.ttl`; shapes for profile requirements; competency queries. | One acquisition and one transformation example demonstrate the pattern without duplicate or reverse relations. |
| [ ] | D03 | **Information-output taxonomy.** Raw data, processed data, observations, events, annotations, features, summaries, estimates, models, figures, tables, and QC reports may require distinct treatment. | Decide which are OWL classes, external classes, roles, file media types, or controlled vocabulary values. Keep ontology scope minimal. | Likely `ontology/modules/hcm-obs.ttl` for observations/results and `hcm-tech.ttl` for data/software artifacts, subject to approved namespaces; mappings, shapes, examples, and context follow. | Approved matrix of artifact type versus representation with no definition-by-example. |
| [ ] | D04 | **End-to-end provenance chain.** The target is animal/environment -> sensor -> acquisition -> raw dataset -> preprocessing -> derived variable -> statistical analysis -> statistical output. | Validate the chain against at least one real HCM dataset and decide attribution rules for group-housed versus individually identified observations. | Process/provenance mappings, ontology modules, `examples/`, new CQ files plus `queries/competency_questions.yaml`, and paper resource/impact sections. | SPARQL query reconstructs the chain and does not infer subject-level attribution from cage occupancy alone. |
| [ ] | D05 | **Temporal ordering and assignment validity.** Housing changes and process order require time without breaking the acyclic ISA graph. | Choose interval and event patterns compatible with OWL-Time, PROV-O, and the selected ISA serialization. | `ontology/modules/hcm-bio.ttl` for assignment record relations, process modules, shapes, examples, and ISA mapping note. Reuse OWL-Time terms where valid. | Example with re-housing reconstructs non-overlapping assignment intervals and serializes successfully. |

## E. Study design and controlled vocabularies

| Done | ID | Item and description | Human review action | What and where to change after approval | Acceptance evidence |
| --- | --- | --- | --- | --- | --- |
| [ ] | E01 | **Study Factor and Factor Value.** `hcm-bio:StudyFactors` is an information-content class with the preferred singular label, but there is no factor-value model. | Confirm the current definition, the retained plural IRI, the ISA and STATO targets, and the distinction among factor, independent variable, condition, and value. Do not change the published IRI to make it singular. | `ontology/modules/hcm-bio.ttl`, mapping artifact, `docs/ISA-RO-CRATE-MAPPING.md`, shapes, examples, queries, context, and generated `dist/`. If replacement is required, deprecate/map rather than rename by IRI. | Study with at least two factors and multiple values serializes to the selected ISA representation. |
| [ ] | E02 | **Experimental Group versus Study Factor.** `hcm-bio:ExperimentalGroup` is a BFO object aggregate with `hasMember`/`belongsToGroup`; it is not equivalent to Study Factor. | Approve relations for subject assignment and groups defined by combinations of factor values. Decide whether control group/cohort are classes, roles, or controlled terms. | `ontology/modules/hcm-bio.ttl`, shapes, examples, new group/factor CQs, ISA/STATO mappings, and model documentation. | Example shows two groups sharing a factor while differing in factor values; no equivalence between group and factor. |
| [ ] | E03 | **Literal biological and treatment values.** Species, strain, sex, treatment, and some conditions are currently strings. | For each property, choose an external ontology IRI, SKOS concept, OWL individual, or SHACL-constrained literal based on reasoning and exchange requirements. | `ontology/modules/hcm-bio.ttl`, `hcm-obs.ttl`, shapes, context, examples, mapping registry, and documentation. Preserve backward compatibility for existing literal data or provide a migration mapping. | Representation matrix and validation tests for accepted and rejected values. |
| [ ] | E04 | **SKOS candidate schemes.** Behavior labels, housing categories, modalities, device status, QC codes, experimental roles, and processing categories may not need OWL class semantics. | Select only lists with project governance and stable definitions. Decide whether HCMO owns the scheme or references an external vocabulary. | If HCMO-owned, use a reviewed module/artifact under the established namespace and add it to the build contract; update context, shapes, examples, documentation, and versioning policy. | Each scheme has URI policy, `skos:prefLabel`, definitions, optional alternatives/hierarchy, governance owner, and validation tests. |

## F. Serialization and implementation

| Done | ID | Item and description | Human review action | What and where to change after approval | Acceptance evidence |
| --- | --- | --- | --- | --- | --- |
| [ ] | F01 | **Canonical exchange decision.** Decide whether ISA RO-Crate is canonical or one supported export. The canonical ontology source and generated RDF artifacts remain separate from metadata-package formats. | Approve a statement distinguishing ontology representation, instance-data profile, exchange packages, and optional exports. | `docs/ARCHITECTURE.md`, `docs/ISA-RO-CRATE-MAPPING.md`, `README.md`, `hcmo.yaml` only if its existing contract values truly change, and paper sections. | Published serialization policy with canonical/optional formats and versioning rules. |
| [ ] | F02 | **Profile levels.** Investigation, study, assay, process, object/device, observation, and dataset profiles may have different requirements. | Choose the first minimal profile and explicitly defer later profiles. Define required and recommended fields and nesting/conformance rules. | ISA mapping note, profile validation artifact, examples, context, and paper. Avoid changing the `hcmo.yaml` shape as an API without a compatibility design. | Minimal valid and intentionally invalid packages produce expected validation results. |
| [ ] | F03 | **ISA-Tab and ISA-JSON export.** Compatibility is not demonstrated. | Define round-trip scenarios and acceptable information loss; select tool versions. | New deterministic exporter/validator tooling if this repository owns it, otherwise document the external implementation and fixtures. Add fixtures under an approved examples/test path and document it before changing the repo map. | RDF -> ISA format -> RDF comparison report for factors, processes, assignments, and files. |
| [ ] | F04 | **Identifier and URI policy.** Profiles must distinguish persistent ontology IRIs, crate-local entity IDs, external IDs, and application keys. | Approve minting, base-URI, blank-node, versioning, correction, and deprecation rules. | `docs/ARCHITECTURE.md`, mapping registry documentation, JSON-LD context, examples, validation tooling, and paper availability section. | Tests reject key collisions and unresolved required identifiers while allowing several external mappings. |
| [ ] | F05 | **Round-trip and conflict validation.** The current validator parses RDF, runs SHACL, and executes CQs; it does not validate mapping conflicts or ISA packages. | Define error categories and add fixtures for duplicate keys, duplicate canonical mappings, unresolved targets, incompatible mapping strengths, and serialization loss. | Extend `tooling/validate.py` or add narrowly scoped validators invoked by it; add test fixtures and document dependencies in `tooling/requirements.txt`. | Each failure mode has a negative test and CI exits non-zero. |

## G. Publication, testing, and paper

| Done | ID | Item and description | Human review action | What and where to change after approval | Acceptance evidence |
| --- | --- | --- | --- | --- | --- |
| [ ] | G01 | **Protege and reasoner review.** Automated build/SHACL/CQ validation does not replace a UI and DL reasoner check. | Open the generated `dist/hcmo.owl`, verify labels/deprecation/hierarchy, run the agreed reasoner, and inspect unintended inferred types caused by domains/ranges. | Record the dry run in `docs/paper/PROTEGE-REASONER.md` or a dated evaluation file; fix source modules only; regenerate artifacts. | Tool/version, input checksum, screenshots or report, consistency result, and triaged warnings. |
| [ ] | G02 | **OLS ingestion readiness.** Readability, resolvability, metadata, imports, and deprecation display must survive the published artifact. | Perform an OLS-compatible ingestion dry run on the generated release, not historical OWL files. | Source module annotations/import strategy, ontology header metadata, build tooling if serialization changes are needed, and a dated report under `docs/paper/evaluation/`. | Search and hierarchy views display local and reused labels; term IRIs resolve; deprecated terms are marked. |
| [ ] | G03 | **SHACL coverage.** New process, factor, group, provenance, and profile rules need validation without converting closed-world requirements into OWL semantics. | Approve required versus optional fields for each profile and add positive/negative cases. | `shapes/hcm-shapes.ttl`, manifest-listed `examples/`, and `tooling/validate.py`. Keep existing examples conformant and edge examples non-conformant. | Automated expected-pass and expected-fail results for every new constraint family. |
| [ ] | G04 | **Competency-question coverage.** Current CQs cover enclosure assignment, dimensions, provisioning, sensor properties, and long observations, not mappings/processes/factors/provenance. | Add natural-language CQs before modeling each new capability and agree expected results. | `queries/competency_questions.yaml`, new `queries/cq-*.rq`, and representative examples. | Each claimed capability has an executable query with a non-empty expected result fixture. |
| [ ] | G05 | **JSON-LD context.** The context covers current core relations but not proposed mappings, processes, provenance, factors, or profile terms. | Add only stable, approved terms; avoid aliases that collapse distinct IRIs onto one key. | `ontology/context.jsonld`; serialization fixtures; regenerate `dist/hcmo.json`; mapping-conflict tests. | JSON-LD expand/compact round trip preserves all IRIs and value types. |
| [ ] | G06 | **Paper claims and citations.** The paper must distinguish implemented interoperability from roadmap work. | Review every claim against a released artifact and add the missing FAIR Cookbook, ISA RO-Crate, Bioschemas, OBI, PROV-O, and STATO sources. | `docs/paper/references.bib`, `sections/02-related-work.md`, `04-resource.md`, `05-availability.md`, `06-evaluation.md`, `07-impact.md`, `08-conclusion.md`, plus `docs/paper/TODO.md`. | Claim-to-evidence table; citations resolve; unimplemented features are labeled future work. |
| [ ] | G07 | **Release integration.** Any approved ontology change requires synchronized source, generated artifacts, documentation, tests, and version metadata. | Decide whether accumulated semantic changes warrant the next minor version and review deprecations/migrations. | Owning modules, `hcmo.yaml` values without changing its shape, ontology header, `ontology/context.jsonld`, `shapes/`, `examples/`, `queries/`, `CHANGELOG.md`, docs, and regenerated `dist/`. | Two consecutive builds produce no diff; validation passes; changelog includes `old -> new` under `### Renamed` when applicable. |

## Recommended review sequence

1. Reproduce which ontology file was reviewed (A07), then verify the already
   implemented Person/Place/Actuator/property facts (A03-A05 and C01).
2. Obtain Philippe's source materials (B05) and decide the four-category,
   import, and mapping policies (A01-A02 and B01-B04).
3. Approve the ISA/RO-Crate/Bioschemas/OBI/PROV-O/STATO mappings (B06-B10) and
   canonical exchange/profile scope (F01-F02).
4. Model the minimum process/provenance and study-factor slice required by
   agreed competency questions (D01-D05 and E01-E04).
5. Implement serialization, validation, UI/reasoner/OLS testing, and paper
   updates (F03-F05 and G01-G07).

## Human review record

Copy one row per reviewed item. Do not replace unresolved questions with
unreviewed ontology assertions.

| Item ID | Reviewer | Date | Decision (`accept`, `revise`, `reject`, `defer`) | Rationale and semantic effect | Evidence/source | Issue or PR |
| --- | --- | --- | --- | --- | --- | --- |
| A01 | Damien Huzard; co-author review pending | 2026-07-21 | Defer final approval; provisional direction accepted | Prefer direct reuse of authoritative upper-level classes plus a curated, versioned subset of annotations and hierarchy for readable Protégé rendering. Local upper classes are permitted only when narrower or meaningfully different. No ontology axioms changed. | A01 provisional decision and discussion structure above | `docs/philippe-rocca-serra-review` |
| A02 | Damien Huzard; co-author and external review pending | 2026-07-21 | Defer final approval; provisional direction recorded for discussion | Use a layered process architecture: BFO/OBI/SOSA/STATO for semantics, PROV-O for provenance, and ISA/Bioschemas for exchange. Keep plans, executions, and outputs distinct; create local classes only for narrower HCMO meanings. No ontology axioms changed. | A02 provisional decision above and `docs/A02-ISA-STATO-COMPATIBILITY.md` | `docs/philippe-rocca-serra-review` |
| A03 | Damien Huzard | 2026-07-21 | Accept | Keep person identity, provenance responsibility, and contributor credit distinct. Reuse Schema.org, PROV-O, and official CRediT roles in their respective scopes; do not create `hcm:Person`. No ontology axioms changed. | A03 accepted decision and implementation boundary above; Schema.org Person, PROV-O, and CRediT specifications | `docs/philippe-rocca-serra-review` |
| A04 | Damien Huzard | 2026-07-21 | Accept | Keep `schema:Place` as a broad exchange range while distinguishing material facilities, immaterial sites/spatial regions, and geometry. Identify an institute with ROR where eligible and its separate geographic place with GeoNames where available. Do not create `hcm:Place`. No ontology axioms changed. | A04 accepted decision and identifier boundary above; ROR schema v2.1; GeoNames Ontology | `docs/philippe-rocca-serra-review` |
| A05 | Damien Huzard | 2026-07-21 | Accept | Retain the physical HCM actuator specialization and deprecated migration IRI; model actuations, acted-on properties, software controllers, and triggered executions as distinct entities. The future definition expansion is approved but not implemented; no ontology axioms changed. | A05 accepted actuator and actuation boundary above; SOSA/SSN 2023 | `docs/philippe-rocca-serra-review` |
| A06 | Damien Huzard | 2026-07-21 | Accept as required review gate | Require a signed, evidence-based inventory of every active HCMO class and directly referenced external anchor before hierarchy or mapping implementation. Treat every non-`keep` result as a separate reviewed change. No ontology axioms changed. | A06 accepted active-class audit gate above; `dist/profile.json` plus external-anchor supplement | `docs/philippe-rocca-serra-review` |
| A07 | Damien Huzard; reviewed artifact evidence pending | 2026-07-21 | Accept preservation policy; verification pending | Preserve `ontology/legacy/` and `ontology/v2/` as immutable, excluded historical evidence; use modules as source and generated `dist/` files as load targets. No ontology axioms changed. | A07 accepted historical-artifact policy above; exact reviewed file/version/checksum still required | `docs/philippe-rocca-serra-review` |
| B01 | Damien Huzard; co-author validation pending | 2026-07-21 | Defer final approval; directory and hybrid pipeline provisionally accepted | Use `ontology/external/` for locked sources, reviewed selections, and committed per-source subsets. Use a Python-controlled, pinned ROBOT pipeline with MIREOT as the readability default and reviewed locality extraction where additional entailments are required. Keep canonical builds offline. No files or ontology axioms implemented. | B01 provisional directory and extraction decision above; ROBOT extraction documentation | `docs/philippe-rocca-serra-review` |
| B02 | Damien Huzard | 2026-07-21 | Accept | Keep the canonical release self-contained and free of live full-ontology imports. Merge only the approved version-pinned B01 subset; keep any future full-import reasoning profile optional and separate. No ontology axioms changed. | B02 accepted canonical import policy above; B01 co-author validation pending | `docs/philippe-rocca-serra-review` |
| B03 | Damien Huzard; educated co-author feedback pending | 2026-07-21 | Defer | Review the proposed separation of logical axioms, individual identity, conceptual mappings, cross-references, and exchange transformations using concrete HCMO examples. Decide evidence and reviewer thresholds, mapping-graph separation, and SSSOM use before adding mappings. No ontology axioms changed. | B03 informed-review brief above; OWL, SKOS, and SSSOM specifications to be included in the co-author packet | `docs/philippe-rocca-serra-review` |
| B04 | Damien Huzard; B03 co-author decision pending | 2026-07-21 | Defer final approval; registry split provisionally accepted | Keep semantic SSSOM mappings separate from structured exchange transformations and outside the canonical reasoning graph. Final fields, source formats, extensions, and release products depend on B03. No registry or ontology axiom implemented. | B04 provisional mapping-registry architecture above; SSSOM specification | `docs/philippe-rocca-serra-review` |
| B05 | Damien Huzard; missing-source evidence pending | 2026-07-21 | Partially resolved | Confirm Ott et al. as the article and the ISA RO-Crate `ISA term - schema term` file as the exchange mapping source. Retain audited ISA/STATO/FAIR Cookbook sources; continue requesting Philippe's earlier ISA-OBO-PROV mappings. No ontology axioms changed. | B05 source-material register above; DOI `10.1515/jib-2025-0050`; ISA RO-Crate mapping file | `docs/philippe-rocca-serra-review` |
| B06 | Damien Huzard; Philippe Rocca-Serra or designated ISA expert validation pending | 2026-07-21 | Defer final approval; provisional architecture recorded | Validate the initial subject/material/enclosure/protocol/execution/sensor/file/factor mapping and resolve Source/Sample role preservation plus housing-assignment and non-File statistical-result round trips. No mapping or ontology axiom implemented. | B06 validation package above; ISA abstract model and ISA RO-Crate mapping | `docs/philippe-rocca-serra-review` |
| B07 | Damien Huzard; co-author review pending | 2026-07-21 | Defer; adaptation source selected | Adapt Ott et al.'s prospective/retrospective and computational multi-typing pattern for HCMO without applying Workflow Run RO-Crate types to physical acquisition automatically. Decide type identity, semantic/exchange layering, versions, validation, and a minimal example. No profile or ontology axiom implemented. | B07 HCMO adaptation brief above; Ott et al., DOI `10.1515/jib-2025-0050`, especially Figure 2 | `docs/philippe-rocca-serra-review` |
| B08 | Damien Huzard; co-author and OBI-expert validation pending | 2026-07-21 | Defer final approval; provisional OBI architecture selected | Reuse current OBI protocol and specific executed-process semantics only when definitions fit; keep ISA exchange nodes and HCMO records distinct; do not use deprecated `OBI_0000011`. No mapping or ontology axiom implemented. | B08 candidate matrix above; OBI `v2026-05-08` at `a7aeec49057d9f9ba03d14977576d064f3fa6825` | `docs/philippe-rocca-serra-review` |
| B09 | Damien Huzard; B03/B04 and example validation pending | 2026-07-21 | Defer final approval; provisionally accept | Use PROV-O as a cross-cutting actual-provenance view alongside OBI/SOSA/HCMO semantics. Keep responsibility, equipment participation, plans, specified inputs/outputs, actual usage/generation, and derivation distinct. No mapping or ontology axiom implemented. | B09 provenance architecture above; W3C PROV-O Recommendation | `docs/philippe-rocca-serra-review` |
| B10 | Damien Huzard; ISA/STATO validation by Philippe pending | 2026-07-21 | Defer final approval; provisional STATO architecture selected | Reuse specific STATO analysis variables, models, transformations, and result entities while distinguishing design factors, factor levels, groups, statistical samples, and files. Do not locally repair STATO's deprecated OBI dependency. No mapping or ontology axiom implemented. | B10 candidate and rejection matrix above; STATO `v2026-04-20` at `a5910e6115217a88ee86e2666e12983ef2ef2a42` | `docs/philippe-rocca-serra-review` |

## Required implementation gate for every accepted semantic change

- [ ] The affected term and owning module are identified.
- [ ] Existing IRIs are preserved, or deprecation and replacement mappings are
  documented.
- [ ] Definitions and mapping targets are sourced rather than invented.
- [ ] OWL inferential effects and SHACL validation effects are separately
  reviewed.
- [ ] Examples and competency questions demonstrate the intended behavior.
- [ ] `python tooling/build.py` succeeds.
- [ ] Re-running `python tooling/build.py` produces no diff.
- [ ] `python tooling/validate.py` succeeds.
- [ ] Generated `dist/` changes are committed with their sources.
- [ ] `CHANGELOG.md` contains the semantic effect and a `### Renamed` section
  with `old -> new` entries when any term moved.
