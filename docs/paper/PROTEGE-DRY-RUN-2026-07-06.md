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
| RDF triples | 564 |
| OWL classes | 31 |
| Object properties | 49 |
| Datatype properties | 53 |
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

1. Resolved after pre-check: `hcm:Enclosure` was restored as `owl:Class`
   because legacy HCMO models it as an enclosure artifact class. The v2 hub
   remains `hcm:MonitoredEnclosure`.

2. Resolved after pre-check: `time:hasBeginning` and `time:hasEnd` were restored
   as `owl:ObjectProperty`, matching OWL-Time relation semantics.

3. `UNKNOWN:hasCondition` remains a modeling decision.
   Legacy HCMO used `hcm:hasCondition` as an object property on observation
   windows, not as a simple environmental literal. Do not mint this as an
   `env` datatype property without deciding the observation-condition model.

4. Environmental measured-property terms (`hcm-env:AmbientTemperature`,
   `RelativeHumidity`, gas concentrations, `LightIntensity`, `LightState`) are
   intentionally kept as object properties in v2 according to
   `docs/paper/MODULE-MAP.md`; do not treat this as a Protege error unless the
   reasoner exposes an actual inconsistency.

## SHACL status

SHACL remains deferred. The current shapes/examples target the legacy/live term
set, while this v2 graph is still a draft. The immediate validation target is
OWL consistency/classification in Protege.
