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
checksummed on 15 August 2026. `dist/hcmo.owl` contains 1,397 RDF triples; the
generated profile contains 60 declared release classes, 68 object properties,
and 75 datatype properties, including compatibility and directly referenced
external terms. HermiT loaded 65 classes and reported zero
inconsistent classes. The pre-check also found no active `UNKNOWN:` IRI and no
property declared as both object and datatype. The exact checksum, environment,
output, and triage are archived in
`docs/paper/evaluation/POST-PR24-26-REVIEW-2026-08-15.md`.

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

The accepted round-trip fixture contains a 2 × 2 treatment-by-enrichment
design with eight individually housed animals, 56 repeated dark-phase activity
observations, non-overlapping re-housing, an actual derived tissue Sample, and
separate fitted-model, estimate, confidence-interval, p-value, File, and file-
fragment entities. Canonical HCMO RDF and extended ISA RO-Crate JSON-LD are
graph-isomorphic at 1,539 triples. Dark-phase outcomes use phenomenon intervals,
and the re-housed animal's observations resolve to its new enclosure through
the authoritative assignment. The declared mixed model is executed against the
generated CSV with pinned numerical dependencies; the model serialization and
the active-versus-vehicle contrast at standard enrichment use distinct exact
row fragments. Dedicated shapes and
injected probes reject overlapping, orphaned, reversed, or incompletely
generated housing assignments; generated replacement animals; observation/
housing mismatch; group/factor disagreement; and fabricated ISA assignment
results.

**Competency questions.** Eleven SPARQL queries run over the ontology plus all
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
| environmental specification and observation quantities | 1 |
| current housing at the reviewed reference time | 1 |
| operational and calibration evidence at the reviewed time | 1 |
| housed subjects needing provisioning | 3 |
| properties captured by enclosure sensors | 4 |
| systems with observations lasting at least 24 hours under a condition | 1 |

The zero-row dimensions query is intentional: it verifies absence of missing
records in the positive fixture rather than being accepted as an unexamined
empty result. The three ISA/STATO questions establish a narrow executable
evidence slice; they do not establish HCMO class mappings or formal ISA
RO-Crate conformance.

Five additional exact-answer questions run against the isolated round-trip
fixture: nine housing-history rows, eight authoritative subject/group/factor
rows, eight per-animal repeated-observation counts, four statistical-result/
file-fragment rows including exact values and meaning links, and one
Source-to-derived-Sample row. `roc-validator` 0.11.3 passes all RO-Crate 1.2
required rules and all ISA-specific required rules. Its full inherited ISA run
has one isolated upstream conflict: the embedded ISA profile requires RO-Crate
1.1 although its minimal ISA fixture uses the 1.2 context. We report this as
interoperability evidence, not formal conformance. Separately, pinned
`isatools` 0.14.3 validates an executable native projection and round trip for
the genuine Source-to-Sample collection. Exact HCMO identifiers survive as ISA
comments. The test deliberately excludes non-native housing, direct whole-
animal assay, source-bound factor assignment, group, repeated-observation, and
semantic-result/file-fragment structures and checks their loss manifests.

*Figure F3: Executable 2 × 2 round-trip fixture and its tested identity,
housing, observation, statistical-result, file-fragment, and Source/Sample paths.*
