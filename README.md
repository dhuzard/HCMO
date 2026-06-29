# HCMO — Home-Cage Monitoring Ontology

[![Validate](https://github.com/Neuronautix/HCMO/actions/workflows/validate.yml/badge.svg)](https://github.com/Neuronautix/HCMO/actions/workflows/validate.yml)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-blue.svg)](LICENSE)
[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.18925285-blue.svg)](https://doi.org/10.5281/zenodo.18925285)

HCMO is an ontology for **home-cage monitoring** of laboratory animals. It models
monitored enclosures, biological subjects and experimental groups, the
environment and its measurements, observations and results, and the sensors,
hardware, and software that produce the data — under the **MAPP** framework
(Monitoring and Analytics for Physiological Processes). The project ships as a
standalone, tool-consumable package: a stable release manifest, modular Turtle
sources, generated distributions, SHACL shapes, competency queries, and a
JSON-LD context.

## At a glance

| | |
|---|---|
| **Ontology IRI** | `https://w3id.org/hcmo/ontology/hcm` |
| **Base namespace** | `https://w3id.org/hcmo/ontology/hcm#` |
| **Module sub-namespaces** | `…/hcm/bio#`, `…/hcm/env#`, `…/hcm/obs#` |
| **Version** | `0.0.1` (versionIRI `…/hcm/0.0.1`) |
| **Prefix** | `hcm` |
| **License** | CC BY 4.0 |
| **Release manifest** | [`hcmo.yaml`](hcmo.yaml) |
| **Documentation** | <https://dhuzard.github.io/HCMO/index-en.html> |

> The release manifest [`hcmo.yaml`](hcmo.yaml) is the **contract** that
> downstream tools (e.g. the `hcmo-kgqa-lab` sync layer) read. Its shape is
> treated as an API and kept stable across releases.

## Repository layout

```
hcmo.yaml                      # release manifest (name, version, namespace, modules, dist, shapes, queries, examples)
ontology/
  modules/                     # hand-authored modular sources
    hcm-core.ttl               #   core terms + owl:Ontology header (attribution)
    hcm-bio.ttl                #   subjects, experimental groups        (…/hcm/bio#)
    hcm-env.ttl                #   environment & measurements           (…/hcm/env#)
    hcm-obs.ttl                #   observations & results               (…/hcm/obs#)
  context.jsonld               # JSON-LD context for app developers
  legacy/                      # previous HCMO 1.0.0 ontology (retained, not merged)
dist/                          # GENERATED — never hand-edit
  hcmo.ttl                     #   merged graph, canonical/sorted Turtle (reproducible)
  hcmo.owl                     #   merged graph, RDF/XML
  hcmo.json                    #   merged graph, JSON-LD
  profile.json                 #   flat term inventory {iri,label,comment} + counts
shapes/hcm-shapes.ttl          # SHACL constraints
examples/                      # ABox examples (abox-minimal, abox-edge-cases)
queries/                       # competency_questions.yaml + cq-*.rq
tooling/                       # build.py, validate.py, docs.py, requirements.txt
docs/                          # documentation (incl. MISSING-DEFINITIONS.md)
.github/workflows/             # validate.yml (PR gate), release.yml (tag → assets)
webapp/                        # optional Node.js authoring/blueprint app
```

## Quickstart

```bash
pip install -r tooling/requirements.txt

python tooling/build.py      # regenerate dist/ + profile.json (idempotent, reproducible)
python tooling/validate.py   # parse all TTL + pySHACL + competency queries (the CI gate)
```

- **`tooling/build.py`** merges `ontology/modules/*.ttl` into `dist/` using a
  canonicalized, sorted serialization, so re-running produces byte-identical
  output (clean diffs). Everything in `dist/` is generated — edit the modules,
  not the artifacts.
- **`tooling/validate.py`** parses every TTL, runs the SHACL shapes against the
  examples, and runs every `queries/cq-*.rq` against the merged graph; it exits
  non-zero on failure. It is the same check the PR workflow runs.

## Consuming the ontology

- **Merged graph:** import `dist/hcmo.ttl` (or `dist/hcmo.owl`) into your triple
  store or reasoner.
- **Programmatic inventory:** read `dist/profile.json` for the flat list of
  classes / object properties / datatype properties with labels, comments, and
  counts — ideal for sync layers and UIs.
- **JSON-LD apps:** apply `ontology/context.jsonld` when exchanging data.
- **Validation:** use `shapes/hcm-shapes.ttl` to validate payloads during
  ingestion; see `examples/` for conformant and intentionally-invalid ABoxes.
- **Everything is discoverable from `hcmo.yaml`** — resolve module, dist, shapes,
  queries, and example paths from there rather than hard-coding them.

## Documentation

📖 **Published docs:** <https://dhuzard.github.io/HCMO/index-en.html>

Human-readable HTML documentation is generated from the merged graph with
[WIDOCO](https://github.com/dgarijo/Widoco) (overview, term cross-reference,
namespace declarations, a WebVOWL diagram, and provenance).

```bash
python tooling/build.py      # ensure dist/ is current
python tooling/docs.py       # render docs/widoco/ (needs a Java 11+ runtime)
# then open docs/widoco/index.html
```

`tooling/docs.py` downloads a pinned WIDOCO release into `tooling/.widoco/` on
first run (override with `--jar PATH` or `WIDOCO_JAR`). The generated site under
`docs/widoco/` is **not committed** — it is published to GitHub Pages by
`.github/workflows/docs.yml` on every push to `main`. Term descriptions are
sourced from the `owl:Ontology` header and `rdfs:comment`; terms still missing
definitions (see `docs/MISSING-DEFINITIONS.md`) render with empty descriptions.

> To serve the published site, enable Pages once in **Settings → Pages →
> Source: "GitHub Actions"**.

## Status & known issues

This is an early release (`0.0.1`) derived from a Chowlk diagram export.
`docs/MISSING-DEFINITIONS.md` tracks the open data-quality work, including:

- Terms still lacking `rdfs:comment` definitions (labels are present).
- Chowlk placeholder/erroneous terms preserved as authored (`UNKNOWN:*`,
  `ns:Class2`, `xsd:boolean`/`xsd:integer` typed as properties) — to be re-mapped
  or removed at the source.
- `shapes/`, `examples/`, and `queries/` currently reference the legacy 1.0.0
  term set and need re-authoring against the MAPP terms (competency queries
  return 0 rows until then).

Per project policy, missing labels and definitions are **listed, not fabricated**.

## Web authoring app (optional)

A Node.js app under `webapp/` supports form-based authoring and a blueprint
checklist. From `webapp/`: `npm install` then `npm run dev` (serves on
`http://localhost:3000`); `npm test` runs the API/UI tests. The app predates the
MAPP reorganization and targets the legacy term set.

## Contributors

- **Damien Huzard** — [0000-0003-4820-7951](https://orcid.org/0000-0003-4820-7951)
- **Konstantin Todorov** — [0000-0002-9116-6692](https://orcid.org/0000-0002-9116-6692)
- **Cyril Gilbert** — _ORCID: TBD_
- **Pierre Larmande** — [0000-0002-2923-9790](https://orcid.org/0000-0002-2923-9790)
- **Gaoussou Sanou** — _ORCID: TBD_
- **Serge Sonfack** — _ORCID: TBD_
- **Antoine Tofano** — _ORCID: TBD_

Attribution is also recorded on the `owl:Ontology` header (`dcterms:creator`,
using ORCID IRIs where known) and in [`CITATION.cff`](CITATION.cff).

## Citation

If you use HCMO, please cite it via [`CITATION.cff`](CITATION.cff) (GitHub's
"Cite this repository") or the DOI [10.5281/zenodo.18925285](https://doi.org/10.5281/zenodo.18925285).

## License

Released under [CC BY 4.0](LICENSE).
