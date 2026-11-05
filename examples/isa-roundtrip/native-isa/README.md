# Native ISA-API projection of the Figure 3 example

This directory is generated with pinned `isatools` 0.14.3. It contains the
part of the Figure 3 example that standard ISA-JSON and ISA-Tab can represent
without changing the identity or biological role of an entity:

```text
animal-8 (ISA Source)
  -- sample-collection Process / Protocol -->
tissue specimen animal 8 (ISA Sample)
```

The ISA-API outputs are:

- `isa.json`: the initial ISA-JSON document;
- `isatab/i_investigation.txt`: ISA-Tab investigation metadata; and
- `isatab/s_hcmo.txt`: the Source-to-Sample study table.

The full HCMO/extended ISA RO-Crate example remains in `../canonical.ttl` and
`../ro-crate-metadata.json`. The raw and modeled data are in `../data/`.

## Decisions behind the projection

| Figure 3 concept | Decision | Reason |
| --- | --- | --- |
| Animal | ISA Source | It is the starting biological material or organism, not a specimen derived during the study. |
| Tissue specimen | ISA Sample | It is a genuine material specimen derived from the animal by collection. |
| Assay | ISA Assay dataset/branch for the measurement workflow | The assay is not itself the reusable procedure or the behavioral context. The recording method is a Protocol, its execution is a Process, and a deliberately varied context is a factor. |
| Recording | Process executing the recording Protocol; generates `dark-phase-activity.csv` | This is the acquisition step and its direct data output. |
| Model fitting | Process executing the analysis Protocol; consumes `dark-phase-activity.csv` and generates `model-results.csv` | This keeps data acquisition separate from statistical transformation. |
| Specimen collection | Process executing the collection Protocol; consumes the animal Source and generates the tissue Sample | Its output is biological material, not a data file. |
| Physical cage | HCMO `MonitoredEnclosure` | A cage is neither biological material nor a study factor merely because it has an identifier. |
| Cage assignment | HCMO time-bounded `HousingAssignment`, associated with an allocation/rehousing Process | The assignment is a record of where and when the animal was housed; it is not a Sample or DataFile. |
| Treatment and cage enrichment | ISA Study Factors | These are deliberately varied experimental conditions. Cage ID itself is not a factor. |
| Experimental group | Explicit HCMO/STATO population grouping; derivable from factor-value combinations in a native ISA table | A group is not an additional factor. |
| Result CSV | ISA DataFile output | `model-results.csv` is a file artifact. |
| Estimate, confidence interval, and p-value | STATO-typed semantic result entities in the canonical RDF, linked to exact CSV fragments | These meanings are richer than bare ISA-Tab result cells and are not silently flattened. |

The checked-in native projection intentionally stops at the valid
Source-to-Sample collection path. Standard ISA-Tab assay tables start with a
`Sample Name`, and factor values are attached to Samples by the current
ISA-API writer. Treating each unchanged animal as a manufactured Sample proxy
would contradict the accepted animal-as-Source decision. Direct whole-animal
recording, source-bound factor values, explicit group resources, repeated
observations, housing records, and semantic STATO/file-fragment links therefore
remain declared controlled losses until a reviewed ISA configuration or
community convention represents them without that fabrication.

## Reproduce and validate

From the repository root:

```bash
pip install -r tooling/interoperability-requirements.txt
python tooling/validate_isa_native_projection.py --write
python tooling/validate_isa_native_projection.py
```

The second command rebuilds the projection in a temporary directory, checks
that the committed files are byte-for-byte reproducible, validates ISA-JSON
and ISA-Tab, converts JSON to Tab and back, and verifies that the Source,
Sample, collection Process, derivation, and HCMO identifiers survive.
