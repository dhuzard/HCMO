# HCMO documentation

The Home-Cage Monitoring Ontology (HCMO) models monitored enclosures,
animal-to-enclosure housing assignments, biological subjects and groups,
environmental profiles, observations and results, sensors, actuators, software,
and time-series data.

- Ontology IRI: `https://w3id.org/hcmo/ontology/hcm`
- Base namespace: `https://w3id.org/hcmo/ontology/hcm#`
- Version IRI: `https://w3id.org/hcmo/ontology/hcm/0.2.0`
- Standards: BFO/IAO upper anchors, SOSA/SSN observations and devices, and
  OWL-Time temporal entities
- Validation: `python tooling/build.py` followed by `python tooling/validate.py`
- ISA integration note: [`ISA-RO-CRATE-MAPPING.md`](ISA-RO-CRATE-MAPPING.md)
- A02 ISA/STATO compatibility and future-work record:
  [`A02-ISA-STATO-COMPATIBILITY.md`](A02-ISA-STATO-COMPATIBILITY.md)
- Philippe Rocca-Serra meeting record:
  [`meetings/PHILIPPE-ROCCA-SERRA-HCMO-NOTES.md`](meetings/PHILIPPE-ROCCA-SERRA-HCMO-NOTES.md)
- Human review checklist:
  [`PHILIPPE-ROCCA-SERRA-HUMAN-REVIEW-CHECKLIST.md`](PHILIPPE-ROCCA-SERRA-HUMAN-REVIEW-CHECKLIST.md)

Load `dist/hcmo.ttl` or `dist/hcmo.owl`. The source of truth is
`ontology/modules/*.ttl`; files under `dist/` are generated.
