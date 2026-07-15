# Terms needing labels / definitions / cleanup

Auto-derived from `dist/profile.json` (regenerate: `python tooling/build.py`).
Per project policy, missing labels and definitions are **not fabricated** — they are
listed here for the ontology authors to fill in.

## Missing `rdfs:label` (5)

- `https://w3id.org/hcmo/ontology/hcm/obs#`
- `http://purl.org/dc/elements/1.1/creator`
- `http://purl.org/dc/elements/1.1/description`
- `http://purl.org/dc/elements/1.1/title`
- `http://www.w3.org/2002/07/owl#versionInfo`

## Missing definition / `rdfs:comment` (144)

Every authored term currently lacks a definition. Add `rdfs:comment` (and/or
`IAO:0000115`) to each term in `ontology/modules/*.ttl`.

## V2 draft FOOPS definition gap (closed)

FOOPS v0.4.0 on `ontology/v2/hcmo-v2-merged-clean.owl` (2026-07-09) found
definitions for 0/111 assessed v2 terms before the definition pass. The v2
source modules now include `rdfs:comment` definitions for all 111 assessed terms,
and `VOC4` passes in `docs/paper/FOOPS-REPORT-2026-07-09.after-definitions.json`.
Co-authors should still review wording before v2 promotion.

## Chowlk placeholder / likely-erroneous terms (43)

These come from the Chowlk diagram export and are almost certainly not intended
ontology terms. They are **preserved as authored** (not renamed/deleted per policy);
review and either re-map to real IRIs or remove at the source module:

- `http://www.owl-ontologies.com/UNKNOWN#*` — diagram nodes that never got a real namespace.
- `http://www.owl-ontologies.com/ns#Class2`, `...#objectProperty` — placeholder stubs.
- `xsd:boolean`, `xsd:integer` typed as `owl:DatatypeProperty` — these are datatypes, not properties.

- `http://www.owl-ontologies.com/UNKNOWN#StudyFactors`  (label: 'Study Factors')
- `http://www.owl-ontologies.com/ns#Class2`  (label: 'Class2')
- `http://www.owl-ontologies.com/UNKNOWN#communicatesWith`  (label: 'communicates with')
- `http://www.owl-ontologies.com/UNKNOWN#hasEnrichmentReq`  (label: 'has enrichment req')
- `http://www.owl-ontologies.com/UNKNOWN#hasSensors`  (label: 'has sensors')
- `http://www.owl-ontologies.com/UNKNOWN#runsOn`  (label: 'runs on')
- `http://www.owl-ontologies.com/UNKNOWN#supportsEnclosure`  (label: 'supports enclosure')
- `http://www.owl-ontologies.com/ns#objectProperty`  (label: 'object property')
- `http://www.owl-ontologies.com/UNKNOWN#captures`  (label: 'captures')
- `http://www.owl-ontologies.com/UNKNOWN#hasActuators`  (label: 'has actuators')
- `http://www.owl-ontologies.com/UNKNOWN#hasCondition`  (label: 'has condition')
- `http://www.owl-ontologies.com/UNKNOWN#hasDarkPhaseDuration`  (label: 'has dark phase duration')
- `http://www.owl-ontologies.com/UNKNOWN#hasDarkPhaseStart`  (label: 'has dark phase start')
- `http://www.owl-ontologies.com/UNKNOWN#hasDawnDuration`  (label: 'has dawn duration')
- `http://www.owl-ontologies.com/UNKNOWN#hasDimUnit`  (label: 'has dim unit')
- `http://www.owl-ontologies.com/UNKNOWN#hasDuskDuration`  (label: 'has dusk duration')
- `http://www.owl-ontologies.com/UNKNOWN#hasEnrichmentType`  (label: 'has enrichment type')
- `http://www.owl-ontologies.com/UNKNOWN#hasFacilityType`  (label: 'has facility type')
- `http://www.owl-ontologies.com/UNKNOWN#hasFirmware`  (label: 'has firmware')
- `http://www.owl-ontologies.com/UNKNOWN#hasFloorArea`  (label: 'has floor area')
- `http://www.owl-ontologies.com/UNKNOWN#hasFoodReq`  (label: 'has food req')
- `http://www.owl-ontologies.com/UNKNOWN#hasHeight`  (label: 'has height')
- `http://www.owl-ontologies.com/UNKNOWN#hasLength`  (label: 'has length')
- `http://www.owl-ontologies.com/UNKNOWN#hasLightPhaseDuration`  (label: 'has light phase duration')
- `http://www.owl-ontologies.com/UNKNOWN#hasModelNumber`  (label: 'has model number')
- `http://www.owl-ontologies.com/UNKNOWN#hasName`  (label: 'has name')
- `http://www.owl-ontologies.com/UNKNOWN#hasProtocol`  (label: 'has protocol')
- `http://www.owl-ontologies.com/UNKNOWN#hasSafetyReq`  (label: 'has safety req')
- `http://www.owl-ontologies.com/UNKNOWN#hasSamplingRate`  (label: 'has sampling rate')
- `http://www.owl-ontologies.com/UNKNOWN#hasSensorIdentifier`  (label: 'has sensor identifier')
- `http://www.owl-ontologies.com/UNKNOWN#hasSensorTechnology`  (label: 'has sensor technology')
- `http://www.owl-ontologies.com/UNKNOWN#hasSensorType`  (label: 'has sensor type')
- `http://www.owl-ontologies.com/UNKNOWN#hasSocialReq`  (label: 'has social req')
- `http://www.owl-ontologies.com/UNKNOWN#hasType`  (label: 'has type')
- `http://www.owl-ontologies.com/UNKNOWN#hasVersion`  (label: 'has version')
- `http://www.owl-ontologies.com/UNKNOWN#hasWaterReq`  (label: 'has water req')
- `http://www.owl-ontologies.com/UNKNOWN#hasWidth`  (label: 'has width')
- `http://www.owl-ontologies.com/UNKNOWN#isCalibrated`  (label: 'is calibrated')
- `http://www.owl-ontologies.com/UNKNOWN#isOccupied`  (label: 'is occupied')
- `http://www.owl-ontologies.com/UNKNOWN#isOperational`  (label: 'is operational')
- `http://www.owl-ontologies.com/UNKNOWN#partOF`  (label: 'part o f')
- `http://www.w3.org/2001/XMLSchema#boolean`  (label: 'boolean')
- `http://www.w3.org/2001/XMLSchema#integer`  (label: 'integer')

## Other modeling issues to review

- v2 restored `hcm:Enclosure` as an `owl:Class`; the live/legacy audit should be refreshed after v2 promotion.
- v2 normalizes the environmental object properties as lower-camel relation names: `hcm-env:hasAmbientTemperature`, `hasAmmoniaConcentration`, `hasCarbonDioxideConcentration`, `hasOxygenConcentration`, `hasRelativeHumidity`, `hasLightIntensity`, and `hasLightState`.
- `sosa:hasResult` and `sosa:observedProperty` are each declared as BOTH `owl:ObjectProperty` and `owl:DatatypeProperty`.
- `hcm:OWL-Timeintervaltable`, `hcm:Structural&LocationTable` have spreadsheet-derived names (auto-labels "O W L- Timeintervaltable", "Structural& Location Table").
- `hcm-obs:` (the bare namespace IRI `https://w3id.org/hcmo/ontology/hcm/obs#`) is declared an `owl:ObjectProperty` with an empty label.
