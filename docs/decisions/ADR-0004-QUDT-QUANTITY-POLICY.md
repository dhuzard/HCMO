# ADR-0004: QUDT quantity and unit policy

- Status: accepted
- Date: 2026-07-31

## Context

HCMO previously separated numeric literals from free-text unit strings. That
pattern could not reliably compare, convert, or validate enclosure dimensions,
sampling rates, environmental targets, and measurement results.

## Decision

HCMO selectively reuses QUDT 3.4.0. The authoritative schema and unit
vocabulary, their canonical namespaces, used terms, and SHA-256 checksums are
pinned in `external-vocabularies.yaml`.

Every in-scope quantity is a `qudt:QuantityValue` with exactly one
`qudt:numericValue` and exactly one IRI-valued `qudt:hasUnit`. HCMO relation
names identify the role of the quantity:

- enclosure dimensions use `hasHeightQuantity`, `hasLengthQuantity`,
  `hasWidthQuantity`, and `hasFloorAreaQuantity`;
- sensors and time series use `hasSamplingRateQuantity`;
- environmental specifications use `hasSpecifiedValue`; and
- observations use `sosa:hasResult` with `hcm-obs:QuantityValue`, which is also
  a `qudt:QuantityValue`.

QUDT was selected over OM for this release because one compact value-node
pattern covers all required roles and QUDT provides a versioned schema and
unit vocabulary that can be checksummed by the existing external-vocabulary
contract. This is selective reuse, not conformance to all QUDT constraints.

## Consequences

The former local numeric and unit-string properties remain declared and
deprecated. Producers must migrate value/unit pairs together. Units are IRIs,
not labels; applications may render their labels from the pinned QUDT unit
vocabulary. Adding another quantity kind requires an explicit HCMO role
property and a reviewed unit scope, not another free-text unit field.

