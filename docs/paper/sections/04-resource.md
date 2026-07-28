# 4. Resource description

> **Status:** full draft aligned with HCMO 0.2.0. Claims about external
> mappings are limited to axioms and examples present in the release.

HCMO uses the persistent ontology IRI
`https://w3id.org/hcmo/ontology/hcm` and the stable term namespace
`https://w3id.org/hcmo/ontology/hcm#`. Domain-specific terms use four
sub-namespaces beneath the same base: `hcm/bio#`, `hcm/env#`, `hcm/obs#`, and
`hcm/tech#`. Published IRIs are not renamed when terminology changes; obsolete
IRIs are retained in a compatibility module with deprecation and replacement
metadata where a defensible replacement exists.

**Modular organisation.** HCMO 0.2.0 is authored as five active modules. The
minimal core centres on `hcm:Enclosure`, `hcm:MonitoredEnclosure`, enclosure
dimensions, enrichment, and stable housing relations. The bio module represents
subjects, experimental groups, housing assignments, and study factors. The env
module represents environmental profiles, light cycles, gas profiles,
measurement specifications, and environmental properties. The obs module owns
SOSA-style observations and their categorical, quantitative, behavioral, and
tabular results. The tech module represents sensors, actuators, hardware,
software, and time-series resources. A sixth, migration-only module preserves
deprecated HCMO 0.0.1 IRIs but is not a source of terms for new data.

This organisation preserves two boundaries that are important for HCM data.
First, housing context is not reduced to the animal: a housing assignment is an
explicit record linking a subject or group to an enclosure. Second, a physical
sensor, the observation it performs, and the result it produces are separate
entities. For example, `hcm-tech:Sensor` is linked to a monitored enclosure,
captures a `sosa:Property`, and may make a `sosa:Observation`; the observation
then identifies its feature of interest and result using SOSA relations. This
supports provenance-sensitive queries without treating a device, event, and
data value as the same thing.

**Standards reuse.** Physical subjects, enclosures, enrichments, sensors,
actuators, and hardware are anchored under BFO material entity; experimental
groups are anchored as BFO object aggregates. Records, specifications, profiles,
software, and observation-result artifacts use the IAO information-content
anchor. Sensors, actuators, observations, results, and observed properties reuse
SOSA classes and relations, and `hcm-tech:captures` is explicitly a subproperty
of `sosa:observes`. Schema.org supplies contributor and place exchange types.
Selected SemTS terms describe data dimensions and generated time-series
segments. The example ABox uses OWL-Time intervals and the duration competency
query consumes this representation. These are selective references, not claims
that HCMO imports or reproduces the full external ontologies. PROV-O, OBI,
STATO, ISA RO-Crate, and QUDT/OM integration remain separately reviewed roadmap
work.

**Distribution and application support.** The authored modules are merged
deterministically into Turtle, RDF/XML, and JSON-LD distributions. A generated
`profile.json` provides a flat term inventory for synchronization layers and
interfaces, while `ontology/context.jsonld` supports JSON-LD applications.
`hcmo.yaml` is the stable machine-readable contract that identifies the module
order, generated artifacts, shapes, examples, and competency-query index.

The active local inventory contains 29 classes and 81 object or datatype
properties. The generated release additionally contains deprecated
compatibility terms and directly referenced external vocabulary terms. A signed
class audit and property audit record the asserted semantics, restrictions,
inference consequences, current evidence, and unresolved decisions without
turning review notes into unattended ontology rewrites.

*Figure F2: HCMO module overview and the enclosure--subject--sensor--observation--
result path.*
