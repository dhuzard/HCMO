# Alignments

SOSA/SSN
- `hcm:Sensor` ⊑ `sosa:Sensor`
- `hcm:Actuator` ⊑ `sosa:Actuator`
- `hcm:System` ⊑ `sosa:Platform`
- `hcm:hasSensor` ⊑ `sosa:hosts`

OWL-Time
- `hcm:TimeInterval` ⊑ `time:TemporalEntity`

PROV and Agents
- `hcm:producedBy` ⊑ `prov:wasAttributedTo`
- `hcm:Supplier` ⊑ `prov:Agent`, `schema:Organization`

BFO
- `hcm:BehaviorAndPhysiology` ⊑ `bfo:0000015` (process)

Units (QUDT/OM) – Roadmap
- Keep datatype-based dimensions initially.
- Future: model width/length/height as `qudt:QuantityValue` with `qudt:numericValue` and `qudt:unit` (e.g., `unit:CentiM`).

