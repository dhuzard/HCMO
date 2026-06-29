# Resources Track — distilled requirements & compliance checklist

Sources: ISWC 2026 Call for Resources Track Papers; ESWC 2026 Call for Papers —
Resources Track. Both tracks share the criteria below (wording paraphrased).
**Re-verify against the live CfP before submitting** (dates, page limit, template).

## A. Submission mechanics

- [ ] **Format / template:** Springer **LNCS** (LaTeX strongly preferred).
- [ ] **Page limit:** ISWC ~12 pp incl. references *(confirm)* · ESWC 15 pp +
      unlimited references *(per CfP)*. → write to **12 pp incl. refs** to be safe
      for either, expand to 15 only if ESWC is locked.
- [ ] **Anonymity:** **single-anonymous** — authors are **named** (do NOT
      anonymise; the resource and its owners must be inspectable). Reviewers are
      anonymous.
- [ ] **Abstract pre-submission** (~1 week before the paper) — required.
- [ ] **English**, original, not under concurrent review.
- [ ] At least one author registers and presents.

## B. Mandatory resource-metadata block (immediately after the abstract)

The CfP requires these fields right after the abstract (drafted in
`metadata/resource-metadata.md`):

- [ ] **Resource type:** Ontology (+ SHACL shapes, SPARQL competency queries,
      JSON-LD context, examples)
- [ ] **License:** CC BY 4.0
- [ ] **DOI:** 10.5281/zenodo.18925285
- [ ] **URL:** https://w3id.org/hcmo/ontology/hcm (+ repo + docs)

## C. Review criteria → how HCMO must answer each

### 1. Availability  (hard gate)
- [ ] Published at a **persistent URI** (PURL / DOI / **w3id**) → `w3id.org` ✔,
      Zenodo DOI ✔ — **verify the w3id redirect actually resolves** (T2).
- [ ] **Open license** clearly specified → CC BY 4.0 ✔.
- [ ] **Publicly available** (API / Linked Open Data / download / open repo) →
      GitHub + Zenodo + dist artifacts ✔.
- [ ] **Permanent, resource-specific citation** provided → CITATION.cff ✔; ensure
      a canonical bib entry in `references.bib`.

### 2. Description, metadata & FAIR
- [ ] Human- **and** machine-readable description (encourages FAIR) → WIDOCO HTML
      ✔ + ontology metadata (rdfs:label/comment, dcterms, owl:versionIRI).
- [ ] **GAP:** 143 terms lack `rdfs:comment`; 1 missing label; 43 Chowlk
      placeholder/erroneous terms (`UNKNOWN:*`, `ns:Class2`, datatype-as-property).
      → **Must be cleaned before submission** (T4). Reviewers will open the docs.
- [ ] FAIR self-assessment table (F/A/I/R) in `metadata/resource-metadata.md`.

### 3. Design & technical quality
- [ ] Domain, modeling problem, requirements clearly described and well covered.
- [ ] Design/coverage reasonable & logically correct; reuse of standards
      (SOSA/SSN, OWL-Time, PROV, BFO) justified.
- [ ] Advantages, complexities, **limitations** explicitly described.
- [ ] **Quality evidence:** OOPS! pitfall scan + FOOPS! FAIR score + reasoner
      (no unsat/cycles) + SHACL validation + competency-question results (T5).
- [ ] **GAP:** shapes/examples/queries currently target the *legacy* term set →
      competency queries return 0 rows. **Re-author against the clean V1 terms** (T6).

### 4. Impact, reusability & sustainability
- [ ] Interest to the SW community **and** to society (animal welfare, 3Rs,
      reproducibility, FAIR preclinical data).
- [ ] Reusability: modular design, JSON-LD context, alignments, examples.
- [ ] **Sustainability/maintenance plan**: governance, versioning (SemVer +
      versionIRI), issue tracker, release process, who maintains it (T7).
- [ ] Adoption evidence / intended uptake (KGQA layer, authoring webapp,
      vendor-data mapping ambitions).

### 5. Reproducibility
- [ ] Reproducible build (`tooling/build.py` byte-identical) ✔ — document it.
- [ ] Anyone can re-run validation (`tooling/validate.py`) ✔.
- [ ] Provide exact versions, commands, and a tagged release matching the paper.

## D. Pre-submission gate (all must be ✔)
- [ ] w3id PURL resolves; DOI resolves; docs site live.
- [ ] No placeholder terms; all terms labelled + defined.
- [ ] Competency queries return non-zero, meaningful results.
- [ ] OOPS!/FOOPS!/reasoner/SHACL reports archived under `figures/` or appendix.
- [ ] Page count within limit; LNCS template; metadata block present.
- [ ] Canonical citation + tagged release (e.g. `v0.x` matching the paper).
