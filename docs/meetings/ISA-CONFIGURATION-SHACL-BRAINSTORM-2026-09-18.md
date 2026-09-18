# ISA configuration and HCMO--ISA SHACL profile brainstorm

Date: 2026-09-18

Status: discussion record; no option or ontology change is approved

Context: follow-up analysis by Damien Huzard and Codex in response to Philippe
Rocca-Serra's suggestion to justify ISA through an ISA configuration and/or a
SHACL shape covering ISA and HCMO content. Philippe supplied the suggestion;
the analysis and candidate wording below remain for co-author review.

## Question being addressed

What makes ISA a necessary and testable part of the HCMO interoperability
story, rather than an additional vocabulary mentioned only to broaden the
paper's standards coverage?

The working answer is that validation cannot provide the justification by
itself. The justification must begin with a concrete exchange need:

- HCMO describes home-cage subjects, enclosures, assignments, devices,
  observations, and results;
- ISA describes the Investigation--Study--Assay organization, experimental
  factors, protocols, Sources, Samples, processes, and data files; and
- their useful overlap is a multimodal experiment in which home-cage
  behavioural monitoring is connected to specimen collection, downstream
  assays, analysis, and research-data packaging.

If no intended repository, authoring tool, or downstream consumer uses ISA,
then ISA risks being ornamental. In that case it should remain a narrowly
evaluated optional exchange layer, not a dependency or upper ontology for
HCMO.

## Baseline already implemented

This discussion starts from working evidence rather than a blank design:

- `examples/isa-roundtrip/native-isa/` contains a reproducible, pinned
  ISA-API projection of one unchanged animal Source through specimen
  collection to one genuine tissue Sample;
- `examples/isa-roundtrip/canonical.ttl` and
  `examples/isa-roundtrip/ro-crate-metadata.json` contain the richer HCMO RDF
  and extended ISA RO-Crate representations;
- `shapes/isa-hcmo-evidence-shapes.ttl` checks the minimal mixed-vocabulary
  workflow;
- `shapes/isa-hcmo-roundtrip-shapes.ttl` checks animal identity, housing,
  factor/group, observation, and STATO result/file-fragment invariants;
- native ISA losses are declared in `examples/isa-roundtrip/loss/`; and
- `tooling/validate_isa_native_projection.py`, `tooling/validate.py`, and
  `tooling/validate_interoperability.py` exercise separate validation gates.

The accepted modeling boundary remains:

- an animal is an ISA Source, not a manufactured Sample proxy;
- a genuinely derived tissue specimen is an ISA Sample;
- an Assay is the test/workflow grouping, a Protocol is the reusable method,
  and a Process is one execution;
- a behavioural context is not itself an Assay unless it denotes the test;
- a cage is an HCMO monitored enclosure, not an ISA biological material;
- a time-bounded HousingAssignment is not a Sample or data-file result; and
- STATO-typed statistical results remain distinct from the file and exact
  fragments that represent them.

## Option A: create an ISA configuration

An ISA configuration could constrain an authoring workflow by specifying
expected fields, required fields, measurement and technology types, protocol
parameters, and allowed ontology-backed values. Candidate HCM concerns include
animal characteristics, treatment and enrichment factors, recording and
specimen-collection protocols, sensor/platform metadata, sampling and
light-cycle parameters, and raw or derived data files.

### What it could demonstrate

- a practical native ISA authoring template for a defined HCM use case;
- consistent fields and controlled values across HCM submissions; and
- native ISA-JSON/ISA-Tab generation for the supported overlap.

### What it cannot demonstrate by itself

- temporal agreement between observations and housing assignments;
- correct separation of an animal, cage, allocation execution, and assignment
  record;
- preservation of HCMO graph identity and provenance;
- correspondence between STATO results and exact file fragments; or
- validity of the richer RDF/RO-Crate representation.

The documented ISA configuration mechanism is associated with ISAcreator
field and terminology customization. Before investing in it, the co-authors
must confirm that the selected contemporary ISA tooling consumes and enforces
the configuration in the intended workflow.

There is also a structural risk. The ISA abstract model permits an Assay on a
whole initial subject, while the currently tested ISA-API ISA-Tab writer starts
an assay table from `Sample Name` and associates factor values with Samples.
A configuration may relax accepted labels without changing that serialization
topology.

### Proposed feasibility test

Build the smallest possible configuration and accept the option only if it can
demonstrate all of the following without a fabricated Sample:

1. an animal Source directly enters a behavioural recording assay;
2. treatment and enrichment factor values remain attached to the correct
   biological subject;
3. the recording Process and its output data file survive JSON--Tab--JSON;
4. stable HCMO identifiers survive the round trip; and
5. the pinned ISA validator accepts both serializations.

If the test fails, retain the explicit controlled-loss boundary and ask ISA
maintainers whether a supported whole-subject convention exists. Do not alter
the biological roles merely to satisfy a writer.

## Option B: publish an HCMO--ISA SHACL profile

SHACL is suitable for the RDF/extended-crate representation. It cannot directly
validate ISA-Tab or ISA-JSON; those documents must first be converted into an
agreed RDF data graph. Passing an HCMO-maintained shape would therefore mean
conformance to the declared HCMO exchange constraints, not official ISA
conformance.

A cautious name would be **HCMO--ISA interoperability profile** or **HCMO
application profile for ISA/RO-Crate**. The phrase "the ISA SHACL profile"
should be avoided unless an authoritative ISA body publishes or endorses it.

### Candidate reusable ISA-exchange constraints

- Investigation contains Study, and Study contains Assay;
- Assay identifies a measurement type, technology, and protocol as required by
  the selected exchange scope;
- Process executes a Protocol;
- Process inputs and outputs occupy legitimate Source, Sample, or file roles;
- a material output is a genuine derived Sample; and
- the material/data process graph is acyclic.

### Candidate HCMO-extension constraints

- an unchanged animal is not exposed as a newly generated Sample;
- a tissue Sample is derived from its animal Source;
- an enclosure is not a Source, Sample, or factor merely because it has an
  identifier;
- each HousingAssignment identifies its subject, enclosure, and valid interval;
- an allocation Process may generate the assignment record, but the record is
  not an ISA Sample or data file;
- factor values and group membership are complete and mutually consistent;
- an observation's subject, enclosure, and time agree with the applicable
  housing assignment; and
- each semantic statistical result is typed appropriately and represented by
  an exact file fragment without conflating the result and the file.

The current shape files mix reusable class targets with targets for named
fixture individuals. Named-node checks remain valuable regression tests, but
they should not be presented as a general application profile. A future
implementation would separate reusable profile shapes from fixture-specific
tests and include deliberately invalid fixtures for each major boundary.

## Option C: layered validation

The options are complementary rather than alternatives. The strongest design,
if its maintenance cost is justified, has separate gates and separate claims:

| Gate | Candidate mechanism | What a pass would support | What it would not support |
| --- | --- | --- | --- |
| Native ISA authoring and serialization | Pinned ISA-API plus a reviewed configuration, if feasible | The declared native ISA subset has the required fields and survives the tested conversion | Preservation of the richer HCMO graph |
| RO-Crate and selected ISA exchange rules | Pinned RO-Crate/profile validator | The crate satisfies the rules implemented by that pinned validator | ISA-team endorsement or unsupported HCMO semantics |
| HCMO--ISA semantic boundary | Reusable SHACL profile | The RDF graph satisfies the declared cross-model identity, temporal, provenance, and result constraints | Native ISA-Tab/JSON validity |
| Preservation and loss | Exact-answer queries, graph comparison, and loss manifests | Tested information is preserved or explicitly reported as lost | General round-trip completeness outside the fixture |

Each gate should emit its own report. Combining the results into one
undifferentiated statement such as "ISA compliant" would overstate the
evidence.

## Decisions deferred to the co-authors

1. What real consumer or exchange scenario makes ISA useful for HCMO?
2. Is ISA an optional exchange profile or an intended normative dependency?
3. Must native ISA represent the whole-animal behavioural assay, or is the
   Source-to-tissue-Sample overlap sufficient for the current paper?
4. Must study-factor values remain directly attached to animal Sources?
5. Which tool must consume an ISA configuration, and who will maintain its
   version and controlled terminology?
6. Should the existing shapes be generalized into a supported application
   profile, or remain evaluation-fixture checks?
7. Which exact claim is intended: tested interoperability, conformance to an
   HCMO-maintained profile, or formal conformance to an externally governed
   ISA profile?
8. Who owns future updates when ISA, ISA RO-Crate, RO-Crate, or the validators
   change?

## Candidate manuscript wording for later review

> ISA is used as an optional experimental-metadata exchange layer rather than
> as an upper ontology for HCMO. HCMO represents home-cage subjects,
> enclosures, housing assignments, sensors, and observations, whereas ISA
> supplies the Investigation--Study--Assay organization and
> Source--Sample--Process--Data provenance needed to connect behavioural
> monitoring with derived specimens and downstream assays. We evaluate this
> interface through two deliberately separate artifacts: a native ISA-API
> Source-to-Sample projection and an HCMO-extended ISA/RO-Crate RDF graph
> validated with SHACL. Information not represented by the native projection
> is reported explicitly as controlled loss; this evaluation is not presented
> as formal ISA RO-Crate conformance.

This paragraph is a drafting proposal, not approved manuscript text.

## Provisional recommendation, not a decision

For the present paper, the smallest defensible next step would be to generalize
and document the existing SHACL constraints as an HCMO-maintained exchange
profile while retaining the native Source-to-Sample round trip and its loss
manifests. An ISA configuration should be promoted only after the focused
whole-animal feasibility test shows that it enables a real native workflow
without inventing a Sample proxy.
