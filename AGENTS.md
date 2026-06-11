# AGENTS.md — Ontology Agent Instructions (Repo Root)

You are working in an ontology repository. Your job is to preserve semantic quality and long-term maintainability.
Never "just edit labels". Treat every change as a semantic change unless proven otherwise.

## Prime directive
- Do not change meaning silently.
- Do not invent or rename ontology terms. If labels/definitions are missing, list them; do not fabricate.
- If you cannot justify a change with the ontology's modeling patterns and scope, stop and propose alternatives.

## Repo map (authoritative paths)
- Release manifest (the contract downstream tools read): `hcmo.yaml` — its **shape is an API**; keep it stable.
- Hand-authored ontology source modules: `ontology/modules/*.ttl` (`hcm-core`, `hcm-bio`, `hcm-env`, `hcm-obs`).
- JSON-LD context: `ontology/context.jsonld`
- Generated artifacts (**never hand-edit**): `dist/` (`hcmo.ttl` merged/canonical, `hcmo.owl`, `hcmo.json`, `profile.json`).
- Shapes / constraints: `shapes/`
- Examples (ABox): `examples/`
- Queries + competency-question index: `queries/` (`competency_questions.yaml`, `cq-*.rq`)
- Tooling: `tooling/build.py` (regenerate dist), `tooling/validate.py` (CI gate).
- Docs: `docs/` (incl. `docs/MISSING-DEFINITIONS.md`).
- Previous ontology (HCMO 1.0.0, retained not deleted): `ontology/legacy/`.

If these paths change, update this map and `hcmo.yaml` before editing.

## Namespace (authoritative)
- Base namespace: `https://w3id.org/hcmo/ontology/hcm#`
- Ontology IRI: `https://w3id.org/hcmo/ontology/hcm` · versionIRI `…/hcm/0.0.1`
- Module sub-namespaces: `…/hcm/bio#`, `…/hcm/env#`, `…/hcm/obs#`
- Never re-mint IRIs for existing concepts. Deprecate instead. Keep the namespace exactly as authored; if it must change, call it out and bump `owl:versionIRI`.

## Ontology style & best practices (non-negotiable)
### Labels, definitions, and annotations
- Each class/property SHOULD have an `rdfs:label`, a textual definition (`rdfs:comment` and/or `IAO:0000115`), and a lightweight provenance note.
- Missing labels/definitions are tracked in `docs/MISSING-DEFINITIONS.md` — fill them at the source module; do not invent.
- Avoid definition-by-example and circular definitions.

### Modularity
- Put each term in the correct module by namespace (`hcm-core/bio/env/obs`).
- Keep "core" minimal; push application-specific constraints to `shapes/` or `examples/`.
- `dist/` is always regenerated from modules — never edit it by hand.

## Quality gates (must pass before you declare "done")
Run, in order, from the repo root:
1. `python tooling/build.py` — regenerate `dist/` + `profile.json` (must be reproducible: re-running produces no diff).
2. `python tooling/validate.py` — parses every TTL, runs pySHACL of `shapes/` against `examples/`, runs each `queries/cq-*.rq` against the merged graph; exits non-zero on failure.
3. Commit `dist/` changes alongside the module changes (CI fails if `dist/` is stale).

## How to work (required process)
When asked to change anything:
1. Produce a short PLAN: modules touched, impacted terms, expected semantic effect, commands to run.
2. Implement the smallest correct change in `ontology/modules/`.
3. Run the quality gates above.
4. Summarize results + provide a PR-ready `CHANGELOG.md` entry (with a `### Renamed` section if any term moved, as `old -> new`).

## Safety rails
- Do NOT delete terms that may be referenced externally. Deprecate and map replacements.
- Do NOT "rename by IRI change". Labels can change; IRIs should not.
- Everything in `dist/` is generated — regenerate, never hand-edit.
- If a request conflicts with best practice, push back and offer 2–3 safer alternatives.
