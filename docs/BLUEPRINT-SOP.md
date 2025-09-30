# HCMO Blueprint Standard Operating Procedure

## Purpose
Provide a repeatable workflow for mapping a home-cage monitoring (HCM) device export to the TEATIME-powered HCMO blueprint and reporting compatibility metrics.

## Overview
1. Collect reference materials:
   - TEATIME ontology schema (`reference/ontology/TEATIME-HCM-latest.ttl`).
   - Too Big to Lose supplemental metadata (`reference/ontology/too-big-to-lose-supplement.md`).
   - Device export schema (`reference/device/representative-device-export.yaml`).
2. Update `ontology/hcmo-blueprint.yaml` with device-specific mappings and coverage statuses.
3. Maintain the canonical field inventory (`ontology/hcmo-field-inventory.tsv`).
4. Record device-to-ontology mappings in `reference/device/device-to-ontology-mapping.csv`.
5. Refresh the checklist CSV/JSON in `docs/`.
6. Run `node tooling/score_blueprint.mjs` to compute coverage metrics.
7. Produce metadata-entry templates via `node tooling/metadata_entry_tool.mjs`.
8. Capture open issues in `docs/metadata-entry-tool-issues.md` and plan OSF deposition.

## Deliverables
- YAML blueprint with up-to-date mapping data.
- Machine-readable field inventory, mapping CSV, and coverage checklist.
- Automated scoring report and metadata-entry templates (JSON-LD and CSV).
- SOP and issue log documenting outstanding workstreams.

## Deposition Plan
- Package `ontology/`, `reference/`, `docs/`, and `tooling/` artifacts into an OSF release once stakeholder sign-off is received.
- Include README guidance referencing this SOP and checksum details.
