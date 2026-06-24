#!/usr/bin/env python3
"""Generate HTML ontology documentation with WIDOCO (https://github.com/dgarijo/Widoco).

Reads the merged graph path from hcmo.yaml and renders a self-contained HTML
documentation site (overview, term cross-reference, namespace declarations, a
WebVOWL diagram, and provenance) into docs/widoco/. The output is GENERATED and
git-ignored; the published copy is built by .github/workflows/docs.yml.

WIDOCO is a Java tool. This wrapper:
  * finds a JRE on PATH (Java 11+),
  * locates the WIDOCO jar from --jar / $WIDOCO_JAR, else downloads a pinned
    release into tooling/.widoco/ (cached, git-ignored),
  * runs WIDOCO against dist/hcmo.ttl,
  * drops an index.html shim so the site serves at the directory root.

Usage:
  python tooling/docs.py                 # build docs/widoco/ from dist/hcmo.ttl
  python tooling/docs.py --jar PATH      # use a specific WIDOCO jar
  python tooling/docs.py -- -oops        # pass extra flags through to WIDOCO

Overridable via env: WIDOCO_JAR, WIDOCO_VERSION (default 1.4.25), WIDOCO_JDK
(default 11).
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "hcmo.yaml"
OUT_DIR = ROOT / "docs" / "widoco"
CACHE_DIR = ROOT / "tooling" / ".widoco"

WIDOCO_VERSION = os.environ.get("WIDOCO_VERSION", "1.4.25")
WIDOCO_JDK = os.environ.get("WIDOCO_JDK", "11")


def load_manifest() -> dict:
    with open(MANIFEST) as f:
        return yaml.safe_load(f)


def jar_url() -> str:
    name = f"widoco-{WIDOCO_VERSION}-jar-with-dependencies_JDK-{WIDOCO_JDK}.jar"
    return (
        f"https://github.com/dgarijo/Widoco/releases/download/"
        f"v{WIDOCO_VERSION}/{name}"
    )


def resolve_jar(explicit: str | None) -> Path:
    """Return a usable WIDOCO jar, downloading the pinned release if needed."""
    candidate = explicit or os.environ.get("WIDOCO_JAR")
    if candidate:
        p = Path(candidate)
        if not p.exists():
            raise SystemExit(f"ERROR: WIDOCO jar not found: {p}")
        return p

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cached = CACHE_DIR / f"widoco-{WIDOCO_VERSION}_JDK-{WIDOCO_JDK}.jar"
    if cached.exists():
        return cached

    url = jar_url()
    print(f"Downloading WIDOCO {WIDOCO_VERSION} (JDK {WIDOCO_JDK})\n  {url}")
    tmp = cached.with_suffix(".part")
    try:
        urllib.request.urlretrieve(url, tmp)
    except Exception as exc:  # noqa: BLE001 — surface a clear, actionable message
        raise SystemExit(
            f"ERROR: failed to download WIDOCO: {exc}\n"
            f"Download it manually and pass --jar PATH or set WIDOCO_JAR.\n"
            f"  {url}"
        )
    tmp.replace(cached)
    return cached


def write_index_shim() -> None:
    """WIDOCO emits index-en.html; add index.html so the site serves at root."""
    index = OUT_DIR / "index.html"
    if index.exists():
        return
    localized = OUT_DIR / "index-en.html"
    if not localized.exists():
        return
    index.write_text(
        '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
        '<meta http-equiv="refresh" content="0; url=index-en.html">'
        '<link rel="canonical" href="index-en.html">'
        "<title>Redirecting…</title></head>"
        '<body><a href="index-en.html">Ontology documentation</a></body></html>\n'
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jar", help="Path to a WIDOCO jar-with-dependencies.")
    parser.add_argument(
        "extra",
        nargs=argparse.REMAINDER,
        help="Extra flags passed through to WIDOCO (after --).",
    )
    args = parser.parse_args()

    if shutil.which("java") is None:
        raise SystemExit(
            "ERROR: 'java' not found on PATH. WIDOCO needs a Java 11+ runtime.\n"
            "Install a JRE (e.g. Temurin) and re-run."
        )

    manifest = load_manifest()
    ont_file = ROOT / manifest["dist"]["merged_ttl"]
    if not ont_file.exists():
        raise SystemExit(
            f"ERROR: {ont_file.relative_to(ROOT)} not found. "
            "Run `python tooling/build.py` first."
        )

    jar = resolve_jar(args.jar)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    extra = [a for a in args.extra if a != "--"]
    cmd = [
        "java", "-jar", str(jar),
        "-ontFile", str(ont_file),
        "-outFolder", str(OUT_DIR),
        "-rewriteAll",            # overwrite previous output
        "-getOntologyMetadata",   # read title/version/license/creators from the header
        "-uniteSections",         # one HTML page instead of split sections
        "-includeAnnotationProperties",
        "-webVowl",               # embed a WebVOWL diagram
        "-lang", "en",
        *extra,
    ]
    print("Running:\n  " + " ".join(cmd))
    result = subprocess.run(cmd, cwd=ROOT)
    if result.returncode != 0:
        return result.returncode

    write_index_shim()
    print(f"\nDocumentation written to {OUT_DIR.relative_to(ROOT)}/")
    print(f"  open {OUT_DIR.relative_to(ROOT)}/index.html")
    return 0


if __name__ == "__main__":
    sys.exit(main())
