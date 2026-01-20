# AGENT Squad Prompting Protocol

Use the templates below verbatim to trigger the AGENT Squad workflow.

## A) Change request
AGENT SQUAD: Apply this ontology change.

Change: <describe the change in 1–3 sentences>
Scope: <module(s) or domain area>
Constraints:
- preserve existing IRIs
- follow repo modeling patterns
- update definitions + provenance
Deliverables:
1) plan
2) edited files in correct module
3) validation run + results
4) changelog snippet

## B) Best-practice audit request
AGENT SQUAD: Audit the ontology structure and definitions for best practices.

Focus:
- modular architecture sanity (core vs domain vs application)
- IRI policy consistency
- annotation completeness (labels/definitions)
- logical quality (unsats, cycles, misuse of equivalence)
- import hygiene (duplication, orphan references)
Deliverables:
1) findings ranked by risk (high/med/low)
2) concrete refactors (file/module-level)
3) CI/QA recommendations aligned to this repo

## C) "Make it easy to evolve" request
AGENT SQUAD: Propose a controlled evolution workflow for this ontology.

Need:
- a small set of canonical modeling patterns
- term-request template (for humans)
- a lightweight review checklist
- release/versioning scheme
Deliverables:
- docs additions under /docs
- suggested CI commands
- examples of "good" term additions
