# Abstract

> **Status:** full draft (~190 words). LNCS abstract; HCMO only (no MAPP). The
> resource-metadata block (`metadata/resource-metadata.md`) goes immediately after.

Home-Cage Monitoring (HCM) observes laboratory animals continuously and
non-invasively in their own cage, improving the contextual richness and
reproducibility of preclinical data while advancing the 3Rs. Yet HCM systems are
highly heterogeneous — differing in sensors, measured variables, software, and
output formats — and their data are inseparable from a rich experimental context.
This heterogeneity hinders comparison, reuse, and FAIR data sharing. We present
**HCMO, the Home-Cage Monitoring Ontology**, which, to our knowledge, is the first
ontology to model HCM as an integrated system. HCMO is organised into four modules
— animal subject, housing, environment, and technical acquisition — and is built
around an explicit separation of sensor, observation, and result, preserving the
chain from device to interpreted measurement. It reuses established standards
(SOSA/SSN, OWL-Time, UO, PROV, BFO) rather than reinventing them, and is delivered
as a FAIR, tool-consumable package: modular sources, reproducibly generated
distributions (Turtle/OWL/JSON-LD), SHACL shapes, competency-question queries, a
JSON-LD context, persistent identifiers, an open licence, and documentation. We
describe its design, evaluate it through competency questions and ontology-quality
tooling, and discuss its uptake within the COST TEATIME community.

> Keywords: ontology · home-cage monitoring · laboratory animals · FAIR data ·
> knowledge graph · SOSA/SSN · animal welfare · 3Rs
