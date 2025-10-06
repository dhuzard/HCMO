# HCMO Ontology (Home-Cage Monitoring Ontology)

A professional, reusable ontology package for home-cage monitoring (HCMO). It models systems, animals, enclosures, behaviors, sensors/actuators, time intervals, and provisioning needs; aligns to key web standards; ships with SHACL validation, examples, queries, and a JSON-LD context for application developers.

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
- **Data quality**: Enforces practical constraints (<= 24 h window, enclosure dimensions, sensor coverage) with SHACL.
- **Developer-ready**: JSON-LD context and examples; simple upgrade path to QUDT/OM units.
- **FAIR**: Clear IRIs, metadata, governance, and publishing guidance.

## Repository Map
- `ontology/` - Core ontology Turtle files, metadata, and JSON-LD context.
- `shapes/` - SHACL shapes used to validate HCMO payloads.
- `examples/` - Sample ABox datasets demonstrating minimal and edge-case coverage.
- `queries/` - SPARQL queries for common analysis scenarios.
- `tooling/` - Validation script and Python requirements for ontology QA.
- `webapp/` - Node.js authoring and blueprint checklist application.
- `docs/` - Supporting documentation, including field tiers and alignment notes.
- `.github/` - CI workflow and issue templates.

## Prerequisites and Installation
### Ontology tooling
- Install Python 3.11 or later.
- From the repository root, install validation dependencies once: `pip install -r tooling/requirements.txt`.

### Web authoring app
- Install Node.js 20.x or later.
- Change into `webapp/` and install dependencies: `npm install`.

## Ontology validation workflow
Run the full validation loop from the repository root:

```powershell
./tooling/validate.ps1
```

The script will:
1. Ensure `pyshacl` and `rdflib` are available (and install them if missing).
2. Parse every Turtle file under `ontology/`, `shapes/`, and `examples/`, emitting `[OK] Parsed: <file>` lines.
3. Validate `examples/abox-minimal.ttl` against `shapes/hcm-shapes.ttl` with `pyshacl -f human`.

A successful run ends with `Validation passed.`. If parsing or validation fails, the script stops with `Validation failed.` and the upstream error. Troubleshooting tips:
- Confirm Python 3.11+ is on PATH and `pip install -r tooling/requirements.txt` succeeds.
- Use the `-Data` and `-Shapes` parameters to point at alternate Turtle files when developing new payloads.
- If SHACL errors persist, open the report written to the console and cross-reference the offending shapes in `shapes/hcm-shapes.ttl`.

## Web authoring app
### Launch the app
```powershell
cd webapp
npm run dev
```
The server starts on `http://localhost:3000`.

### System Export tab
- Capture system, enclosure, sensors, actuators, welfare needs, and time interval details.
- Submit the form to receive JSON-LD, Turtle, and pySHACL validation output. Three panels appear with copyable text areas plus `Download` buttons.
- The `Download ZIP Bundle` button bundles the JSON-LD, Turtle, and validation report for sharing with downstream systems.

### Blueprint tab
- `docs/FIELD-TIERS.md` supplies the tier inventory surfaced in the UI. Fields are grouped as mandatory, recommended, or optional with rationale and example values.
- The app queries `/api/blueprint/inventory` and `/api/blueprint/examples` to populate tiers and sample datasets. Select an example dataset and click **Load Example** to prefill statuses and notes.
- Update field values and statuses (`provided`, `partial`, `missing`, `unknown`) to track coverage. Summary tiles recompute weighted coverage and mandatory completion as you edit.
- Use **Clear Fields** to reset the checklist before exporting or sharing results.

## Consuming the ontology
- Import `ontology/hcm.ttl`, `ontology/hcm-align.ttl`, and `ontology/hcm-metadata.ttl` into your triple store or reasoning environment.
- Apply the JSON-LD context (`ontology/context.jsonld`) when exchanging data with web applications.
- Use `shapes/hcm-shapes.ttl` to enforce constraints during ingestion pipelines or data QA. The shapes expect the same structure the webapp produces.
- Explore the SPARQL queries in `queries/` (for example `cq-systems-24h-limited.rq`) to answer common competency questions about systems, intervals, and welfare coverage.

## Example data
- `examples/abox-minimal.ttl` - A conformant payload matching the mandatory field coverage described in the blueprint.
- `examples/abox-edge-cases.ttl` - Intentionally invalid scenarios (missing sensors, short intervals, etc.) to exercise SHACL failure paths.
Adapt either file by copying it into a working directory and editing IDs, labels, and measurements while keeping the ontology structure intact.

## Tooling scripts
Currently available:
- `tooling/validate.ps1` - orchestrates Turtle parsing and pySHACL validation (see above).
- `tooling/requirements.txt` - pinned dependencies for validation tooling.

The blueprint TODO (below) tracks planned additions such as a checklist scoring helper and metadata entry CLI; those scripts are not yet implemented.

## Testing
Inside `webapp/`, run the front-end API and UI tests:
```powershell
npm test
```
This exercises the blueprint inventory endpoints and UI guardrails. Run the suite before submitting changes to the form logic, API handlers, or blueprint resources.

## Contribution and support
- Open issues or feature requests through GitHub Issues; use the templates in `.github/ISSUE_TEMPLATE/` when applicable.
- Follow the existing coding style (ES modules in the webapp, Turtle/JSON-LD formatting in ontology assets) and document non-obvious changes inline or in `docs/`.
- Reference semantic version information from `ontology/hcm-metadata.ttl` (current version IRI `https://w3id.org/hcmo/ontology/hcm/1.0.0`) when publishing derived packages.
- For security or data governance concerns, contact the maintainers via the repository issue tracker before disclosing sensitive details.

## Quickstart
1. Install validation tooling and webapp dependencies (see prerequisites above).
2. Run `./tooling/validate.ps1` to confirm ontology and example integrity.
3. Launch the webapp with `npm run dev` and generate a sample export.
4. Import `ontology/hcm.ttl` plus `examples/abox-minimal.ttl` into your triple store and test the queries in `queries/`.

## Ontology blueprint TODO

- Audit existing repo assets (`README`, `docs/`, `schemas/`, `scripts/`) for existing TEATIME/HCM coverage and identify reuse or gaps.
- Add an updated YAML representation of the ontology blueprint under `ontology/` for downstream tooling.
- Collect the latest TEATIME HCM ontology schema and Bains et al. *"Too Big to Lose"* metadata definitions in `reference/ontology/`.
- Gather the representative device's metadata/export specifications (field names, types, units, sampling cadence) in `reference/device/`.
- Design a canonical ontology-field inventory spanning subjects, environment, hardware, software, and outputs as a repo-consumable artifact.
- Map device fields to ontology terms, capturing matches, transforms, gaps, and source notes for stakeholder review.
- Implement a checklist scaffold (spreadsheet in `docs/` plus machine-readable export) tracking check / warning / fail coverage and rationale.
- Prototype an automated scoring routine summarizing coverage by domain and overall alignment using sample metadata.
- Draft a stakeholder memo summarizing ambiguous mappings, open questions, and proposed device-specific extensions.
- Record outcomes of the stakeholder feedback loop and propagate approved adjustments into the mapping artifacts.
- Finalize blueprint deliverables (checklist, README/SOP, reproducible mapping workflow) and plan OSF or similar deposition.
- Capture beta metadata-entry tool requirements (inputs, validation, JSON-LD/CSV export) and log follow-up implementation issues.

### Completed

- Classify each ontology field as Mandatory, Recommended, or Optional with supporting evidence (`docs/FIELD-TIERS.md`).

**Blueprint assets**  
- YAML blueprint: `ontology/hcm-blueprint.yaml`  
- Field inventory: `ontology/hcm-field-inventory.tsv`  
- Device export spec: `reference/device/representative-device-export.yaml`  
- Device mapping log: `reference/device/device-to-ontology-mapping.csv`  
- Coverage checklist: `docs/hcm-blueprint-checklist.csv` and `docs/hcm-blueprint-checklist.json`  
- Scoring script: `node tooling/score_blueprint.mjs [checklist]`  
- Metadata-entry tool: `node tooling/metadata_entry_tool.mjs --format jsonld|csv --out <file>`  
- SOP and issue log: `docs/BLUEPRINT-SOP.md`, `docs/metadata-entry-tool-issues.md`

## Namespaces and IRIs
- Base ontology IRI: `https://w3id.org/hcmo/ontology/hcm`
- Version IRI: `https://w3id.org/hcmo/ontology/hcm/1.0.0`
- Prefixes used: `hcm`, `sosa`, `ssn`, `time`, `prov`, `dcterms`, `qudt`, `unit`, `om`, `schema`, `bfo`

See alignments in `docs/ALIGNMENTS.md`.

## What's in the ontology

**Core classes (selected)**  
- `hcm:System` - HCM system composed of enclosure, hardware, software; hosts sensors and actuators.  
- `hcm:Animal` - Experimental animal.  
- `hcm:Enclosure` subset of `hcm:PhysicalSpace` - Housing environment; has `hcm:Dimensions`.  
- `hcm:BehaviorAndPhysiology` - Observed process; has `hcm:CircadianRhythm`; observed over `hcm:TimeInterval`.  
- `hcm:Sensor`, `hcm:Actuator`, `hcm:Hardware`, `hcm:Software`, `hcm:Supplier`.  
- `hcm:NeedsSequence`, `hcm:LimitedInteractionWithHumans`, `hcm:Dimensions`, `hcm:TimeInterval`.  

**Key object properties**  
- System composition: `hcm:hasEnclosure`, `hcm:hasHardware`, `hcm:hasSoftware`, `hcm:hasSensor`, `hcm:hasActuator`, `hcm:producedBy`, `hcm:collectsInfoOn`.  
- Animal, enclosure, needs: `hcm:livesIn`, `hcm:provides`, `hcm:requiresToThrive`.  
- Behavior context: `hcm:isDisplayedInside`, `hcm:hasCircadianRhythm`, `hcm:extendsEnoughToCapture`.  
- Sensing and actuation: `hcm:captures`, `hcm:elicits`.  
- Space and geometry: `hcm:hasDimensions`.  

**Key datatype properties**  
- Dimensions: `hcm:width`, `hcm:length`, `hcm:height`, `hcm:unit`.  
- Time: `hcm:durationHours`, `hcm:isExtendable`.  
- Needs (booleans): `hcm:hasFood`, `hcm:hasWater`, `hcm:hasSocialContacts`, `hcm:hasSafetyFromThreat`, `hcm:hasEnvironmentalEnrichment`.  

**Selected OWL axioms**  
- Disjointness: `hcm:Sensor` disjoint `hcm:Actuator`, `hcm:Hardware` disjoint `hcm:Software`.  
- Restrictions: `hcm:System` has exactly one `hcm:hasEnclosure`, at least one `hcm:hasSensor`.  

## Standards alignment

- SOSA/SSN: `hcm:Sensor` subset of `sosa:Sensor`, `hcm:Actuator` subset of `sosa:Actuator`, `hcm:System` subset of `sosa:Platform`, `hcm:hasSensor` subset of `sosa:hosts`.  
- OWL-Time: `hcm:TimeInterval` subset of `time:TemporalEntity`.  
- PROV/Agents: `hcm:producedBy` subset of `prov:wasAttributedTo`; `hcm:Supplier` subset of `prov:Agent` and `schema:Organization`.  
- BFO: `hcm:BehaviorAndPhysiology` subset of `bfo:0000015` (process).  

Details and rationale are documented in `docs/ALIGNMENTS.md`.

## SHACL validation

Shapes in `shapes/hcm-shapes.ttl` check:  
- System: exactly one enclosure, at least one sensor.  
- Behavior: must link to an enclosure and a time interval.  
- Time interval: `durationHours` <= 24, `isExtendable` boolean, explicit `LimitedInteractionWithHumans`.  
- Enclosure: must have a dimensions record.  
- Dimensions: width, length, height > 0; unit present.  

Run locally (PowerShell):  
```powershell
./tooling/validate.ps1
```
