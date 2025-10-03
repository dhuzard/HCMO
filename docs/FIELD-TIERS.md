# Field Tiers (Mandatory / Recommended / Optional)

Each field below includes a description, rationale, example value, validation notes, and downstream utility. Types use JSON-friendly terminology; link to ontological IRIs when appropriate.

## Mandatory Fields
| Field | Description | Rationale | Example Value | Validation Notes | Downstream Utility |
| ----- | ----------- | --------- | ------------- | ---------------- | ------------------ |
| `system_id` | Unique identifier for the monitoring system instance. | Enables cross-dataset reconciliation and auditing. | `hcmo-system-001` | Non-empty string; prefer URI or globally unique ID. | Linking device exports, provenance tracking. |
| `subject_id` | Identifier for the subject or cohort. | Maintains longitudinal traceability. | `S-00123` | String; uniqueness scoped to protocol; optional CURIE. | Cohort analytics, welfare follow-up. |
| `protocol_id` | Reference to protocol or ethical approval. | Maintains traceability to governance artifacts. | `doi:10.1234/hcmo-proto` | String or IRI; must resolve or be documented. | Compliance review, reproducibility. |
| `session_interval` | Start/End timestamps of monitoring session. | Needed to interpret derived metrics. | `{ "start": "2025-09-15T08:00:00Z", "end": "2025-09-16T08:00:00Z" }` | ISO 8601 timestamps; end > start. | Time-based analytics, cross-system alignment. |
| `enclosure_reference` | Identifier for the monitored enclosure. | Connects provisioning, environment attributes. | `ENC-42-A` | String; should map to facility inventory. | Facility management integration. |

## Recommended Fields
| Field | Description | Rationale | Example Value | Validation Notes | Downstream Utility |
| ----- | ----------- | --------- | ------------- | ---------------- | ------------------ |
| `device_model` | Human-readable model or build name. | Contextualizes capabilities and limitations. | `Model X Rev 3` | String; keep manufacturer neutral if NDA-bound. | Troubleshooting, replication planning. |
| `sampling_strategy` | Summary of sampling cadence and modality. | Clarifies signal expectations. | `IR beam, 1Hz continuous` | String; consider structured object if precise modeling needed. | Time-series harmonization, QA checks. |
| `enclosure_profile` | Structured description of enclosure (dimensions, materials). | Bridges to welfare guidelines. | `{ "dimensions_cm": { "length": 50, "width": 30, "height": 20 } }` | Numeric values > 0; specify units. | Welfare verification, cross-facility benchmarking. |
| `operator_contact` | Point of contact for system owner or steward. | Supports collaboration and updates. | `hcm-team@example.org` | Valid email or ticket queue URL. | Escalations, checklist maintenance. |
| `data_product_links` | URIs for derived data artifacts. | Facilitates reproducibility. | `[ "https://example.org/data/system-001/day-01.csv" ]` | URI array; confirm accessibility metadata. | Meta-analysis pipelines, archival handoffs. |

## Optional Fields
| Field | Description | Rationale | Example Value | Validation Notes | Downstream Utility |
| ----- | ----------- | --------- | ------------- | ---------------- | ------------------ |
| `firmware_version` | Firmware or software build identifier. | Aids debugging and historical context. | `v1.2.3` | String; align with vendor versioning. | Regression analysis, compatibility checks. |
| `calibration_notes` | Human-entered notes about calibration steps. | Captures tacit knowledge. | `Calibrated IR array on 2025-09-10.` | Free text; include timestamp if possible. | Audit trails, reproducibility narratives. |
| `derived_kpis` | Key performance indicators derived from monitoring. | Encourages consistent, shareable metrics. | `{ "mean_activity_index": 0.68 }` | JSON object with numeric values; document formulas elsewhere. | Comparative analysis, dashboards. |
| `maintenance_schedule` | Planned maintenance/updates cadence. | Keeps future changes visible to collaborators. | `Quarterly sensor cleaning, annual firmware audit.` | Free text or structured schedule. | Sustained operations, reliability planning. |
| `data_retention_policy` | Statement on how long data is stored. | Addresses compliance and privacy concerns. | `Raw video 30 days, derived metrics 5 years.` | Free text; align with institutional policy. | Compliance audits, onboarding communications. |

## Usage Notes
- Treat Mandatory fields as the minimum for cross-repository interoperability.
- Recommended fields improve reuse and comparability; include when available.
- Optional fields capture additional context; promote them to higher tiers when consensus emerges.
- Submit proposals for tier changes via the documentation improvement issue template before editing this file.
