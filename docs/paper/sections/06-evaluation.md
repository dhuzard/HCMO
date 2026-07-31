# 6. Evaluation

> **Status:** full draft aligned with the canonical 0.2.0 artifact. OOPS! and
> FOOPS! results on the historical clean-v2 precursor are reported separately
> from checks rerun directly on `dist/hcmo.owl`.

HCMO is evaluated at four complementary levels: common ontology pitfalls and
FAIR metadata, OWL consistency, instance-data validation, and executable
competency questions. Reports and raw outputs are retained in the repository so
that historical scores are not silently attributed to a later artifact.

**Pitfalls and FAIRness.** OOPS! was run on the public clean-v2 precursor and
archived in `docs/paper/evaluation/`. The final rerun on 15 July 2026 reported no
critical or important pitfalls. Its remaining P13 minor finding concerned eight
inverse relationships that were intentionally not asserted: the candidate
pairs did not have definition-level bidirectional identity, and adding them
merely to silence the scanner would introduce false entailments. FOOPS! 0.4.0
on the same precursor improved from 0.49444446 to 1.0 after adding ontology
metadata, textual definitions, and logo metadata. These reports document the
quality-remediation history. Because HCMO 0.2.0 includes subsequent promotion,
compatibility, and contribution-workflow changes, OOPS! and FOOPS! must be run
once more on the final paper-matching distribution before submission.

**Logical consistency.** The canonical RDF/XML artifact was rebuilt and
checksummed on 31 July 2026. `dist/hcmo.owl` contained 1,279 RDF triples; the
generated profile contained 56 declared release classes, 57 object properties,
and 73 datatype properties, including compatibility terms. HermiT reported zero
inconsistent classes. The pre-check also found no active `UNKNOWN:` IRI and no
property declared as both object and datatype. The exact checksum, environment,
output, and triage are archived in
`docs/paper/evaluation/PROTEGE-HERMIT-2026-07-31.md`. A final visual Protege
inspection remains required for hierarchy readability and deprecated-term
display; it is not conflated with the automated consistency result.

**SHACL validation.** The validator supplies the canonical ontology as a
separate ontology graph and enables RDFS entailment when validating each
example. This allows domain, range, and subclass consequences to select the
same `sh:targetClass` constraints as explicit types. Three positive examples
conform, while two edge-case examples produce their reviewed violations. One
negative fixture deliberately omits explicit `rdf:type`: it conforms when
validated without the ontology, then fails when ontology-aware inference selects
the intended targets. This differential test guards the validator's entailment
contract while keeping profile requiredness in SHACL rather than translating it
into OWL existential semantics. A separate ISA/STATO evidence shape validates
the pinned workflow boundary; an injected process/data cycle is required to
fail.

**Competency questions.** Eight SPARQL queries run over the ontology plus all
positive examples. Negative fixtures are isolated from the query graph. The
validator checks both query-index completeness and the complete expected answer
rows, including bindings, unbound values, and multiplicity:

| Competency question | Exact answers |
| --- | ---: |
| subjects assigned by monitored enclosure | 3 |
| ISA factor/group assignment | 1 |
| ISA raw-file recording provenance | 1 |
| OBI transformation and STATO result provenance | 1 |
| enclosures missing dimension records | 0 |
| housed subjects needing provisioning | 3 |
| properties captured by enclosure sensors | 3 |
| systems with observations lasting at least 24 hours under a condition | 1 |

The zero-row dimensions query is intentional: it verifies absence of missing
records in the positive fixture rather than being accepted as an unexamined
empty result. The three ISA/STATO questions establish a narrow executable
evidence slice; they do not establish HCMO class mappings or formal ISA
RO-Crate conformance.
