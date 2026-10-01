# Security policy

HCMO is an ontology, its SHACL shapes, SKOS vocabularies, examples and
validation tooling. It does not run a hosted service, but the Python tooling and
GitHub workflows execute in contributors' environments and in CI, and the data
files under `docs/hcm-systems/` and `examples/` must not expose personal or
confidential information.

## Reporting a vulnerability or a data exposure

Please **do not open a public issue**. Report privately, preferably through
GitHub's "Report a vulnerability" button on the repository's Security tab, or by
email to the maintainer at damien.huzard@gmail.com with:

- what you found and where (file, workflow or URL),
- how to reproduce it, and
- what you think the impact is.

We aim to acknowledge a report within 7 days and to tell you the outcome or a
plan within 30 days. This is a volunteer-maintained research project, so these
are targets, not guarantees.

## In scope

- Code and workflows in `tooling/` and `.github/workflows/` (for example unsafe
  handling of input files, or leaked tokens or credentials).
- Personal data, animal-identifying data or confidential vendor data committed to
  the repository, including the dataset files under `docs/hcm-systems/`.

## Out of scope

- Modelling disagreements or ontology design questions (open a normal issue).
- Vulnerabilities in third-party tools or vocabularies we only reference.

## Supported versions

Only the latest release and the `main` branch receive fixes. Released versions are
listed in [`CHANGELOG.md`](CHANGELOG.md).
