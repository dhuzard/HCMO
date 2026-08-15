# Paper-matching release gate

## Current state

- The immutable `v0.2.0` tag points to commit
  `3f7c308f21c92e91d400fbf1c5914b5ff9e0ddc7` from 17 July 2026.
- The reviewed post-PR #26 graph is 24 commits ahead of that tag.
- `hcmo.yaml` and the ontology header still identify version `0.2.0`.
- The public PURL currently serves a 1,252-triple graph that is not isomorphic
  to the reviewed 1,397-triple candidate.
- The paper must therefore not identify the post-PR #26 graph as the tagged
  `v0.2.0` release.

## Required release decision

Assign a version greater than `0.2.0` before submission. `0.3.0` is the
conservative recommendation because the candidate adds substantial semantic
models, deprecations, external-vocabulary contracts, examples, constraints, and
executable interoperability evidence. The version is deliberately not changed
in this documentation-only PR.

## Release procedure

1. Merge the accepted ontology and paper changes.
2. Update `hcmo.yaml`, the root ontology `owl:versionIRI`/`owl:versionInfo`, and
   version-bearing documentation in one release PR.
3. Run `python tooling/build.py` twice and require byte-identical artifacts.
4. Run `python tooling/validate.py`, HermiT, the external-vocabulary network
   check, RO-Crate validation, and the native ISA projection.
5. Run OOPS! on the generated RDF/XML artifact and FOOPS! through the public
   ontology PURL; archive both raw responses and their triage.
6. Deploy the candidate and confirm that PURL content negotiation returns the
   same 1,397-triple graph in the supported RDF serializations.
7. Confirm documentation, DOI metadata, and release files.
8. Create the matching Git tag and GitHub/Zenodo release.
9. Replace "candidate" in the paper with the chosen version only after the tag
   and public artifacts exist.
