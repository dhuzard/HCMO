# Competency questions on the public SPARQL endpoint (2026-10-29)

Run of `tooling/run_cqs.py` against the public, read-only Fuseki endpoint
`https://sparql.hcmo.metadatapp.net/` (permanent address
`https://w3id.org/hcmo/sparql`, perma-id/w3id.org#7018, merged later the same
day), as evidence
for the paper (§4, §6).

- Run at: 2026-10-29T10:49Z (UTC), from a local checkout of `main` at 4abefb1.
- Deployed image: built from `main` at 4abefb1 (HCMO 0.4.1 data) by the
  `SPARQL deploy` workflow,
  <https://github.com/dhuzard/HCMO/actions/runs/40851386614>, which ran the same
  check on `/hcmo` after deploying (PASS).
- Expected answers: `queries/competency_questions.yaml`, compared row by row
  in the validator's canonical form.

## `/hcmo` (reference graph)

```text
$ python tooling/run_cqs.py --endpoint https://sparql.hcmo.metadatapp.net/hcmo/sparql
endpoint: https://sparql.hcmo.metadatapp.net/hcmo/sparql
[OK]   animals-by-enclosure: 3 exact answer(s)
[OK]   isa-factor-group-assignment: 1 exact answer(s)
[OK]   isa-recording-provenance: 1 exact answer(s)
[OK]   isa-statistical-result-provenance: 1 exact answer(s)
[OK]   missing-dimensions: 0 exact answer(s)
[OK]   environment-spec-observation: 1 exact answer(s)
[OK]   current-housing-at-time: 1 exact answer(s)
[OK]   status-evidence-at-time: 1 exact answer(s)
[OK]   needs-provisioning: 4 exact answer(s)
[OK]   sensors-behaviors: 5 exact answer(s)
[OK]   systems-24h-limited: 1 exact answer(s)
[OK]   social-interaction-partners: 2 exact answer(s)
result: PASS
```

## `/hcmo-0.4.1` (the same data under the release name)

```text
$ python tooling/run_cqs.py --endpoint https://sparql.hcmo.metadatapp.net/hcmo-0.4.1/sparql
endpoint: https://sparql.hcmo.metadatapp.net/hcmo-0.4.1/sparql
[OK]   animals-by-enclosure: 3 exact answer(s)
[OK]   isa-factor-group-assignment: 1 exact answer(s)
[OK]   isa-recording-provenance: 1 exact answer(s)
[OK]   isa-statistical-result-provenance: 1 exact answer(s)
[OK]   missing-dimensions: 0 exact answer(s)
[OK]   environment-spec-observation: 1 exact answer(s)
[OK]   current-housing-at-time: 1 exact answer(s)
[OK]   status-evidence-at-time: 1 exact answer(s)
[OK]   needs-provisioning: 4 exact answer(s)
[OK]   sensors-behaviors: 5 exact answer(s)
[OK]   systems-24h-limited: 1 exact answer(s)
[OK]   social-interaction-partners: 2 exact answer(s)
result: PASS
```
