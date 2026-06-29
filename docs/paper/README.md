# HCMO Resource Paper — working folder

This folder holds everything needed to write and submit a **Resources Track**
paper describing HCMO for **ISWC** or **ESWC**. The resource being presented is
the **Home-Cage Monitoring Ontology (HCMO)**, under the MAPP framework.

## Target venue (to confirm — see `TODO.md` T1)

Both tracks publish in **Springer LNCS**, use **single-anonymous** review
(reviewers anonymous, **authors visible** — resource ownership must be checkable),
require an **abstract pre-submission**, and a **mandatory resource-metadata block**
right after the abstract. Differences are minor (exact page limit, dates).

| | ISWC 2026 | ESWC 2026 |
|---|---|---|
| Location | Bari, Italy | (see CfP) |
| Page limit | ~12 pp LNCS incl. refs *(confirm)* | 15 pp + unlimited refs *(per CfP)* |
| Abstract / paper | 2 May / 7 May 2026 (AoE) — **passed** | Dec 2025 — **passed** |
| Status | plan for **next cycle** | plan for **next cycle** |

> Both 2026 deadlines have passed. Treat this as preparation for the next round;
> re-confirm dates, page limit, and template against the live CfP once it opens.

## Folder layout

```
docs/paper/
  README.md               # this file
  TODO.md                 # precise, tracked task list + change log
  CALL-REQUIREMENTS.md    # distilled track requirements + compliance checklist
  OUTLINE.md              # section-by-section outline with page budget
  metadata/
    resource-metadata.md  # the mandatory "after the abstract" block + FAIR table
  sections/               # one Markdown stub per paper section (draft here first)
  figures/                # diagrams (architecture, ontology overview, examples)
  references.bib          # BibTeX bibliography
```

## Workflow

1. Draft prose in `sections/*.md` (easy to review/diff).
2. Keep `CALL-REQUIREMENTS.md` green — every mandatory criterion must be satisfied
   *before* submission.
3. Track progress and decisions in `TODO.md` (status + change log).
4. Port to LNCS LaTeX (Overleaf) only once content stabilises.

## The resource at a glance (evidence to cite)

- Ontology IRI / PURL: <https://w3id.org/hcmo/ontology/hcm>
- Documentation (WIDOCO): <https://dhuzard.github.io/HCMO/index-en.html>
- Code repository: <https://github.com/dhuzard/HCMO>
- DOI (Zenodo): <https://doi.org/10.5281/zenodo.18925285>
- License: CC BY 4.0
- Standards reused: SOSA/SSN, OWL-Time, PROV, BFO; SHACL; JSON-LD; (roadmap QUDT/OM)
- Engineering: release manifest, modular Turtle, reproducible build, CI gate,
  SHACL shapes, SPARQL competency questions.
