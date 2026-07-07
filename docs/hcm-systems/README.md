# HCM Systems — data & documentation for HCMO validation

This folder collects, **per HCM system**, the information needed to feed HCMO with
**real and mocked data** for validation: vendor/system documentation, spec sheets,
academic papers, and sample datasets (real exports + synthetic mocks). The goal is
to exercise the ontology (`dist/hcmo.ttl`), SHACL shapes (`shapes/`), and competency
queries (`queries/`) against payloads that resemble what each real system produces.

> Why this exists: HCMO models enclosures, subjects/groups, environment &
> measurements, observations/results, and the sensors/hardware/software that produce
> the data. To validate that model we need concrete, per-system examples of *what
> data actually comes out* (parameters, sample rates, file formats, units) so we can
> author faithful ABox instances and mock exports.

## Layout

```
hcm-systems/
  README.md                 # this file
  CATALOG.md                # master index of systems extracted from the literature
  catalog.ttl               # generated sparse RDF catalog for Fuseki lookup
  FORM-FIELD-MAPPING.md     # contribution form to RDF mapping
  FUSEKI-LOADING.md         # named-graph loading workflow
  REFERENCES.md             # papers/patents/standards to dig into, grouped by modality
  LLM-RESEARCH-PROMPT.md    # reusable prompt to research each system with an LLM
  contribute/               # public, static form for system owners to submit their system + data
    index.html              #   self-contained page (mailto → damien.huzard@gmail.com)
  _template/                # copy this to start a new system folder
    README.md               #   system profile (fill from research)
    docs/                   #   manuals, brochures, spec sheets, API docs
    papers/                 #   PDFs / preprints (or a links.md if not redistributable)
    datasets/
      real/                 #   real exports (anonymised, license-checked)
      mock/                 #   synthetic data hand-authored to match the real schema
  systems/                  # one folder per system (same shape as _template/)
    DVC_Tecniplast/         #   ★ first worked example: profile + real export + mock traces
```

## Worked examples

- **[`systems/DVC_Tecniplast/`](systems/DVC_Tecniplast/)** — Tecniplast DVC®: a
  source-cited system profile, a **real** cohort export, and **synthetic traces that
  mirror the real CSV schema exactly** (with a deterministic generator). Use it as the
  template for how a filled-in system folder should look.

## How to add a system

1. Pick a system from [`CATALOG.md`](CATALOG.md) (or a new one).
2. `cp -r _template <system-slug>` (lowercase, hyphenated, e.g. `tecniplast-dvc`).
3. Run [`LLM-RESEARCH-PROMPT.md`](LLM-RESEARCH-PROMPT.md) for it, paste the result
   into the folder's `README.md`, and cite sources.
4. Drop any manuals/brochures into `docs/`, papers into `papers/` (or list links in
   `papers/links.md` when files can't be redistributed).
5. Add at least one **mock dataset** under `datasets/mock/` that matches the real
   output schema, plus any real export you can share under `datasets/real/`.
6. When the schema is clear, author a matching HCMO ABox under `../../examples/` and
   note the class/property mapping in the system `README.md`.

For graph ingestion, use [`FORM-FIELD-MAPPING.md`](FORM-FIELD-MAPPING.md) to review
the form-to-RDF projection and [`FUSEKI-LOADING.md`](FUSEKI-LOADING.md) for the
Fuseki named-graph workflow.

## Data hygiene

- **Licensing:** only commit vendor PDFs / datasets you have the right to
  redistribute. Otherwise record a URL + citation in `papers/links.md` or the
  profile, and keep the binary out of git.
- **Real data must be de-identified:** no animal-facility identifiers, personnel
  names, or unpublished results without permission.
- **Facts vs. mocks:** in profiles, state only what a source supports (link it).
  Follow repo policy — *list unknowns, don't fabricate them*. Mock datasets are
  clearly synthetic and live only under `datasets/mock/`.

See [`CATALOG.md`](CATALOG.md) for the systems extracted from the HCM technologies
book chapter (Huzard et al. 2026), and [`REFERENCES.md`](REFERENCES.md) for the
references behind each.
