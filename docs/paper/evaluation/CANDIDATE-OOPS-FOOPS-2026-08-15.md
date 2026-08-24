# OOPS! and FOOPS! review of the HCMO 0.3.0 release candidate

Date: 2026-08-15

Scope: the HCMO 0.3.0 release-candidate graph used by the paper draft. This
graph succeeds the immutable `v0.2.0` tag but is not called a published 0.3.0
release until its matching commit is merged, tagged, and deployed.

Follow-up (2026-08-24): PR review replaced the historical version-specific DOI
with the stable Zenodo concept DOI in ontology and citation metadata. This did
not change any class or property axiom, but it changed the assessed RDF bytes;
therefore the raw scans below remain dated evidence and must be rerun on the
tagged artifact before release claims are finalized.

## OOPS!

The official OOPS! REST service assessed `dist/hcmo.owl` as embedded RDF/XML.
The raw response is `oops-post-pr26-candidate-2026-08-15.xml`.

| Code | Level | Reported scope | Triage |
| --- | --- | ---: | --- |
| P04 | Minor | 1 | Canonical BFO root `BFO:0000001`; intentionally the root of the flattened upper presentation. |
| P08 | Minor | 5 | Reused SOSA, PROV, and SemTS terms; authoritative annotations remain in pinned external vocabularies. |
| P10 | Important | global | Generic missing-disjointness heuristic with no affected pair. No disjointness axiom is invented without domain evidence. |
| P13 | Minor | 32 properties | Absence of explicit inverses is not an error. Suggested inverse pairs require definition-level bidirectional identity and are not added merely for scanner compliance. |
| P22 | Minor | 1 comparison | Numeric canonical BFO IRI compared with an HCMO CamelCase IRI; unavoidable cross-vocabulary naming difference. |
| P34 | Important | 18 occurrences | Reused SOSA, SemTS, QUDT, Schema.org, and PROV classes/properties are referenced without copying their declarations into the merged HCMO graph. Their editions and checksums are enforced by the external-vocabulary contract. |
| P35 | Important | 1 | `sosa:observes`, governed by the same SOSA 2017 external-vocabulary policy as P34. |

No reported item demonstrates an OWL inconsistency. HermiT independently loads
the candidate with zero inconsistent classes. P34/P35 document the deliberate
boundary between selective reuse and bundling complete third-party ontologies;
they must not be "fixed" by minting HCMO replacements or by copying partial
external semantics without review.

## FOOPS!

The official FOOPS! `/assessOntologyFile` endpoint assessed the canonical
candidate RDF/XML file, `dist/hcmo.owl`. RDF/XML is used because it identifies
the root HCMO ontology header unambiguously to the scanner when the merged graph
also contains the separately identified upper-level presentation graph. The raw
response is `foops-post-pr26-candidate-2026-08-15.json`.

Overall score: **1.0**.

All FOOPS! checks pass for the uploaded candidate file, including ontology
metadata, versioning, licensing, provenance, vocabulary reuse, labels, and
definitions.

This result is file-specific. A separate content-negotiation check on the public
PURL returned 1,252 triples, while the candidate has 1,397, and the graphs are
not isomorphic. The public deployment must be updated before the candidate-file
score can be attributed to the released PURL representation.

## Release conclusion

The candidate passes logical, SHACL, competency-question, interoperability, and
FOOPS! file-assessment gates. OOPS! findings are triaged rather than hidden.
This report records the 0.3.0 version IRI. Because citation metadata changed in
the 2026-08-24 follow-up, both services must be rerun on the tagged artifact;
PURL content negotiation must then be verified after deployment.

## Raw-report checksums

- OOPS! XML SHA-256: `C257A3DA7025ADFDC646B43058C8F0C67749C13B1D417A7A37314184021F9454`
- FOOPS! JSON SHA-256: `57C9D39782EB14A58D31817829655E85B14F5DE39BE493C69D367C51C31770D2`
