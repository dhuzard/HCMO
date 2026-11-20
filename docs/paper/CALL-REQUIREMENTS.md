# ESWC 2027 Resources Track — submission checks

Verified on **18 November 2026** against the published
[Resources Track call](https://2027.eswc-conferences.org/calls/papers-resource-track/)
and [author AI policy](https://2027.eswc-conferences.org/guidelines/generative-ai-authors/).
This replaces the provisional ESWC 2026 baseline. The dated technical evidence
and remaining actions are in
[`evaluation/SUBMISSION-CHECK-2026-11-18.md`](evaluation/SUBMISSION-CHECK-2026-11-18.md).

## Submission mechanics

| Requirement | Status |
| --- | --- |
| English, LNCS manuscript; 15 pages plus references | Pass: references start on page 15; 17 pages total |
| Single-anonymous review, authors visible | Pass: eight named authors, affiliations and ORCIDs |
| Resource type, licence, DOI and URL after abstract | Pass: identifies the published 0.4.1 release |
| Separate Use of Generative AI section immediately before bibliography | Pass: GAIDeT tasks and tools disclosed |
| Abstract deadline | 10 December 2026, 23:59 AoE (UTC−12) |
| Full-paper deadline | 17 December 2026, 23:59 AoE (UTC−12) |
| EasyChair track | Resources Track at <https://easychair.org/conferences/?conf=eswc2027> |

## Resource and evidence

- [x] Public version DOI: `10.5281/zenodo.23315766`; CC BY 4.0.
- [x] Ontology and version IRIs resolve to graph-equivalent Turtle, RDF/XML
      and JSON-LD distributions of published 0.4.1 (1,464 triples).
- [x] Public source tag, WIDOCO documentation, BioPortal registration and
      Supplementary Fig. S1 are discoverable.
- [x] Reproducible build, SHACL positive/negative fixtures, twelve competency
      questions, and HermiT consistency checks pass.
- [x] Extended RO-Crate validation and native ISA conversion pass with the
      documented ISA-profile exception and controlled losses.
- [x] The manuscript distinguishes published ontology bytes from corrected
      post-release validation and query tooling.
- [x] Modelling, reuse, limitations, comparison, maintenance and potential
      adoption are described. Adoption is not presented as measured uptake.
- [x] Dated OOPS!/FOOPS!/AskWol evidence remains explicitly dated; no new
      service scores are claimed by this submission audit.

## Human and portal checks still open

- [ ] Document final-version approval and agreement to submission from all
      eight coauthors. No objections were reported after the internal comment
      deadline; this audit has not verified approval.
- [ ] Confirm originality and absence of concurrent review.
- [ ] Complete the abstract registration and full-paper upload in EasyChair;
      match title, eight-author order, abstract and keywords to the final PDF.
- [ ] Tick the Use of Generative AI box in EasyChair.
- [ ] Confirm an author will register and present if accepted.

The BioPortal version-label follow-up and the distinction between the archived
nine-creator resource and the eight-author manuscript are documented in the
dated audit. Neither has been silently changed in an external service.
