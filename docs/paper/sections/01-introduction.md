# 1. Introduction

> **Status:** full draft (artifact-independent), from Gilbert (2026). Uses `\cite{}`
> keys defined in `references.bib`. Brand: **HCMO only** (no MAPP). ~1.5 pp.

Behavioural testing is central to preclinical research: it is used to characterise
disease models, assess the effects of treatments, and detect behavioural changes
linked to a physiological or experimental state. In rodents, this still relies
heavily on short tests performed *outside* the animal's home cage, in a novel
environment \cite{kiryk2026}. Such protocols capture only a narrow window of an
animal's activity, are frequently run during the light phase even though rodents
are predominantly nocturnal, and require handling and transfer that introduce
stress and behavioural bias. Together these factors limit the observation of
circadian rhythms, spontaneous behaviours, and subtle changes that emerge only
over long periods, and they contribute to the variability of results across
experiments and laboratories \cite{kiryk2026}.

Home-Cage Monitoring (HCM) inverts this logic: instead of bringing the animal to
the test, the observation is brought into the animal's usual environment. Through
sensors, hardware, and software, an HCM system continuously and non-invasively
observes an animal living in a space that provides food, water, social contact,
and safety, over days or weeks and with limited human intervention
\cite{kiryk2026,huzard2026tech}. This yields more regular, better-contextualised
data and supports the 3Rs (Replacement, Reduction, Refinement) — particularly
Refinement — by reducing handling and handling-related stressors. HCM is, however,
not automatically superior to classical tests: results depend strongly on the
sensor type, the analysis software, the definition of the measured variables, and
the documentation of the experimental context. HCM therefore does not remove
methodological bias so much as *shift* part of it toward technical choices,
interpretation algorithms, and metadata quality \cite{kiryk2026}.

This shift creates a data-interoperability problem. HCM systems vary widely —
video, RFID, infrared and motion sensors, food- and water-intake tracking, or
combinations thereof; commercial, lab-built, or hybrid \cite{huzard2026tech,duarte2026diy}.
Two studies may measure closely related behaviours while using different sensors
and producing different parameters and file formats. Crucially, HCM data are inseparable from
their experimental context: a measurement is interpretable only if one also knows
the animal (species, strain, sex, age, genotype), the enclosure and its
environmental conditions, the device and its configuration, the time, and the
protocol \cite{forrest2026}. This heterogeneity hinders comparison, reuse, and
integration, and stands in the way of FAIR (Findable, Accessible, Interoperable,
Reusable) data \cite{fair}. In animal research, data quality is moreover an
*ethical* concern, since the data are the durable result of animal experimentation
\cite{petit2026wellfair}.

Controlled vocabularies, taxonomies, thesauri, or JSON metadata standards help,
but they fall short for a domain whose value lies in the *relations* between an
animal, an enclosure, a sensor system, a protocol, environmental conditions,
observed behaviours, and provenance. An ontology goes beyond normalising terms: it
formalises the concepts of the domain, specifies their relations, reuses existing
identifiers, and makes the data queryable, comparable, and integrable, while
enabling consistency checking and inference \cite{noy2001}. It also provides an
explicit scaffold for downstream AI: rather than letting models infer relations
from statistical association alone, an ontology constrains interpretation and
makes HCM data usable as a knowledge graph \cite{forrest2026}.

**Contributions.** We present **HCMO**, the Home-Cage Monitoring Ontology. To our
knowledge it is the first ontology to model HCM as an integrated system. Concretely:

1. **An ontology for the HCM domain** organised into five domain modules —
   *core* (enclosures), *bio* (subjects, groups, and housing assignments),
   *env* (environmental conditions and specifications), *obs* (observations and
   results), and *tech* (hardware, sensors, software, and time series) —
   built around an explicit *sensor ≠ observation ≠ result* separation.
2. **Reuse of established standards** rather than reinvention: SOSA
   \cite{sosa}, OWL-Time \cite{owltime}, BFO \cite{bfo}, IAO, and SEMTS.
3. **A FAIR, tool-consumable resource package**: a stable release manifest,
   modular Turtle sources, a reproducibly generated merged graph (TTL/OWL/JSON-LD),
   SHACL shapes, a JSON-LD context, competency-question SPARQL, HTML documentation,
   a persistent IRI, an open licence (CC BY 4.0), and a DOI.
4. **A competency-question-driven evaluation** of coverage and quality.

The ontology is the contribution; natural-language querying of the resulting
knowledge graph and a form-based authoring application are discussed as outlook
(§7), not claimed here. The resource is being developed with a working group of
the COST **TEATIME** network, grounding it in real domain needs.
