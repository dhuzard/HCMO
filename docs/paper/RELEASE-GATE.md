# Paper-matching release gate

## 0.4.0 (in progress)

The paper describes **HCMO 0.4.0** (decided 2026-10-12). 0.4.0 adds the
multi-animal behaviour model (ADR-0006, accepted), file-format and data-access
SKOS links, the optional BFO/SOSA bridge profile (ADR-0005, accepted; not in
the default release) and the generated external-reuse report. `mod:status`
stays `"draft"`.

Release procedure (same gates as 0.3.0):

1. Release branch `release/0.4.0`: version metadata, ontology header (version
   IRI, prior version, issued/modified dates, nine authors in paper order),
   `CITATION.cff`, CHANGELOG cut, documentation and manuscript updated. ✔
2. `hcmo.yaml`, root `owl:versionIRI`/`owl:versionInfo`, competency-question
   index, contribution form and `CITATION.cff` identify `0.4.0` (checked by
   `tooling/validate.py`). ✔
3. `python tooling/build.py` run twice with byte-identical artifacts. ✔
4. `tooling/validate.py`, HermiT (`tooling/reason.py`), the external-vocabulary
   network check, the interoperability validation and the bridge-profile check. ✔
5. Merge the release PR; tag `v0.4.0` and publish the GitHub release (the
   `release` workflow attaches `hcmo.ttl`, `hcmo.owl`, `hcmo.json`,
   `profile.json`, `hcmo.yaml`; `release-evidence` archives AskWol).
6. Zenodo mints the 0.4.0 version DOI; record it in `CITATION.cff`, the README,
   `docs/paper/metadata/resource-metadata.md`, the manuscript availability
   statement and `references.bib` (`hcmo` entry).
7. Confirm that `https://w3id.org/hcmo/ontology/hcm` and `…/hcm/0.4.0` return
   the 1,464-triple graph by content negotiation, and that the WIDOCO site shows
   0.4.0 (redeployed from `main` by the `docs` workflow).
8. Re-run OOPS! on the 0.4.0 RDF/XML and FOOPS! on the PURL; archive raw output
   and triage under `evaluation/`, then update the manuscript's scan table
   (still reporting the 0.3.0 scans until then).

## 0.3.0 record (published 2026-08-31)

- The immutable `v0.3.0` tag points to commit
  `3083d2307d5cbac97bcaee189b75fdf909d0de5f`.
- The GitHub release is published with `hcmo.ttl`, `hcmo.owl`, `hcmo.json`,
  `profile.json`, and `hcmo.yaml` assets.
- Zenodo archives version 0.3.0 as DOI `10.5281/zenodo.22208202`; the stable
  concept DOI remains `10.5281/zenodo.18925284`.
- The unversioned and `…/hcm/0.3.0` PURLs route content-negotiated RDF to the
  release assets, and the public WIDOCO site describes HCMO rather than MAPP.
- The paper may call this the **published HCMO 0.3.0 release**. The distinct
  `mod:status "draft"` value is retained as the ontology-maturity statement.
- The immutable ontology header also retains its pre-publication
  `dcterms:issued "2026-03-09"`, `dcterms:publisher "Huzard group"`, and earlier
  `bibo:authorList` order. These do not affect term IRIs or graph availability,
  but correcting them in RDF (or promoting `mod:status`) requires a metadata-only
  patch release such as 0.3.1 rather than rewriting the 0.3.0 tag.
- The Zenodo title, version, date, DOI, file, CC BY 4.0 license, and confirmed
  creator order were verified on 31 August 2026. The creator-order correction
  was metadata-only and did not change the tag or ontology IRIs.

### 0.3.0 publication decision

Version `0.3.0` is published and citable. The archived tag and Zenodo record are
immutable: subsequent metadata or maturity changes belong in a new patch
release. In particular, changing `mod:status` from `draft` to another maturity
term would change ontology bytes and must not be retroactively applied to 0.3.0.

### 0.3.0 release procedure

1. Review and merge the accepted ontology, release-metadata, and paper changes. ✔
2. Confirm that `hcmo.yaml`, the root ontology
   `owl:versionIRI`/`owl:versionInfo`, and version-bearing documentation all
   identify `0.3.0`. ✔
3. Run `python tooling/build.py` twice and require byte-identical artifacts. ✔
4. Run `python tooling/validate.py`, HermiT, the external-vocabulary network
   check, RO-Crate validation, and the native ISA projection. ✔
5. Run OOPS! on the generated RDF/XML artifact and FOOPS! through the public
   ontology PURL; archive both raw responses and their triage.
6. Create and publish the matching Git tag and GitHub release so that the
   `releases/latest` PURL targets can resolve the 0.3.0 assets. ✔
7. Publish the matching Zenodo version and documentation, then confirm the
   version-specific DOI metadata and release files. ✔
8. Confirm that PURL content negotiation returns the same 1,397-triple graph in
   every supported RDF serialization. ✔
9. Replace "release candidate" with "release" in the paper only after the tag
   and public artifacts exist. ✔

AskWol is handled separately by `.github/workflows/release-evidence.yml`: its
raw beta-service response is archived as non-blocking evidence and interpreted
under `evaluation/ASKWOL-TRIAGE.md`.
