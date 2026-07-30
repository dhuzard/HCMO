# Protégé and HermiT evaluation, 2026-07-30

## Scope

This evaluation targets the canonical generated OWL artifact after adding the
checksummed external upper projection. It supersedes the automated artifact
measurements in the 2026-07-28 report without altering that historical record.

| Field | Value |
| --- | --- |
| Input | `dist/hcmo.owl` |
| Ontology IRI | `https://w3id.org/hcmo/ontology/hcm` |
| Version IRI | `https://w3id.org/hcmo/ontology/hcm/0.2.0` |
| Size | 146,352 bytes |
| SHA-256 | `AF143C468778ABF5D794A295464E32367A4C4BA0083502C0AA2A65173F935BC3` |
| Automated reasoner bridge | Owlready2 0.51 |
| RDF parser | RDFLib 7.6.0 |

The checksum was unchanged after a second deterministic build.

## Automated HermiT result

Command:

```text
python tooling/reason.py --java-memory 512
```

Result:

```text
Source: dist/hcmo.owl
Triples: 1308
Classes: 90
Object properties: 57
Datatype properties: 73
UNKNOWN IRIs: 0
Loaded classes: 67
Inconsistent classes: 0
HermiT consistency check passed.
```

The parser count includes named external classes in the source-faithful
BFO/IAO projection and external classes referenced by axioms. The generated
profile continues to report 56 declared release classes. No property is typed
as both an object and datatype property.

## SHACL and competency-query result

`python tooling/validate.py` passed on the same 1,308-triple ontology graph.
The standard examples produced their reviewed positive and negative outcomes,
including the ontology-aware inferred-target probe. The dedicated ISA/STATO
evidence graph conformed, while an injected cyclic process/data graph did not.

All eight competency questions matched their complete expected answer rows:

| Competency question | Expected and observed exact answers |
| --- | ---: |
| `animals-by-enclosure` | 3 |
| `isa-factor-group-assignment` | 1 |
| `isa-recording-provenance` | 1 |
| `isa-statistical-result-provenance` | 1 |
| `missing-dimensions` | 0 |
| `needs-provisioning` | 3 |
| `sensors-behaviors` | 3 |
| `systems-24h-limited` | 1 |

## Triage

- **Pass:** canonical OWL parses and HermiT reports zero inconsistent classes.
- **Pass:** no active `UNKNOWN:` IRI remains.
- **Pass:** source-contract, SHACL, ISA evidence, and exact-answer CQ gates pass.
- **Expected inference:** `hcm-tech:captures` is classified under
  `sosa:observes`.
- **Open UI evidence:** labels, deprecated-term display, and hierarchy
  screenshots in Protégé.
