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
| Singular/plural duplicates (`hasDimension(s)`, `hasSensor(s)`) | Enclosure dimensions use `hasDimensions` for one dimensions record. The SemTS-derived `hasDimension` reference remains provisional pending canonical-IRI and semantic review and is not counted as implemented reuse. Sensor monitoring uses `monitoredBy`; physical cage installation uses the separate, non-inverse `installedIn` relation. The plural UNKNOWN relation was removed. | core and tech modules |
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

## Follow-up additions received on 2026-07-30

Philippe added three points after reviewing the meeting record. They refine the
open A01/A02 design work; they do not by themselves authorize new ontology
classes, imports, or mapping axioms.

### Readable upper-level presentation

Philippe described the following as a useful end-user presentation rather than
a formal recommendation:

```text
Thing / Entity
├── Material Entity
├── Information Entity
├── Quality / Property
└── Process Entity
```

Damien accepted this pragmatic two-view policy on 2026-07-31. The default HCMO
release retains direct canonical BFO/IAO anchors but exposes only Entity,
Material entity, Information content entity, Quality, and Process through
source-entailed navigation shortcuts. The full continuant/dependent-continuant
hierarchy is retained in the optional
`ontology/profiles/external-upper-developer.ttl` profile. No duplicate HCMO
upper classes or equivalences between BFO, SIO, SULO, ONTOP, SOSA, and PROV-O
are asserted.

For provenance, the duration-bearing PROV-O class corresponding to an executed
process is `prov:Activity`. PROV-O has no general `prov:Event` class;
`prov:InstantaneousEvent` is reserved for instantaneous generation, usage,
invalidation, start, and end events. The BFO process hierarchy remains the
semantic upper-process backbone; PROV-O remains a cross-cutting provenance view.

### OBI acquisition meanings

The word *acquisition* must be qualified in HCMO documentation and examples.
The pinned OBI `v2026-05-08` source supports three distinct cases:

| Intended meaning | Candidate representation | HCMO policy |
| --- | --- | --- |
| Purchasing or otherwise procuring an existing sensor | `OBI_0600010` material acquisition; alternative label “material procurement” | Directly reuse only when the modeled execution gains possession of the physical sensor. |
| Retrieving or copying information that already exists | `OBI_0600013` information acquisition; alternative label “data collection” | Directly reuse only when possession of existing information is gained. |
| Producing new measurements with a sensor | SOSA `Observation`; optionally an encompassing `OBI_0000070` assay when its evaluant and objective fit | Describe this as sensor recording or observation generation, not generic OBI acquisition. |

`OBI_0600013` explicitly excludes processes that create or change information,
including assays and data transformations. OBI also declares assay disjoint
with information acquisition. HCMO therefore does not mint or map a generic
`SensorAcquisition` class. The current ontology contains no such class.

### STATO and ISA

Philippe confirmed that HCMO's connection to STATO and ISA is a worthwhile
topic and offered to present STATO to the group. The next step is an
evidence-review session around one concrete HCM workflow, not immediate
alignment axioms. The external-vocabulary contract is now implemented in
`external-vocabularies.yaml`, pinning OBI, STATO, ISA, and the selected ISA
RO-Crate draft. The concrete acyclic workflow and answer-based competency
questions are now implemented as an evidence slice. The remaining review
package should contain:

1. explicit decisions on mapping strength; and
2. resolution of the housing-assignment and non-file statistical-result ISA
   round-trip losses.

Until that review is complete, the STATO and ISA types in the bridge remain
instance-level interoperability evidence rather than HCMO class mappings or a
claim of formal ISA RO-Crate conformance.
