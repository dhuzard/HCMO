# HCMO Blueprint Field Tiers

This inventory enumerates the fields used by the HCMO authoring form and classifies each as Mandatory, Recommended, or Optional. The tiers align with the UI markers and the generated SHACL validation reports.

## Mandatory Fields

| Field | Description | Rationale | Example Value | Validation Notes | Downstream Utility |
| --- | --- | --- | --- | --- | --- |
| Base IRI | Canonical base IRI used to mint all resource identifiers. | Required to generate stable, dereferenceable IRIs in exports. | https://mfg.example.com/hcm/id/ | Must end with `/` or `#`; validated prior to export. | Enables consistent joins across datasets and triples. |
| System ID | Identifier for the monitored system instance. | Ensures the system platform is uniquely addressable. | hcmo-system-001 | Must be non-empty string. | Links sensors, actuators, and intervals back to the platform. |
| Hardware ID | Identifier for the core hardware assembly. | Required to represent physical hardware in the ontology. | HW_01 | Non-empty string; used as fragment on Base IRI. | Supports provenance and hardware-level maintenance tracking. |
| Software ID | Identifier for the orchestration software. | Needed to track software agents involved in data capture. | SW_01 | Non-empty string. | Enables provenance assertions about software components. |
| Supplier ID | Identifier for the equipment supplier or integrator. | Mandatory to attribute the system to a supplier. | SupplierAcme | Non-empty string. | Supports procurement, compliance, and contact workflows. |
| Protocol ID | Identifier for the experimental or operational protocol followed. | Required to connect system activity to a protocol definition. | protocol-2025-09 | Non-empty string. | Enables linking to study protocols and SOP repositories. |
| Enclosure ID | Identifier for the housing enclosure. | Mandatory to describe the physical environment. | enclosure-12A | Non-empty string. | Enables enclosure-level welfare and capacity reporting. |
| Width (cm) | Interior enclosure width in centimeters. | Required to validate spatial sufficiency. | 60 | Numeric; must be > 0. | Drives enclosure capacity calculations and welfare checks. |
| Length (cm) | Interior enclosure length in centimeters. | Required to validate spatial sufficiency. | 90 | Numeric; must be > 0. | Supports welfare scoring and footprint planning. |
| Height (cm) | Interior enclosure height in centimeters. | Required to validate spatial sufficiency. | 50 | Numeric; must be > 0. | Enables volumetric reasoning and enrichment placement. |
| Unit | Unit of measure for enclosure dimensions. | Needed so width/length/height values are interpretable. | cm | Must match recognised units (e.g., cm, in). | Facilitates automated unit conversions. |
| Animal ID | Identifier for the focal animal or cohort. | Mandatory to associate observations with animals. | animal-42 | Non-empty string. | Anchors behavioural observations to a subject. |
| Behavior ID | Identifier for the observed behaviour or physiological process. | Required for behaviour-to-ontology mapping. | behaviour-activity | Non-empty string. | Enables downstream behaviour analytics and tagging. |
| Session Start | Timestamp for the beginning of the observation interval. | Needed to define temporal coverage. | 2025-09-12T08:00 | Must precede Session End; converted to xsd:dateTime. | Supports time-based joins and auditing. |
| Session End | Timestamp for the end of the observation interval. | Needed to define temporal coverage. | 2025-09-13T08:00 | Must follow Session Start; converted to xsd:dateTime. | Enables duration calculations and shift planning. |
| Interval ID | Identifier for the explicit time interval resource. | Mandatory to model the interval as a distinct node. | interval-001 | Non-empty string. | Links behaviours, sessions, and outputs temporally. |
| Duration (hours) | Duration of the session in hours. | Required for SHACL constraints; ensures 24h maximum. | 24 | Numeric; must be <= 24. | Supports SLA reporting and throughput metrics. |
| Extendable Flag | Boolean indicating whether the session can be extended. | Mandatory to capture limited interaction policy. | true | Must be true/false value. | Informs welfare and staffing decisions. |
| Sensor Inventory | At least one sensor entry with identifier and label. | Required to satisfy SHACL `hcm:hasSensor` constraint. | IR_Sensor_1 | At least one sensor ID must be present. | Enables mapping of sensed signals to ontology nodes. |
| Actuator Inventory | At least one actuator entry with identifier and label. | Required to represent actuators in the system. | Feeder_1 | At least one actuator ID must be present. | Supports intervention tracing and automation planning. |

## Recommended Fields

| Field | Description | Rationale | Example Value | Validation Notes | Downstream Utility |
| --- | --- | --- | --- | --- | --- |
| System Label | Human-readable label for the system. | Aids operators and reviewers. | System A (rack 3, cage 12) | Optional free text. | Improves dashboards and audit logs. |
| Software Label | Human-readable label for the software component. | Clarifies software responsibilities. | Telemetry service | Optional free text. | Supports support triage and documentation. |
| Protocol Label | Human-readable protocol name. | Provides context beyond the protocol ID. | Baseline acclimation | Optional free text. | Helps stakeholders interpret mappings. |
| Enclosure Label | Human-readable label for the enclosure. | Eases communication across teams. | Home cage pod 12A | Optional free text. | Useful for facilities management. |
| Animal Label | Display label for the animal or cohort. | Improves interpretability of reports. | C57BL/6J cohort 7 | Optional free text. | Supports animal care coordination. |
| Behavior Label | Descriptive label for the behaviour. | Clarifies what the behaviour ID encodes. | Locomotion activity | Optional free text. | Helps analysts and annotators. |
| Circadian Label | Note on circadian rhythm alignment. | Captures phase (light/dark) context. | Lights-off cycle | Optional free text. | Guides interpretation of behaviour changes. |
| Interval Label | Human-readable label for the interval. | Provides quick reference for scheduling. | Day 1 observation window | Optional free text. | Aids scheduling and compliance reporting. |
| Operator Contact | Shared mailbox or operator contact. | Ensures downstream teams can reach the owner. | hcmo-operations@example.org | Valid email format recommended. | Supports incident escalation and collaboration. |
| Limited Interaction Label | Description for the limited interaction policy. | Documents how human interaction is minimised. | Minimal human contact | Optional free text. | Useful for ethics reviews and SOP traceability. |
| Data Product Links | URLs for derived artefacts or datasets. | Encourages linking exported data products. | https://example.org/datasets/hcmo-system-001/day-01.csv | Provide one URL per line. | Simplifies downstream ingestion and QC. |

## Optional Fields

| Field | Description | Rationale | Example Value | Validation Notes | Downstream Utility |
| --- | --- | --- | --- | --- | --- |
| Ingestion Timestamp | Timestamp when the export was ingested. | Useful for pipeline bookkeeping. | 2025-09-13T09:15 | Optional ISO 8601 timestamp. | Supports backfill detection and auditing. |
| Hardware Label | Human-readable label for the hardware. | Helps identify hardware components quickly. | Control board | Optional free text. | Useful for inventory management. |
| Supplier Label | Display label for the supplier organisation. | Provides friendlier context in reports. | Acme supply partners | Optional free text. | Supports procurement coordination. |
| Welfare Needs Notes | Notes on welfare needs beyond boolean checkboxes. | Captures nuances of enrichment and care. | Additional chew toys rotated weekly. | Optional narrative. | Supports welfare committee reviews. |
| Additional Sensors Notes | Notes about sensor configurations or calibration. | Records context not captured by IDs alone. | IR sensors calibrated weekly. | Optional narrative. | Helps QA and device specialists. |
