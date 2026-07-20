# OOPS! evaluation report, 2026-07-20

Source tested: `dist/hcmo.owl` from HCMO 0.2.0

Tool: OOPS! REST service, `https://oops.linkeddata.es/rest`.

Raw response: `oops-hcmo-0.2.0-2026-07-20.xml`.

## Result

| Code | Importance | Affected | Interpretation |
|---|---:|---:|---|
| P08 Missing annotations | Minor | 7 | All affected IRIs are reused BFO, IAO, or SOSA terms. HCMO deliberately does not copy external labels and definitions into its modules. |
| P10 Missing disjointness | Important | 1 generic finding | OOPS provides no affected class pair. HCMO asserts only reviewed disjointness and does not add broad disjointness without a domain justification. |
| P13 Inverses not explicitly declared | Minor | 30 | Inverses are optional. Candidate relations require individual review; scanner-driven inverse assertions previously produced P05 critical findings. |
| P22 Mixed naming conventions | Minor | 1 group | The comparison mixes the numeric external BFO IRI `BFO_0000019` with the local `HealthStatusObservation` name. This is not an HCMO naming inconsistency. |
| P34 Untyped class | Important | 19 reported occurrences | The affected resources are external SOSA, BFO, IAO, Schema.org, and SEMTS classes or properties used in restrictions. They are typed in their source vocabularies; HCMO's architecture policy reuses them by reference and avoids local redeclaration. |
| P35 Untyped property | Important | 1 | The affected resource is the external `sosa:observes` property, used as a superproperty of `hcm-tech:captures`. It is not re-declared locally. |

No critical pitfall was reported.

## Triage decision

The 0.2.0 result differs from the pre-promotion v2 scan because the active
modules no longer include local scaffolding declarations and annotations for
external vocabularies. Adding copies of external SOSA/BFO/IAO/Schema/SEMTS
declarations solely to silence P08, P22, P34, or P35 would conflict with the
repository policy documented in `docs/ARCHITECTURE.md`.

P10 and P13 remain modelling-review prompts. Disjointness and inverse axioms
will be added only when domain semantics or a competency question requires them,
not to obtain an empty scanner report.

## Reproducibility context

- HermiT: 56 HCMO classes loaded, zero inconsistent classes.
- Active `UNKNOWN:` IRIs: zero.
- Build: reproducible.
- SHACL: three positive examples conform; the negative edge-case example is
  correctly non-conformant.
- Competency-query execution: five queries execute without error; expected-answer
  tests over example data remain to be completed.
