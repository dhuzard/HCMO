# Gilbert (2026) — internship report: designing an ontology for home-cage monitoring

Historical source for the HCMO resource paper. It records how the first HCMO
model was designed, before the ontology reached its current modular form.

| | |
|---|---|
| **Title** | *Designing an Ontology for Home-Cage Monitoring: structuring, interoperability, and reuse of data* |
| **Author** | Cyril Gilbert |
| **Date** | 16 June 2026 |
| **Supervision** | Damien Huzard |
| **Language** | French (original); English working translation |

## Contents

| Path | What it is |
|---|---|
| [`hcmo-report.fr.pdf`](hcmo-report.fr.pdf) | The original report (French). |
| [`hcmo-report.en.md`](hcmo-report.en.md) | English working translation: a faithful adaptation, not a line-by-line translation. Sections: introduction, scientific context (home-cage monitoring), ontologies and the Semantic Web, work carried out, discussion and perspectives, references. |
| [`figures/`](figures/) | Figures used by the translation. `ext_fig*` are figures from other works that the report reproduces (Home Cage Monitoring Definition Olog, HCM parameters, KG/LLM querying pipeline, Gene Ontology prediction, WellFAIR ecosystem). `fig07`–`fig10` are the HCMO bio, housing, environment and technology module diagrams. |
| `figures/version_rapport.*` | Editable sources of the report's model diagram (draw.io, draw.io XML, Turtle). |

## Status and use

- This is a **historical record**, not normative documentation. The ontology
  modules in `ontology/modules/` and the generated `dist/` artefacts are
  authoritative; where the report and the ontology differ, the ontology wins.
- The English translation is the primary domain and design source cited while
  drafting the resource paper (see [`../../README.md`](../../README.md)).
- Third-party figures (`ext_fig*`) belong to their original authors; cite the
  original works rather than this folder.
