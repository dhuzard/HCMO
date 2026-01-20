# AGENTS.md — Ontology Agent Instructions (Repo Root)

You are working in an ontology repository. Your job is to preserve semantic quality and long-term maintainability.
Never "just edit labels". Treat every change as a semantic change unless proven otherwise.

## Prime directive
- Do not change meaning silently.
- If you cannot justify a change with the ontology's modeling patterns and scope, stop and propose alternatives.

## Repo map (authoritative paths)
- Source ontology modules: `ontology/` (`hcm.ttl`, `hcm-align.ttl`, `hcm-metadata.ttl`)
- JSON-LD context: `ontology/context.jsonld`
- Imports: declared in `ontology/hcm-metadata.ttl` (no separate imports folder)
- Releases / exports: none in repo (do not add generated artifacts without instruction)
- Shapes / constraints: `shapes/`
- Competency questions / examples: `examples/`
- Queries: `queries/`
- Docs: `docs/`

If these paths change, update this map in your plan before editing.

## Ontology style & best practices (non-negotiable)
### Identifiers & IRIs
- Every entity must have a stable IRI following the project pattern (no random hashes, no ad-hoc base IRIs).
- Never re-mint IRIs for existing concepts. Deprecate instead.

### Labels, definitions, and annotations
- Each class/property MUST have:
  - rdfs:label (one preferred label per language)
  - a textual definition (e.g., IAO:0000115 or equivalent)
  - provenance note (source or rationale; lightweight is fine)
- Synonyms must be typed (exact/broad/narrow/related) if your stack supports it.
- Avoid "definition-by-example" and avoid circular definitions.

### Modeling discipline
- Use the canonical design patterns documented in `docs/MODEL.md`.
- Prefer necessary & sufficient conditions ONLY when you can defend them under reasoning.
- Use imports deliberately; never duplicate imported terms.

### Modularity
- Changes must go into the correct ontology file (`ontology/hcm.ttl`, `ontology/hcm-align.ttl`, or `ontology/hcm-metadata.ttl`).
- Keep the "core" minimal; push application-specific constraints to shapes or examples.

## Quality gates (must pass before you declare "done")
Minimum gates:
1) Syntax/parse check for all ontology sources
2) Reasoning check: no unsatisfiable classes introduced
3) Report of changed entities (diff)
4) Linting/annotation completeness (labels + definitions coverage)

Run the repo's existing validation script first:
- `./tooling/validate.ps1`

If a reasoner or lint step is not available locally, propose a minimal CI addition
(ROBOT verify/report/reason or equivalent) before declaring completion.

## How to work (required process)
When asked to change anything:
1) Produce a short PLAN that includes:
   - files/modules touched
   - impacted terms
   - expected semantic effect
   - tests/commands you will run
2) Implement the smallest correct change.
3) Run quality gates.
4) Summarize results + provide a PR-ready changelog entry.

## Safety rails
- Do NOT delete terms that may be referenced externally. Deprecate and map replacements.
- Do NOT "rename by IRI change". Labels can change; IRIs should not.
- If a request conflicts with best practice, push back and offer 2–3 safer alternatives.

## Communication format
- Use this structure in your responses:
  1) What I understood
  2) Plan
  3) Proposed modeling (with rationale)
  4) Implementation notes
  5) Validation results
  6) Changelog snippet
