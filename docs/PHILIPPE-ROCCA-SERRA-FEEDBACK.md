# Philippe Rocca-Serra feedback implementation record

Date received: July 2026. Target release: HCMO 0.1.0.

This record covers the earlier cleanup already implemented for HCMO 0.1.0.
The later interoperability meeting is preserved in
[`meetings/PHILIPPE-ROCCA-SERRA-HCMO-NOTES.md`](meetings/PHILIPPE-ROCCA-SERRA-HCMO-NOTES.md),
with unresolved and follow-up work routed through the
[`PHILIPPE-ROCCA-SERRA-HUMAN-REVIEW-CHECKLIST.md`](PHILIPPE-ROCCA-SERRA-HUMAN-REVIEW-CHECKLIST.md).

| Feedback | Resolution | Evidence |
| --- | --- | --- |
| HCMO name conflicts with MAPP description | Ontology title, description, manifest, README, and current documentation now consistently use Home-Cage Monitoring Ontology. | `hcmo.yaml`, ontology header, `README.md` |
| Unknown namespace/prefix | No `UNKNOWN:` or `ns:` artifact is present in the active graph. Original export source is archived and excluded from the manifest. | `ontology/legacy/mapp-0.0.1/`, `hcm-compat.ttl` |
| Classes lack upper anchors | Every active class has an explicit named/restriction anchor. Domain entities use BFO/IAO; sensing, observation, property, and result classes use SOSA where semantically applicable. | `ontology/modules/*.ttl`, metadata audit |
| Classes lack textual definitions | Every active and deprecated HCMO class/property has an `rdfs:comment`; active missing-definition count is zero. | `docs/MISSING-DEFINITIONS.md` |
| Study factor is an enclosure | Removed. `hcm-bio:StudyFactors` is an IAO information-content entity, with the preferred label “Study Factor” and independent-variable semantics aligned with ISA. | `hcm-bio.ttl` |
| `OWL-Timeintervaltable` is unclear | Confirmed as an invalid Chowlk/spreadsheet artifact; deprecated explicitly with no replacement. The supported model uses SOSA and OWL-Time. | `hcm-compat.ttl` |
| Dangling `.../obs#` property | Removed from the active graph and retained only in archived source. | active-graph audit |
| Duplicate `communicatesWith` | `UNKNOWN:communicatesWith` removed; current relation is `hcm-tech:communicatesWith`. Published `hcm:communicatesWith` is deprecated and mapped. | `hcm-tech.ttl`, `hcm-compat.ttl` |
| Singular/plural duplicates (`hasDimension(s)`, `hasSensor(s)`) | Enclosure dimensions use singular relation name `hasDimensions` to one dimensions record; SEMTS `hasDimension` retains its external time-series meaning. Sensor relation is `monitoredBy` with inverse `installedIn`; plural UNKNOWN relation removed. | core and tech modules |
| Duplicate `hasResult` | HCMO observations now use canonical `sosa:hasResult`. Local 0.0.1 `hcm:hasResult` is deprecated without an equivalence assertion because the legacy restriction used the reverse direction. | observation and compatibility modules |
| Object properties lack domain/range | Every active HCMO object property now has both. Union domains/ranges are used where a relation intentionally applies to several technical or experimental classes. | metadata audit |
| Duplicate data properties (`hasName`, `hasUnit`, sampling rate) | Unknown duplicates removed; unit relation consolidated to `hcm:hasUnit` for results and measurement specifications; sampling rate moved to `hcm-tech`; valid published IRIs are deprecated/mapped. | core, tech, compatibility modules |
| Data properties lack domain/range | Every active HCMO datatype property now has both. Generic name/description properties use `owl:Thing` domains. | metadata audit |
| Clarify ISA relation and cage allocation | Added a reviewed design note and RDF example. Whole animals map to ISA Source; physical cages remain HCMO entities; allocation is an HCMO n-ary assignment and proposed ISA Process; cage ID is a parameter value, not automatically a Study Factor. | `docs/ISA-RO-CRATE-MAPPING.md`, `examples/isa-hcmo-bridge.ttl` |
| Clarify monitoring files | HCMO remains format-neutral. ISA RO-Crate files are Assay outputs; repository examples use CSV. | ISA mapping note and examples |

## Items for the expert call

The ontology-side defects are resolved. The call should focus on choices that
require ISA round-trip expertise rather than unilateral ontology edits:

1. exact ISA Process/Protocol representation of allocation and re-housing;
2. whether cage ID should be duplicated as a Protocol Parameter Value;
3. Assay granularity by modality, enclosure, or data-product family;
4. serialization of assignment validity intervals in an acyclic ISA graph;
5. target version and conformance URI for the draft ISA RO-Crate profile.
