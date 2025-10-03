# Too Big to Lose Supplement Metadata Notes

- Citation: Bains et al., "Too Big to Lose" (Nature Scientific Data, under review).
- Summary: Contains minimal metadata fields for home-cage monitoring datasets, aligning with TEATIME domains.
- Access: Upload the official supplemental tables when licence permits.
- Key tables to ingest:
  - Subject descriptors (strain, sex, age, genotype, experimental group).
  - Housing and environment (enclosure size, light cycle, enrichment, husbandry notes).
  - Hardware/software (system model, sensor list, sampling rates, firmware, acquisition software).
  - Data outputs (modality, format, QC metrics, provenance links).
- Integration guidance: Normalize column headers to snake_case for CSV ingestion and track provenance in `source_documents` within `ontology/hcm-blueprint.yaml`.
