# 5. Engineering, availability, and sustainability

> **Status:** draft. The *engineering infrastructure* (manifest, reproducible
> build, CI, SHACL, docs, licensing) is artifact-independent and stable; items
> that depend on the clean V1 or external setup are marked **[pending: …]**.
> Brand: HCMO only. ~1.5 pp.

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
modular Turtle sources (the *bio/housing/env/tech* modules). A build step merges
them into a canonical, sorted serialisation, producing byte-identical output on
re-run so that version-control diffs stay clean. The merged graph is published in
three syntaxes — Turtle, RDF/XML (OWL), and JSON-LD — together with a flat term
inventory (`profile.json`: IRIs, labels, comments, and counts) intended for sync
layers and user interfaces. Everything under the distribution directory is
generated; only the modules are edited by hand. *[pending: regenerate from the
clean V1; the currently committed distribution is a superseded export — see
`AUDIT.md`.]*

**Continuous validation.** A validation step parses every Turtle file, runs the
SHACL shapes against the example ABoxes (one conformant, one with intentional
violations), and executes each competency-question query against the merged graph,
exiting non-zero on failure. The same check runs in CI as the pull-request gate,
and a tag-triggered workflow attaches the distributions to a GitHub release. This
makes the resource's quality claims reproducible by any third party. *[pending:
competency queries return results only once re-authored against the V1 terms — T6.]*

**Availability (FAIR).** HCMO targets the Resources-Track availability criteria
\cite{fair}:

- *Findable / Interoperable identification.* The ontology and its terms are
  identified by a persistent `w3id.org` IRI; the resource is archived on Zenodo
  with a DOI. *[pending: create the w3id redirect so the IRI dereferences — T2.]*
- *Accessible.* Sources and distributions are openly available from the public
  Git repository and the Zenodo deposit (download), with HTML documentation served
  via GitHub Pages. A public **SPARQL endpoint** will be provided for live
  querying. *[pending: host the endpoint — T6b.]*
- *Interoperable.* The model reuses SOSA/SSN \cite{sosa}, OWL-Time \cite{owltime},
  UO \cite{uo}, PROV \cite{provo}, and BFO \cite{bfo}; a JSON-LD context is shipped
  for application developers exchanging data.
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
