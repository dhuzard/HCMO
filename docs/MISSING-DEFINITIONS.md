# Definition and modeling-quality status

Generated-profile audit for HCMO 0.2.0. Regenerate the profile with
`python tooling/build.py` before updating this report.

## Active-term metadata

- Missing `rdfs:label`: **0**
- Missing textual definition (`rdfs:comment` or `IAO:0000115`): **0**
- Active object/datatype properties missing `rdfs:domain`: **0**
- Active object/datatype properties missing `rdfs:range`: **0**
- Active classes without an explicit named or restriction-based upper anchor:
  **0**

## Resolved export artifacts

`UNKNOWN:` terms, `ns:` placeholders, `xsd:boolean`/`xsd:integer` declarations
as properties, and the bare `https://w3id.org/hcmo/ontology/hcm/obs#` property
are not present in the active graph. They remain only in the archived 0.0.1
source under `ontology/legacy/mapp-0.0.1/` for auditability.

`hcm:OWL-Timeintervaltable` is retained as a deprecated 0.0.1 IRI with an
explicit note that it was an invalid Chowlk/spreadsheet artifact and has no
asserted replacement. The valid temporal model uses SOSA temporal properties
with OWL-Time temporal entities.

## Open semantic decisions

- `hcm:hasUnit`, `hcm-obs:hasNumericValue`, and environmental literal values
  remain a lightweight pattern pending a reviewed choice between QUDT and OM.
- `hcm-obs:hasCondition` deliberately has `owl:Thing` as its range until an
  experimental-condition model is selected with domain experts.
- Deprecated 0.0.1 IRIs remain in `hcm-compat.ttl` for compatibility. Consumers
  should follow `dcterms:isReplacedBy` where one is asserted, read the migration
  note where no exact replacement exists, and should not mint new data with
  deprecated terms.
