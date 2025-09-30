# HCMO Ontology (Home‑Cage Monitoring Ontology)

A professional, reusable ontology package for home‑cage monitoring (HCMO). It models systems, animals, enclosures, behaviors, sensors/actuators, time intervals, and provisioning needs; aligns to key web standards; ships with SHACL validation, examples, queries, CI, and a JSON‑LD context for application developers.

- Ontology core: `ontology/hcm.ttl`
- Standards alignment: `ontology/hcm-align.ttl`
- Ontology metadata and imports: `ontology/hcm-metadata.ttl`
- SHACL shapes: `shapes/hcm-shapes.ttl`
- Examples (ABox): `examples/`
- SPARQL queries: `queries/`
- JSON‑LD context: `ontology/context.jsonld`
- Validation script and CI: `tooling/validate.ps1`, `.github/workflows/validate.yml`
- Web-based authoring app: `webapp/`

## Why HCMO?
- Interoperability: Aligns with SOSA/SSN (sensing/actuation), OWL‑Time, PROV, and BFO.
- Data quality: Enforces practical constraints (≥24h window, enclosure dimensions, etc.) with SHACL.
- Developer‑ready: JSON‑LD context and examples; simple upgrade path to QUDT/OM units.
- FAIR: Clear IRIs, metadata, governance, and publishing guidance.

## Web Authoring App

- Install once: `cd webapp && npm install`
- Start locally: `npm run dev` (serves http://localhost:3000)
- Fill the form (base IRI, system/enclosure/sensor/actuator/time interval) and press **Generate & Validate**
- Download JSON-LD, Turtle, or the ZIP bundle; validation mirrors `tooling/validate.ps1`
- Optional CLI check: `node examples/sample-request.mjs` posts the sample payload and prints the SHACL result

## Quickstart

1) Install validation tooling
- Python 3.11+ and `pip`
- Install dependencies: `pip install -r tooling/requirements.txt`

2) Validate the minimal example
- PowerShell: `./tooling/validate.ps1`
  - Parses all TTL files and validates `examples/abox-minimal.ttl` against `shapes/hcm-shapes.ttl`.

3) Try the queries
- Load `ontology/hcm-metadata.ttl` and `examples/abox-minimal.ttl` into your triple store (e.g., Jena/Fuseki, GraphDB).
- Run queries from `queries/` (e.g., `cq-systems-24h-limited.rq`).

## Ontology Blueprint TODO

- Audit existing repo assets (`README`, `docs/`, `schemas/`, `scripts/`) for existing TEATIME/HCM coverage and identify reuse or gaps.
- Add an updated YAML representation of the ontology blueprint under `ontology/` for downstream tooling.
- Collect the latest TEATIME HCM ontology schema and Bains et al. “Too Big to Lose” metadata definitions in `reference/ontology/`.
- Gather the representative device’s metadata/export specifications (field names, types, units, sampling cadence) in `reference/device/`.
- Design a canonical ontology-field inventory spanning subjects, environment, hardware, software, and outputs as a repo-consumable artifact.
- Map device fields to ontology terms, capturing matches, transforms, gaps, and source notes for stakeholder review.
- Classify each ontology field as Mandatory, Recommended, or Optional with supporting evidence.
- Implement a checklist scaffold (spreadsheet in `docs/` plus machine-readable export) tracking ✔️/⚠️/❌ coverage and rationale.
- Prototype an automated scoring routine summarizing coverage by domain and overall alignment using sample metadata.
- Draft a stakeholder memo summarizing ambiguous mappings, open questions, and proposed device-specific extensions.
- Record outcomes of the stakeholder feedback loop and propagate approved adjustments into the mapping artifacts.
- Finalize blueprint deliverables (checklist, README/SOP, reproducible mapping workflow) and plan OSF or similar deposition.
- Capture beta metadata-entry tool requirements (inputs, validation, JSON-LD/CSV export) and log follow-up implementation issues.

**Blueprint Assets**
- YAML blueprint: `ontology/hcmo-blueprint.yaml`
- Field inventory: `ontology/hcmo-field-inventory.tsv`
- Device export spec: `reference/device/representative-device-export.yaml`
- Device mapping log: `reference/device/device-to-ontology-mapping.csv`
- Coverage checklist: `docs/hcmo-blueprint-checklist.csv` and `docs/hcmo-blueprint-checklist.json`
- Scoring script: `node tooling/score_blueprint.mjs [checklist]`
- Metadata-entry tool: `node tooling/metadata_entry_tool.mjs --format jsonld|csv --out <file>`
- SOP & issue log: `docs/BLUEPRINT-SOP.md`, `docs/metadata-entry-tool-issues.md`

## Namespaces and IRIs
- Base ontology IRI: `https://w3id.org/hcmo/ontology/hcm`
- Version IRI: `https://w3id.org/hcmo/ontology/hcm/1.0.0`
- Prefixes used: `hcm`, `sosa`, `ssn`, `time`, `prov`, `dcterms`, `qudt`, `unit`, `om`, `schema`, `bfo`

See alignments in `docs/ALIGNMENTS.md`.

## What’s in the Ontology

Core classes (selected)
- `hcm:System` – HCM system composed of enclosure, hardware, software; hosts sensors/actuators.
- `hcm:Animal` – Experimental animal.
- `hcm:Enclosure` ⊑ `hcm:PhysicalSpace` – Housing environment; has `hcm:Dimensions`.
- `hcm:BehaviorAndPhysiology` – Observed process; has `hcm:CircadianRhythm`; observed over `hcm:TimeInterval`.
- `hcm:Sensor`, `hcm:Actuator`, `hcm:Hardware`, `hcm:Software`, `hcm:Supplier`.
- `hcm:NeedsSequence`, `hcm:LimitedInteractionWithHumans`, `hcm:Dimensions`, `hcm:TimeInterval`.

Key object properties
- System composition: `hcm:hasEnclosure`, `hcm:hasHardware`, `hcm:hasSoftware`, `hcm:hasSensor`, `hcm:hasActuator`, `hcm:producedBy`, `hcm:collectsInfoOn`.
- Animal ↔ Enclosure ↔ Needs: `hcm:livesIn`, `hcm:provides`, `hcm:requiresToThrive`.
- Behavior context: `hcm:isDisplayedInside`, `hcm:hasCircadianRhythm`, `hcm:extendsEnoughToCapture`.
- Sensing/Actuation: `hcm:captures`, `hcm:elicits`.
- Space/Geometry: `hcm:hasDimensions`.

Key datatype properties
- Dimensions: `hcm:width`, `hcm:length`, `hcm:height`, `hcm:unit`.
- Time: `hcm:durationHours`, `hcm:isExtendable`.
- Needs (simple booleans): `hcm:hasFood`, `hcm:hasWater`, `hcm:hasSocialContacts`, `hcm:hasSafetyFromThreat`, `hcm:hasEnvironmentalEnrichment`.

Selected OWL axioms
- Disjointness: `hcm:Sensor ⟂ hcm:Actuator`, `hcm:Hardware ⟂ hcm:Software`.
- Restrictions: `hcm:System` has exactly 1 `hcm:hasEnclosure`, at least 1 `hcm:hasSensor`.

## Standards Alignment

- SOSA/SSN: `hcm:Sensor` ⊑ `sosa:Sensor`, `hcm:Actuator` ⊑ `sosa:Actuator`, `hcm:System` ⊑ `sosa:Platform`, `hcm:hasSensor` ⊑ `sosa:hosts`.
- OWL‑Time: `hcm:TimeInterval` ⊑ `time:TemporalEntity`.
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

Run locally (PowerShell)
- `./tooling/validate.ps1`

Run in CI
- GitHub Action in `.github/workflows/validate.yml` parses TTL and runs pySHACL.

## Examples

Minimal instance
- `examples/abox-minimal.ttl` covers one system with sensors/actuators, one animal, an enclosure with dimensions, a 24h interval, and limited human interaction.

Edge cases (expected SHACL failures)
- `examples/abox-edge-cases.ttl` includes: system without sensors, time interval < 24h, enclosure without dimensions, behavior missing enclosure, negative height.

## Queries (Competency Questions)

The `queries/` directory provides SPARQL for common questions.

- 24h + limited interaction
  - `queries/cq-systems-24h-limited.rq` – find systems where behaviors use a time interval ≥ 24h and limited human interaction.
- Animals by enclosure/system
  - `queries/cq-animals-by-enclosure.rq`
- Missing dimensions
  - `queries/cq-missing-dimensions.rq`
- Sensors and behaviors they capture
  - `queries/cq-sensors-behaviors.rq`
- Needs provisioning gaps
  - `queries/cq-needs-provisioning.rq`

Example: run with Apache Jena `arq`
- `arq --data=ontology/hcm.ttl --data=examples/abox-minimal.ttl --query=queries/cq-systems-24h-limited.rq`

## JSON‑LD for Developers

A compact JSON‑LD context is provided at `ontology/context.jsonld`. Example payload:

```
{
  "@context": "https://w3id.org/hcmo/ontology/context.jsonld",
  "@id": "https://example.org/id/System_A",
  "@type": "System",
  "hasEnclosure": { "@id": "https://example.org/id/Enc_01" },
  "hasSensor": [ { "@id": "https://example.org/id/IR_Sensor_1" } ],
  "hasActuator": [ { "@id": "https://example.org/id/Feeder_1" } ],
  "collectsInfoOn": { "@id": "https://example.org/id/Mouse_1" }
}
```

## Programmatic Usage (Python/RDFLib + pySHACL)

```
from rdflib import Graph
from pyshacl import validate

# Load ontology + shapes + data
ont = Graph().parse('ontology/hcm.ttl', format='turtle')
ali = Graph().parse('ontology/hcm-align.ttl', format='turtle')
meta = Graph().parse('ontology/hcm-metadata.ttl', format='turtle')
sh  = Graph().parse('shapes/hcm-shapes.ttl', format='turtle')
abox= Graph().parse('examples/abox-minimal.ttl', format='turtle')

data = ont + ali + meta + abox

conforms, report_graph, report_text = validate(
    data_graph=data,
    shacl_graph=sh,
    inference='rdfs',
    abort_on_error=False,
    meta_shacl=False,
    advanced=True
)
print('Conforms:', conforms)
print(report_text)
```

## Typical Use Cases

- Benchmark an HCM system design
  - Model systems, enclosures, sensors, actuators; validate cardinalities and constraints.
- Long‑run behavior studies
  - Assert ≥24h intervals with limited human interaction; query which systems comply.
- Facility inventory and QA
  - Ensure all enclosures have dimension records; find missing or invalid data.
- Protocol comparison
  - Compare needs provisioning across enclosures; identify gaps or differences.
- Pipeline integration (LIMS/ELN)
  - Use JSON‑LD context to serialize system/animal metadata from applications.

## Extending the Model

- Units (QUDT/OM)
  - Replace simple dimension datatypes with `qudt:QuantityValue` and `qudt:unit` (e.g., `unit:CentiM`). See `docs/ALIGNMENTS.md` for the pattern.
- Observations (SOSA)
  - Introduce `sosa:Observation` to capture measurement semantics; link to `hcm:BehaviorAndPhysiology` and features of interest (animals).
- N‑ary composition events
  - Reify `System` composition as an event with roles if component‑level provenance is needed.

## Governance and Versioning

- Version: `1.0.0` (see `docs/CHANGELOG.md`).
- Deprecation: mark terms with `owl:deprecated true` and point to replacements.
- Licensing: CC BY 4.0 (see `LICENSE`).
- Contributions: open issues/PRs for new terms, alignments, or shapes.

## Publishing

- Reserve `w3id` at `https://w3id.org/hcmo` and redirect to your published ontology and docs.
- Distribute: `ontology/hcm.ttl`, `ontology/hcm-align.ttl`, `ontology/hcm-metadata.ttl`, `ontology/context.jsonld`.
- Optional: register in LOV/BioPortal when scope stabilizes.

## References

- SOSA/SSN: `http://www.w3.org/ns/sosa/`, `http://www.w3.org/ns/ssn/`
- OWL‑Time: `http://www.w3.org/2006/time#`
- PROV: `http://www.w3.org/ns/prov#`
- QUDT: `http://qudt.org/schema/qudt/`, Units: `http://qudt.org/vocab/unit/`
- BFO: `http://purl.obolibrary.org/obo/BFO_`

---

For implementation details and design rationale, see `docs/MODEL.md` and `docs/ALIGNMENTS.md`.
