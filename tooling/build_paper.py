#!/usr/bin/env python3
"""Export the reviewed Markdown paper draft as an Overleaf-ready LNCS package."""

from __future__ import annotations

import re
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAPER = ROOT / "docs" / "paper"
OUT = PAPER / "overleaf"
ARCHIVE = PAPER / "hcmo-overleaf-upload.zip"
SECTIONS = sorted((PAPER / "sections").glob("[0-9][0-9]-*.md"))


def latex_plain(value: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(char, char) for char in value)


def inline(value: str) -> str:
    protected: list[str] = []

    def keep(rendered: str) -> str:
        protected.append(rendered)
        return f"@@HCMO{len(protected) - 1}@@"

    value = value.replace("—", "---").replace("–", "--")
    value = value.replace("“", "``").replace("”", "''")
    value = value.replace("‘", "`").replace("’", "'")
    for symbol, rendered in {
        "→": r"$\rightarrow$",
        "↔": r"$\leftrightarrow$",
        "≠": r"$\neq$",
        "×": r"$\times$",
        "°": r"$^{\circ}$",
        "§": r"\S{}",
    }.items():
        value = value.replace(symbol, keep(rendered))
    value = re.sub(r"\\cite\{([^}]+)\}", lambda m: keep(r"\cite{" + m.group(1) + "}"), value)
    value = re.sub(r"`([^`]+)`", lambda m: keep(r"\nolinkurl{" + m.group(1) + "}"), value)
    value = re.sub(
        r"\[([^]]+)\]\((https?://[^)]+)\)",
        lambda m: keep(r"\href{" + m.group(2) + "}{" + latex_plain(m.group(1)) + "}"),
        value,
    )
    value = re.sub(r"\*\*([^*]+)\*\*", lambda m: keep(r"\textbf{" + latex_plain(m.group(1)) + "}"), value)
    value = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", lambda m: keep(r"\emph{" + latex_plain(m.group(1)) + "}"), value)
    value = latex_plain(value)
    for index in reversed(range(len(protected))):
        rendered = protected[index]
        value = value.replace(f"@@HCMO{index}@@", rendered)
    return value


def emit_table(lines: list[str], start: int) -> tuple[list[str], int]:
    rows: list[list[str]] = []
    index = start
    while index < len(lines) and lines[index].lstrip().startswith("|"):
        cells = [cell.strip() for cell in lines[index].strip().strip("|").split("|")]
        if not all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            rows.append(cells)
        index += 1
    columns = max(len(row) for row in rows)
    spec = "X" + "r" * (columns - 1)
    output = [r"\begin{table}[t]", r"\centering", r"\small", rf"\begin{{tabularx}}{{\linewidth}}{{@{{}}{spec}@{{}}}}", r"\toprule"]
    for row_index, row in enumerate(rows):
        output.append(" & ".join(inline(cell) for cell in row) + r" \\")
        if row_index == 0:
            output.append(r"\midrule")
    output.extend([r"\bottomrule", r"\end{tabularx}", r"\end{table}"])
    return output, index


def convert_section(path: Path) -> str:
    lines = path.read_text(encoding="utf-8").splitlines()
    output: list[str] = []
    paragraph: list[str] = []
    list_kind: str | None = None

    def flush_paragraph() -> None:
        if paragraph:
            joined = paragraph[0].strip()
            for part in paragraph[1:]:
                joined += ("" if joined.endswith("-") else " ") + part.strip()
            output.append(inline(joined))
            output.append("")
            paragraph.clear()

    def close_list() -> None:
        nonlocal list_kind
        if list_kind:
            output.append(rf"\end{{{list_kind}}}")
            output.append("")
            list_kind = None

    index = 0
    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if not stripped:
            flush_paragraph()
            close_list()
            index += 1
            continue
        if stripped.startswith(">"):
            index += 1
            continue
        figure = re.match(r"\*Figure (F[123]):", stripped)
        if figure:
            flush_paragraph()
            close_list()
            while not stripped.endswith(".*") and index + 1 < len(lines):
                index += 1
                stripped += " " + lines[index].strip()
            output.append(rf"\input{{figures/{figure.group(1).lower()}.tex}}")
            output.append("")
            index += 1
            continue
        if stripped.startswith("# "):
            flush_paragraph()
            title = re.sub(r"^#\s+(?:\d+\.\s*)?", "", stripped)
            if title.lower() == "abstract":
                output.append(r"\begin{abstract}")
            else:
                output.append(rf"\section{{{inline(title)}}}")
            index += 1
            continue
        if stripped.startswith("|"):
            flush_paragraph()
            close_list()
            table, index = emit_table(lines, index)
            output.extend(table + [""])
            continue
        bullet = re.match(r"^-\s+(.*)", stripped)
        number = re.match(r"^\d+\.\s+(.*)", stripped)
        if bullet or number:
            flush_paragraph()
            wanted = "itemize" if bullet else "enumerate"
            if list_kind != wanted:
                close_list()
                output.append(rf"\begin{{{wanted}}}")
                list_kind = wanted
            output.append(r"\item " + inline((bullet or number).group(1)))
            index += 1
            continue
        paragraph.append(stripped)
        index += 1

    flush_paragraph()
    close_list()
    if path.name.startswith("00-"):
        output.append(r"\keywords{ontology \and home-cage monitoring \and laboratory animals \and FAIR data \and SOSA/SSN \and 3Rs}")
        output.append(r"\end{abstract}")
    return "\n".join(output).strip() + "\n"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    section_out = OUT / "sections"
    section_out.mkdir(parents=True, exist_ok=True)
    for path in SECTIONS:
        rendered = convert_section(path)
        (section_out / f"{path.stem}.tex").write_text(rendered, encoding="utf-8", newline="\n")
    aggregate = OUT / "paper.tex"
    if aggregate.exists():
        aggregate.unlink()
    shutil.copyfile(PAPER / "references.bib", OUT / "references.bib")
    with zipfile.ZipFile(ARCHIVE, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(item for item in OUT.rglob("*") if item.is_file()):
            info = zipfile.ZipInfo(path.relative_to(OUT).as_posix())
            info.date_time = (1980, 1, 1, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())
    print(
        f"Exported {len(SECTIONS)} sections to {OUT.relative_to(ROOT).as_posix()} "
        f"and {ARCHIVE.relative_to(ROOT).as_posix()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
