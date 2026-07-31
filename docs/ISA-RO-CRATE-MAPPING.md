# HCMO, ISA, and ISA RO-Crate mapping

Status: accepted serialization policy with executable evidence. This document
distinguishes HCMO semantics, extended ISA RO-Crate exchange, controlled-loss
ISA-JSON/ISA-Tab projections, and mappings that remain review-only.

The A02 process-layer audit and ISA/STATO compatibility findings are recorded in
[`A02-ISA-STATO-COMPATIBILITY.md`](A02-ISA-STATO-COMPATIBILITY.md). Those
findings now include an executable instance-level evidence slice. They do not
constitute HCMO class mappings or formal ISA RO-Crate conformance.

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
| Animal-to-cage allocation | ISA Process applying a housing/allocation protocol; cage ID may also be a protocol parameter value | Actual time-bounded `hcm-bio:HousingAssignment` linked by `hcm-bio:assignedToEnclosure` | Animal, enclosure, execution, and assignment record remain distinct; the assignment is not an ISA process result. |
| Cage as an experimental variable | ISA Study Factor only when housing/cage condition is deliberately manipulated | `hcm-bio:StudyFactors` (preferred label: Study Factor) plus the applicable enclosure/environment attributes | A cage identifier alone is not a study factor. |
| Sensor-recording procedure | ISA Protocol/LabProtocol and executed Process/LabProcess; sensor can be protocol equipment | `hcm-tech:Sensor`, `sosa:madeBySensor` | Separates the planned recording procedure from what actually ran and avoids conflating new observations with OBI procurement or retrieval. |
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

The crate context adds the four HCMO namespaces and Bioschemas. The current
fixture declares RO-Crate 1.2 only. It does not invent an ISA `conformsTo` URI
while the draft still says that its permalink is pending.

## Executable evidence boundary

`examples/isa-hcmo-bridge.ttl` implements an acyclic
recording → raw file → transformation → derived file chain. The particular
recording execution is typed as an OBI assay, and the particular transformation
as an OBI data transformation. The evidence graph also contains particular
STATO factor-level, study-group-population, and sample-mean instances. These
instance types are evidence for a concrete workflow; they do not imply
equivalence or subclass mappings for the corresponding HCMO classes.

The housing process is a Bioschemas `LabProcess` and `prov:Activity`. It generates the
`hcm-bio:HousingAssignment` through `prov:generated`; the assignment is not a
`schema:result` because it is neither an ISA Sample nor a File/MediaObject.
Dedicated shapes in `shapes/isa-hcmo-evidence-shapes.ttl` enforce that boundary
and reject a cyclic process/data graph. Exact-answer competency questions trace
the raw file, factor/group assignment, and typed statistical result.

## Accepted boundary and remaining dependency

The generated `examples/isa-roundtrip/` crate demonstrates the accepted
allocation, re-housing, Source/Sample, 2 × 2 factor/group, repeated-observation,
and result-fragment patterns. HCMO RDF and the extended crate are lossless;
ISA-JSON and ISA-Tab are controlled-loss projections. Their currently tested
native overlap is one animal Source → genuine tissue Sample collection,
executed with pinned `isatools` 0.14.3 through JSON → Tab → JSON. Explicit
`Comment[HCMO IRI]` annotations preserve source identities because ISA-Tab
regenerates internal identifiers. Housing, direct whole-animal recording,
source-bound factor values, explicit groups, repeated observations, and
semantic STATO/file-fragment links remain declared losses. A broader native
HCM assay projection requires a reviewed ISA configuration. The unresolved
profile decision is external: ISA must confirm a permanent profile URI, base
RO-Crate edition, and endorsed validator procedure before formal conformance is
claimed.
