#!/usr/bin/env python3
"""Stage the RDF files that the w3id rules redirect to, for GitHub Pages.

GitHub release downloads end at a signed storage URL served as
`application/octet-stream`, which RDF crawlers (LOV, AskWol) do not parse.
GitHub Pages serves `.ttl`, `.owl`, `.jsonld` and `.nt` with their RDF media
types, so the docs workflow copies the files there and the w3id rules point to
these paths (under https://dhuzard.github.io/HCMO/):

  dist/<version>/hcmo.{ttl,owl,jsonld}   exact assets of release v<version>
  dist/latest/hcmo.{ttl,owl,jsonld}      exact assets of the latest release
  vocab/<scheme>.ttl                     SKOS vocabularies, one per scheme slug
  profile/bfo-sosa-bridge.ttl            optional bridge profile (latest release)
  ontology/external/upper-presentation.ttl
                                         upper-level presentation module (latest release)

Release assets are downloaded unchanged with the GitHub CLI (`gh`); only
`hcmo.json` is renamed to `hcmo.jsonld` so that Pages serves it as JSON-LD.
Vocabularies, profile and upper module are read from the latest release tag,
so everything served matches a published release.

Usage: python tooling/publish_rdf.py --out docs/widoco   (needs gh and git tags)
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from rdflib import Graph, RDF
from rdflib.namespace import SKOS

ROOT = Path(__file__).resolve().parent.parent
VERSION_TAG = re.compile(r"^v(\d+\.\d+(?:\.\d+)?)$")
ASSETS = {"hcmo.ttl": "hcmo.ttl", "hcmo.owl": "hcmo.owl", "hcmo.json": "hcmo.jsonld"}
VOCAB_BASE = "https://w3id.org/hcmo/id/vocab/"
TAG_FILES = {
    "ontology/profiles/bfo-sosa-bridge.ttl": "profile/bfo-sosa-bridge.ttl",
    "ontology/modules/external-upper.ttl": "ontology/external/upper-presentation.ttl",
}


def run(*cmd: str) -> str:
    return subprocess.run(cmd, cwd=ROOT, check=True, capture_output=True).stdout.decode("utf-8")


def releases() -> tuple[list[tuple[str, str]], str]:
    listed = json.loads(run("gh", "release", "list", "--limit", "200",
                            "--json", "tagName,isDraft,isPrerelease,isLatest"))
    published = [(r["tagName"], VERSION_TAG.match(r["tagName"]).group(1)) for r in listed
                 if not r["isDraft"] and not r["isPrerelease"] and VERSION_TAG.match(r["tagName"])]
    latest = [r["tagName"] for r in listed if r.get("isLatest")]
    if not latest:
        raise SystemExit("no release is marked latest")
    return published, latest[0]


def download(tag: str, target: Path) -> bool:
    with tempfile.TemporaryDirectory() as tmp:
        try:
            run("gh", "release", "download", tag, "--dir", tmp,
                *[arg for name in ASSETS for arg in ("--pattern", name)])
        except subprocess.CalledProcessError:
            return False
        if not all((Path(tmp) / name).is_file() for name in ASSETS):
            return False
        target.mkdir(parents=True, exist_ok=True)
        for name, published in ASSETS.items():
            shutil.copyfile(Path(tmp) / name, target / published)
    return True


def tag_file(tag: str, path: str) -> bytes:
    return subprocess.run(["git", "show", f"{tag}:{path}"], cwd=ROOT, check=True,
                          capture_output=True).stdout


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", required=True, type=Path)
    out = parser.parse_args().out
    published, latest = releases()

    staged = []
    for tag, version in published:
        ok = download(tag, out / "dist" / version)
        print(f"{'staged' if ok else 'skipped (assets missing)'}: dist/{version}/ <- {tag}")
        if ok:
            staged.append(tag)
    if not staged:
        raise SystemExit("no published release has the hcmo.ttl/owl/json assets")
    if latest not in staged:
        # A release published moments ago may not have its assets attached yet;
        # serve the newest complete release until the next run.
        print(f"warning: latest release {latest} has no assets yet; using {staged[0]}")
        latest = staged[0]
    latest_version = VERSION_TAG.match(latest).group(1)
    shutil.copytree(out / "dist" / latest_version, out / "dist" / "latest", dirs_exist_ok=True)
    print(f"staged: dist/latest/ <- {latest}")

    listing = run("git", "ls-tree", "--name-only", f"{latest}:vocabularies").split()
    for name in sorted(n for n in listing if n.endswith(".ttl")):
        data = tag_file(latest, f"vocabularies/{name}")
        schemes = [str(s) for s in Graph().parse(data=data, format="turtle").subjects(RDF.type, SKOS.ConceptScheme)]
        if len(schemes) != 1 or not schemes[0].startswith(VOCAB_BASE):
            raise SystemExit(f"vocabularies/{name}: expected one scheme under {VOCAB_BASE}, got {schemes}")
        target = out / "vocab" / f"{schemes[0][len(VOCAB_BASE):]}.ttl"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        print(f"staged: {target.relative_to(out).as_posix()} <- {latest}:vocabularies/{name}")

    for source, published_path in TAG_FILES.items():
        target = out / published_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(tag_file(latest, source))
        print(f"staged: {published_path} <- {latest}:{source}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
