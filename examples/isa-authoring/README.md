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

- **Policy review pending.** `docs/A02-ISA-STATO-COMPATIBILITY.md` lists a
  direct whole-animal HCM assay projection as *Deferred* until a reviewed ISA
  configuration exists, and both loss contracts under
  `../isa-roundtrip/loss/` prohibit minting a Sample proxy for an unchanged
  animal. This example introduces that configuration (`config/`) but has not
  been reviewed against those contracts: the home-cage monitoring assay
  consumes `animal-N-sample-1`, the output of the `sample collection`
  protocol, which the companion transcriptomics assay also consumes. A
  home-cage recording observes the whole animal, not a collected specimen.
  Accepting this example as the reviewed configuration means updating the
  loss contracts, the A02 roadmap row, `docs/ISA-RO-CRATE-MAPPING.md` and
  `../isa-roundtrip/native-isa/README.md`; otherwise the monitoring branch
  must be remodelled (for example a distinct, explicitly documented
  whole-animal Sample carrying the Source's `Comment[HCMO IRI]`).
- **Issue #61 is not closed by this example yet.** It asks for an experiment
  represented *using HCMO*; no HCMO term, IRI or ontology source reference
  appears in the ISA files. Use *refs #61* rather than *closes #61* until the
  HCMO identity columns below exist.
- **JSON-LD.** PR #62 intended the ISA-JSON to be testable with
  `ontology/context.jsonld`. That context maps HCMO properties, not ISA-JSON
  keys. The pinned ISA-API can emit ISA-JSON-LD (`Investigation.to_dict(ld=True)`
  after `isatab.load`), but it references its bundled OBO context by local
  file path and the output contains no HCMO IRI, so there is nothing for the
  HCMO context to resolve until HCMO IRIs are carried in the instance.
- Every row carries `Factor Value[monitoring day] = 1`; the repeated-measure
  design named in the study description is not yet represented (the generated
  fixture in `../isa-roundtrip/data/dark-phase-activity.csv` has 7 days per
  animal).
- The activity count is recorded as `Comment[raw signal]`; the raw files named
  in `Raw Data File` are not part of the repository.
- Term accessions were checked against OLS4 (2026-11-05). `factorial design`
  is `OBI:0500014` and `repeated measure design` is `OBI:0500002`, both imported
  by STATO (the original `STATO:0000234` is *residual*); the `nucleic acid
  sequencing` protocol is `EFO:0004170` (the original `OBI:0001959` is
  *multiplexed nucleotide library sequencing*). `phenotyping`, `home cage
  monitoring`, `data acquisition` and the `environment` factor type still have
  no accession. Candidates: `EFO:0920062` *phenotyping* and `MMO:0000596`
  *home cage monitoring method*. They are left for the configuration review
  because MMO is not yet a declared term source and the protocol type
  (`data acquisition` vs `home cage monitoring`) is still undecided.
- The transcription-profiling assay is synthetic (placeholder file names,
  flowcell and library metadata).
- No HCMO IRIs are carried yet. Adding `Comment[HCMO IRI]` columns, as in
  `../isa-roundtrip/native-isa/isatab/s_hcmo.txt`, would allow cross-checking
  against `../isa-roundtrip/canonical.ttl`.
