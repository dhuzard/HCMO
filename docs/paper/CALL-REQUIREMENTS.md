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
- [x] **License:** CC BY 4.0
- [x] **DOI:** version DOI 10.5281/zenodo.22208202 (concept DOI
      10.5281/zenodo.18925284).
- [x] **URL:** https://w3id.org/hcmo/ontology/hcm (+ repo + docs)

## C. Review criteria → how HCMO must answer each

### 1. Availability  (hard gate)
- [x] Published at a **persistent URI** (PURL / DOI / **w3id**) → verified
      against the 0.3.0 release on 2026-08-31.
- [x] **Open license** clearly specified → CC BY 4.0 ✔.
- [x] **Publicly available** (Linked Open Data / download / open repo) →
      GitHub + Zenodo + dist artifacts ✔.
- [x] **Permanent, resource-specific citation** provided → CITATION.cff +
      version-specific canonical BibTeX entry.

### 2. Description, metadata & FAIR
- [ ] Human- **and** machine-readable description (encourages FAIR) → WIDOCO HTML
      ✔ + ontology metadata (rdfs:label/comment, dcterms, owl:versionIRI).
- [x] Active terms have labels and textual definitions; no `UNKNOWN:` IRI or
      object/datatype property punning remains in the generated release. Historical
      Chowlk output is retained only as source material.
- [ ] FAIR self-assessment table (F/A/I/R) in `metadata/resource-metadata.md`.

### 3. Design & technical quality
- [ ] Domain, modeling problem, requirements clearly described and well covered.
- [ ] Design/coverage reasonable & logically correct; reuse of standards
      (SOSA/SSN, OWL-Time, PROV, BFO) justified.
- [ ] Advantages, complexities, **limitations** explicitly described.
- [ ] **Quality evidence:** OOPS! pitfall scan + FOOPS! FAIR score + reasoner
      (no unsat/cycles) + SHACL validation + competency-question results (T5).
- [x] Shapes, positive and negative examples, eleven canonical competency
      questions, and five isolated round-trip questions target the 0.3.0 release
      candidate and are checked against complete expected answers.

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
- [x] w3id PURL resolves; version DOI resolves; HCMO 0.3.0 docs site is live.
- [ ] No placeholder terms; all terms labelled + defined.
- [x] Competency queries return reviewed results; the intentional zero-row
      missing-dimensions query is checked as an exact expected answer.
- [x] OOPS!/FOOPS! evidence is archived and triaged; current HermiT, SHACL, CQ,
      ISA projection, and RO-Crate reports are archived under
      `docs/paper/evaluation/`. AskWol release evidence is non-blocking and
      retains documented exceptions while the service remains beta.
- [ ] Page count within limit; LNCS template; metadata block present.
- [x] Canonical citation + tagged `v0.3.0` release matching the paper.
