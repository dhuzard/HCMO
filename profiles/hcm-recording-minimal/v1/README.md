# HCM Recording Minimal v1

This optional engineering draft is pending expert approval. It is a per-entity recording profile, not a new ontology release or an assertion of scientific mapping accuracy. `field-contract.yaml` is the machine-readable contract. Its source commit pins repository content; each source has a raw-byte SHA-256. SKOS files are separately pinned because they are outside the OWL manifest. Update requires a new reviewed profile version; run `python tooling/validate_recording_minimal.py` offline to verify pins, membership, and synthetic cases. The checker exposes `load_contract()` and `validate(case, contract, graphs)` for consumers. It checks one flattened per-entity bundle; entity identifiers and linking are a caller responsibility. It is not a complete RDF or core SHACL validator.

`min_count` and `max_count` apply to each entity represented, not to a study. This bundle requires enclosure and sensor identifiers and a subject species; other fields are optional. Omitted means unknown or not supplied, never negative; null and blank scalar values are invalid. Normalizations are profile-side records, not triples using the literal properties. Preserve exact source values and alternatives. Reviewed mappings require evidence, reviewer, explicit permitted IRI and pinned scheme membership; unreviewed values remain unresolved with no asserted IRI. No taxonomy is approved: all taxon records remain unresolved until a source-authoritative, licensed species-rank release is pinned and reviewed. Depth-video additionally requires a reported depth-channel evidence fact; reviewed sensor technology requires a reported system-technology evidence fact. These facts are submitter assertions for review, not proof. `IR video` alone does not establish depth, and `EMF` alone does not establish the system technology. It does not automatically infer mappings from text. `skos:broader` describes only the actual vocabulary hierarchy; video does not imply depth video and an EMF report does not identify a particular technology.

The policy restricts sampling rate to positive numeric values in QUDT Hz. This is a profile restriction, not an ontology restriction. Time is a local clock value unless an offset is explicitly present; a light phase duration and dark phase start do not establish lighting exposure or a timezone. See `gaps.yaml` for non-single-IRI fields. CEDAR export can represent individual strings, dates, and simple enumerations, subject to its own constraints; this profile does not assert that a CEDAR terminology server indexes SKOS. Nested QUDT, evidence-bound mappings, local scheme validation and cross-field rules must be retained outside a simple template or reported as unsupported. No CEDAR template is published here.

## Worked synthetic projection

Legacy input `species: "reported mouse"`, `sensor technology: "infrared camera with documented illumination"`, `sampling rate: 30 Hz` is represented in the positive JSON fixture as the exact literal values, an unresolved taxon, a reviewed technology mapping with synthetic evidence, and `sampling_rate: {numeric_value: 30, unit: "http://qudt.org/vocab/unit/HZ"}`. A canonical RDF projection of the supported subset (identifiers invented solely for this fixture) is:

```turtle
@prefix hcm: <https://w3id.org/hcmo/ontology/hcm#> .
@prefix bio: <https://w3id.org/hcmo/ontology/hcm/bio#> .
@prefix tech: <https://w3id.org/hcmo/ontology/hcm/tech#> .
@prefix qudt: <http://qudt.org/schema/qudt/> .
@prefix unit: <http://qudt.org/vocab/unit/> .
@prefix ex: <https://example.org/synthetic/> .
ex:subject a bio:Subject ; bio:hasSpecies "reported mouse" .
ex:sensor a tech:Sensor ; tech:hasSensorIdentifier "synthetic-sensor-1" ;
  tech:hasSensorTechnology "infrared camera with documented illumination" ;
  tech:hasSamplingRateQuantity [ a qudt:QuantityValue ; qudt:numericValue 30 ; qudt:hasUnit unit:HZ ] .
ex:cage a hcm:MonitoredEnclosure ; hcm:hasEnclosureIdentifier "synthetic-cage-1" .
```

The example shows the property projection, not a complete core-SHACL-conformant graph (core also requires dimensions, housing assignment, and other context). The JSON fixture is validated by the profile checker; RDF graph conformance requires the core shapes and complete context separately. The unresolved taxon and SKOS mappings remain in the JSON evidence records; no new HCMO predicates are minted. `ontology/context.jsonld` is pinned, but field names in the profile JSON are application keys, not a claimed JSON-LD context.
