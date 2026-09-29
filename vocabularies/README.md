# HCMO SKOS vocabularies

Controlled vocabularies (value sets) for HCMO data. They are **not** part of the
release manifest (`hcmo.yaml`) and are not merged into `dist/`; the ontology
only references them through `hcm-tech:hasFileFormatConcept` and
`hcm-tech:hasDataAccessMethod`, whose range is `skos:Concept`.

| File | Scheme IRI | Source |
|---|---|---|
| `file-formats.ttl` | `https://w3id.org/hcmo/id/vocab/file-format` | Hand-authored |
| `data-access-methods.ttl` | `https://w3id.org/hcmo/id/vocab/data-access-method` | Hand-authored |
| `vendors.ttl` | `https://w3id.org/hcmo/id/vocab/vendor` | Generated from `docs/hcm-systems/CATALOG.md` |
| `systems.ttl` | `https://w3id.org/hcmo/id/vocab/system` | Generated from `docs/hcm-systems/CATALOG.md` |

## Using the file-format vocabulary

```turtle
ex:activity-export a hcm-tech:TimeSeries ;
  hcm-tech:hasFileFormatConcept <https://w3id.org/hcmo/id/vocab/file-format/csv> ;
  hcm-tech:hasFileFormat "text/csv" ;   # backward-compatible string: the notation
  hcm-tech:hasDataAccessMethod <https://w3id.org/hcmo/id/vocab/data-access-method/file-export> .
```

- The concept IRI is the canonical value; `skos:notation` holds the media type
  when one exists, and the legacy `hasFileFormat` string should repeat it (or the
  `skos:prefLabel` when the concept has no notation).
- Generic formats are top concepts. Vendor-specific export formats are narrower
  concepts (for example, the DVC Analytics exports under CSV), `skos:related` to
  the system that produces them and grouped in a per-provider `skos:Collection`.
  Only exports documented with a source are listed.
- The ordered `form-options` collection in each hand-authored file drives the
  chips of the contribution form (`docs/hcm-systems/contribute/`).

## Editing

1. Edit `file-formats.ttl`, `data-access-methods.ttl`, or `CATALOG.md`.
2. Run `python tooling/export_hcm_vocab.py` to regenerate `vendors.ttl`,
   `systems.ttl`, and the form chips.
3. Run `python tooling/validate.py`; step 8 checks that the generated outputs
   are current, validates the vocabularies with `shapes/vocab-shapes.ttl`, and
   checks how the examples use them.

Concept IRIs are never re-minted: the generator fails if a previously generated
vendor or system IRI would disappear. Deprecate a concept instead of removing it.
The `https://w3id.org/hcmo/id/` path currently redirects to the repository as a
whole, so concept IRIs do not yet dereference to their descriptions.
