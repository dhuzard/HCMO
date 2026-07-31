# Protégé and HermiT evaluation, 2026-07-31

## Scope

This evaluation targets the canonical generated OWL artifact after introducing
the five-anchor end-user upper presentation. The optional source-faithful
developer profile is parsed and contract-validated separately because it is
deliberately outside the release manifest. This report supersedes the automated
artifact measurements in the 2026-07-30 report.

| Field | Value |
| --- | --- |
| Input | `dist/hcmo.owl` |
| Ontology IRI | `https://w3id.org/hcmo/ontology/hcm` |
| Version IRI | `https://w3id.org/hcmo/ontology/hcm/0.2.0` |
| Size | 142,733 bytes |
| SHA-256 | `60074FD3909C44F061FA2474AB4A8078E1146512FE0A62B566BECF58633BF5AD` |
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
Triples: 1279
Classes: 84
Object properties: 57
Datatype properties: 73
UNKNOWN IRIs: 0
Loaded classes: 61
Inconsistent classes: 0
HermiT consistency check passed.
```

The parser count includes the five named external classes in the default
BFO/IAO presentation and external classes referenced by axioms. The generated
profile continues to report 56 declared release classes. The optional developer
profile declares the 11 pinned source terms, reproduces their immediate
BFO/IAO hierarchy, and adds the reviewed object-aggregate refinement for
`hcm-bio:ExperimentalGroup`; validation checks those conditions explicitly.
No property is typed as both an object and datatype property.

## SHACL and competency-query result

`python tooling/validate.py` passed on the same 1,279-triple ontology graph.
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
- **Pass:** the default five-anchor presentation and optional 11-term developer
  hierarchy match their reviewed contracts.
- **Expected inference:** `hcm-tech:captures` is classified under
  `sosa:observes`.
- **Open UI evidence:** labels, deprecated-term display, and the two hierarchy
  views should still be inspected in Protégé by a human reviewer.
