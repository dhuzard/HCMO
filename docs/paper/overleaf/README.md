# Authoritative Overleaf / LNCS manuscript

This directory contains the authoritative manuscript maintained in the PLMLatex
project. Changes exported from PLMLatex must be imported here before the paper
package is rebuilt. The older Markdown drafts under `docs/paper/sections/` are
retained as review history and no longer generate these LaTeX files.

Build the deterministic upload/archive ZIP from the repository root:

```powershell
uv run --python 3.13 tooling/build_paper.py
```

Edit the manuscript in PLMLatex, then export and synchronize its `.tex`, `.bib`,
figure, and README sources into this directory. Before submission, replace the
affiliation placeholder in `main.tex` and verify the live venue template and
metadata-block requirements.

The build also creates `docs/paper/hcmo-overleaf-upload.zip` with deterministic
case-sensitive POSIX-name ordering, timestamps, permissions, LF-normalized text,
and uncompressed ZIP members, so its bytes do not depend on checkout line
endings or zlib versions. Import that archive with Overleaf's **New Project ->
Upload Project** action.
