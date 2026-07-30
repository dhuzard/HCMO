# Protege and HermiT evaluation, 2026-07-28

## Scope

This evaluation targets the canonical generated OWL artifact for HCMO 0.2.0,
not the historical files under `ontology/v2/`.

| Field | Value |
| --- | --- |
| Input | `dist/hcmo.owl` |
| Ontology IRI | `https://w3id.org/hcmo/ontology/hcm` |
| Version IRI | `https://w3id.org/hcmo/ontology/hcm/0.2.0` |
| Size | 139,426 bytes |
| SHA-256 | `09EB2DF8568E128F6EF7A977C7F295E8E1ACA5626A011BD5D043E7B7EA3AAC8A` |
| Protege installation prepared | Protege Desktop 5.6.9 |
| Protege bundled runtime | OpenJDK 11.0.25, 64 bit |
| Automated reasoner bridge | Owlready2 0.51 |
| RDF parser | RDFLib 7.6.0 |
| Command-line Java runtime | Java 8 update 431, 32 bit |

The checksum was recorded after two reproducible builds. `git diff -- dist`
reported no generated-content change.

## Automated HermiT result

Command:

```text
python tooling/reason.py --java-memory 512
```

Result:

```text
Source: dist/hcmo.owl
Triples: 1252
Classes: 79
Object properties: 57
Datatype properties: 73
UNKNOWN IRIs: 0
Loaded classes: 56
Inconsistent classes: 0
HermiT consistency check passed.
```

The parser's 79 class IRIs include named external classes referenced in axioms,
while the generated profile reports 56 declared release classes. No property is
simultaneously declared as an object and datatype property.

HermiT reclassified `hcm-tech:captures` beneath `sosa:observes`, which is the
intended consequence of the asserted `rdfs:subPropertyOf` axiom. No
unsatisfiable HCMO class was reported.

## SHACL and competency-query result

`python tooling/validate.py` passed on the same 1,252-triple ontology graph.
Five example graphs produced their reviewed conformant/non-conformant outcomes,
including the ontology-aware inferred-target probe. The five competency
questions returned their exact expected row counts:

| Competency question | Expected and observed rows |
| --- | ---: |
| `animals-by-enclosure` | 3 |
| `missing-dimensions` | 0 |
| `needs-provisioning` | 3 |
| `sensors-behaviors` | 3 |
| `systems-24h-limited` | 1 |

## Manual Protege inspection

Protege Desktop 5.6.9 is installed and the canonical file to open is
`dist/hcmo.owl`. The final UI evidence remains a short human check:

1. verify that the ontology and version IRIs above are displayed;
2. inspect active and deprecated terms in the class/property tabs;
3. confirm that the five active module namespaces are readable;
4. start HermiT and inspect `owl:Nothing` for unsatisfiable named classes; and
5. capture the hierarchy and reasoner-active views.

This report does not claim that those visual checks were automated. The
command-line HermiT result establishes consistency of the exact checksummed
artifact; the screenshots and UI observations complete checklist item G01.

## Triage

- **Pass:** canonical OWL parses and HermiT reports zero inconsistent classes.
- **Pass:** no active `UNKNOWN:` IRI remains.
- **Pass:** SHACL and competency-query gates pass on the current release graph.
- **Expected inference:** `hcm-tech:captures` is classified under
  `sosa:observes`.
- **Open UI evidence:** labels, deprecated-term display, and hierarchy
  screenshots in Protege.
