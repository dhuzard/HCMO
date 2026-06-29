# 7. Impact, use cases, and outlook

> **Status:** full draft (artifact-independent). Scope (HITL R2/R3): the items
> below are **potential uses / outlook enabled by HCMO**, not contributions claimed
> by this paper. HCMO only. ~1 pp.

**Why HCMO matters.** By giving the HCM domain a shared, machine-actionable model,
HCMO addresses a concrete obstacle to open, comparable preclinical science. Linking
each measurement to its subject, enclosure, environment, device, and protocol makes
datasets findable, comparable across systems and laboratories, and reusable —
turning siloed, vendor-specific exports into interoperable knowledge. Because, in
animal research, the data are the durable result of the experiment, better data
structuring is also an ethical contribution, supporting the 3Rs and the WellFAIR
view that data quality is part of animal welfare \cite{petit2026wellfair,fair}.

**Reasoning and data quality.** Beyond organisation, the ontology enables
reasoning. A first, immediately useful level is consistency and completeness
checking — for example, flagging an observation whose numeric value has no unit, or
an animal not assigned to an enclosure over a given interval — which helps surface
missing metadata at ingestion. A second level uses HCMO as an explicit scaffold for
AI: rather than letting a model infer relations from statistical association alone,
the ontology constrains *which* entities and relations are admissible and *what*
context is needed to interpret a measurement, making downstream analyses more
controlled and explainable.

**Potential uses (outlook).** HCMO is designed to underpin further tooling that we
do not claim as contributions here:

- *Knowledge-graph question answering.* HCMO can structure an HCM knowledge graph
  queried in natural language: a question is translated to a formal query, executed
  over the graph, and the result rendered back as text — a pattern demonstrated in
  related work on biomedical knowledge graphs and embeddings
  \cite{sanou2026,bian2025}. The same graph can support symbolic reasoning or
  graph-learning methods that exploit the ontology's hierarchical structure
  \cite{butz}.
- *Assisted authoring.* A form-based authoring application can guide users through
  the mandatory and recommended fields, exporting conformant ABoxes — lowering the
  barrier for biologists to produce well-structured, SHACL-valid data.
- *Vendor-data mapping.* Proprietary device exports can be lifted into HCMO,
  enabling cross-system comparison without forcing a single acquisition format.

**Adoption path.** Development is grounded in the COST **TEATIME** network, which
provides domain feedback and a route to real datasets for validation and uptake.
This community anchoring is intended to drive adoption beyond a single laboratory
and to keep the model aligned with evolving HCM practice.
