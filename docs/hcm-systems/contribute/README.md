# Contribution form

[`index.html`](index.html) is a **self-contained, static** page (no build, no
backend, no external requests) that lets HCM system owners describe their system and
route it — plus a sample dataset — to `damien.huzard@gmail.com`.

It is grounded in [`../../FIELD-TIERS.md`](../../FIELD-TIERS.md): fields are marked
**Required / Recommended / Optional**, machine identifiers (Base IRI, System ID, …)
are auto-minted from human-friendly answers, and the page renders in light/dark.

## What it does
- Live "required fields" progress + missing-field checklist.
- **Review submission** → a Markdown summary and a JSON payload (`hcmo-contribution/0.2`).
- **Turtle view** → a Fuseki-ready HCMO 0.2.0 ABox graph using current instance
  patterns: explicit `rdf:type` class assertions, instance-to-instance object
  links, and instance-to-literal data values.
- **Triples CSV view/download** → one RDF triple per row with `subject`,
  `predicate`, and `object` columns, absolute IRIs, and RDF lexical literals.
- **Copy** the summary, **download triples CSV**, or **Email to Damien** (opens a pre-filled
  `mailto:` and copies the full details to the clipboard as a paste fallback; the
  contributor attaches their dataset file to that email).

## Hosting

**Primary — GitHub Pages (self-hosted): `https://dhuzard.github.io/HCMO/contribute/`**

The repo's Pages site is the WIDOCO output in `docs/widoco/` (built and deployed by
[`.github/workflows/docs.yml`](../../../.github/workflows/docs.yml) on every push to
`main`). That workflow copies this form into `docs/widoco/contribute/index.html`
before upload, so it is served at the URL above. Nothing else is needed — merge to
`main` and the next Docs run publishes it. (Ensure **Settings → Pages → Source =
"GitHub Actions"**; the workflow tries to enable this automatically.)

- Mirror (Claude Artifact, instant preview): https://claude.ai/code/artifact/3d9548e3-dbe1-4c1f-b4f3-5f7484a59c10

## Maintenance
Edit `index.html` only. The GitHub Pages copy is automatic (workflow step above). If
you also refresh the Artifact mirror, regenerate the body-only version by stripping
the `<!doctype>/<html>/<head>/<body>` wrapper (keep `<style>`, the body markup, and
`<script>`), since the Artifact host injects its own document skeleton.

## Incoming data
Submissions arrive by email as Markdown; JSON, Turtle, and triple CSV can be
reviewed in the page before sending. Drop each into the matching
`../<system-slug>/` folder (real exports under `datasets/real/`), use the JSON to
seed the system `README.md`, and load the Turtle into Fuseki when building the
instance graph. Turtle is the direct Fuseki import format; CSV is intended for
tabular ETL or transformation before bulk loading.

The field-level RDF projection is documented in
[`../FORM-FIELD-MAPPING.md`](../FORM-FIELD-MAPPING.md).
