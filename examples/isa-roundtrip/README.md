# HCMO ISA/STATO round-trip fixture

This directory contains the generated 2 × 2 treatment-by-enrichment example
used in Figure 3 and in the executable interoperability evaluation. The
canonical HCMO RDF and extended ISA RO-Crate carry the same graph. Native
ISA-JSON and ISA-Tab cover the narrower, controlled-loss Source-to-Sample path.

## Artifact map

| Artifact | Purpose |
| --- | --- |
| `canonical.ttl` | Canonical HCMO RDF, including PROV process/output links, STATO-typed statistical entities, and exact CSV row fragments. |
| `ro-crate-metadata.json` | Graph-isomorphic extended ISA RO-Crate serialization. |
| `data/dark-phase-activity.csv` | Generated per-animal repeated-observation matrix used as model input. |
| `data/model-results.csv` | Generated result matrix with explicit STATO IRIs, authoritative labels, and links to the semantic result entities. |
| `native-isa/` | Reproducible ISA-API JSON and ISA-Tab Source-to-Sample projection. |
| `loss/` | Controlled-loss contracts for the native ISA projections. |
| `queries/` and `competency_questions.yaml` | Exact-answer checks for housing, factors/groups, observations, result fragments, and Source/Sample identity. |

## STATO annotations in the result matrix

The CSV retains one model row and one treatment-contrast row. Annotation
columns identify the semantic entity represented by each result field and the
class used for that entity in `canonical.ttl`:

| Result | STATO class |
| --- | --- |
| Fitted model | `STATO_0000464` — linear mixed model |
| Active-versus-vehicle estimate | `STATO_0000384` — contrast estimate |
| 95% confidence interval | `STATO_0000231` — 95% confidence interval |
| p-value | `STATO_0000700` — p-value |

The `*_stato_iri` and `*_stato_label` cells are explicit CSV annotations. The
normative RDF semantics remain in `canonical.ttl`: each model or statistical
result is a separate entity, is typed with the corresponding STATO class, and
is connected by `schema:about` to an exact RFC 7111 row fragment of
`model-results.csv`. The result file itself is not asserted to be one of those
STATO result classes.

## Reproduce and validate

From the repository root:

```bash
python tooling/generate_isa_roundtrip_fixture.py
python tooling/validate.py
python tooling/validate_interoperability.py
python tooling/validate_isa_native_projection.py
```

The generator owns `canonical.ttl`, `ro-crate-metadata.json`, and both files in
`data/`; do not edit those generated artifacts directly.
