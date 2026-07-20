# 5. Engineering, availability, and sustainability

> **Status:** full draft reconciled with HCMO 0.2.0. External deployment and
> paper-matching archival tasks remain marked as pending. ~1.5 pp.

HCMO is released not as a single file but as a **tool-consumable package** designed
so that downstream tools can resolve every component programmatically.

**Release manifest as a stable contract.** A machine-readable manifest
(`hcmo.yaml`) declares the ontology's identity (name, version, namespace, prefix,
ontology and version IRIs), the ordered list of source modules, the generated
distributions, the SHACL shapes, the competency-question index, and the example
datasets. Its *shape* is treated as an API and kept stable across releases, so a
consumer (e.g. a synchronisation or question-answering layer) can discover paths
from the manifest rather than hard-coding them.

**Modular sources and reproducible distributions.** The ontology is authored as
five domain Turtle sources (*core/bio/env/obs/tech*) plus a migration-only
compatibility module. A build step merges them into a canonical, sorted
serialisation, producing byte-identical output on
re-run so that version-control diffs stay clean. The merged graph is published in
three syntaxes — Turtle, RDF/XML (OWL), and JSON-LD — together with a flat term
inventory (`profile.json`: IRIs, labels, comments, and counts) intended for sync
layers and user interfaces. Everything under the distribution directory is
generated; only the modules are edited by hand. Version 0.2.0 is the first tagged
release of this promoted five-module structure.

**Continuous validation.** A validation step parses every Turtle file, runs the
SHACL shapes against the example ABoxes (three conformant and one with intentional
violations), and executes each competency-question query against the merged graph,
exiting non-zero on failure. The same check runs in CI as the pull-request gate,
and a tag-triggered workflow attaches the distributions to a GitHub release. This
makes the resource's quality claims reproducible by any third party. The five
queries execute against the 0.2.0 vocabulary; answer-bearing tests over example
data remain part of the pre-submission evaluation work.

**Availability (FAIR).** HCMO targets the Resources-Track availability criteria
\cite{fair}:

- *Findable / Interoperable identification.* The ontology and its terms are
  identified by a persistent `w3id.org` IRI (`https://w3id.org/hcmo/ontology/hcm#`,
  which dereferences via HTTP 303 content negotiation to the documentation); the
  resource is archived on Zenodo with a DOI.
- *Accessible.* Sources and distributions are openly available from the public
  Git repository and the Zenodo deposit (download), with HTML documentation served
  via GitHub Pages. A public **SPARQL endpoint** will be provided for live
  querying. *[pending: host the endpoint — T6b.]*
- *Interoperable.* The model reuses SOSA \cite{sosa}, OWL-Time \cite{owltime},
  BFO \cite{bfo}, IAO, and selected SEMTS terms; a JSON-LD context is shipped for
  application developers exchanging data. QUDT/OM and broader provenance
  alignment remain roadmap items.
- *Reusable.* The resource is licensed CC BY 4.0, carries provenance on the
  ontology header (creators with ORCIDs, version IRI), and provides a canonical
  citation (`CITATION.cff`) plus a DOI.

Human- and machine-readable documentation is generated from the merged graph with
WIDOCO \cite{widoco2017} (overview, term cross-reference, namespace declarations, a
WebVOWL diagram, and provenance), published at the project's documentation site.

**Sustainability and governance.** HCMO is **lab-maintained** by the Huzard group:
development is on GitHub with public issues and pull requests, versioning follows
SemVer mirrored by `owl:versionIRI`, and terms are deprecated rather than deleted
or re-minted to protect external references. The COST **TEATIME** network serves as
the community feedback channel grounding the model in real domain needs. A FAIR
self-assessment (F/A/I/R) is given in the appendix (see
`metadata/resource-metadata.md`).

*Figure F1: HCMO architecture and the reproducible build/release pipeline
(sources → merged distributions → validation/CI → tagged release + Zenodo).*
