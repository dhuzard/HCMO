# Optional BFO/SOSA bridge profile

Status: **proposed**, opt-in, not part of the default release. Decision record:
[ADR-0005](decisions/ADR-0005-BFO-SOSA-BRIDGE-POLICY.md); evidence:
[ADR-0005-evidence-audit.md](decisions/ADR-0005-evidence-audit.md).

## What it does

HCMO places its own terms under BFO/IAO and reuses SOSA 2017 for observations,
sensors and actuators, but nothing connects the two trees. The profile composes
two published one-way alignments so that SOSA terms receive a BFO placement,
without HCMO writing any statement about W3C terms and without declaring any
equivalence between SOSA and BFO:

```text
SOSA --(W3C SSN 2017 section 6.5, non-normative)--> PROV-O
     --(Prudhomme et al. 2025, Sci Data 12:282, CC0)--> BFO
```

For example, `sosa:Observation ⊑ prov:Activity` (W3C) and
`prov:Activity ≡ BFO process` (Prudhomme), so an observation is inferred to be a
BFO process. The four HCMO observation classes (and
`hcm-obs:GasConcentrationObservation`) become processes with no edit to any HCMO
module.

The profile adds **no axiom of its own** and no direct HCMO link: it only
declares the import closure
([`ontology/profiles/bfo-sosa-bridge.ttl`](../ontology/profiles/bfo-sosa-bridge.ttl)).

## Inferred placements (verified on the prefix-repaired chain, HermiT)

| SOSA / HCMO class | BFO placement |
| --- | --- |
| `sosa:Sensor`, `sosa:Actuator`, `sosa:Sampler` | material entity |
| `sosa:Observation`, `sosa:Actuation`, `sosa:Sampling` | process |
| `sosa:Result`, `sosa:ObservableProperty`, `sosa:FeatureOfInterest`, `sosa:Platform` | continuant (only) |
| `sosa:Procedure` | generically dependent continuant |
| `hcm-obs:BehaviorObservation`, `WeightObservation`, `HealthStatusObservation`, `EnvironmentObservation`, `GasConcentrationObservation` | process |

`sosa:Result` is only a continuant, so a physical specimen remains a valid
result. Each consequence is recorded with its source and rationale in
[`mappings/semantic/hcmo-external.sssom.tsv`](../mappings/semantic/hcmo-external.sssom.tsv)
(review-only; including the rejected `Result ⊑ information entity` and the
deferred `ObservableProperty ⊑ specifically dependent continuant`).

## Two commitments the bridge introduces

These come from the BFO alignment, **not from SOSA**. SOSA places no such
constraint.

### 1. Software sensors: the carrier pattern

Every `sosa:Sensor` becomes a BFO material entity, and `hcm-tech:Software` is an
information content entity, which BFO makes disjoint from material entities. An
individual typed as both is therefore inconsistent.

Model two things instead (optional documented pattern):

- the **code** stays `hcm-tech:Software` (information);
- the **deployed, running installation** is the sensor, a material carrier,
  distinct from the code and from the execution process. It bears a quality
  (`BFO:0000196` bearer of, `BFO:0000019` quality) that concretizes
  (`BFO:0000059`) the code.

```turtle
ex:tracker-code a hcm-tech:Software .
ex:tracker-run-cage7 a hcm-tech:Sensor ;            # the running installation
    BFO:0000196 ex:tracker-run-cage7-state .         # bearer of
ex:tracker-run-cage7-state a BFO:0000019 ;           # quality
    BFO:0000059 ex:tracker-code .                    # concretizes
ex:obs-1 a hcm-obs:BehaviorObservation ;
    sosa:madeBySensor ex:tracker-run-cage7 .
```

Do not write `ex:tracker-run-cage7 BFO:0000059 ex:tracker-code`: the domain of
*concretizes* is a process or specifically dependent continuant, so the direct
statement is inconsistent with the pinned BFO. `hcm-tech:runsOn` links software to
hardware and is not a concretization. Whether this pattern suits real toolchains
(DeepLabCut, SLEAP, Live Mouse Tracker) is a co-author judgement, still pending.

`shapes/profiles/bfo-sosa-bridge-shapes.ttl` flags a Software individual typed as
a sensor and a sensor that concretizes code directly.

### 2. A process cannot be a feature of interest

The chain makes `sosa:hasFeatureOfInterest` a kind of `prov:used`, so its filler
must be a participating continuant. Use the **subject, group or enclosure** as the
feature of interest and record the behavioural bout, interaction or session as the
observed phenomenon or result (this is how ADR-0006 models multi-animal events).
A process used as a feature of interest is inconsistent under the bridge. The
profile shapes raise a warning for it. Current HCMO examples are unaffected.

## The four narrower-than-SOSA classes

HCMO keeps its four specialisations; each is narrower than its SOSA counterpart
and carries HCMO machinery that a W3C class cannot. No class is retired.

- **`hcm-tech:Sensor`**: a device capturing signals about behaviour, physiology or
  the enclosure environment. Its material parent restricts it to physical
  devices; `sosa:Sensor` also admits agents and software.
- **`hcm-tech:Actuator`**: a device eliciting or perturbing behaviour, physiology
  or the monitored environment, explicitly typed as a material entity. Three
  properties depend on it (`hasActuator`, `hasModelNumber`, `communicatesWith`).
  The SOSA 2017 definition is "a device"; the HCMO class adds the HCM scope.
- **`hcm-obs:ObservationResult`**: an information artifact produced by a home-cage
  monitoring observation, with four subclasses (behavior, categorical, location
  table, quantity). A physical specimen can be a generic `sosa:Result` without
  being an `hcm-obs:ObservationResult`.
- **`hcm-env:EnvironmentalProperty`**: an environmental parameter measured,
  specified or controlled in home-cage monitoring, typed as a BFO quality.

## Using the profile

Load `dist/hcmo.owl`, the pinned BFO and IAO (see `external-vocabularies.yaml`),
the SOSA 2017 file, PROV-O, the two vendored alignments in
[`third_party/bfo-sosa-bridge/`](../third_party/bfo-sosa-bridge/README.md) and,
optionally, `ontology/profiles/external-upper-developer.ttl`. The simplest way is
the self-contained bundle:

```bash
python tooling/bridge_profile.py package     # writes build/bridge/protege/
```

The default release (`hcmo.yaml`, `dist/`) is unchanged by the profile.

## Unparseable upstream alignment

The published PROV-to-BFO file does not parse (undeclared `:` and `xsd:`
prefixes). HCMO vendors it verbatim plus a copy with exactly those two prefix
declarations prepended; CI proves the difference is only those lines. Results are
therefore "on the prefix-repaired alignment". The problem is reported upstream
([#44](https://github.com/BFO-Mappings/PROV-to-BFO/issues/44), fix proposed in
[#43](https://github.com/BFO-Mappings/PROV-to-BFO/pull/43)); the patch is dropped
as soon as the authors publish a parseable tag. Details: `third_party/bfo-sosa-bridge/README.md`.

## Quality gates

```bash
python tooling/bridge_profile.py check --bfo both
```

downloads and checksum-verifies the pinned inputs, then checks: vendored-file
integrity; profile declares no axiom and the default release is unchanged; no
unsatisfiable class (default and developer presentations, pinned and
alignment-target BFO); the positive examples are consistent; the seven probes in
`examples/profiles/bfo-sosa-bridge/probes.yaml` give their expected outcome;
**zero new named subsumptions** inside the HCMO, SOSA or BFO hierarchies; the
expected BFO placements; and the profile SHACL shapes. Every explicit disjointness
axiom the combination makes relevant is written to `build/bridge/*-disjointness.txt`
for review. The taxonomy check is finite; it is not a proof of conservative
extension.

## Limits

- Tested with HermiT through Owlready2 only. Replay in Protégé and ROBOT is an
  acceptance requirement (ADR-0005).
- The pinned BFO differs from the release the alignment targets by annotation-only
  triples; the check runs against both.
- The authors' optional RO and CCO mappings and the W3C bfo-prov mapping are not
  part of the chain and are untested.
- SOSA 2017 only. The SOSA/SSN 2023 edition is a Working Draft that deprecates
  `sosa:Result` and `sosa:ObservableProperty`; using it would need a new ADR.
- `sosa:Sample` is not placed by the pinned alignment (the live W3C file adds
  `sosa:Sample ⊑ prov:Entity`; the commit pinned with SOSA 2017 does not).
