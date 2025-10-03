# Changelog

## [0.2.1] - 2025-10-03
### Added
- Webapp alignment with the device-agnostic VMG: updated form fields for protocol/session metadata, tier-driven blueprint UI, ethics notices, and illustrative examples.
- Node-based regression tests covering the blueprint inventory/examples and the ethics notice.

### Changed
- Blueprint API now parses `docs/FIELD-TIERS.md` directly and returns tier-oriented responses with updated status icons.

## [0.2.0] - 2025-09-30
### Added
- Device-agnostic README with explicit purpose, principles, field tiers, examples policy, and ethics guidance.
- Conceptual, field tier, policy, ethics, and contribution documentation plus illustrative examples.
- Contributor hygiene assets (CONTRIBUTING, Code of Conduct, CODEOWNERS, issue templates, citation metadata).

### Changed
- Established semantic versioning for documentation and bumped the VMG to 0.2.0.

### Deprecated
- None.

### Removed
- None.

## 1.0.0 – Initial release
- TBox: core classes/properties, disjointness, basic restrictions.
- Alignments: SOSA/SSN, PROV, OWL-Time, BFO.
- SHACL: system, behavior, time interval, enclosure, dimensions.
- Examples: minimal and edge-case datasets.
- Queries: five competency questions.
- JSON-LD context.
- CI: pySHACL validation workflow.
