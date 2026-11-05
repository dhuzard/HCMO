# OOPS!, FOOPS! and AskWol review of the HCMO 0.4.1 release

Date: 2026-10-12

Scope: the published `v0.4.1` release (tag on commit `9503ae4`, Zenodo DOI
`10.5281/zenodo.23315766`). The scanned file is the `hcmo.owl` release asset,
byte-identical to `dist/hcmo.owl` at the tag (1,464 triples). It replaces the
0.3.0 evidence in `CANDIDATE-OOPS-FOOPS-2026-08-15.md` as the basis of the
paper's scan table.

## OOPS!

Official REST service `https://oops.linkeddata.es/rest`, RDF/XML embedded in
the request. Raw response: `oops-v0.4.1-2026-10-12.xml` (131 triples).

| Code | Level | 0.3.0 | 0.4.1 | Change |
| --- | --- | ---: | ---: | --- |
| P04 | Minor | 1 | 1 | — |
| P08 | Minor | 5 | 5 | — |
| P10 | Important | global | global | — |
| P13 | Minor | 32 | 37 | The five new object properties (`hcm-obs:involvesSubject`, `hasInitiator`, `hasRecipient`; `hcm-tech:hasFileFormatConcept`, `hasDataAccessMethod`) have no declared inverse. |
| P22 | Minor | 1 | 1 | — |
| P34 | Important | 18 | 19 | `skos:Concept`, the range of the two new `hcm-tech` properties, is referenced without its declaration. |
| P35 | Important | 1 | 1 | — |

Triage is unchanged from 0.3.0. P13: inverses are not added without
definition-level evidence. P34/P35: reused terms, including `skos:Concept`, are
governed by the pinned external-vocabulary contract and are not copied into the
merged graph. No finding shows an OWL inconsistency; HermiT loads the release
with zero inconsistent classes.

## FOOPS!

| Mode | Raw response | Score | Failing checks |
| --- | --- | ---: | --- |
| File, `/assessOntologyFile` (as for 0.3.0) | `foops-v0.4.1-file-2026-10-12.json` | 1.0 | none (15 checks) |
| PURL, `/assessOntology` on `https://w3id.org/hcmo/ontology/hcm` | `foops-v0.4.1-purl-2026-10-12.json` | 0.875 | FIND2 (prefix not retrievable from a prefix registry); FIND3 and FIND3_BIS (ontology not found in a public registry) |

The PURL mode adds findability tests that the file mode does not run. The
three failures are real and fixable outside the ontology: register the `hcm`
prefix (prefix.cc) and list HCMO in a public registry (LOV, BioPortal or OLS;
FAIRsharing). Tracked in `docs/BACKLOG.md`.

## AskWol

Automated by `.github/workflows/release-evidence.yml` (run 38240506029, ref
`v0.4.1`); raw response and summary archived as the run artifact (90 days).

- Pass: domain/range, datatypes, imports, IRI scheme, open licence (CC BY 4.0);
  reasoner snapshot consistent, 0 unsatisfiable classes, 0 inconsistent
  individuals.
- Documented exceptions, unchanged (see `ASKWOL-TRIAGE.md`): mixed hash/slash
  namespaces, creator/date/publisher read from the auxiliary upper-presentation
  header, historical `…/hcm/0.0.1` provenance, external namespace bases (OBO,
  MOD), language tags.
- **New finding, not reproducible:** the namespace probe reports HTTP 404 for
  `https://w3id.org/hcmo/ontology/hcm#` and the four module namespaces. The same
  result appears in the automated runs for v0.3.1 and v0.4.0; the manual run of
  2026-08-31 resolved them. On 2026-10-12 every one of these namespaces resolved
  in our checks (303 then 200) with no `Accept` header, `text/turtle`,
  `application/rdf+xml`, `text/html` and `*/*`; with GET and HEAD; with the `#`
  dropped or percent-encoded; and for the parent paths. The cause appears to be
  on the AskWol side (beta service). Treated as non-blocking; to confirm with a
  manual AskWol run or the AskWol maintainers.
