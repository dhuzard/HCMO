# Paper-matching release gate

## Current state

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

## Publication decision

Version `0.3.0` is published and citable. The archived tag and Zenodo record are
immutable: subsequent metadata or maturity changes belong in a new patch
release. In particular, changing `mod:status` from `draft` to another maturity
term would change ontology bytes and must not be retroactively applied to 0.3.0.

## Release procedure

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
