#!/usr/bin/env python3
"""Package the authoritative Overleaf manuscript as a deterministic ZIP."""

from __future__ import annotations

import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAPER = ROOT / "docs" / "paper"
OUT = PAPER / "overleaf"
ARCHIVE = PAPER / "hcmo-overleaf-upload.zip"
ARCHIVE_TEXT_SUFFIXES = {".bib", ".md", ".tex"}

def archive_payload(path: Path) -> bytes:
    """Return platform-independent bytes for a paper-package member."""
    data = path.read_bytes()
    if path.suffix.lower() not in ARCHIVE_TEXT_SUFFIXES:
        return data
    text = data.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
    return text.encode("utf-8")


def main() -> int:
    section_paths = sorted((OUT / "sections").glob("[0-9][0-9]-*.tex"))
    required = [OUT / "main.tex", OUT / "references.bib", *section_paths]
    missing = [path for path in required if not path.is_file()]
    if missing or len(section_paths) != 9:
        names = ", ".join(path.relative_to(ROOT).as_posix() for path in missing)
        raise RuntimeError(
            "Authoritative Overleaf source is incomplete: expected main.tex, "
            f"references.bib, and 9 sections; missing: {names or 'none'}"
        )
    with zipfile.ZipFile(ARCHIVE, "w", compression=zipfile.ZIP_STORED) as archive:
        members = (item for item in OUT.rglob("*") if item.is_file())
        for path in sorted(members, key=lambda item: item.relative_to(OUT).as_posix()):
            info = zipfile.ZipInfo(path.relative_to(OUT).as_posix())
            info.date_time = (1980, 1, 1, 0, 0, 0)
            info.create_system = 3
            info.compress_type = zipfile.ZIP_STORED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, archive_payload(path))
    print(
        f"Packaged {len(section_paths)} authoritative Overleaf sections from "
        f"{OUT.relative_to(ROOT).as_posix()} into {ARCHIVE.relative_to(ROOT).as_posix()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
