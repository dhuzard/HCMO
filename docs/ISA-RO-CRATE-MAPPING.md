# HCMO, ISA, and ISA RO-Crate mapping

Status: design note for expert review. This document distinguishes assertions
that are already represented in HCMO 0.1.0 from proposed serialization choices
for Metadatapp and ISA RO-Crate.

The A02 process-layer audit and ISA/STATO compatibility findings are recorded in
[`A02-ISA-STATO-COMPATIBILITY.md`](A02-ISA-STATO-COMPATIBILITY.md). Those
findings are future work and do not constitute accepted ontology mappings.

## Current Metadatapp export

`Neuronautix/metadatapp-oss/templates/ro-crate-metadata.jsonld.tpl` is a generic
RO-Crate 1.1 template. Its local terms alias `Experiment`, `Study`, `Subject`,
and related concepts to Schema.org classes, but the exported graph currently
contains only the root `Dataset` and its `Person` creator. It does not yet emit
the Investigation/Study/Assay hierarchy, LabProcess graph, Sample/Source
entities, parameter values, or a declaration of conformance to the ISA
RO-Crate profile. It is therefore a useful container for an ISA-compatible
graph, but is not itself an ISA RO-Crate implementation yet.

## Recommended object mapping

| Experimental concept | ISA / ISA RO-Crate representation | HCMO representation | Rationale |
| --- | --- | --- | --- |
| Overall experiment | ISA Investigation; ISA RO-Crate `schema:Dataset` with `additionalType` `Investigation` | Outside HCMO scope | The investigation contains studies and their metadata. |
| HCM study | ISA Study; ISA RO-Crate `schema:Dataset` with `additionalType` `Study` | May mention HCMO study factors | Study factors belong to experimental design, not beneath an enclosure class. |
| Whole animal at study entry | ISA Source; represented by the ISA RO-Crate Sample profile | `hcm-bio:Subject` | ISA defines a Source as starting biological material; an assay may be performed on a whole initial subject. |
| Tissue, aliquot, or derived specimen | ISA Sample/Material; ISA RO-Crate Sample with `derivesFrom` | Usually outside HCMO scope | Keep the animal and a derived specimen as distinct entities. |
| Physical cage | Not an ISA Source or Sample | `hcm:MonitoredEnclosure` | A cage is equipment/housing context, not biological material. |
| Animal-to-cage allocation | ISA Process applying a housing/allocation protocol; cage ID may also be a protocol parameter value | `hcm-bio:HousingAssignment` linked by `hcm-bio:assignedToEnclosure` | The n-ary assignment record can later carry start/end time and provenance without treating cage identity as a biological characteristic. |
| Cage as an experimental variable | ISA Study Factor only when housing/cage condition is deliberately manipulated | `hcm-bio:StudyFactors` (preferred label: Study Factor) plus the applicable enclosure/environment attributes | A cage identifier alone is not a study factor. |
| Sensor/acquisition procedure | ISA Protocol/LabProtocol and executed Process/LabProcess; sensor can be protocol equipment | `hcm-tech:Sensor`, `sosa:madeBySensor` | Separates planned acquisition from what actually ran. |
| HCM measurements | ISA Assay plus LabProcess | HCMO observation subclasses and SOSA relations | Use the animal as feature of interest for attributable measurements; use the enclosure for cage-level aggregate/environment observations. |
| Raw/derived monitoring files | ISA Data node; ISA RO-Crate `File` or `MediaObject` produced by LabProcess and included in the Assay dataset | `hcm-tech:TimeSeries` and format/storage metadata | HCMO is format-neutral; current repository examples use CSV time-series and event exports. |

## Allocation and attribution pattern

The stable link is:

```text
ISA Study
  └─ ISA Source / Bioschemas Sample = animal = hcm-bio:Subject
       └─ hcm-bio:hasHousingAssignment → hcm-bio:HousingAssignment
            └─ hcm-bio:assignedToEnclosure → hcm:MonitoredEnclosure
                 └─ hcm-tech:monitoredBy → hcm-tech:Sensor
```

The corresponding ISA Process records the allocation event and executed housing
protocol. A cage identifier can be repeated as a protocol parameter value for
round-trip ISA compatibility, while the parameter value should point to or use
the identifier of the same HCMO enclosure entity.

For group-housed cages, signals that do not identify individuals are enclosure-
level observations. Subject-level attribution is valid only where the sensing
method identifies the animal. The active housing assignment establishes which
subjects were present, but it does not by itself turn a cage-level aggregate
signal into an individual measurement.

## Minimal ISA RO-Crate extension pattern

An ISA RO-Crate graph can add HCMO types and relations without replacing the
profile's Schema.org/Bioschemas types:

```json
{
  "@id": "#animal-1",
  "@type": ["bioschemas:Sample", "hcm-bio:Subject"],
  "name": "animal-1",
  "hcm-bio:hasHousingAssignment": {"@id": "#assignment-1"}
},
{
  "@id": "#assignment-1",
  "@type": "hcm-bio:HousingAssignment",
  "hcm-bio:assignedToEnclosure": {"@id": "#cage-12"}
},
{
  "@id": "#cage-12",
  "@type": "hcm:MonitoredEnclosure",
  "hcm:hasEnclosureIdentifier": "rack-3-cage-12"
}
```

The crate context must add the four HCMO namespaces and Bioschemas. The root
metadata entity should declare both the selected RO-Crate version and the ISA
RO-Crate profile when the full profile requirements are implemented.

## Questions to settle with ISA expertise

1. Should a housing assignment be serialized as the result of a dedicated ISA
   LabProcess, as a parameterized animal-allocation process, or both for robust
   ISA-Tab/ISA-JSON round-tripping?
2. Which protocol type and parameter term should identify cage allocation and
   cage identifier without overloading an ISA characteristic?
3. Should HCM acquisition be one Assay per sensing modality, one Assay per
   enclosure, or one Assay per data-product family in Metadatapp?
4. How should assignment validity intervals be serialized so cage changes can
   be reconstructed without breaking the acyclic ISA process graph?
5. Which ISA RO-Crate version/profile URI should Metadatapp target while the
   published profile remains a draft?
