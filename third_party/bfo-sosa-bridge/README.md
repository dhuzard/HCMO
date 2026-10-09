# Vendored alignments for the optional BFO/SOSA bridge profile

These files are third-party inputs of `ontology/profiles/bfo-sosa-bridge.ttl`
(ADR-0005). They are **not** HCMO ontology sources, are not read by the default
build, and are excluded from line-ending conversion (`.gitattributes`) so their
bytes match the recorded SHA-256 on every platform. Checksums are pinned in
`external-vocabularies.yaml` and enforced by `python tooling/bridge_profile.py check`.

| File | Source | SHA-256 | Licence |
| --- | --- | --- | --- |
| `prov-bfo-directmappings.original.ttl` | [BFO-Mappings/PROV-to-BFO](https://github.com/BFO-Mappings/PROV-to-BFO) tag `v2025-01-19` (commit `067e8863…`), `prov-bfo-directmappings.ttl`, verbatim | `e8a91f34…c8f4` | CC0 (declared in the file) |
| `prov-bfo-directmappings.prefix-fixed.ttl` | the file above with two lines prepended and one token corrected (see below) | `edacf1c2…e282` | CC0 |
| `sosa-prov-mapping.ttl` | [w3c/sdw](https://github.com/w3c/sdw) commit `6dc60593…` (the commit pinned for SOSA 2017), `ssn/rdf/sosa-prov-mapping.ttl`, verbatim; the W3C one-way SOSA to PROV-O alignment referenced from SSN 2017 section 6.5 (non-normative) | `83bbf59e…42fb` | W3C Software and Document licence |

## Why a patched copy

The published PROV-to-BFO mapping (tag `v2025-01-19` and `main`) does not parse as
Turtle: it uses the default prefix `:` (SWRL variables, line 319) and `xsd:`
(line 323) without declaring them. Reasoners and RDF toolkits reject it. Line 147
of the tagged file also has a typo (`rdfs:comment:`, which is a distinct IRI, not
`rdfs:comment`); upstream fixed it on `main` (their #41) but it remains in the
tag pinned here. ROBOT 1.9.10 rejects the file on that token (replay by Cyril
Gilbert, 2026-10-09), so the patched copy corrects it too.

`prov-bfo-directmappings.prefix-fixed.ttl` differs from the original by exactly
two edits. First, these two lines are prepended, byte for byte:

```turtle
@prefix : <https://raw.githubusercontent.com/BFO-Mappings/PROV-to-BFO/main/prov-bfo-directmappings.ttl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
```

Second, the single occurrence of `rdfs:comment:` (line 147 of the original) is
replaced by `rdfs:comment`. No logical axiom is changed: the edit turns one
annotation on a misspelled predicate into an ordinary `rdfs:comment`. CI fails
if the patched file is anything other than those two lines followed by the
original bytes with that one token corrected, or if the misspelled predicate
still appears in the parsed graph. Results obtained with it must be described as
"on the repaired alignment", never as raw-source success.

**Upstream status:** reported as
[BFO-Mappings/PROV-to-BFO#44](https://github.com/BFO-Mappings/PROV-to-BFO/issues/44),
with the fix proposed in
[#43](https://github.com/BFO-Mappings/PROV-to-BFO/pull/43) (the same two
declarations and the same default namespace, the document base plus `#`; both open
at the time of writing). When a corrected tag exists, pin it in
`external-vocabularies.yaml`, delete the
`.prefix-fixed.ttl` file and the repair check, and re-run the matrix. Replay
status: Protégé 5.6.9 / HermiT 1.4.3.456 and ROBOT 1.9.10 accept the repaired
bundle (Cyril Gilbert, 2026-10-09).

## Notes

- The live-served `https://www.w3.org/ns/sosa/prov/` differs from the pinned
  `sosa-prov-mapping.ttl` by one extra statement, `sosa:Sample rdfs:subClassOf
  prov:Entity`. HCMO pins the immutable commit file that matches the pinned SOSA
  2017 artifact, so `sosa:Sample` is not placed under a BFO category by this
  profile.
- The same W3C repository also holds an unreferenced `ssn/rdf/bfo-prov-mapping.ttl`
  that maps `prov:Entity` to BFO independent continuant. It is **not** used and
  should not be loaded together with the PROV-to-BFO mapping.
- The authors' companion RO and CCO mappings are not part of this profile.
