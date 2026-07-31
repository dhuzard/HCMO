# ISA RO-Crate interoperability validation — 2026-07-31

This report records executable interoperability evidence. It is not a formal
ISA RO-Crate conformance statement.

## Pinned tools and profiles

- RO-Crate 1.2 Recommendation (`https://w3id.org/ro/crate/1.2`).
- ISA RO-Crate `1.0.0-draft.1`, commit
  `d77e5a90aee0d23289c2174b229146a5bf2e18c7`.
- `roc-validator` 0.11.3, commit
  `9f82e49ad5889371e62d5ba784284ac6651be630`.
- `isatools` 0.14.3, commit
  `3ee762eddc9a9cd86546ceb2307b71fe1c4435b2`.

## Results

| Validation layer | Result |
| --- | --- |
| HCMO canonical RDF versus extended ISA RO-Crate JSON-LD | Pass: graph-isomorphic, 1,587 triples |
| HCMO/ISA/STATO SHACL invariants | Pass |
| Overlapping-housing negative probe | Correctly rejected |
| Orphan/reversed/incomplete-allocation housing probes | Correctly rejected |
| Unchanged animal as ISA result | Correctly rejected |
| Observation/enclosure disagreement after re-housing | Correctly rejected |
| Five exact-answer round-trip competency questions | Pass |
| Pinned mixed-model generation from the activity CSV | Pass: model and contrast use separate exact row fragments |
| RO-Crate 1.2 required validator rules | Pass |
| ISA-specific required validator rules | Pass |
| Full ISA validator with inherited base profile | One known upstream base-version conflict |
| Native ISA-JSON validation | Pass |
| ISA-JSON → ISA-Tab → ISA-JSON Source/Sample projection | Pass: distinct Source and real Sample, collection process, derivation, and HCMO IRI comments preserved |

The final row occurs because the validator's embedded ISA profile declares
RO-Crate 1.1 as its base while the validator's own minimal ISA fixture uses the
RO-Crate 1.2 context. HCMO deliberately declares only the approved 1.2 core
profile and does not add a misleading 1.1 `conformsTo` assertion merely to make
the inherited validator green.

`python tooling/validate_interoperability.py` accepts only this isolated known
issue. Any additional required validator issue fails the gate. If the upstream
base-version mismatch is fixed, a complete pass is also accepted.

`python tooling/validate_isa_native_projection.py` tests only the part native
to both ISA serializations: animal Source → specimen collection → genuine
tissue Sample. Housing, direct whole-animal recording, factor assignments on
animal Sources, explicit groups, repeated observations, and semantic
STATO/file-fragment links remain explicit controlled losses. This boundary
avoids inventing a Sample proxy for an unchanged animal. A broader HCM assay
projection requires a separately reviewed ISA measurement/technology
configuration.

Formal conformance remains deferred until ISA publishes or confirms a stable
profile URI, base RO-Crate edition, and endorsed validation procedure.
