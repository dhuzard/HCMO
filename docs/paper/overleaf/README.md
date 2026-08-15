# Overleaf / LNCS export

This directory is the reviewable, near-submission LaTeX export of the Markdown
draft. Upload the directory to an Overleaf project created from the Springer LNCS
template, or copy `llncs.cls` and `splncs04.bst` from that template into this
directory.

Regenerate the derived section files and bibliography from the repository root:

```powershell
uv run --python 3.13 tooling/build_paper.py
```

Edit prose in `docs/paper/sections/*.md`, not in generated
`overleaf/sections/*.tex`. `main.tex`, `figures/*.tex`, and this README are
hand-authored. Before sharing the hosted project, replace the affiliation and
email placeholder in `main.tex`, confirm author order, and verify the live venue
template and metadata-block requirements.
