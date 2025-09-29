# HCMO Authoring Webapp

A minimal Node/Express + static front-end that helps hardware manufacturers author HCM data that conform to the HCMO ontology and SHACL shapes bundled in this repository.

## Features
- Guided form that mirrors the required fields enforced by `shapes/hcm-shapes.ttl`.
- Generates JSON-LD using `ontology/context.jsonld` terms directly in the browser.
- Server converts JSON-LD to Turtle, runs pySHACL, and returns:
  - JSON-LD payload ready for API ingestion.
  - Turtle serialization for ontology consumers.
  - Validation report plus both serializations bundled into a ZIP archive.
- Validation mirrors the existing PowerShell pipeline (parse ? pySHACL with RDFS inference and advanced reporting).

## Getting Started
```bash
cd webapp
npm install
npm run dev
```
The server defaults to `http://localhost:3000` and serves the static form from `public/index.html`.

## Usage
1. Choose a base IRI for the dataset (trailing `/` or `#`).
2. Fill in system, enclosure, sensor/actuator, and observation window details.
3. Add as many sensors/actuators as needed using the **Add** buttons.
4. Click **Generate & Validate**.
5. Review JSON-LD, Turtle, and the human-readable validation output. Use the download buttons to grab individual files or the bundle.

## API Endpoint
- `POST /api/export`
  - Body: `{ "jsonld": <document> }`
  - Response: `{ conforms, turtle, validationReport, zipBase64, zipFilename }`

The route writes a temporary Turtle file, runs `python -m pyshacl` with `shapes/hcm-shapes.ttl`, and packages the results. Temporary files are cleaned automatically.

## Notes
- Ensure Python with `pyshacl` and `rdflib` is available (matching the root repo requirements).
- Update `baseContext` in `public/app.js` if the ontology context evolves.
- For production, consider replacing the ad-hoc IRI derivations with a persistent identifier service and wiring authentication/authorization around the export endpoint.\n## Sample Validation Script\n\n`ash\ncd webapp\nnode examples/sample-request.mjs\n`\n\nThe script spins up the Express app on an ephemeral port, posts a minimal JSON-LD payload, and prints the HTTP status plus the SHACL conformance flag.\n