# SemTS and SOSA migration

This note covers data or extensions based on HCMO drafts that used versioned
SemTS entity IRIs or `sosa:Property`. The normative policy is recorded in
[ADR-0002](decisions/ADR-0002-SEMTS-SOSA-EDITION-POLICY.md).

## Safe term substitutions

| Earlier reference | Current reference | Migration condition |
| --- | --- | --- |
| `https://w3id.org/semts/ontology/120#DataDimension` | `https://w3id.org/semts/ontology#DataDimension` | Direct IRI correction. |
| `https://w3id.org/semts/ontology/120#TimeSeriesSegment` | `https://w3id.org/semts/ontology#TimeSeriesSegment` | Direct IRI correction. |
| `http://www.w3.org/ns/sosa/Property` | `http://www.w3.org/ns/sosa/ObservableProperty` | Use for properties that a sensor can observe under the HCMO SOSA 2017 policy. Do not treat this as a universal equivalence between editions. |

## Relations requiring semantic review

- Do not blindly replace `.../120#hasDimension`. For a
  `semts:TimeSeriesSegment` linked to its data dimensions, replace the intended
  relation with canonical `https://w3id.org/semts/ontology#segmentDimension`.
  An observation itself should instead identify what was observed with
  `sosa:observedProperty`.
- Do not blindly replace `.../120#generated`. Canonical `semts:generated` is
  restricted to SemTS knowledge-generation entities and outputs. Use it only
  when those SemTS roles are genuinely modeled. For ordinary provenance, use
  the appropriate PROV-O pattern with an explicit activity and generated
  entity.

The incorrect versioned IRIs are absent from the active HCMO release. They may
remain in archived legacy or historical design-source files, which are not
release modules and must not be copied into new data.

