# HCMO Device-Agnostic VMG Webapp

This Node/Express + static front-end provides a lightweight workbench for producing illustrative HCMO exports and checking VMG coverage without freezing device-specific mappings.

## Highlights
- Mirrors the device-agnostic field tiers defined in [`docs/FIELD-TIERS.md`](../docs/FIELD-TIERS.md); Mandatory fields are enforced in the form.
- Embeds reminders about the non-freeze policy, ethics approvals placeholder **(O)**, and collaboration pathways for device owners.
- Generates JSON-LD using `ontology/context.jsonld`, converts it to Turtle, and runs pySHACL via the `/api/export` endpoint.
- Blueprint tab pulls tier metadata directly from `docs/FIELD-TIERS.md` and provides minimal/extended examples aligned to `docs/EXAMPLES/`.
- New regression tests (`npm test`) cover the inventory API, example presets, and ethics notice text.

## Getting Started
```bash
cd webapp
npm install
npm run dev
```
The server listens on `http://localhost:3000` and serves the UI from `public/index.html`.

## Usage
1. Enter a base IRI and required system/protocol/enclosure identifiers (all Mandatory fields are marked with the `M` tag).
2. Provide session start/end timestamps alongside the interval metadata; the form checks that the end follows the start.
3. Add at least one sensor and actuator using the repeatable controls.
4. Click **Generate & Validate** to obtain JSON-LD, Turtle, and a pySHACL report. Download individual files or the ZIP bundle.
5. Switch to the **Metadata Blueprint** tab to review Mandatory / Recommended / Optional coverage. Load the minimal or extended examples to compare against `docs/EXAMPLES/`.

## API Endpoint
- `POST /api/export`
  - Body: `{ "jsonld": <document> }`
  - Response: `{ conforms, turtle, validationReport, zipBase64, zipFilename }`

Temporary Turtle files are validated with `python -m pyshacl` against `shapes/hcm-shapes.ttl` and cleaned automatically.

## Tests
```bash
npm test
```
The Node test suite exercises the blueprint inventory endpoint, example presets, and verifies that the ethics reminder remains present in `public/index.html`.

## Sample Validation Script
```bash
cd webapp
node examples/sample-request.mjs
```
The script boots the Express app on an ephemeral port, posts the minimal mandatory payload, and prints the HTTP status plus the SHACL conformance flag.

## Maintenance Notes
- Update `docs/FIELD-TIERS.md` first; the webapp parses the Markdown directly. Re-run `npm test` after any tier changes.
- Adjust `public/app.js` if the ontology context or new tiered fields are introduced.
- Ethics approvals placeholder **(O)** appears across README, UI, and documentation—replace it when an authoritative citation becomes available.
