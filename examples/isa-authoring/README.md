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
assays, data files, characteristic accessions, HCMO IRIs, contacts) with the
committed file.

## HCMO identity

The example links to HCMO the same way the native projection
(`../isa-roundtrip/native-isa/isatab/s_hcmo.txt`) does: a `Comment[HCMO IRI]`
names the individual of the canonical HCMO graph
(`../isa-roundtrip/canonical.ttl`) that an ISA object stands for. A comment is
added only where the identity holds one-to-one:

| ISA object | HCMO IRI (`https://example.org/hcmo/isa-roundtrip/…`) | Canonical type |
| --- | --- | --- |
| Source `animal-1` … `animal-8` (`s_hcmo_study.txt`) | `animal-1` … `animal-8` | `hcm-bio:Subject` |
| Study factor `drug` | `factor-treatment` | `hcm-bio:StudyFactors` |
| Study factor `environment` | `factor-enrichment` | `hcm-bio:StudyFactors` |
| Protocol `data acquisition` | `protocol-recording` | `bioschemas:LabProtocol` |

The day-1 activity values in `a_hcmo_monitoring.txt` equal the canonical
`result-N-day-1` values. No IRI is given where the example differs from the
canonical data: the `animal-N-sample-1` Samples (the canonical graph collects
one tissue specimen, from animal-8 only), cages `A`–`D` (the canonical animals
are housed in cages 1–9), `growth protocol`, `sample collection`, the
`monitoring day` factor, and the synthetic transcriptomics branch. The
validator checks that every IRI exists in `canonical.ttl` with the type above
(and, for animals, the same name) and that every Source carries one.

## Known limitations and open items

- **Whole-animal Sample convention: adopted, pending ISA confirmation.** The
  home-cage monitoring assay consumes `animal-N-sample-1`, the Sample each
  animal yields through the `sample collection` protocol; the transcriptomics
  assay consumes the same Samples. This is the usual ISA way to give an assay
  on a whole animal the Sample input that ISA requires. HCMO adopts it for HCM
  assays in ISA, with the details (protocol naming, and whether monitoring and
  transcriptomics share one Sample per animal) left to the ISA maintainers'
  review of PR #62. Until that review is settled, the following still describe
  the earlier position, under which this projection was deferred and a Sample
  for an unchanged animal was prohibited: the loss contracts under
  `../isa-roundtrip/loss/`, the A02 roadmap row in
  `docs/A02-ISA-STATO-COMPATIBILITY.md`, `docs/ISA-RO-CRATE-MAPPING.md`,
  `../isa-roundtrip/native-isa/README.md`, and the paper's use-case section
  and Figure 3 caption. They are updated in a follow-up.
- **HCMO term source.** The identity comments above link the example to HCMO
  data, but no ISA ontology annotation uses an HCMO class: the measurement,
  technology and protocol types the configuration keys on have no HCMO class
  equivalent, so no HCMO `Term Source` is declared (an unused source would only
  add a validator warning).
- **JSON-LD.** PR #62 intended the ISA-JSON to be testable with
  `ontology/context.jsonld`. That context maps HCMO properties, not ISA-JSON
  keys. The pinned ISA-API can emit ISA-JSON-LD (`Investigation.to_dict(ld=True)`
  after `isatab.load`), but it references its bundled OBO context by local
  file path, and the HCMO IRIs it now carries are plain `Comment` values, so
  `ontology/context.jsonld` still has nothing to resolve.
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
