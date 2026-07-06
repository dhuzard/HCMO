# Terms needing labels / definitions / cleanup

Auto-derived from `dist/profile.json` (regenerate: `python tooling/build.py`).
Per project policy, missing labels and definitions are **not fabricated** — they are
listed here for the ontology authors to fill in.

## Missing `rdfs:label` (1)

- `https://w3id.org/hcmo/ontology/hcm/obs#`

## Missing definition / `rdfs:comment` (143)

Every authored term currently lacks a definition. Add `rdfs:comment` (and/or
`IAO:0000115`) to each term in `ontology/modules/*.ttl`.

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
- v2 keeps `hcm-env:AmbientTemperature`, `AmmoniaConcentration`, `CarbonDioxideConcentration`, `OxygenConcentration`, `RelativeHumidity`, `LightIntensity`, and `LightState` as environmental object properties by the `docs/paper/MODULE-MAP.md` placement decision.
- `sosa:hasResult` and `sosa:observedProperty` are each declared as BOTH `owl:ObjectProperty` and `owl:DatatypeProperty`.
- `hcm:OWL-Timeintervaltable`, `hcm:Structural&LocationTable` have spreadsheet-derived names (auto-labels "O W L- Timeintervaltable", "Structural& Location Table").
- `hcm-obs:` (the bare namespace IRI `https://w3id.org/hcmo/ontology/hcm/obs#`) is declared an `owl:ObjectProperty` with an empty label.
