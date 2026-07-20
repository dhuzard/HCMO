# Paper figures

This directory contains the three figures selected for the HCMO resource paper.
The editable `drawio` file is the source of each figure; SVG is preferred for the
paper, PDF is the print fallback, and PNG is a review preview.

| ID | File | Intended section | Purpose |
|---|---|---|---|
| F1 | `F1-release-pipeline.drawio` | Section 5 | Authoritative modules, reproducible build, validation gates, and publication outputs. |
| F2 | `F2-domain-model.drawio` | Section 4 | Five-module domain model centred on the monitored enclosure and the sensor-observation-result pattern. |
| F3 | `F3-minimal-abox.drawio` | Sections 4 and 6 | Worked instance graph based on `examples/abox-minimal.ttl`. |

The older images under `docs/paper/sources/figures/` and the historical
`version_rapport.drawio` are retained as provenance only. They are not paper
candidates because they contain pre-0.2.0 namespaces, former module placements,
or Chowlk placeholder terms.

Before submission, regenerate the SVG/PDF/PNG exports from the editable sources
and inspect them at the final column width. This export step is deliberately kept
separate from ontology generation: the figures explain the release but are not
normative ontology artifacts.
