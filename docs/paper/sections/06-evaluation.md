# 6. Evaluation

> **Status:** full draft based on the archived assessments and the active HCMO
> 0.2.0 validation gates. ~1.5 pp.

We evaluate HCMO along four complementary dimensions: logical consistency,
ontology-design pitfalls and FAIRness, constraint validation, and executable
competency queries. The reports and scripts are retained in the repository so
that the checks can be repeated against the paper-matching release.

## 6.1 Logical consistency and structural quality

The active release is built from `ontology/modules/` into `dist/hcmo.owl` and
classified with HermiT through the reproducible `tooling/reason.py` command. On
HCMO 0.2.0, the merged graph contains 1,252 triples; the reasoner loads 56 HCMO
classes and reports zero inconsistent classes. The pre-check also confirms that
no active `UNKNOWN:` IRI remains and that no property is simultaneously declared
as an object and datatype property. This result establishes consistency of the
asserted OWL model; it does not by itself establish completeness of instance data,
which is handled separately with SHACL.

## 6.2 OOPS! and FOOPS!

OOPS! was used during the pre-release v2 review to identify modelling pitfalls.
After term-by-term remediation, the public rerun of 15 July 2026 reported no
critical or important pitfalls and retained only P13 (minor) for eight inverses.
A second run on the promoted 0.2.0 RDF/XML artifact on 20 July reported no
critical pitfall, but reported P10, P34, and P35 as important, together with P08,
P13, and P22 as minor. P34/P35 and the affected P08/P22 elements concern external
SOSA, BFO, IAO, Schema.org, and SEMTS terms used by reference but not redeclared
locally. This is consistent with HCMO's dependency policy. P10 provides no
concrete class pair, while P13 identifies optional inverses; neither is bulk-fixed
without domain justification. Both raw responses and their triage are archived
under `docs/paper/evaluation/`.

FOOPS! 0.4.0 assessed the same clean v2 lineage. Its score increased from
0.49444446 to 0.92222226 after adding ontology-level FAIR metadata, to 0.9888889
after completing term definitions, and to 1.0 after adding canonical logo
metadata. The archived machine reports expose each intermediate result. The
public API rerun on the promoted 0.2.0 RDF/XML artifact retained a score of
1.0, with all 15 reported checks at status `ok` and labels and definitions found
for all 186 assessed terms. The raw JSON response is archived alongside the
earlier remediation reports.

## 6.3 SHACL validation

OWL and SHACL have different roles in HCMO. OWL captures semantic typing and
supports inference, while SHACL checks application-level intake requirements.
Version 0.2.0 provides ten node shapes covering monitored enclosures, dimensions,
subjects, housing assignments, light cycles, sensors, behaviour observations,
quantitative values, observation intervals, and time series.

The automated validation gate parses every ontology, shape, example, and
distribution artifact. It then evaluates three positive examples, all of which
conform, and one edge-case example containing intentional violations, which is
correctly reported as non-conformant. This positive/negative design guards both
against rejecting valid data and against shapes that pass every graph vacuously.

## 6.4 Competency questions and coverage

Five SPARQL queries are indexed in `queries/competency_questions.yaml`. They ask
about subjects assigned to enclosures, missing enclosure dimensions, incomplete
husbandry requirements, properties captured by enclosure sensors, and long
behaviour observations under stated conditions. The validation gate executes all
five queries successfully against the merged ontology graph, confirming syntax
and vocabulary alignment. They currently return zero rows because that graph is
the ontology distribution and does not include the example ABoxes. Thus the
present result is an execution check, not yet evidence that every paper-level
competency question returns an expected answer over representative data.

Before submission, the query harness will be extended or invoked over the merged
ontology-plus-example graph, expected answers will be recorded, and the five
repository queries will be reconciled with the six competency questions in
Section 3. This is the main remaining evaluation gap. Broader empirical coverage
over heterogeneous commercial and laboratory-built HCM systems will require the
real system profiles being collected through the TEATIME network.

Overall, the available evidence supports the structural and engineering quality
of HCMO 0.2.0: HermiT finds no inconsistency, the local build and validation gates
pass, SHACL distinguishes conformant and intentionally invalid examples, and
FOOPS! confirms the FAIR metadata of the active release, while the current OOPS!
report documents the consequences of reusing external terms without copying
their declarations. Answer-bearing competency-query tests remain the principal
unfinished evaluation action.
