# Home-Cage Monitoring Ontology: interoperability, structure, and implementation

Meeting participant: Philippe Rocca-Serra

Meeting date: not recorded in the supplied notes

Repository capture date: 2026-07-20

Status: meeting record; proposals and open questions are not accepted ontology changes

## Meeting objective

The discussion focused on improving the structure, readability,
interoperability, and practical serialization of the Home-Cage Monitoring
Ontology, or HCMO. Particular attention was given to alignment with ISA,
RO-Crate, OBO ontologies, PROV-O, STATO, OBI, Bioschemas, and FAIR
implementation practices.

## 1. ISA and RO-Crate interoperability

A principal recommendation was to support an export based on ISA RO-Crate.
Compatibility with ISA-Tab and ISA-JSON should also be evaluated, although
these formats may be implemented as secondary serialization options rather than
as the primary representation.

The FAIR Cookbook contains relevant guidance on connecting ISA and RO-Crate.
Philippe also shared an article and an implementation describing an ISA profile
for RO-Crate, including mappings between:

- Bioschemas entities;
- ISA concepts and structures;
- RO-Crate entities and properties; and
- RDF representations.

These resources should be incorporated into the HCMO design checklist and cited
in the ontology paper when discussing FAIRness and interoperability.

HCMO may require several profiles operating at different levels. For example,
one profile could represent the overall ISA investigation or study object,
while more specific profiles could represent study factors, experimental
groups, observations, devices, processes, and generated datasets.

The implementation should determine how HCMO concepts map to:

- ISA study and assay structures;
- ISA study factors;
- ISA-Tab fields;
- ISA-JSON fields;
- ISA RO-Crate entities;
- Bioschemas types and properties;
- OBO Foundry terms;
- PROV-O provenance entities and activities;
- STATO statistical concepts; and
- Wikidata identifiers, where useful.

Existing mappings previously developed by Philippe between ISA, OBO
ontologies, PROV-O, and potentially Wikidata should be reviewed before creating
new mappings.

## 2. Mapping architecture

The mappings should be represented explicitly within the HCMO resources rather
than being managed only through application-specific Python code.

A previous Python implementation encountered difficulties when several URIs
could correspond to the same key or internal concept. A more formal mapping
layer may resolve this problem by distinguishing:

- the canonical HCMO identifier;
- exact equivalence mappings;
- close or broader conceptual mappings;
- serialization-specific field mappings; and
- external vocabulary identifiers.

The implementation should avoid treating every mapping as strict identity.
Appropriate semantic relationships may include:

- `owl:equivalentClass`;
- `owl:equivalentProperty`;
- `owl:sameAs`, only when true identity is justified;
- `skos:exactMatch`;
- `skos:closeMatch`;
- `skos:broadMatch`;
- `skos:narrowMatch`; and
- database cross-references or annotation properties.

The choice of mapping predicate should depend on the semantic strength of the
relationship.

## 3. Ontology readability in Protege and OLS

Opening the current OWL file in Protege exposes identifiers such as
`BFO_0000019`, rather than immediately understandable labels. This makes the
ontology difficult to inspect and navigate.

The ontology should therefore ensure that labels from imported resources are
available and displayed. Every reused class should retain or expose:

- its source URI;
- its preferred `rdfs:label`;
- relevant synonyms;
- its source ontology; and
- mapping or equivalence annotations where applicable.

The import strategy should also be revised. Full ontology imports may introduce
unnecessary complexity and unreadable hierarchies. A more controlled import
mechanism, such as a MIREOT-style subset or another curated import workflow,
should be considered.

The OWL release intended for Ontology Lookup Service ingestion must be
self-consistent, readable, and resolvable. Labels, definitions, imports,
domains, ranges, and source annotations should remain accessible after
publication.

## 4. Proposed upper-level organization

To make HCMO easier to understand, its domain concepts could be organized
beneath four principal categories:

1. Process entity.
2. Physical entity.
3. Material entity.
4. Information entity.

This simplified navigation structure should remain semantically compatible with
the relevant upper ontology. The exact relationship between "physical entity"
and "material entity" must nevertheless be clarified, because material entities
are generally treated as a type of continuant or physical entity in BFO-aligned
models.

The four-category view could be implemented as a user-facing organizational
layer, while preserving more formally correct upper-level axioms underneath.

Each HCMO term should be placed under the appropriate category and connected to
its source class through explicit mappings, synonyms, or equivalence statements.

## 5. Classes requiring review

The following placements were discussed:

- `Person` should be placed under material entity.
- `Place` may also belong under material entity, although the distinction
  between a physical location, a spatial region, and a facility should be
  checked.
- `Actuator` should be placed under material entity.
- The ontology currently appears to contain duplicated actuator subclasses.
  These duplicates must be identified, compared, and either merged or
  distinguished.

The class hierarchy should be reviewed systematically to identify:

- duplicate concepts;
- incorrectly placed classes;
- imported classes without labels;
- classes lacking definitions;
- classes with ambiguous source mappings; and
- unnecessary locally created terms that already exist elsewhere.

## 6. Object properties

Every object property should have a documented domain and range.

This is important for several reasons:

- it makes the ontology easier to read;
- it clarifies which entities can participate in each relation;
- it supports competency questions concerning links between variables and
  entities;
- it improves consistency checking; and
- it may assist automated reasoning and ontology navigation.

However, domain and range axioms must be used carefully. In OWL, they are
inferential axioms rather than simple validation constraints. Assigning an
overly narrow domain or range can unintentionally classify entities.

For each property, HCMO should document:

- preferred label;
- definition;
- source or provenance;
- domain;
- range;
- inverse property, where relevant;
- parent property;
- examples of use; and
- applicable competency questions.

SHACL shapes may be useful alongside OWL axioms when the objective is data
validation rather than logical inference.

## 7. Addition of processes

Processes should be represented more explicitly in HCMO.

A process-centred model would make it possible to describe:

- inputs;
- outputs;
- participating entities;
- devices or actuators involved;
- agents responsible for the process;
- temporal ordering;
- generated data;
- transformations applied to data; and
- experimental and analytical events.

Potential processes include:

- housing assignment;
- animal allocation;
- acclimatization;
- behavioural recording;
- sensor measurement;
- event detection;
- data acquisition;
- data preprocessing;
- feature extraction;
- statistical analysis;
- data transformation;
- annotation; and
- quality-control assessment.

Processes can connect material entities with information entities. For example,
an animal and a sensor may participate in a recording process that generates a
time-series dataset.

This structure should improve alignment with:

- OBI for investigations, assays, inputs, and outputs;
- PROV-O for entities, activities, agents, generation, derivation, and
  attribution;
- STATO for statistical analysis and statistical outputs; and
- ISA for study and assay workflows.

The interoperability enabled by these process representations should be
described explicitly in the HCMO paper.

## 8. Inputs, outputs, and information entities

Each relevant process should identify its expected inputs and outputs.

Outputs may include different types of information entities, such as:

- raw data;
- processed data;
- behavioural observations;
- detected events;
- annotations;
- extracted features;
- summary measures;
- statistical estimates;
- statistical models;
- figures;
- tables; and
- quality-control reports.

This distinction will support the description of transformations from
observations to derived variables and statistical results.

It should also make it possible to represent the provenance chain from:

1. animal or home-cage environment;
2. recording device or sensor;
3. acquisition process;
4. raw dataset;
5. preprocessing process;
6. derived variable;
7. statistical analysis; and
8. statistical output.

## 9. Study factors and experimental groups

The representation of study factors requires further work.

HCMO should establish how the following concepts are related:

- study factor;
- factor value;
- independent variable;
- experimental condition;
- treatment;
- genotype;
- sex;
- age;
- housing condition;
- experimental group;
- control group;
- cohort; and
- subject assignment.

The ontology should determine how these concepts map to ISA study factors and
STATO concepts.

An experimental group should not automatically be treated as equivalent to a
study factor. A study factor generally represents a variable or condition,
while an experimental group represents a collection of subjects sharing one or
more factor values.

The model may therefore require explicit relations such as:

- group has member;
- subject assigned to group;
- group defined by factor value;
- study has factor;
- subject has factor value;
- assay evaluates factor; and
- statistical analysis uses variable.

The ISA representation and the STATO representation should be examined together
before selecting final classes and relations.

## 10. Controlled vocabularies and SKOS

SKOS was suggested as a possible mechanism for representing controlled
vocabularies.

SKOS may be appropriate for controlled lists whose elements do not require full
OWL class semantics. Examples could include:

- behavioural labels;
- housing-condition categories;
- recording modalities;
- device-status values;
- quality-control codes;
- experimental role terms; and
- data-processing categories.

A SKOS concept scheme can provide preferred labels, alternative labels,
definitions, and broader or narrower relationships without requiring every
controlled term to become an OWL class.

A decision is still required concerning which elements should be represented
as:

- OWL classes;
- OWL individuals;
- SKOS concepts;
- literal values constrained by SHACL; or
- externally maintained controlled vocabulary terms.

## 11. Serialization and FAIR publication

The target serialization should support RDF while remaining compatible with
established research-data packaging formats.

ISA RO-Crate is a strong candidate for the principal exchange format because it
can combine:

- structured study metadata;
- linked data;
- file-level descriptions;
- provenance;
- Bioschemas annotations; and
- references to external ontologies.

ISA-Tab and ISA-JSON compatibility should be evaluated as complementary
representations.

The HCMO serialization strategy should define:

- the canonical ontology representation;
- the canonical metadata profile;
- required and optional fields;
- mappings to ISA;
- mappings to RO-Crate;
- mappings to Bioschemas;
- mappings to OBI, PROV-O, and STATO;
- RDF serialization formats;
- identifier and URI policies;
- validation mechanisms; and
- versioning and correction procedures.

## Action checklist from the meeting

### Ontology structure

- Reorganize HCMO concepts under a simplified upper-level structure.
- Clarify the distinction between physical entity and material entity.
- Add process entities and process-specific relations.
- Place person, actuator, and relevant physical objects under material entity.
- Determine the correct ontological treatment of place.
- Identify and resolve duplicated actuator subclasses.
- Review all classes for labels, definitions, synonyms, and provenance.

### Properties and reasoning

- Define a domain and range for every object property.
- Check that domains and ranges do not create unintended OWL inferences.
- Add inverse and parent properties where useful.
- Connect properties to competency questions.
- Consider SHACL for constraint validation.

### Imports and publication

- Revise the ontology import strategy.
- Ensure imported terms retain readable labels.
- Produce a clean OWL release suitable for OLS ingestion.
- Test the ontology in Protege and an automated reasoner.
- Check URI resolution and imported-term accessibility.

### ISA and RO-Crate

- Review the FAIR Cookbook guidance on ISA and RO-Crate.
- Review the shared ISA RO-Crate profile article and implementation.
- Locate and examine `ISA RO-Crate Mapping.md`.
- Create an HCMO-to-ISA mapping table.
- Create an HCMO-to-RO-Crate mapping table.
- Create an HCMO-to-Bioschemas mapping table.
- Evaluate ISA-Tab and ISA-JSON exports.
- Define which profiles apply at investigation, study, assay, process, object,
  and dataset levels.

### External ontologies

- Review existing ISA-to-OBO mappings.
- Map investigation and assay processes to OBI.
- Map provenance entities and processes to PROV-O.
- Map statistical variables, analyses, and outputs to STATO.
- Evaluate Wikidata mappings where stable ontology terms are unavailable.
- Record the strength and type of every external mapping.

### Study design

- Formalize study factors and factor values.
- Distinguish study factors from experimental groups.
- Model subject-to-group assignment.
- Model groups defined by combinations of factor values.
- Determine the corresponding ISA and STATO representations.

### Controlled vocabularies

- Identify candidate vocabularies for SKOS representation.
- Decide which terms require OWL semantics and which only require controlled
  labels.
- Define concept schemes, preferred labels, synonyms, and hierarchy rules.

### Implementation

- Replace ambiguous Python key-to-URI handling with an explicit mapping
  registry.
- Permit several external mappings for one HCMO concept.
- Distinguish exact identity from approximate or broader mappings.
- Add validation tests for duplicated keys, unresolved URIs, and conflicting
  mappings.
- Test RDF serialization and round-trip conversion.
- Validate generated ISA RO-Crate packages.

### Paper

The HCMO paper should explain that interoperability is achieved through:

- reuse of established ontology terms;
- explicit semantic mappings;
- ISA and RO-Crate compatibility;
- process-based input and output modelling;
- provenance alignment with PROV-O;
- experimental workflow alignment with OBI;
- statistical alignment with STATO;
- machine-readable RDF serialization;
- controlled-vocabulary management;
- validation and resolvable identifiers.

## Open questions

1. Should ISA RO-Crate become the canonical metadata exchange format, or only
   one supported export?
2. Which ISA RO-Crate profile and mapping implementation did Philippe
   recommend?
3. Should the four top-level categories be formal OWL parents or only a
   simplified navigation layer?
4. How should place be represented: material entity, spatial region, site,
   facility, or another imported concept?
5. Which study-factor concepts already exist in STATO, OBI, or ISA-related
   ontologies?
6. Which vocabularies should use SKOS rather than OWL classes?
7. Should mappings be embedded in the OWL file, maintained in a separate
   mapping artifact, or both?
8. Which elements are required for the first HCMO ISA RO-Crate profile?
9. Which mappings developed previously by Philippe can be reused directly?
10. Should SHACL shapes be delivered alongside the ontology and metadata
    profile?

## Resources still to add

- Link to the relevant FAIR Cookbook recipe.
- Link to the ISA RO-Crate profile article.
- Link to the implementation repository.
- Link to `ISA RO-Crate Mapping.md`.
- Philippe's previous ISA-OBO-PROV-O mapping resources.
- Relevant STATO terms for factors, variables, analyses, and outputs.

## Repository follow-up

Use the
[human review checklist](../PHILIPPE-ROCCA-SERRA-HUMAN-REVIEW-CHECKLIST.md)
to record decisions and route approved work to exact repository artifacts.
