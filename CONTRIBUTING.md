# Contributing to HCMO

Thank you for helping improve the Home-Cage Monitoring Ontology. HCMO is an
ontology: every change is a semantic change until shown otherwise, so the
process below is stricter than for a typical code repository. Please read it
before opening a pull request.

By participating you agree to the [Code of Conduct](CODE_OF_CONDUCT.md).
Contributions are released under the repository [licence](LICENSE) (CC BY 4.0).

## What you can contribute

- **A monitoring system or dataset**: use the contribution form under
  [`docs/hcm-systems/contribute/`](docs/hcm-systems/contribute/) and open an
  issue with the exported Turtle, or follow the per-system layout in
  [`docs/hcm-systems/`](docs/hcm-systems/).
- **A new or changed term** (class, property, definition, alignment): open a
  "Term request" issue first so scope, module and modelling pattern can be
  agreed before you edit.
- **Missing labels or definitions**: see
  [`docs/MISSING-DEFINITIONS.md`](docs/MISSING-DEFINITIONS.md). Fill them in the
  source module; please do not invent definitions you cannot source.
- **Examples, shapes, competency questions, documentation, bug reports.**

## Repository map

| Path | What it is | Hand-edit? |
|---|---|---|
| `ontology/modules/*.ttl` | Ontology source (`hcm-core`, `hcm-bio`, `hcm-env`, `hcm-obs`, `hcm-tech`, ...) | Yes |
| `dist/` | Merged and serialised release artefacts | **Never**, regenerate |
| `shapes/`, `examples/`, `queries/` | SHACL, ABox examples, competency questions | Yes |
| `hcmo.yaml` | Release manifest read by downstream tools; its shape is an API | Carefully |

[`AGENTS.md`](AGENTS.md) holds the authoritative repository map and modelling
rules.

## Ground rules for ontology changes

1. **Do not change meaning silently.** Describe the semantic effect of every change.
2. **Never re-mint or rename IRIs.** Labels may change; IRIs must not. Deprecate
   a term and map its replacement instead of deleting it.
3. **Put each term in the right module** by namespace; keep `hcm-core` minimal and
   push application-specific constraints to `shapes/` or `examples/`.
4. **Every class and property needs** an `rdfs:label`, a textual definition
   (`rdfs:comment` and/or `IAO:0000115`) and a short provenance note. Avoid
   circular definitions and definition-by-example.
5. **Prefer reuse** of the external vocabularies recorded in
   [`external-vocabularies.yaml`](external-vocabularies.yaml) over new terms.

## Workflow

```bash
pip install -r tooling/requirements.txt

# 1. Edit ontology/modules/*.ttl (and shapes/, examples/, queries/ as needed)
python tooling/build.py      # 2. regenerate dist/ (re-running must give no diff)
python tooling/validate.py   # 3. parse, SHACL, competency questions (the CI gate)
```

Then:

- Commit the regenerated `dist/` **together with** the module change. CI fails if
  `dist/` is stale.
- Add an entry under `## [Unreleased]` in [`CHANGELOG.md`](CHANGELOG.md); list any
  moved term in a `### Renamed` section as `old -> new`.
- Open a pull request against `main` and fill in the template. Keep it small and
  focused: one semantic concern per pull request.

If you are unsure whether a change fits the ontology's scope or patterns, open an
issue first; we would rather discuss alternatives early.

## Reporting problems

- Modelling or data problems: a "Bug report" issue.
- Security concerns or exposed personal/confidential data: see
  [`SECURITY.md`](SECURITY.md); do not open a public issue.
