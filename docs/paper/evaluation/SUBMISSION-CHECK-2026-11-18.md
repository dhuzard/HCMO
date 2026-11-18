# HCMO submission check — 18 November 2026

**Technical readiness: passed. Human declarations and EasyChair submission:
not verified.**

Scope: the authoritative `docs/paper/overleaf/` manuscript, confirmed by Damien
as the final PLMLatex copy on 18 November. Repository base commit:
`81440fe` (with the submission-preparation changes in the working tree).
The manuscript describes the immutable **HCMO 0.4.1** release,
DOI **10.5281/zenodo.23315766**.

## Files to use

- Compiled paper: `docs/paper/overleaf/main.pdf`.
- Named copy: `build/submission-audit-2026-11-18/HCMO-ESWC2027-submission.pdf`.
- Reproducible source archive: `docs/paper/hcmo-overleaf-upload.zip`.
- Supplementary Fig. S1: `docs/paper/supplementary/hasse-2x2-design.pdf`.
- Copyable portal metadata: `build/submission-audit-2026-11-18/easychair-metadata.txt`.
- Saved author form records: `docs/paper/metadata/submission-authors.csv`,
  also reproduced in `docs/paper/metadata/authors.md`. The country values are
  the supplied entries; the foreign-affiliation check is noted there.

The PDF and local audit scratch files are git-ignored. The source archive,
manuscript sources and this report are the reviewable repository changes.

## Checks and results

| Check | Result |
| --- | --- |
| `python tooling/build.py`, repeated | Byte-identical generated distributions; no content changes against the committed generated files |
| `python tooling/validate.py` | PASS: parsing, release/external contracts, SHACL, ISA evidence, round-trip invariants, mappings, 12 competency questions and SKOS checks |
| Positive / negative SHACL examples | Three positive fixtures conform; negative fixtures give 18 and 5 results; all three multi-animal rules fire |
| Round-trip fixture | 1,539 graph-isomorphic triples; five exact-answer questions pass |
| `python tooling/reason.py` | PASS on current checkout: 66 loaded classes, zero inconsistent classes |
| HermiT on downloaded published 0.4.1 RDF/XML | PASS: 1,464 triples, 66 loaded classes, zero inconsistent classes |
| `python tooling/external_vocab.py --verify-network` | All 15 pinned external artifact checksums match |
| `python tooling/run_cqs.py --endpoint https://w3id.org/hcmo/sparql` | All 12 expected answer sets match through the published permanent URL |
| Versioned SPARQL dataset `/hcmo-0.4.1/sparql` | All 12 expected answer sets match |
| `python tooling/validate_interoperability.py` | RO-Crate 1.2 and ISA-specific required rules pass; only the documented upstream base-version mismatch remains |
| `python tooling/validate_isa_native_projection.py` | Reproducible native ISA-JSON/ISA-Tab; Source/Sample identity and derivation preserved |
| `python tooling/validate_recording_minimal.py` | Pinned inputs and all 24 synthetic cases pass; this optional engineering draft is outside the paper's release claims |
| Clean pdfLaTeX → BibTeX → pdfLaTeX × 2 | 17 pages total; references begin on page 15; 35 resolved references; no undefined references or citations, no overfull boxes |
| PDF inspection | No review annotations or TODO text; all 26 fonts embedded; title, author block, figures and back matter inspected |
| Source ZIP built twice | Byte-identical; 15 source files; valid CRCs; no PDF, compiler debris or shared review threads included |
| Author metadata | Eight names in the same order as `CITATION.cff`; all ORCID check digits valid |

Local portability findings were resolved without changing committed content:
the native ISA byte comparison initially encountered checkout line endings,
and the optional profile pins initially encountered CRLF instead of their
pinned LF bytes. Native outputs were regenerated with the existing tool;
pinned source files were restored to their already-committed LF bytes only
after confirming their hashes. Both checks then passed.

The only remaining LaTeX warning is `newunicodechar` redefining the em dash;
it is unrelated to missing content or layout. The archived service assessments
remain the **12 October 2026** OOPS!/FOOPS!/AskWol results. This audit does not
claim new scores from those services.

## Reproducing the post-release SHACL results

The manuscript's corrected SHACL results are pinned to commit
[`81440fee6eda4eb5f626957589bd1a4e7988347f`](https://github.com/dhuzard/HCMO/tree/81440fee6eda4eb5f626957589bd1a4e7988347f),
not to the archived `v0.4.1` validation files. A clean `git archive` export
of that commit was rebuilt and validated on 18 November 2026. Both commands
exited zero: all three positive fixtures conform, the negative fixtures yield
18 and 5 results, and all three multi-animal rules fire. The complete output is
archived in
[`SHACL-VALIDATION-81440fe-2026-11-18.txt`](SHACL-VALIDATION-81440fe-2026-11-18.txt).

Environment: Python 3.12.6, rdflib 7.2.1, pySHACL 0.31.0 and PyYAML 6.0.3.
To reproduce in a separate checkout:

```text
git clone https://github.com/dhuzard/HCMO.git HCMO-validation
cd HCMO-validation
git checkout --detach 81440fee6eda4eb5f626957589bd1a4e7988347f
python -m pip install "rdflib==7.2.1" "pyshacl==0.31.0" "PyYAML==6.0.3"
python tooling/build.py
python tooling/validate.py
```

## Release and public access

The DOI, GitHub release, WIDOCO documentation, linked example/evaluation
folders and supplementary PDF resolved successfully. Both unversioned and
versioned ontology IRIs returned graph-equivalent Turtle, RDF/XML and JSON-LD,
each identifying 0.4.1 and containing 1,464 triples.

The current checkout has 1,459 triples because Antoine Toffano was removed
from current creator metadata after release. A graph comparison isolates
creator/person annotations and author-list links; ontology term counts and
logical axioms are unchanged. The paper's 1,464-triple count and nine-creator
resource citation describe the archived release correctly. The current
manuscript has eight authors; these are different records.

The public Zenodo API already includes Benoît Girard and Philippe Rocca-Serra
among the archived nine creators, resolving two stale checklist items.
Girard's archived affiliation is empty; his manuscript and `CITATION.cff`
affiliation is present.

[BioPortal](https://bioportal.bioontology.org/ontologies/HCMO) lists HCMO as
public and reports an upload on 3 November 2026. Its displayed version label
is `2026-07-31`, although its version IRI is `…/hcm/0.4.1` and its notes
identify 0.4.1. Follow up on the root-header/version-label selection. The
manuscript claims registration, which is supported; this audit did not update
the registry. Direct scripted access returned 403, while the browser retrieval
exposed the public entry.

A bare GET to the SPARQL API returns 404 without a query. Actual SPARQL requests
through the w3id URL and versioned dataset pass all twelve questions; this is
not a failed query-service test.

## Changes made for submission

- Incorporated Cyril's review: linked the SHACL results to their verified
  source commit and added the practical consequences of native ISA information
  loss. The previously corrected space after "prefixes." remains present in
  the source and rebuilt PDF.
- Revised the abstract around the domain problem, modelling contribution and
  intended reuse. Removed its detailed HermiT/SPARQL result sentence and
  shortened the standards and release-artifact lists at Damien's request.
- Disabled blue review highlighting and removed unused annotation/TODO packages.
- Removed the visible BioPortal reminder; retained its precise follow-up above.
- Put the GAIDeT disclosure in a separate **Use of Generative AI** section
  immediately before the bibliography, as the
  [ESWC author policy](https://2027.eswc-conferences.org/guidelines/generative-ai-authors/)
  specifies. Extended the declared Codex model range to GPT-6.2 for this audit.
- Fitted Fig. 4 to the text width and allowed emergency line stretching to
  resolve three text overflows without changing margins or font sizes.
- Fixed a missing sentence space, pinned the SOSA bibliography link to the
  cited 2017 Recommendation, and protected FAIR, COST and ISO/IEC capitalisation.
- Refreshed the venue checklist, author checklist, paper README, TODO and
  changelog; rebuilt the deterministic source archive.

No ontology modules, term meanings, IRIs, axioms or manifest API were changed.

## Remaining human checks

1. **Coauthor approval:** Damien initially reported no replies after the internal
   comment deadline. Cyril subsequently supplied the review comments addressed
   above. Final-version approval remains unverified.
   [Springer's authorship policy](https://www.springernature.com/gp/policies/book-publishing-policies)
   requires coauthor approval and agreement to submission.
2. **EasyChair:** register the abstract, select Resources Track, upload the
   corrected PDF, match the eight-author order and tick the AI-use box. Check
   originality/concurrent-review declarations and save the submission receipt.
   No portal submission was performed by this audit.
3. **Presentation:** confirm who will register and present if accepted.

**Corresponding-author decision resolved:** Damien selected Konstantin Todorov
and Damien Huzard on 18 November 2026. Cyril Gilbert remains first author;
Konstantin and Damien retain their co-last roles. The manuscript and author
metadata reflect this decision. Choose the EasyChair contact from this pair.

The published [Resources Track call](https://2027.eswc-conferences.org/calls/papers-resource-track/)
sets abstract and full-paper deadlines of **10 and 17 December 2026**,
respectively, at **23:59 AoE (UTC−12)**. Today's submission is therefore an
early submission against the conference deadlines.

Machine-readable hashes and local command logs are in
`build/submission-audit-2026-11-18/`. The source archive and PDF hashes are
recorded in `final-checks.json` after final verification.
