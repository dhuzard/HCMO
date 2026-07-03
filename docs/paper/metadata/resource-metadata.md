# Resource metadata block (place immediately after the abstract)

The CfP requires these fields right after the abstract. Paste as-is (update the
DOI/URL/version once the paper-matching release is cut, T9).

```
Resource type: Ontology (with SHACL shapes, SPARQL competency queries,
               JSON-LD context, and example datasets)
License:       CC BY 4.0
DOI:           10.5281/zenodo.18925285
URL:           https://w3id.org/hcmo/ontology/hcm
```

Supplementary links (provide for reviewers):

- Documentation (WIDOCO): https://dhuzard.github.io/HCMO/index-en.html
- Code repository: https://github.com/dhuzard/HCMO
- Canonical citation: see `CITATION.cff` in the repository

---

## FAIR self-assessment (for §5 / appendix)

| Principle | How HCMO satisfies it | Evidence | Gap / action |
|-----------|-----------------------|----------|--------------|
| **F1** Globally unique, persistent IDs | w3id PURL + per-term IRIs; Zenodo DOI | `w3id.org/hcmo/...` (303→docs), DOI | ✓ PURL resolves (T2 done) |
| **F2** Rich metadata | `owl:Ontology` header (creators, version, license); WIDOCO | header, docs site | Add missing term defs (T5) |
| **F3** Metadata include data ID | Ontology IRI in metadata | header | — |
| **F4** Indexed/searchable | Zenodo; GitHub; (target LOV registration) | Zenodo, GitHub | Register in LOV (future) |
| **A1** Retrievable by ID over open protocol | HTTPS dereference + download | repo/dist | ✓ PURL 303 content negotiation confirmed |
| **A2** Metadata persist | Zenodo archival | DOI | — |
| **I1** Formal knowledge representation | OWL 2 in Turtle/RDF/XML/JSON-LD | `dist/` | — |
| **I2** FAIR vocabularies | Reuse SOSA/SSN, OWL-Time, PROV, BFO | alignments | Add QUDT/OM (roadmap) |
| **I3** Qualified references | `rdfs:subClassOf`/alignment axioms | `docs/ALIGNMENTS.md` | — |
| **R1** Rich, accurate attributes | labels/comments, provenance | modules | Complete defs (T5) |
| **R1.1** Clear license | CC BY 4.0 | LICENSE, header | — |
| **R1.2** Provenance | dcterms:creator, ORCIDs, versionIRI | header, CITATION.cff | — |
| **R1.3** Community standards | LNCS/OBO-style practices, SHACL, SKOS notes | shapes/docs | — |
