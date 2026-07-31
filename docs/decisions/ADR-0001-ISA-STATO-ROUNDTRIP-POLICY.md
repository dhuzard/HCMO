# ADR-0001: ISA/STATO round-trip and mapping policy

Status: accepted by Damien Huzard on 2026-07-31.

## Decision

HCMO RDF is the canonical semantic representation. An extended ISA RO-Crate
may preserve HCMO entities and relations losslessly. ISA-JSON and ISA-Tab are
supported projections whose controlled losses must be reported rather than
hidden.

The model keeps four entities distinct: the animal, the enclosure, the
allocation execution, and the `hcm-bio:HousingAssignment` record. A housing
assignment documents actual housing during a validity interval. Allocation is
a `bioschemas:LabProcess`/PROV activity that uses the unchanged animal and
enclosure and generates the HCMO record through PROV; it has no fabricated ISA
Sample or File result. Animal identity is stable. Only actual specimen
collection creates a new Sample.

ISA Source and Sample are instance-level workflow roles. HCMO asserts no class
mapping from `hcm-bio:Subject` to either role. If ISA-Tab cannot carry a direct
whole-animal assay without a Sample proxy, the projection reports a limitation;
HCMO does not invent a specimen.

Housing validity intervals use half-open `[start, end)` semantics so a subject
may move at the exact end/start boundary without overlap. Reversed and
zero-length intervals are invalid. Overlapping housing assignments are
prohibited in the standard profile.
Extensions that permit an exceptional overlap must state and validate their
reason. `hcm:hasMonitoredAnimals` is deprecated; current membership is derived
at a stated time from authoritative time-bounded housing assignments.

`hcm-bio:StudyFactors` denotes an independent-variable specification belonging
to a study design. Subject-level factor assignments are authoritative. Named
experimental groups remain explicit populations, and any group-level factor
combination must match every member.

Statistical result entities and their serializing files/fragments remain
distinct. The first evidence profile permits an exact file fragment to use
`schema:about` as a weak exchange link to a STATO result. This does not assert a
strong carrier/content ontology relation.

External class mappings default to instance evidence or a review-only mapping
registry. Equivalence or subclass axioms require explicit promotion after
positive and negative fixtures, exact-answer competency questions, reasoner
review, and HCMO-domain plus source-vocabulary approval.

Formal ISA RO-Crate conformance is deferred until ISA confirms a permanent
profile URI, its base RO-Crate edition, and an endorsed validation procedure.

## Pinned evidence targets

- RO-Crate 1.2 Recommendation: `https://w3id.org/ro/crate/1.2`.
- ISA RO-Crate `1.0.0-draft.1`: commit
  `d77e5a90aee0d23289c2174b229146a5bf2e18c7`.
- `roc-validator` 0.11.3: commit
  `9f82e49ad5889371e62d5ba784284ac6651be630`.
- ISA API 0.14.3: commit
  `3ee762eddc9a9cd86546ceb2307b71fe1c4435b2`.

The validator currently supplies both RO-Crate 1.2 and ISA rules, but its ISA
profile declares RO-Crate 1.1 as its base while its minimal ISA fixture uses the
1.2 context. Validation is therefore evidence, not formal conformance.

## Consequences

- Generic HCMO ISA evidence checks do not require every `LabProcess` to have an
  object and result; execution-specific shapes may require them.
- HCMO publishes separate semantic-mapping and exchange-transformation
  registries. Neither is merged into `dist/hcmo.*`.
- Round-trip acceptance compares semantic invariants, not JSON byte equality.
- Every projection records preserved, transformed, and lost assertions.
- Historical fixtures do not materialize `hcm:hasMonitoredAnimals`; observation
  locations must match the authoritative assignment for the full phenomenon
  interval.
