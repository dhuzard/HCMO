# 8. Conclusion and future work

> **Status:** full draft (artifact-independent). HCMO only. ~0.5 pp.

We presented HCMO, the first ontology to model Home-Cage Monitoring as an
integrated system spanning the animal subject, its housing, the environment, and
the technical acquisition chain. HCMO captures HCM data together with the
experimental context that makes them interpretable, keeps sensor, observation, and
result distinct, and reuses established Semantic Web standards (SOSA, OWL-Time,
BFO, IAO, and SEMTS) rather than reinventing them. It is delivered as a FAIR,
tool-consumable resource — modular sources, reproducible distributions, SHACL
shapes, competency-question queries, a JSON-LD context, persistent identifiers, an
open licence, and documentation — and is grounded in the COST TEATIME community.

**Limitations.** HCMO is an early, evolving resource. Some conceptual boundaries
are still being stabilised, most notably between raw data, processed measurement,
interpreted observation, and biological result, where the same information can be
viewed at several levels. The diversity of HCM systems makes a single model that is
both broad enough to be reusable and precise enough to describe individual
experiments an ongoing balance. Alignment to external vocabularies is deliberately
partial in this version, and complex pathologies, experimental treatments, advanced
statistics, and AI models on the data were intentionally left out of scope to keep
the core stabilisable.

**Future work.** Planned directions include recording expected answers for
competency queries; freezing a paper-matching release and its archived quality
reports; systematic alignment decisions (reuse as-is vs specialise vs keep
HCMO-specific) and bridge modules to adjacent ontologies (e.g. OBI, MEDO) and
to taxa/anatomy/device vocabularies; modelling quantities and units with QUDT/OM;
populating the ontology with real datasets via the TEATIME network and publishing
the corresponding SPARQL queries; and supporting the downstream uses outlined in
§7. Through these steps, HCMO aims to become a community reference that improves the
annotation, comparison, and reuse of HCM data across laboratories.
