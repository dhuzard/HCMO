# HCMO Resource Paper — working outline and page budget

Working title: **HCMO: An Ontology for Home-Cage Monitoring of Laboratory Animals**

Target: **ESWC 2027 Resources Track**, Springer LNCS. The official 2027 call
had not published its page limit on 2026-09-17. Until it does, use the ESWC
2026 allowance of **15 content pages plus unlimited references** only as a
provisional planning baseline; see `CALL-REQUIREMENTS.md`.

Canonical released module structure: **core / bio / env / obs / tech**, plus
the migration-only compatibility module. Do not restore the obsolete
`bio / housing / env / tech` planning structure.

## Structural references

The working structure adapts two accepted ESWC 2026 Resources Track ontology
papers supplied by Philippe Rocca-Serra:

- [OntoPFAS: an Ontology for the Forever Chemicals](https://drive.google.com/file/d/1FtmMij2o-dwE35IVEsCABhdd0B8ciNTA/view):
  Introduction; Related Work; Methodology; OntoPFAS; PFAS Data Hub Mapping;
  Metrics, Evaluation and Potential Impact; Conclusions.
- [SemTS: The Semantic Time Series Ontology](https://drive.google.com/file/d/1pFtICg_D-YBRnslGpxjGUB4L1m2DhHjD/view):
  Introduction and Motivation; Related Work; The Semantic Time Series Ontology;
  Evaluation; Discussion and Future Work; Conclusion.

HCMO follows the methodological clarity of OntoPFAS while retaining the clear
evaluation/discussion boundary visible in SemTS. The examples guide structure
and emphasis; they do not override the forthcoming ESWC 2027 call.

## Proposed seven-section structure

| § | Section | Provisional pages | Key content and evidence |
|---|---------|------------------:|--------------------------|
| — | Title, authors, abstract, resource block | 0.6 | Named authors if the 2027 track remains single-anonymous; abstract around 200 words; Resource type / License / DOI / URL immediately after it if retained by the call. |
| 1 | **Introduction and motivation** | 1.4 | Home-cage monitoring, continuous/non-invasive measurement, reproducibility and 3Rs; vendor silos and the semantic interoperability gap; HCMO objective and concise contribution list. Keep implementation and evaluation detail out of the introduction. |
| 2 | **Related work** | 1.1 | HCM resources and data models; relevant ontology-engineering approaches; SOSA/SSN, BFO/IAO, OWL-Time, PROV-O, QUDT, SemTS, OBI/STATO, ISA/Bioschemas and RO-Crate positioned by role. Explain the remaining gap without repeating the full vocabulary inventory. |
| 3 | **Methodology** | 1.7 | Scope and requirement elicitation; competency questions; criteria for selecting/reusing external semantic resources; mapping-strength policy; modularization and engineering workflow; publication/maintenance method; evaluation design. Describe the method used to produce and test HCMO, not the ontology inventory itself. |
| 4 | **HCMO** | 3.0 | Requirements summary; five released modules plus compatibility boundary; core modeling decisions (enclosure, subject/group, time-bounded housing, environment, device, observation, result); direct reuse and bridge axioms; metadata reuse versus domain reuse; identifiers, serialization, documentation and availability. Include the ontology overview figure. |
| 5 | **Interoperability use cases** | 2.0 | A compact ordinary HCM path, followed by the 2 × 2 ISA/RO-Crate fixture as the principal worked case. Show factor/group, animal Source, genuine derived Sample, housing/re-housing, repeated observations, statistical result, CSV fragment and controlled-loss native ISA projection. Link directly to repository inputs, outputs and manifests. Use Figure 3 here. |
| 6 | **Metrics, evaluation, and potential impact** | 2.5 | Separate subsections for ontology/release metrics; logical consistency; OOPS!/FOOPS!; SHACL and negative probes; exact-answer competency queries; ISA/STATO and round-trip evidence; limitations of the evidence; then potential scientific, welfare/3Rs, FAIR and tooling impact. Do not let prospective impact read as an evaluation result. |
| 7 | **Discussion, limitations, future work, and conclusion** | 1.0 | Interpret what the evaluation establishes; delimit formal alignment and ISA-conformance claims; discuss current coverage and adoption limits; give a prioritized roadmap; close with a short conclusion rather than repeating the abstract. |
| — | Funding, provenance, CRediT, acknowledgements, competing interests, reproducibility statement | 1.7 | Preserve required declarations and remove duplicate provenance/availability prose. |
| — | References | unlimited (about 3 current pages) | Excluded from the provisional ESWC 2026 content-page baseline; recheck against the ESWC 2027 call. |

**Provisional pre-reference total: 15.0 pages.** The clean local build on
2026-09-17 produced 16 pre-bibliography pages and 3 reference pages, so the
restructure must save at least one content page before accommodating any new
material.

## Section boundaries

- Section 3 owns **how HCMO was designed, selected, built, and evaluated**.
- Section 4 owns **what HCMO contains and how it is published**.
- Section 5 owns **worked instance-level interoperability demonstrations**.
- Section 6 owns **measured outcomes and bounded impact claims**.
- Section 7 owns **interpretation, limitations, roadmap, and synthesis**.

These boundaries are the primary control against the current repetition of
vocabulary lists, validation qualifications, availability statements and ISA
conformance caveats.

## Narrative spine

1. HCM produces rich welfare and physiology data, but vendor and study silos
   obstruct comparison, integration and FAIR reuse.
2. Existing resources cover important parts of the problem but not the complete
   enclosure–subject–environment–device–observation–result path.
3. HCMO was developed through an explicit requirements, reuse, engineering and
   evaluation methodology.
4. HCMO provides a modular ontology and reproducible release implementing that
   path without conflating physical entities, processes and information results.
5. Worked use cases test ordinary HCM queries and a deliberately bounded
   ISA/RO-Crate interoperability path.
6. Logical, constraint, competency-query, FAIR and round-trip evidence establish
   specific strengths while leaving explicit alignment and adoption limits.
7. The resource can support interoperable HCM research, welfare/3Rs work and
   future tooling if the documented governance and alignment roadmap continues.

## Figure allocation

- **Figure 1 — Development and release methodology:** requirements and resource
  selection through modular source, build, validation and publication.
- **Figure 2 — HCMO overview:** modules, upper anchors and key relations.
- **Figure 3 — Interoperability use case:** 2 × 2 design and one traceable path
  across HCMO, extended ISA RO-Crate and controlled-loss native ISA outputs,
  with repository pointers and non-crossing arrows.
