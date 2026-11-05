# HCMO ISA authoring example

Hand-authored ISA-Tab and ISA-JSON instance of a 2 × 2 (drug × cage
environment) home-cage monitoring study with a companion transcriptomics assay
(issue #61), together with the ISA configuration that makes a
`phenotyping` / `home cage monitoring` assay valid for the ISA-API validator.

This directory is **not** the generated round-trip fixture. The canonical HCMO
RDF, the extended ISA RO-Crate and the reproducible native ISA projection stay
under `../isa-roundtrip/`; this example shows how an ISA curator would author
the same kind of study by hand with ISA tooling.

## Layout

| Path | Purpose |
| --- | --- |
| `isatab/i_Investigation_hcmo.txt` | Investigation and study metadata, factors, protocols, assays. |
| `isatab/s_hcmo_study.txt` | Source-to-Sample table: 8 animals, growth protocol, cage parameter, sample collection. |
| `isatab/a_hcmo_monitoring.txt` | Home-cage monitoring assay (`data acquisition` protocol, one raw file per animal). |
| `isatab/a_hcmo_rnaseq.txt` | Synthetic transcription-profiling assay illustrating a multimodal study. |
| `isajson/isa.json` | ISA-JSON produced from `isatab/` with the configuration in `config/json/default`. |
| `config/xml/` | ISA-Tab validator configuration (`isatab.validate`). |
| `config/json/default/` | ISA-JSON validator / converter configuration (`isajson.validate`, `isatab2json.convert`). |
| `reading-and-validating-isa-tab.ipynb` | Walk-through of loading, validating and converting the example. |

## Configuration provenance

The configuration files are copies of the `isatools` 0.14.3 defaults plus the
HCMO additions. Keep this list current when a file changes.

| File | Status |
| --- | --- |
| `config/xml/hcagemonitoring.xml` | New: `phenotyping` / `home cage monitoring` assay table with a `data acquisition` protocol field. |
| `config/json/default/phenotyping_homecagemonitoring.json` | New: `(Sample)->(data acquisition)->(DataFiles)`. |
| `config/xml/investigation.xml` | Default, with `is-required` relaxed on the Investigation and Study PubMed ID / DOI fields. |
| `config/xml/transcription_seq.xml` | Default, with `Parameter Value[library layout]` renamed `Parameter Value[library_layout]`. |
| `config/xml/studySample.xml`, `config/json/default/study_config.json`, `config/json/default/transcription_seq.json` | Identical to the defaults; vendored because `isatools` loads configurations from one directory only. |

## Validate and regenerate

From the repository root:

```bash
pip install -r tooling/interoperability-requirements.txt
python tooling/validate_isa_authoring_example.py          # validate ISA-Tab and ISA-JSON, compare structure
python tooling/validate_isa_authoring_example.py --write  # regenerate isajson/isa.json from isatab/
```

The ISA-API mints UUID-based `@id` values on every conversion, so
`isajson/isa.json` is not byte-reproducible. The validator therefore compares
the structure of a fresh conversion (sources, samples, protocols, factors,
assays, data files, characteristic accessions) with the committed file.

## Known limitations and open items

- Every row carries `Factor Value[monitoring day] = 1`; the repeated-measure
  design named in the study description is not yet represented (the generated
  fixture in `../isa-roundtrip/data/dark-phase-activity.csv` has 7 days per
  animal).
- The activity count is recorded as `Comment[raw signal]`; the raw files named
  in `Raw Data File` are not part of the repository.
- The `repeated measure design` design descriptor has no verified STATO
  accession yet. `phenotyping`, `home cage monitoring`, `data acquisition` and
  the `environment` factor type have no ontology accession.
- The transcription-profiling assay is synthetic (placeholder file names,
  flowcell and library metadata).
- No HCMO IRIs are carried yet. Adding `Comment[HCMO IRI]` columns, as in
  `../isa-roundtrip/native-isa/isatab/s_hcmo.txt`, would allow cross-checking
  against `../isa-roundtrip/canonical.ttl`.
