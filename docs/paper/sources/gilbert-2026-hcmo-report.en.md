# Designing an Ontology for Home-Cage Monitoring: structuring, interoperability, and reuse of data

> **English working translation** of the internship report by **Cyril Gilbert**
> (16 June 2026), supervised by Damien Huzard. Source: `gilbert-2026-hcmo-report.fr.pdf`
> (in this folder). This is a faithful adaptation, not a literal line-by-line
> translation; it is the primary domain/design source for the HCMO resource paper.
> Figures referenced below are extracted under `sources/figures/`.

---

## 1. Introduction

In preclinical research, behavioural tests are used to study how an animal
reacts in a given situation — to characterise a disease model, assess a
treatment's effect, or detect behavioural changes linked to a physiological or
experimental state. These tests are central to interpreting animal models.

Preclinical research still relies heavily on **short behavioural tests** in
rodents, often performed **outside the animal's home cage**, in a novel
environment. This can introduce stress and alter the observed behaviours. Such
tests also give a limited view of the animal's real activity: they are short and
frequently run during the day, whereas rodents are more active at night. These
limitations contribute to variability of results across experiments and labs.

**Home-Cage Monitoring (HCM)** proposes a different approach: instead of bringing
the animal to the test, the observation is brought into its usual environment.
Through sensors, hardware, and software, the animal can be followed over long
periods with limited human intervention, yielding more regular, better
contextualised data. HCM contributes to the **3Rs** (Replacement, Reduction,
Refinement) — especially Refinement — by limiting direct handling and
handling-related stressors.

However, the diversity of systems, sensors, measured variables, and their
metadata calls for **more formal structuring**. The objective of this work was to
propose a **first ontology** capable of representing the domain's key concepts and
their relations, to facilitate **reuse, interoperability, and FAIR compliance**
(Findable, Accessible, Interoperable, Reusable).

Beyond data reuse, this structuring matters for **AI uses**. HCM data can be seen
as a future **knowledge graph** in which animals, cages, sensors, observations,
measurements, and metadata are explicitly linked — a basis for queries,
reasoning, or graph machine-learning methods (e.g. knowledge-graph embeddings).
Exchanges with Konstantin Todorov, given his work on knowledge graphs and their
exploitation by learning methods, were important here.

Building an ontology is not merely drawing a data schema: it is about precisely
defining the meaning of the concepts, the relations, and the rules that let a
machine interpret this knowledge. Unlike a classical database (mainly values in
tables), an ontology **formalises a domain**, improving inference, consistency
checking, and knowledge reuse.

> **This report presents an intermediate state of the work: not a finalised
> ontology, but a first structuring of the domain (V1)**, built from reading,
> exchanges with the supervising team, and modelling trials.

## 2. Scientific context: Home-Cage Monitoring

Classical behavioural phenotyping in rodents often relies on short tests outside
the home cage, frequently involving physical transfer to a new test area with
time-limited observation. These conditions reduce the ability to observe
**circadian rhythms** (24 h cycle), spontaneous behaviours, and subtle changes
that appear more clearly over long periods.

Tests such as the open field or certain mazes remain useful for targeted
behaviours but capture only a limited window of real activity; transfer and human
handling can introduce stress or behavioural bias, complicating interpretation.

HCM **inverts the experimental logic**: the observation device is integrated into
the animal's usual environment. An HCM system collects information on an animal
living in a space that provides food, water, social contact, and safety. The
system combines a **living environment, hardware, sensors, sometimes actuators,
and acquisition/analysis software** (see *Figure 1 — conceptual definition of HCM
via the Olog model*, after Kiryk et al.). HCM is therefore a **complete system**,
not a single isolated sensor.

This approach can yield data over days or weeks, capturing spontaneous
behaviours, circadian rhythms, micro-variations in activity, or early signs of
pathology — with ethical benefits (less handling, less stress, 3Rs).

> **Caveat (important for the paper's honesty):** HCM should not be presented as
> automatically superior to classical tests. It has its own limits. Results depend
> strongly on the sensor type, the analysis software's quality, the definition of
> measured variables, and the documentation of experimental context. HCM **does
> not remove methodological bias — it shifts part of it** toward technical
> choices, interpretation algorithms, and metadata quality.

*Figure 2* illustrates the diversity of behavioural and physiological parameters
measurable in HCM. This richness creates new difficulties: HCM systems vary
widely (sensors, software, species, parameters, output formats), which complicates
comparison, reuse, and integration. This is exactly where **ontology-based
structuring** becomes relevant — linking measurements to their experimental,
technical, and biological context.

## 3. Ontologies, the Semantic Web, and data structuring

### 3.1 Foundations of the Semantic Web

The Semantic Web aims to make data more machine-understandable, via a layered
architecture (*Figure 3*):

- **URI/IRI** — globally unique, stable, reusable identifiers for resources
  (a class, property, or entity).
- **RDF** — the base representation model: information as **triples**
  (subject–predicate–object) forming a graph (e.g. animal→cage→HCM system,
  sensor→observation). Serialisable as RDF/XML or **Turtle**; Turtle was the
  target format here, being readable for manual checking.
- **RDFS** — a first semantic layer: classes, subclasses, properties, domain and
  range.
- **OWL** — richer constraints: property restrictions, class equivalences, logical
  relations; usable by **reasoners** that check consistency and infer new facts.
- **SPARQL** — querying RDF graphs (e.g. find sensors associated with a cage, the
  observations produced by a device, or measurements lacking a unit).

The goal is not just a visual schema, but a representation usable by Semantic Web
tools: identifiers for concepts, RDF triples for relations, OWL classes/properties
for structure, and SPARQL for querying.

### 3.2 Design methodologies

An ontology is rarely built in one pass. Work usually starts by identifying domain
needs, often expressed as **competency questions** — questions the ontology should
be able to answer. Recent methods such as **SAMOD** and **LOT** propose
**incremental construction**: enrich by stages, test, then correct. This iterative
logic suits HCM, where concepts are numerous and sometimes hard to stabilise.

### 3.3 Role of language models and knowledge graphs

Large language models (LLMs) can assist some ontology-engineering steps:
proposing concepts, reformulating competency questions, organising a first model,
or extracting structured elements from text/unstructured data. Two modes:

- **Top-Down** — the model assists, but the **expert keeps control**.
- **Bottom-Up** — the model extracts elements directly from data to propose a
  structure, often via **Retrieval-Augmented Generation (RAG)**.

For HCMO, AI is not only an aid to construction: the **ontology can structure the
future use of AI**. By imposing explicit classes, relations, and constraints, it
prevents automated processing from relying solely on hard-to-interpret
statistical associations. HCMO can thus serve as a **basis for an HCM knowledge
graph**.

*Figure 4* (schema by Gaoussou Sanou) shows a concrete KG-querying pipeline: a
natural-language question is turned into a **Cypher** query by a **LangChain**
module, executed on a **Neo4j** graph, and the results are converted back to text.
The LLM does not query raw data but relies on an explicit graph. Such a graph
could likewise be queried via **SPARQL**, used for symbolic reasoning, or fed to
graph-learning methods. **Knowledge-graph embeddings** represent entities and
relations in a vector space to explore similarities, predict missing links, or
identify recurring profiles; recent biomedical-KG/embedding work shows their value
for exploring entity relations and predictive tasks.

Another use exploits an ontology's **hierarchical structure** directly in a
predictive model. In protein-function prediction work, Antoine Toffano uses the
**Gene Ontology** to represent functions and their hierarchical dependencies
(*Figure 5*): a general biological function can subsume more specific ones,
yielding predictions more consistent with biological knowledge and more
interpretable.

> These approaches must be used cautiously — they may propose false or overly
> general relations. **Human validation remains necessary**, especially when the
> ontology underpins downstream automated processing.

### 3.4 Best practices and tooling

- **Protégé** — create OWL classes, properties, axioms; works with reasoners.
- **WIDOCO** — generate readable documentation.
- **OOPS!** — detect frequent pitfalls (poorly described classes, ambiguous
  relations).

### 3.5 Why go all the way to an ontology?

Several levels of structuring exist: a **controlled vocabulary** (common terms),
a **taxonomy** (simple hierarchy), a **thesaurus** (vocabulary relations:
synonyms, broader/associated terms), and a **metadata standard** (e.g. JSON).
These are useful but limited for a complex domain like HCM. HCM data do not
describe isolated measurements: they link an animal, a cage, a sensor system, an
experimental protocol, environmental conditions, observed behaviours, and
provenance metadata. **Interoperability in HCM needs both shared vocabularies and
shared ontologies**, able to connect behaviours, physiological measurements, and
experimental conditions in a machine-exploitable semantic layer.

An ontology goes beyond word normalisation: it formalises concepts, specifies
relations, reuses existing identifiers, and makes data more queryable, comparable,
and integrable. In preclinical research this aligns with **FAIR**. The **WellFAIR**
approach (*Figure 6*) stresses that **data quality is also an ethical issue**,
since data are the durable result of animal experimentation.

## 4. Work carried out during the internship

### 4.1 Domain analysis

Before modelling, it was necessary to clarify the objects, practices, and
scientific needs of HCM, and to identify recurring notions: the observed animal,
its living environment, hardware devices, sensors, software, produced
measurements, observed behaviours, and the metadata needed to interpret the data.

HCM differs from classical tests by relying on **continuous or repeated
acquisition in the animal's usual environment**. It is not enough to know that a
measurement was produced: one must describe **under what conditions, with which
system, on which animal, in which cage, with which environmental parameters, at
what time, and under which protocol**. HCM data are **inseparable from their
experimental context**.

A key difficulty is the **diversity of HCM systems**: video, RFID, infrared
sensors, motion sensors, food/water-intake tracking, or combinations; systems may
be commercial, lab-built, or hybrid. This diversity is a scientific asset but
complicates comparison and reuse — two experiments may measure similar behaviours
with very different sensors, formats, and parameters.

The analysis also highlighted the importance of **metadata** — not secondary
add-ons but determinants of understanding: species, strain, sex, age, housing
conditions, enrichment, cage configuration, sensor type, acquisition frequency,
software, protocol, applied data processing. Without these, a measurement becomes
hard to interpret, compare, or reuse.

Consequently, HCM was treated as a **set of relations** rather than a list of
objects: an animal lives in an environment; a system observes it; a sensor
produces a measurement; a measurement concerns a behaviour or physiological
variable; all of it sits within an experimental protocol. This **relational view
justifies an ontology**.

### 4.2 Main concepts (the four module families)

Concepts were grouped into **four families = the HCMO modules**, keeping a
consistent reading order between domain analysis, concept presentation, and model
figures:

- **HCMO-bio** — the animal subject and biological observations (species, strain,
  sex, age, genotype; weight, health, behaviour observations).
- **HCMO-housing** — housing and experimental context (cage, animal-to-environment
  assignment, experimental groups, study factors).
- **HCMO-env** — environmental conditions (cage dimensions, enrichment, light
  cycles, gas profiles, and measurable properties like temperature, humidity,
  light intensity).
- **HCMO-tech** — technical devices (hardware, sensors, software, time series, and
  produced data objects), covering technologies such as video, RFID, infrared,
  motion sensors, lickometers/passage gates, weight sensors, physiological
  devices.

This separation avoids mixing things of different natures (the animal, its
environment, the producing sensor, the transforming software, the documenting
metadata) and keeps coherence with the graphical views.

> **Note on the published repo vs. this report:** the report names modules
> `bio / housing / env / tech`, whereas the released ontology uses
> `core / bio / env / obs`. Reconcile naming before the paper (see OPEN-QUESTIONS).

### 4.3 Construction method

- First explored **LinkML** with a YAML representation to describe classes and
  properties; a working spreadsheet listed concepts, properties, expected types,
  and important relations.
- Then moved to **Chowlk**, which turns a graphical conceptualisation made in
  **diagrams.net** into OWL (serialised in **Turtle**). This kept a readable
  graphical model that is easy to discuss with domain experts while remaining
  convertible to Semantic Web formats — well suited to a V1.
- Tool roles differ by phase: **Protégé** for exploring OWL structure and checking
  properties; **WIDOCO** and **OOPS!** for documentation and QA; **Chowlk**
  privileged for the current graphical-modelling phase.

**Competency questions** guided stabilisation, covering animal-to-cage assignment,
experimental groups, weight/behaviour observations, environmental conditions,
measurement provenance, and metadata quality. Examples:

- Which enclosure is `Subject_001` assigned to at time *T*?
- Which subjects are currently housed in `Room_101`?
- What is the latest recorded weight of `Subject_001`?
- Which subjects were exposed to temperature above 25 °C?
- Which sensors monitor `Enclosure_A2`?
- Are there observations with numeric values but no units?

A substantial part of these can be represented by the current modules, justifying
the **V1** status: not finalised, but already covering the main identified needs.

### 4.4 Characteristics of HCMO and intended uses

**Table 1 — Main characteristics of the current HCMO version**

| Element | Count |
|---|---|
| HCMO-specific classes | ~45 |
| HCMO-specific properties | ~46 |
| Reused classes | 6 |
| Reused properties | 17 |
| Declared prefixes | 12 |

These figures indicate the model's size and the share of already-reused
resources, situating HCMO as a **shareable resource**, close to the criteria
expected for publishable ontology resources in the Semantic Web community (e.g.
at conferences such as **ISWC**).

> At this stage, **HCMO has no public repository or SPARQL endpoint yet**. Next
> steps: publish the OWL/Turtle file, document the ontology, provide instance
> examples, then offer SPARQL queries matching the competency questions. *(NB:
> the GitHub repo, w3id PURL, Zenodo DOI, and WIDOCO docs now exist — update this
> when writing the paper.)* The "in-use" part (instances + queries) is to be
> developed in future report versions.

### 4.5–4.6 Building the ontology — classes and relations

The full model was too dense to read directly, so it was split into **thematic
working views** (not independent ontologies): metadata/prefixes, the animal
subject, housing, environment, environmental observations, and technical
acquisition.

- **HCMO-bio** (*Figure 7*, `fig07_hcmo-bio.png`): centred on `hcm-bio:Subject`,
  linked to weight, health, and behaviour observations; **behavioural results are
  represented separately from observation events**, preserving the concerned
  subject, observed property, observation time, used procedure, and (when present)
  the associated result. Observation classes reuse **SOSA** properties
  (`sosa:resultTime`, `sosa:observedProperty`, `sosa:usedProcedure`,
  `sosa:hasResult`, `sosa:hasFeatureOfInterest`) and **OWL-Time**
  (`time:hasBeginning/hasEnd/inXSDDateTime`, `time:ProperInterval`).
- **HCMO-housing** (*Figure 8*, `fig08_hcmo-housing.png`): links the subject, its
  experimental group, and the enclosure. A `HousingAssignment` class represents
  the assignment **in time** rather than treating cage membership as permanent;
  relations to groups and study factors place housing in the protocol context.
- **HCMO-env** (*Figure 9*, `fig09_hcmo-env.png`): associates the enclosure with an
  environmental profile (dimensions, light cycle, measurement specifications).
  Environmental **properties** (temperature, humidity, gas concentrations) are
  **distinguished from the values** describing them, allowing one property to have
  several quantitative or categorical observations.
- **HCMO-tech** (*Figure 10*, `fig10_hcmo-tech.png`): the acquisition chain among
  hardware, sensors, software, and time series — a sensor is installed in an
  enclosure, communicates with hardware/software, and produced data can be
  organised into time series and segments, keeping **technical provenance**
  separate from biological interpretation.

**Key modelling choice (*Figure 11*):** do **not** conflate the **sensor** (a
technical device), the **observation** (the measurement act/event in context), and
the **result** (the produced value/interpretation). This lets the model state that
a given sensor produced an observation, that the observation concerns a particular
property, and that the result has a value, a unit, and possibly a confidence
level. This matters in HCM because outputs are not always behaviours directly: a
camera, weight sensor, or RFID first produces signals/measurements, later
transformed by software to infer a behaviour, activity, or physiological state.
The chain **device → observation → measurement → interpretation** is preserved,
keeping the link between data and its production context.

## 5. Discussion and perspectives

The model is a **first working version (V1)** — not finalised, but a first
stabilised state: main modules identified, a large part of the competency
questions representable, and first views discussed with domain experts. The work
draws on exchanges with Damien Huzard and a working group linked to the **COST
TEATIME** network (incl. Benoît Petit-Demoulière, Davor Virag, Vootele Voikar),
confronting the model with real domain needs rather than purely theoretical
reading.

**Limitations:**

1. **Maturity.** The big families are representable, but some boundaries remain
   hard to stabilise — notably between **raw data, processed measurement,
   interpreted observation, and biological result**. The same information may be a
   sensor-produced datum, a contextualised observation, or a software-interpreted
   result. To be refined.
2. **System diversity.** Hard to produce a single model covering all cases
   (video, RFID, motion, weight, intake-tracking, physiological devices) without
   becoming too general. HCMO must stay **broad enough to be reusable, precise
   enough to describe experiments** — an ongoing balance.
3. **Deliberate omissions in V1.** Precise pathologies, complex experimental
   treatments, advanced statistics, and AI models on the data were left aside to
   keep the model stabilisable; priority was the main chain (subject →
   environment → acquisition → observation → measurement → result → metadata).
4. **Alignment.** V1 already uses some standards/vocabularies (**SOSA**,
   **OWL-Time**, **UO**), but alignment is **partial**. Next steps must
   systematically decide which concepts to reuse as-is, specialise, or keep
   HCMO-specific, to avoid an isolated ontology.

**Reasoning value.** Beyond organising data, the ontology enables reasoning. A
first level is classical: check that an observation has a unit, that an animal is
linked to a cage over a time interval, or that an environmental measurement is
linked to a sensor — helping detect inconsistencies or missing metadata. A second
level concerns **AI**: HCMO can constrain interpretation by providing an explicit
domain structure (which entities exist, which relations are possible, which
context is needed to interpret a measurement), making analyses more controlled,
explainable, and FAIR-compatible.

**Positioning vs. LOT.** Construction began with needs and competency questions,
then progressive model building — close to a **release-candidate** preliminary
state in the LOT sense: not yet stable or published, but structured enough to be
evaluated, discussed, and corrected with experts.

**Evaluation plan (multi-level):** (i) user-need satisfaction via competency
questions and expert feedback; (ii) quantitative measures — number of questions
covered, classes/properties, proportion of aligned concepts, errors found by
validation tools; (iii) practical evaluation — whether the ontology really
produces useful, queryable, reusable annotations in HCM use cases.

**Next steps:** documentation, concrete use cases, adding instances, and alignment
with other vocabularies/ontologies. Longer term, HCMO could underpin better
annotation of HCM datasets, ease cross-lab comparison, and support more advanced
analysis, including with AI tools.

## References

Key references from the report (full list in the source PDF):

- [4] Chávez-Feria, García-Castro, Poveda-Villalón. **Chowlk**: from UML-based
  ontology conceptualizations to OWL. ESWC 2022, LNCS 13261, 338–352.
- [7] Forrest, Huzard, Restivo, Baran, Petit-Demoulière. **Data sharing and
  metadata.** In *Home Cage Monitoring in Rodents: A Global Effort*, Springer 2026.
- [9] Garijo. **WIDOCO**: A Wizard for Documenting Ontologies. ISWC 2017,
  LNCS 10588, 94–102.
- [11] Huzard et al. **Technologies for home cage monitoring in preclinical
  research.** In *Home Cage Monitoring in Rodents*, Springer 2026.
- [12] Kiryk, Bartelik, Wells, Gates. **Home cage monitoring: where we are and
  what we need?** In *Home Cage Monitoring in Rodents*, Springer 2026.
- [13] Moxon et al. **LinkML**: a general-purpose data modeling framework. ICBO
  2021, CEUR 3073, 148–151.
- [14] Noy & McGuinness. **Ontology Development 101.**
- [15] Peroni. **SAMOD**: A Simplified Agile Methodology for Ontology Development.
  OWLED 2017, LNCS 10161, 55–69.
- [16] Petit-Demoulière & Huzard. **Data welfare is animal welfare: building a
  WellFAIR research ecosystem.** *Neuroscience Applied* 5:106998, 2026.
- [17] Poveda-Villalón et al. **LOT**: An industrial-oriented ontology engineering
  framework. *Eng. Appl. of AI* 111:104755, 2022.
- [18] Poveda-Villalón, Suárez-Figueroa, Gómez-Pérez. **Validating Ontologies with
  OOPS!** EKAW 2012, LNCS 7603, 267–281.
- [19] Sanou, Manso, Todorov, Giudicelli, Duroux, Kossida. **Therapeutic mAb
  repurposing in oncology via IMGT/mAb-KG embeddings.** *BMC MIDM* 26(1):89, 2026.
- [2] Butz, Azé, Todorov, Toffano, Larmande. **Leveraging ontology structure for
  machine learning in knowledge graphs.**
- [1] Bian. **LLM-empowered knowledge graph construction: a survey**, 2025.
  arXiv:2510.20345. · [3] Cappelli & Di Marzo Serugendo, *Electronics* 14(14):2863,
  2025. · [8] Gangemi et al., **Modelling Ontology Evaluation and Validation**,
  ESWC 2006, LNCS 4011. · [5] Dean & Schreiber, **OWL**. · [10] Horridge,
  *Practical Guide to Building OWL Ontologies with Protégé*. · [6]
  Duarte-Domingues et al., **DIY Home Cage Monitoring**, Springer 2026. · [20]
  Stanford BMIR, **Protégé 5 Documentation**.
