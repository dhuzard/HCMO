# HCMO Ontology (Home-Cage Monitoring Ontology)

A professional, reusable ontology package for home-cage monitoring (HCMO). It models systems, animals, enclosures, behaviors, sensors/actuators, time intervals, and provisioning needs; aligns to key web standards; ships with SHACL validation, examples, queries, CI, and a JSON-LD context for application developers.

- Ontology core: `ontology/hcm.ttl`
- Standards alignment: `ontology/hcm-align.ttl`
- Ontology metadata and imports: `ontology/hcm-metadata.ttl`
- SHACL shapes: `shapes/hcm-shapes.ttl`
- Examples (ABox): `examples/`
- SPARQL queries: `queries/`
- JSON-LD context: `ontology/context.jsonld`
- Validation script and CI: `tooling/validate.ps1`, `.github/workflows/validate.yml`
- Web-based authoring app: `webapp/`

## Why HCMO?
- **Interoperability**: Aligns with SOSA/SSN (sensing/actuation), OWL-Time, PROV, and BFO.
- **Data quality**: Enforces practical constraints (≥24h window, enclosure dimensions, etc.) with SHACL.
- **Developer-ready**: JSON-LD context and examples; simple upgrade path to QUDT/OM units.
- **FAIR**: Clear IRIs, metadata, governance, and publishing guidance.

## Web Authoring App

The web UI packaged in `webapp/` doubles as an authoring tool and a blueprint-driven checklist for mapping device exports to HCMO.

### Author HCMO payloads
- Requires Node.js 20.x or later (ESM + tooling compatibility).
- Install once: `cd webapp && npm install`
- Start locally: `npm run dev` (serves http://localhost:3000)
- Use the guided form to capture system, enclosure, sensors, actuators, interval, and welfare needs; it mirrors the SHACL shapes in `shapes/hcm-shapes.ttl`.
- Press **Generate & Validate** to produce JSON-LD and Turtle output while running the same pySHACL validation as `tooling/validate.ps1`.
- Download individual serializations or the bundled ZIP for downstream ingestion.
- Field markers in the form align with the blueprint classification (mandatory / recommended / optional) surfaced in the checklist tab.
- Optional CLI check: `node examples/sample-request.mjs` posts the sample payload and prints the SHACL result.

### Mapping checklist workflow
- Switch to the **Metadata Blueprint Coverage** tab to load the master field inventory from `ontology/hcm-field-inventory.tsv`, grouped by blueprint domain.
- Each field exposes its blueprint designation and a status selector (`provided`, `partial`, `missing`, `unknown`) so you can track how well a device export satisfies the TEATIME requirements; add notes to capture transformations, owners, or next steps.
- The summary cards recalculate overall weighted coverage and mandatory completion as you work, matching the metrics reported in `docs/hcm-blueprint-checklist.*` and the scoring helper in `tooling/score_blueprint.mjs`.
- Use the example dropdown to preload mappings derived from `reference/device/device-to-ontology-mapping.csv`; tweak them to build a device-specific checklist, or reset the panel to start from scratch before sharing the results with stakeholders.

## Quickstart

1. **Install validation tooling**
   - Python 3.11+ and `pip`
   - Install dependencies: `pip install -r tooling/requirements.txt`

2. **Validate the minimal example**
   - PowerShell: `./tooling/validate.ps1`
   - Parses all TTL files and validates `examples/abox-minimal.ttl` against `shapes/hcm-shapes.ttl`.

3. **Try the queries**
   - Load `ontology/hcm-metadata.ttl` and `examples/abox-minimal.ttl` into your triple store (e.g., Jena/Fuseki, GraphDB).
   - Run queries from `queries/` (e.g., `cq-systems-24h-limited.rq`).

## Ontology Blueprint TODO

- Audit existing repo assets (`README`, `docs/`, `schemas/`, `scripts/`) for existing TEATIME/HCM coverage and identify reuse or gaps.
- Add an updated YAML representation of the ontology blueprint under `ontology/` for downstream tooling.
- Collect the latest TEATIME HCM ontology schema and Bains et al. *“Too Big to Lose”* metadata definitions in `reference/ontology/`.
- Gather the representative device’s metadata/export specifications (field names, types, units, sampling cadence) in `reference/device/`.
- Design a canonical ontology-field inventory spanning subjects, environment, hardware, software, and outputs as a repo-consumable artifact.
- Map device fields to ontology terms, capturing matches, transforms, gaps, and source notes for stakeholder review.
- Classify each ontology field as Mandatory, Recommended, or Optional with supporting evidence.
- Implement a checklist scaffold (spreadsheet in `docs/` plus machine-readable export) tracking ✔️ / ⚠️ / ❌ coverage and rationale.
- Prototype an automated scoring routine summarizing coverage by domain and overall alignment using sample metadata.
- Draft a stakeholder memo summarizing ambiguous mappings, open questions, and proposed device-specific extensions.
- Record outcomes of the stakeholder feedback loop and propagate approved adjustments into the mapping artifacts.
- Finalize blueprint deliverables (checklist, README/SOP, reproducible mapping workflow) and plan OSF or similar deposition.
- Capture beta metadata-entry tool requirements (inputs, validation, JSON-LD/CSV export) and log follow-up implementation issues.

**Blueprint Assets**  
- YAML blueprint: `ontology/hcm-blueprint.yaml`  
- Field inventory: `ontology/hcm-field-inventory.tsv`  
- Device export spec: `reference/device/representative-device-export.yaml`  
- Device mapping log: `reference/device/device-to-ontology-mapping.csv`  
- Coverage checklist: `docs/hcm-blueprint-checklist.csv` and `docs/hcm-blueprint-checklist.json`  
- Scoring script: `node tooling/score_blueprint.mjs [checklist]`  
- Metadata-entry tool: `node tooling/metadata_entry_tool.mjs --format jsonld|csv --out <file>`  
- SOP & issue log: `docs/BLUEPRINT-SOP.md`, `docs/metadata-entry-tool-issues.md`

## Namespaces and IRIs
- Base ontology IRI: `https://w3id.org/hcmo/ontology/hcm`
- Version IRI: `https://w3id.org/hcmo/ontology/hcm/1.0.0`
- Prefixes used: `hcm`, `sosa`, `ssn`, `time`, `prov`, `dcterms`, `qudt`, `unit`, `om`, `schema`, `bfo`

See alignments in `docs/ALIGNMENTS.md`.

## What’s in the Ontology

**Core classes (selected)**  
- `hcm:System` – HCM system composed of enclosure, hardware, software; hosts sensors/actuators.  
- `hcm:Animal` – Experimental animal.  
- `hcm:Enclosure` ⊑ `hcm:PhysicalSpace` – Housing environment; has `hcm:Dimensions`.  
- `hcm:BehaviorAndPhysiology` – Observed process; has `hcm:CircadianRhythm`; observed over `hcm:TimeInterval`.  
- `hcm:Sensor`, `hcm:Actuator`, `hcm:Hardware`, `hcm:Software`, `hcm:Supplier`.  
- `hcm:NeedsSequence`, `hcm:LimitedInteractionWithHumans`, `hcm:Dimensions`, `hcm:TimeInterval`.  

**Key object properties**  
- System composition: `hcm:hasEnclosure`, `hcm:hasHardware`, `hcm:hasSoftware`, `hcm:hasSensor`, `hcm:hasActuator`, `hcm:producedBy`, `hcm:collectsInfoOn`.  
- Animal ↔ Enclosure ↔ Needs: `hcm:livesIn`, `hcm:provides`, `hcm:requiresToThrive`.  
- Behavior context: `hcm:isDisplayedInside`, `hcm:hasCircadianRhythm`, `hcm:extendsEnoughToCapture`.  
- Sensing/Actuation: `hcm:captures`, `hcm:elicits`.  
- Space/Geometry: `hcm:hasDimensions`.  

**Key datatype properties**  
- Dimensions: `hcm:width`, `hcm:length`, `hcm:height`, `hcm:unit`.  
- Time: `hcm:durationHours`, `hcm:isExtendable`.  
- Needs (simple booleans): `hcm:hasFood`, `hcm:hasWater`, `hcm:hasSocialContacts`, `hcm:hasSafetyFromThreat`, `hcm:hasEnvironmentalEnrichment`.  

**Selected OWL axioms**  
- Disjointness: `hcm:Sensor ⊓ hcm:Actuator ⊑ ⊥`, `hcm:Hardware ⊓ hcm:Software ⊑ ⊥`.  
- Restrictions: `hcm:System` has exactly 1 `hcm:hasEnclosure`, at least 1 `hcm:hasSensor`.  

## Standards Alignment

- SOSA/SSN: `hcm:Sensor` ⊑ `sosa:Sensor`, `hcm:Actuator` ⊑ `sosa:Actuator`, `hcm:System` ⊑ `sosa:Platform`, `hcm:hasSensor` ⊑ `sosa:hosts`.  
- OWL-Time: `hcm:TimeInterval` ⊑ `time:TemporalEntity`.  
- PROV/Agents: `hcm:producedBy` ⊑ `prov:wasAttributedTo`; `hcm:Supplier` ⊑ `prov:Agent`, `schema:Organization`.  
- BFO: `hcm:BehaviorAndPhysiology` ⊑ `bfo:0000015` (process).  

Details and rationale in `docs/ALIGNMENTS.md`.

## SHACL Validation

Shapes in `shapes/hcm-shapes.ttl` check:  
- System: exactly one enclosure; at least one sensor.  
- Behavior: must link to an enclosure and a time interval.  
- Time interval: `durationHours` ≥ 24, `isExtendable` boolean, and explicit `LimitedInteractionWithHumans`.  
- Enclosure: must have a dimensions record.  
- Dimensions: width/length/height > 0; unit present.  

Run locally (PowerShell):  
```powershell
./tooling/validate.ps1
