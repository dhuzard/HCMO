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
| [ ] | A05 | **Actuator placement and apparent duplication.** The active class is already a material entity through `BFO_0000040`; the second IRI is deprecated migration support. | Verify in Protege/OLS that the duplicate report refers to `hcm-tech:Actuator` and deprecated `hcm:Actuator`. Confirm that the deprecation and replacement are visible. | Normally no class merge. If display metadata is insufficient, update annotations in `ontology/modules/hcm-compat.ttl` or the curated external-label/mapping layer; never delete the deprecated IRI. Update `docs/PHILIPPE-ROCCA-SERRA-FEEDBACK.md` with verification evidence. | Screenshot or hierarchy export showing one active class and one clearly deprecated replacement mapping. |
| [ ] | A06 | **Systematic active-class audit.** Presence checks have passed, but definitions, anchors, synonyms, and provenance still require expert review. | Review all active classes in `dist/profile.json` against domain meaning and source ontologies. Mark each as keep, revise annotation, map, deprecate, or needs evidence. | Definitions and axioms must be edited in the owning `ontology/modules/*.ttl` file. Track unresolved text in `docs/MISSING-DEFINITIONS.md`; record external alignments in the approved mapping artifact; regenerate `dist/`. | Signed inventory covering every active class and explaining every changed semantic axiom. |
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
| [ ] | B01 | **Curated external-label strategy.** The merged release lacks labels for the 11 external axiom targets listed above. Full imports could make the hierarchy unnecessarily large. | Choose a versioned MIREOT-style subset, an import module, or another curated mechanism. Approve source ontology versions, annotation properties, update procedure, and license/provenance requirements. | Preferred candidate is a hand-authored or reproducibly generated module under `ontology/modules/`, added to the `modules` list in `hcmo.yaml`; document it in `ontology/AGENTS.md`, `docs/ARCHITECTURE.md`, and `docs/ALIGNMENTS.md`. If a new path is introduced, update the root repo map before using it. Never hand-edit `dist/`. | Reopening `dist/hcmo.owl` shows readable external labels; rebuild is reproducible; source/version annotations are queryable. |
| [ ] | B02 | **Import policy.** The active ontology currently has no `owl:imports`. | Decide whether the release should remain import-free with curated annotations or assert limited imports. Consider offline builds, OLS ingestion, ontology size, version pinning, and license compatibility. | Ontology header in `ontology/modules/hcm-core.ttl`; import/annotation module if approved; build and validation tooling if imports must be resolved; `docs/ARCHITECTURE.md` and release documentation. | Documented policy and successful offline parse, reasoner, and OLS dry run. |
| [ ] | B03 | **Mapping-strength policy.** Exact identity, logical equivalence, and SKOS similarity are currently not governed. | Define evidence thresholds for `owl:equivalentClass`, `owl:equivalentProperty`, `owl:sameAs`, SKOS match predicates, broader/narrower mappings, and simple cross-references. State whether SKOS mapping predicates may annotate OWL entities. | Add the policy to `docs/ALIGNMENTS.md`. Store approved mappings in a dedicated module such as `ontology/modules/hcm-mappings.ttl` or another reviewed artifact; add it to `hcmo.yaml` if it is part of the release. Extend validation for missing evidence and conflicting mapping strengths. | Policy examples approved by an ontology reviewer; every mapping has target IRI, predicate, source, reviewer, date, and evidence. |
| [ ] | B04 | **Mapping registry data model.** One HCMO concept must support multiple external and serialization-specific mappings without collapsing URIs into one application key. | Approve registry fields: canonical HCMO IRI, target IRI/field, target scheme/version, mapping predicate, profile/serialization scope, evidence, provenance, status, and notes. Decide RDF versus a tabular source with generated RDF. | Ontology mappings belong in the approved mapping artifact; field-level mappings belong in `docs/ISA-RO-CRATE-MAPPING.md` or a machine-readable registry. Add a new tooling script only for deterministic validation/generation; do not overload `tooling/build.py` with application-specific keys. | Test fixtures demonstrate several mappings per HCMO term and reject duplicate registry identities, unresolved IRIs, and contradictory exact/broad mappings. |
| [ ] | B05 | **Source materials supplied by Philippe.** The FAIR Cookbook recipe, ISA RO-Crate article, implementation repository, prior ISA-OBO-PROV mappings, and STATO references are absent from the supplied notes. | Obtain the exact URLs, versions/commits, licenses, and the mapping files Philippe intended. Review them before minting or asserting mappings. | Add bibliographic sources to `docs/paper/references.bib`; add design evidence to `docs/ISA-RO-CRATE-MAPPING.md` and `docs/ALIGNMENTS.md`; preserve third-party license and attribution requirements. | All resources have stable citations and a recorded reviewed version. |
| [ ] | B06 | **HCMO-to-ISA mapping.** The existing table covers investigation, study, source/sample, enclosure, assignment, acquisition, observation, and files, but remains a proposal. | Review each row against the selected ISA model and add cardinality, direction, transformation rule, and round-trip loss notes. | Extend `docs/ISA-RO-CRATE-MAPPING.md`; update `examples/isa-hcmo-bridge.ttl`; add machine-readable entries to the mapping registry if approved. Ontology axioms change only when the relationship is semantic rather than serialization-specific. | Reviewer-approved table with a working example for Investigation -> Study -> Assay -> Process -> Data. |
| [ ] | B07 | **HCMO-to-RO-Crate and Bioschemas mappings.** Current examples use Schema.org/Bioschemas types without a complete profile contract. | Approve the RO-Crate version, ISA profile URI, Bioschemas profiles/types, required fields, and conformance declarations. | `docs/ISA-RO-CRATE-MAPPING.md`, `examples/isa-hcmo-bridge.ttl`, profile validation shapes or tooling, `ontology/context.jsonld` where prefixes/terms are stable, and paper sections. | A packaged example validates against the chosen profile and declares conformance explicitly. |
| [ ] | B08 | **OBI mapping.** Investigation, assay, allocation, acquisition, and analysis processes are not mapped to OBI. | Review candidate OBI terms and relations with definitions and logical context; avoid equivalence based only on similar labels. | Approved mapping artifact and `docs/ALIGNMENTS.md`; process classes/properties in their owning modules only if HCMO specialization is needed; examples and competency questions. | Each mapping has semantic-strength justification and one valid RDF use case. |
| [ ] | B09 | **PROV-O mapping.** The active graph does not model activities, agents, generation, derivation, or attribution for experimental data. | Decide which HCMO processes/entities specialize or merely map to PROV-O and how planned ISA processes relate to executed provenance activities. | Mapping artifact and `docs/ALIGNMENTS.md`; process/data modules; `examples/isa-hcmo-bridge.ttl` or a dedicated provenance example; shapes and queries for required provenance. | End-to-end provenance query from subject/enclosure and sensor through raw data to derived output. |
| [ ] | B10 | **STATO mapping.** Study factors, variables, analyses, and statistical outputs lack reviewed STATO mappings. | Jointly review STATO and ISA definitions before selecting targets. Record rejected candidates as well as accepted ones. | `ontology/modules/hcm-bio.ttl` for approved study-design semantics, the relevant process/result module for analyses and outputs, mapping artifact, examples, queries, and `docs/ALIGNMENTS.md`. | Factor/variable and analysis/output examples round-trip without treating an experimental group as a factor. |
| [ ] | B11 | **Wikidata fallback.** Wikidata should not replace an available stable ontology term without a policy. | Define allowed use cases, identifier stability checks, mapping predicate, and review cadence. | Mapping policy and registry only; ontology modules change only for an approved semantic relation. | Each Wikidata mapping documents why no suitable maintained ontology term was selected. |

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
| A07 | Damien Huzard; reviewed artifact evidence pending | 2026-07-21 | Accept preservation policy; verification pending | Preserve `ontology/legacy/` and `ontology/v2/` as immutable, excluded historical evidence; use modules as source and generated `dist/` files as load targets. No ontology axioms changed. | A07 accepted historical-artifact policy above; exact reviewed file/version/checksum still required | `docs/philippe-rocca-serra-review` |

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
