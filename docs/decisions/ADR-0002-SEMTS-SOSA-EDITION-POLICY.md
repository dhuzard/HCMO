# ADR-0002: SemTS reuse and SOSA edition policy

- Status: accepted
- Date: 2026-07-31
- Scope: normative HCMO modules, examples, external-vocabulary contract, and
  resource-paper claims

## Context

HCMO previously combined SOSA 2017 terms with `sosa:Property`, a term from the
developing SOSA/SSN 2023 Edition. It also constructed SemTS entity IRIs below
the SemTS 1.2.0 version IRI (`https://w3id.org/semts/ontology/120#`). SemTS
1.2.0 instead declares its entities below the unversioned
`https://w3id.org/semts/ontology#` namespace.

Correcting only the SemTS namespace would not repair the model. The earlier
`semts:hasDimension` observation restriction does not correspond to the
SemTS 1.2.0 relation, and `semts:generated` is specifically a relation from a
SemTS knowledge-generation entity to a knowledge-generation output. Neither
meaning fits the axioms in which HCMO used those properties.

## Decision

1. The normative HCMO release uses the W3C SOSA/SSN Recommendation of
   2017-10-19. The ontology artifact is pinned to W3C's historical repository
   commit `6dc6059362b82955707937401d8d3db340429293` and its SHA-256.
2. `hcm-env:EnvironmentalProperty` specializes
   `sosa:ObservableProperty`, and `hcm-tech:captures` has that class as its
   range. HCMO does not normatively use `sosa:Property` while the later edition
   remains a Working Draft.
3. HCMO selectively reuses SemTS 1.2.0 through canonical unversioned entity
   IRIs. The SemTS version IRI identifies the reviewed ontology artifact; it is
   not an entity namespace.
4. `hcm-obs:EnvironmentObservation` uses `sosa:observedProperty` for its
   environmental property. It has no SemTS dimension restriction.
5. `hcm-obs:LocationResultTable` is both an HCMO observation result and a
   `semts:TimeSeriesSegment`. Its optional dimensions use
   `semts:segmentDimension` with `semts:DataDimension` values.
6. HCMO removes the ill-fitting `semts:generated` axiom. Provenance generation
   relations remain available through PROV-O when an actual activity/entity
   generation claim is present; they are not inferred merely from being a
   location result table.
7. HCMO does not declare foreign, mistakenly constructed SemTS IRIs deprecated.
   Their migration is documented as a data/source repair because HCMO does not
   own those IRIs.

## Consequences

- SOSA reuse is edition-consistent and remains based on a W3C Recommendation.
- SemTS becomes implemented selective reuse for the location time-series
  result pattern, rather than a provisional namespace reference.
- Existing data using a versioned SemTS entity IRI requires migration. A class
  IRI can be substituted directly, but property migration is conditional on
  the intended subject and relation semantics.
- Adopting a later SOSA edition is a future semantic migration requiring a new
  ADR, a pinned immutable artifact, an impact review, and updated tests.

