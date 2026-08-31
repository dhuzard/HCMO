# AskWol release-evidence policy and triage

AskWol is integrated as a **non-blocking, archived release-evidence job** while
the service remains beta. The workflow submits the tagged RDF/XML distribution,
retains the raw JSON response and a deterministic Markdown summary for 90 days,
and records service failures without blocking a release. It can also be run
manually against an explicit tag.

AskWol complements, but does not replace, the repository's blocking build,
parsing, SHACL, competency-question, interoperability, and reasoner checks.
Findings are reviewed before any ontology change. In particular, scanner output
does not authorize changing or re-minting published HCMO IRIs.

## Current 0.3.0 triage

A manual run on 31 August 2026, after restoring the GitHub release assets and
PURL targets, parsed the release and resolved the HCMO core and four module
namespaces. Domain/range, datatype, import, IRI-scheme, open-license, and
reasoner checks passed; no logical contradiction or unsatisfiable named class
was reported.

The remaining findings are triaged as follows:

| Finding | Triage | Release treatment |
| --- | --- | --- |
| Mixed hash/slash strategy under the HCMO base | The stable design uses `hcm#` for core and `hcm/bio#`, `hcm/env#`, `hcm/obs#`, and `hcm/tech#` for modules. | Accepted architectural exception; do not re-mint IRIs. |
| Missing creator/date/publisher | AskWol selects `https://w3id.org/hcmo/ontology/external/upper-presentation` from the merged file as the ontology header. The root HCMO header carries this metadata. | Tool-selection exception; retain the auxiliary header and root metadata. |
| Undefined internal `…/hcm/0.0.1` | This IRI occurs as historical `dcterms:source` provenance, not as a current class or property. | Accepted provenance exception. |
| OBO and MOD namespace-base resolution | AskWol tests namespace bases; HCMO governs the exact reused IRIs and versions through `external-vocabularies.yaml`. | Review against the external-vocabulary contract; do not copy or rewrite external terms merely for the scanner. |
| No language tags | Current annotations are English-only and consistently untagged. | Non-blocking documentation/localization enhancement. |

Deprecated HCMO terms reported as warnings are intentional compatibility terms
and remain published with deprecation and replacement metadata.

## Workflow evidence contract

- Workflow: `.github/workflows/release-evidence.yml`
- Submitted artifact: rebuilt `dist/hcmo.owl` from the selected release ref
- Archived files: `raw-response.json`, `request.log`, and `summary.md`
- Retention: 90 days in the GitHub Actions artifact store
- Trigger: published GitHub release or manual dispatch with a ref/tag
- Gate semantics: informational and non-blocking
