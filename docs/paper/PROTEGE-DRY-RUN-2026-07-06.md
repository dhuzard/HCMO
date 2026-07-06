# Protege pre-check report, 2026-07-06

Source tested: `ontology/v2/hcmo-v2-merged.ttl` on `main`.

This is not a full Protege/HermiT/ELK run. It is a pre-check done before the
manual Protege pass, using RDF parsing and OWL typing sanity checks.

## Automated checks

Command scope:

- parse `ontology/v2/hcmo-v2-merged.ttl` with `rdflib`;
- count declared classes and properties;
- detect properties declared both as `owl:ObjectProperty` and
  `owl:DatatypeProperty`;
- detect `owl:onProperty` values without an object/datatype property
  declaration;
- detect restrictions where `owl:someValuesFrom` / `owl:allValuesFrom` point
  to class-like values through a datatype property.

Results:

| Check | Result |
|---|---:|
| RDF triples | 565 |
| OWL classes | 30 |
| Object properties | 47 |
| Datatype properties | 56 |
| Annotation properties | 4 |
| Properties typed both object and datatype | 0 |
| `owl:onProperty` without object/datatype declaration | 0 |
| Obvious restriction type warnings | 0 |
| Remaining `UNKNOWN:` IRIs | 7 |

Remaining placeholders:

- `UNKNOWN:captures`
- `UNKNOWN:hasActuators`
- `UNKNOWN:hasCondition`
- `UNKNOWN:hasEnrichmentReq`
- `UNKNOWN:hasSensors`
- `UNKNOWN:hasType`
- `UNKNOWN:partOF`

## Items to inspect in Protege

These are not proven inconsistencies from the pre-check. They are modeling
points that should be inspected during the Protege reasoner/debug pass.

1. `hcm:Enclosure` is currently declared as `owl:DatatypeProperty`.
   The term name looks class-like, and the v2 design says the core hub is
   `hcm:MonitoredEnclosure`. Decide whether `hcm:Enclosure` is obsolete cruft,
   a label/property artifact, or a class that was lost during Chowlk export.

2. `time:hasBeginning` and `time:hasEnd` are currently declared as
   `owl:DatatypeProperty`.
   In OWL-Time these are normally object relations to `time:Instant`. The v2
   graph currently uses only cardinality restrictions on them, so this did not
   trigger the automated restriction check, but Protege may make the modeling
   issue more visible.

3. `UNKNOWN:hasCondition` remains a modeling decision.
   Legacy HCMO used `hcm:hasCondition` as an object property on observation
   windows, not as a simple environmental literal. Do not mint this as an
   `env` datatype property without deciding the observation-condition model.

## SHACL status

SHACL remains deferred. The current shapes/examples target the legacy/live term
set, while this v2 graph is still a draft. The immediate validation target is
OWL consistency/classification in Protege.
