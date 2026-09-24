# BFO / SOSA double hierarchy — decision package and work plan

> **2026-09-24 update:** co-authors voted for option (a) with (d) as fallback.
> The provisional position — reuse the published SOSA→PROV-O→BFO alignments in
> an opt-in, tested profile, with no direct equivalence — is recorded in
> [`meetings/CO-AUTHOR-EMAIL-REPLIES-2026-09-24.md`](meetings/CO-AUTHOR-EMAIL-REPLIES-2026-09-24.md)
> §4.2 and awaits Philippe's confirmation. It supersedes the narrowed Motion 2
> in §5 below where the two differ (notably on `sosa:Sensor`).

> **Correction (2026-09-24): `hcm-tech:Actuator` is kept.** Accepted review
> item A05 (Damien Huzard, 2026-07-21) retains it as the physical,
> home-cage-specific subclass of BFO material entity and `sosa:Actuator`,
> which also covers software and other systems; it is therefore narrower
> than the SOSA class. The "genuine near-duplicate" finding in §2.4, the
> Actuator deprecation in Phase 4 (§3.4) and its estimate, and Motion 3 as
> first drafted are superseded: no HCMO class is deprecated. A correction
> was sent to the co-authors on 2026-09-24.

Status: **proposal for the co-author vote.** Nothing here is an approved
ontology, claim, or generated-artifact change. No module under
`ontology/modules/` is modified on this branch.

Raised by: Philippe Rocca-Serra. Recorded in
[`meetings/CO-AUTHOR-MEETING-2026-09-18.md`](meetings/CO-AUTHOR-MEETING-2026-09-18.md)
section 2, action 2.

Scope of this document: (1) the verified current state; (2) a per-axiom review
of the concrete option (a) proposal ([§2](#2-the-option-a-proposal-as-tabled)),
which is expected to be put to the vote; and (3) the work breakdown, gates, and
fallbacks.

---

## 1. Verified current state

Every number below is reproducible from a clean checkout. The commands are in
[§1.6](#16-reproduction).

### 1.1 Only four classes are genuinely double-parented under BFO and SOSA

| HCMO class | BFO/IAO parent | SOSA parent |
| --- | --- | --- |
| `hcm-env:EnvironmentalProperty` | `BFO:0000019` quality | `sosa:ObservableProperty` |
| `hcm-obs:ObservationResult` | `IAO:0000030` information content entity | `sosa:Result` |
| `hcm-tech:Actuator` | `BFO:0000040` material entity | `sosa:Actuator` |
| `hcm-tech:Sensor` | `BFO:0000040` material entity | `sosa:Sensor` |

That is the entire BFO/SOSA overlap. It is four classes, not a pervasive
pattern.

### 1.2 The observation classes are SOSA-only — the current state is not even consistently double

`hcm-obs:BehaviorObservation`, `hcm-obs:EnvironmentObservation`,
`hcm-obs:HealthStatusObservation`, and `hcm-obs:WeightObservation` are
subclasses of `sosa:Observation` **and of nothing in BFO**. They have no upper
anchor on the OBO side at all.

This is a real defect independent of the vote, and it points the opposite way
from the complaint: the honest description of HCMO today is not "double
parenting everywhere" but "dual anchoring in four places, a missing BFO anchor
in four others." `docs/UPPER-LEVEL-VIEW.md` already concedes the gap — "the
Process / event anchor is available for navigation, but HCMO currently defines
no local process class" — which is true only because the observation classes
were never anchored there.

The tabled proposal fixes this, via `sosa:Observation ⊑ BFO:0000015`.

### 1.3 How load-bearing each of the four classes is

This matters for the deduplication rationale in
[§2.3](#23-the-deduplication-rationale-holds-for-one-class-of-the-four).

| Class | Domain of | Range of | HCMO subclasses | Other |
| --- | --- | --- | --- | --- |
| `hcm-tech:Sensor` | 7 properties | 2 properties | — | 4 union domains, 3 SHACL shapes, 7 example graphs, the ISA RO-Crate JSON |
| `hcm-tech:Actuator` | — | `hasActuator` | — | 2 union domains |
| `hcm-obs:ObservationResult` | `hasConfidenceScore` | — | `BehaviorResult`, `CategoricalResult`, `LocationResultTable`, `QuantityValue` | — |
| `hcm-env:EnvironmentalProperty` | — | 7 properties | — | — |

### 1.4 A second, identical question exists for PROV-O

`hcm:OperationalAssessment` and `hcm-tech:CalibrationActivity` are both
`BFO:0000015` **and** `prov:Activity`. Structurally this is the same question
as the SOSA one, and `docs/ALIGNMENTS.md` already answers it — "PROV-O remains
a cross-cutting provenance view," no equivalence asserted.

The vote must state whether the decision covers only BFO/SOSA or all external
dual anchors. Deciding BFO/SOSA in isolation leaves the repository with two
contradictory policies for the same modelling situation.

### 1.5 The disjointness premise is prospective, not current

**SOSA asserts no disjointness at all.** The pinned SOSA 2017 artifact
(`external-vocabularies.yaml` → `sosa-2017`, sha256 `c70b0d1c…a0392`) is 345
triples containing **zero** `owl:disjointWith` and **zero**
`owl:AllDisjointClasses`. All nine core classes — `Sensor`, `Actuator`,
`ObservableProperty`, `Result`, `Observation`, `FeatureOfInterest`, `Platform`,
`Procedure`, `Sampler` — are primitive roots with **no asserted superclass**.
The integrated `ssn.ttl` from the same commit also has zero disjointness. SOSA
is deliberately under-axiomatised; that is the design of the Recommendation.

**HCMO ships no disjointness either.** The merged graph (1397 triples,
identical in `dist/hcmo.ttl`) contains zero `owl:disjointWith`, zero
`owl:AllDisjointClasses`, zero `owl:equivalentClass`, and zero `owl:imports`.
`ontology/modules/external-upper.ttl` is a five-class flattened presentation;
`ontology/profiles/external-upper-developer.ttl` restores the intermediate
hierarchy but also asserts no disjointness.

So there is **no logical conflict in HCMO today**, and none appears even if a
consumer loads full BFO 2020 and IAO alongside it: BFO's disjointness is real,
but it cannot clash with SOSA classes that carry no axioms. The HermiT gate
(`.github/workflows/reason.yml` → `tooling/reason.py`) passes for exactly this
reason, and would keep passing if we did nothing.

**This does not make the concern wrong — it makes it prospective.** The tabled
proposal is precisely what would make BFO's disjointness bite the SOSA tree,
because it puts SOSA classes underneath disjoint BFO branches. Read that way,
the meeting's worry is a correct anticipation of the consequences of adopting
(a) or (d), not a description of the current release. The practical effect is
that the burden of proof sits on the bridge axioms, one at a time — which is
what [§2](#2-the-option-a-proposal-as-tabled) does.

Two things follow for the current release, independent of the vote:

- The user-visible problem today is **presentational**: a class appears in two
  disconnected root trees in Protégé, WebVOWL, and the WIDOCO pages, and HCMO
  publishes no rule telling a consumer how to read that.
- Doing nothing is logically safe. Asserting the bridge is what can introduce
  an inconsistency, in HCMO and in every downstream graph that loads it.

### 1.6 Reproduction

```bash
# 1. The four dual-parented classes, the SOSA-only classes, and the PROV pair
python - <<'PY'
import yaml, pathlib
from rdflib import Graph, RDF, RDFS, OWL, URIRef
g = Graph()
for m in yaml.safe_load(open('hcmo.yaml'))['modules']:
    g.parse(pathlib.Path(m), format='turtle')
fams = {'http://purl.obolibrary.org/obo/BFO_':'BFO',
        'http://purl.obolibrary.org/obo/IAO_':'IAO',
        'http://www.w3.org/ns/sosa/':'SOSA',
        'http://www.w3.org/ns/prov#':'PROV'}
for s in sorted(set(g.subjects(RDF.type, OWL.Class))):
    if not str(s).startswith('https://w3id.org/hcmo/ontology/hcm'):
        continue
    seen = {n for o in g.objects(s, RDFS.subClassOf) if isinstance(o, URIRef)
            for p, n in fams.items() if str(o).startswith(p)}
    if len(seen) > 1:
        print(sorted(seen), s)
print('disjointWith:', len(list(g.triples((None, OWL.disjointWith, None)))))
print('equivalentClass:', len(list(g.triples((None, OWL.equivalentClass, None)))))
PY

# 2. The pinned SOSA artifact carries no disjointness
curl -sSL -o /tmp/sosa.ttl \
  https://raw.githubusercontent.com/w3c/sdw/6dc6059362b82955707937401d8d3db340429293/ssn/integrated/sosa.ttl
sha256sum /tmp/sosa.ttl   # must equal external-vocabularies.yaml sosa-2017
grep -c -i disjoint /tmp/sosa.ttl   # 0
```

---

## 2. The option (a) proposal as tabled

The proposal has two independent parts. They should be voted separately,
because one is cheap and uncontroversial and the other is not.

> **Part 1 — reporting.** Distinguish reuse for ontology metadata tracking
> (annotation properties: `dcterms`, `schema.org` contributor/creator) from
> reuse of types/classes, object properties, and data properties.
>
> **Part 2 — axioms.** Assert `sosa:Actuator` under material entity,
> `sosa:Sensor` under material entity, `sosa:Observation` under process, and
> `sosa:Result` under information entity.
>
> **Rationale for part 2.** Avoid having two URIs for the same entity:
> `http://www.w3.org/ns/sosa/Actuator` and `…/hcm/tech#Actuator`.

Part 2 is option **(d)** "anchor SOSA inside BFO" written out as axioms, plus a
deduplication goal that (d) alone does not imply. The label matters less than
the content, but the ADR should record it as (d)+dedup so the minutes and the
implementation agree.

### 2.1 Part 1 is right and should be adopted regardless of the vote

`docs/ALIGNMENTS.md` currently lists Schema.org as "Implemented selective reuse
— Contributor, place, and exchange terms" in the same table as BFO/IAO and SOSA
class reuse. That flattens two different kinds of commitment: reusing
`schema:creator` to describe the ontology is a metadata choice with no
semantic consequence for HCM data, whereas placing `hcm-tech:Sensor` under
`sosa:Sensor` constrains every instance graph.

Splitting the claim-strength table by reuse *kind* — annotation properties,
classes, object properties, data properties — is a documentation change with no
axiom impact. It sharpens the paper's reuse claims and costs well under a day.
It is listed as [Phase 5a](#35-phase-5--presentation-and-documentation--115-days).

### 2.2 Part 2, axiom by axiom against the pinned source

Two of the four hold. Two do not.

| Proposed axiom | Verdict | Evidence from the pinned SOSA 2017 artifact |
| --- | --- | --- |
| `sosa:Actuator ⊑ BFO:0000040` material entity | **Sound** | Definition is device-only: "A device that is used by, or implements, an (Actuation) Procedure that changes the state of the world." |
| `sosa:Observation ⊑ BFO:0000015` process | **Sound, and valuable** | An Observation is an act carried out over time. This is also the axiom that repairs the four unanchored observation classes in [§1.2](#12-the-observation-classes-are-sosa-only--the-current-state-is-not-even-consistently-double). |
| `sosa:Sensor ⊑ BFO:0000040` material entity | **Unsound** | Definition: "**Device, agent (including humans), or software (simulation)** involved in, or implementing, a Procedure." Software is an IAO information content entity, which BFO makes disjoint from material entity. |
| `sosa:Result ⊑ IAO:0000030` information entity | **Unsound** | `sosa:Result` is "The Result of an Observation, Actuation, or **act of Sampling**", and SOSA states "A Sample is the result from an act of Sampling" and "Physical samples are sometimes known as 'specimens'", with the example "Crushing a rock sample in a ball mill." A physical specimen is a material entity, disjoint from ICE. |

The two unsound axioms are not abstract risks. Each one makes a real graph
inconsistent the moment full BFO is in the closure:

- **`sosa:Sensor`.** HCMO itself declares `hcm-tech:Software ⊑ IAO:0000030`. A
  video-tracking component that both implements a sensing procedure and is
  software — an ordinary HCM configuration — becomes inconsistent in HCMO's
  own vocabulary. The breakage is not confined to third parties.
- **`sosa:Result`.** Any consumer graph that carries a physical specimen
  through `sosa:hasResult` breaks. HCMO does not do this today, but SOSA
  explicitly licenses it, and the axiom would be published as a statement
  about the W3C class, not about HCMO's use of it.

**Safe restatements.** Both can be kept if narrowed to the HCMO term, which is
what HCMO actually means:

```turtle
# instead of  sosa:Sensor ⊑ BFO:0000040
hcm-tech:Sensor  rdfs:subClassOf BFO:0000040, sosa:Sensor .   # i.e. unchanged
sosa:Sensor      skos:closeMatch BFO:0000040 .                # registry note only

# instead of  sosa:Result ⊑ IAO:0000030
hcm-obs:ObservationResult rdfs:subClassOf IAO:0000030, sosa:Result .  # unchanged
```

That is: for `Sensor` and `Result`, the existing double parenting **is** the
correct modelling. HCMO's classes are narrower than SOSA's in exactly the way
that makes the BFO anchor true of them and false of their SOSA parents.

### 2.3 The fourth dual-parented class is missing from the list

`hcm-env:EnvironmentalProperty` is `BFO:0000019` + `sosa:ObservableProperty`,
and no axiom is proposed for `sosa:ObservableProperty`. The list therefore
resolves at most three of the four cases in [§1.1](#11-only-four-classes-are-genuinely-double-parented-under-bfo-and-sosa).

If it is added, the target should be `BFO:0000020` **specifically dependent
continuant**, not `BFO:0000019` quality: SOSA's "observable quality (property,
characteristic)" covers dispositions and functions, which are BFO realizables,
not qualities. `BFO:0000020` is already in the pinned BFO `used_terms` and in
the developer profile, but **not** in the five-class default presentation — so
adding it either introduces a sixth default anchor or keeps the bridge
developer-only. That is a genuine decision, not a detail.

### 2.4 The deduplication rationale holds for one class of the four

"Two URIs for the same entity" is the strongest argument in the proposal, and
it is correct — for `Actuator`. For the others the two URIs do not denote the
same entity, and the table in [§1.3](#13-how-load-bearing-each-of-the-four-classes-is) shows
what retiring them would cost:

- **`hcm-tech:Actuator` — genuine near-duplicate.** No HCMO subclasses, not the
  domain of anything, only the range of `hasActuator` and a member of two union
  domains. Its definition adds "elicits or perturbs behavior, physiology, or
  the monitored environment", which is HCM scoping that could live as a
  comment. **Deprecating it in favour of `sosa:Actuator` is cheap and defensible.**
- **`hcm-tech:Sensor` — not a duplicate.** `sosa:Sensor` includes human eyes and
  simulations; HCMO's is an HCM device. It is the domain of 7 HCMO properties
  and the range of 2, the target of 3 SHACL shapes, and instantiated in 7
  example graphs plus the ISA RO-Crate JSON. Retiring it re-points all of those
  onto a W3C class and loses the narrowing that makes the BFO anchor true.
- **`hcm-obs:ObservationResult` — not a duplicate.** It has four HCMO
  subclasses and is the domain of `hasConfidenceScore`.
- **`hcm-env:EnvironmentalProperty` — not a duplicate.** Range of 7 HCMO
  properties.

A defensible dedup scope is therefore: **deprecate `hcm-tech:Actuator`, keep
the other three.** Under `AGENTS.md` that is deprecation with
`dcterms:isReplacedBy sosa:Actuator` and a `hcm-compat.ttl` entry, never
deletion, and it needs a `### Renamed` changelog section.

### 2.5 Packaging: these axioms must not ship in the default graph

Asserting `rdfs:subClassOf` on `sosa:*` URIs adds axioms to terms HCMO does not
own, which then propagate to everyone who loads the HCMO file — the pattern the
linked-data literature calls *ontology hijacking*. This is not a reason to
refuse the proposal; it is a reason to package it as a separate bridge ontology
with its own IRI that consumers opt into, exactly as
`ontology/profiles/external-upper-developer.ttl` is packaged today. Shipping it
inside `dist/hcmo.ttl` would make every HCMO consumer silently inherit a
contested alignment with a W3C Recommendation.

### 2.6 What this means for the vote

The motion should be narrowed before it is put, not after:

1. **Adopt part 1** (annotation vs. class/property reuse reporting)
   unconditionally — it is a reporting fix with no axiom impact.
2. **Adopt `sosa:Observation ⊑ BFO:0000015` and
   `sosa:Actuator ⊑ BFO:0000040`** in an opt-in bridge module. Both are
   entailed by the pinned definitions, and the first repairs a real gap.
3. **Do not assert `sosa:Sensor ⊑ BFO:0000040` or
   `sosa:Result ⊑ IAO:0000030`.** Record both as SSSOM `closeMatch` rows.
   Keep the existing double parenting on the HCMO classes, which is where the
   material-entity and ICE claims are actually true.
4. **Decide `sosa:ObservableProperty` separately**, with `BFO:0000020` as the
   target if it is adopted.
5. **Scope the dedup to `hcm-tech:Actuator`.**

Under that motion the double parenting on `Sensor`, `Result`, and
`EnvironmentalProperty` **remains**, so [Phase 5](#35-phase-5--presentation-and-documentation--115-days)
still has to publish the reconciliation rule. The bridge reduces the problem;
it does not remove it.

---

## 3. Work breakdown

Phases 0–1 precede the vote. Phases 2–8 are conditional on the outcome.
"Gate" means the command that must pass before the phase is done. Estimates
assume the narrowed motion in [§2.6](#26-what-this-means-for-the-vote); the
unnarrowed version is larger and carries the [§2.2](#22-part-2-axiom-by-axiom-against-the-pinned-source)
breakage.

### 3.0 Phase 0 — decision package (before the vote) · ~0.5 day

1. Circulate Philippe's comment verbatim, as the meeting action says, together
   with §1 and §2 of this document, so the vote is taken against the verified
   artifact state and the per-axiom review.
2. Put the two unsound axioms to Philippe directly with the source quotes from
   [§2.2](#22-part-2-axiom-by-axiom-against-the-pinned-source). If he intends
   them anyway — e.g. on the view that HCMO should not serve consumers who
   type software as `sosa:Sensor` — that is a legitimate call for the group,
   but it must be made knowingly and recorded in the ADR.
3. Get explicit answers to the scope questions in [§6](#6-open-questions-the-plan-cannot-settle).

Owner: Damien. **No repository change.**

### 3.1 Phase 1 — ADR-0005 · ~0.5 day

Write `docs/decisions/ADR-0005-BFO-SOSA-BRIDGE-POLICY.md` following the shape
of ADR-0002: context, numbered decision, consequences. It must record the
per-axiom verdicts including the rejected ones and why, the dedup scope, the
default-vs-opt-in answer, and the vote itself (date, participants, outcome).

Gate: none (docs only). Blocks every later phase.

### 3.2 Phase 2 — the bridge module · ~1–1.5 days

New file `ontology/profiles/sosa-bfo-bridge.ttl` with its own `owl:Ontology`
IRI under `https://w3id.org/hcmo/ontology/external/`, following the
`external-upper.ttl` pattern: canonical IRIs only, source-faithful labels,
`dcterms:source` provenance per term.

- Assert only the axioms agreed in Phase 1. Do not re-mint any IRI, and do not
  assert `owl:equivalentClass` — no BFO/SOSA pair is coextensive.
- Record every pair as an SSSOM row in
  `mappings/semantic/hcmo-external.sssom.tsv`, matching the existing rows. The
  `sosa:Sensor` and `sosa:Result` pairs are registry-only.
- Register the file and its terms in `external-vocabularies.yaml` under a new
  `sosa_bfo_bridge:` key mirroring `developer_upper_profile:`, with the
  matching check in `tooling/external_vocab.py`.
- Keep it **out** of `hcmo.yaml` `modules:` per [§2.5](#25-packaging-these-axioms-must-not-ship-in-the-default-graph).
  Note that `hcmo.yaml`'s shape is the downstream API, so adding a top-level
  key there is itself a contract change; follow the developer-profile
  precedent of living outside the manifest.

Gate: `python tooling/build.py` produces no `dist/` diff (opt-in), or a
reviewed diff (default).

### 3.3 Phase 3 — consistency and entailment gates · ~1 day

This is what buys down the [§2.2](#22-part-2-axiom-by-axiom-against-the-pinned-source)
risk, and it is the part most likely to be skipped under time pressure.

- Extend `tooling/reason.py` (or add a sibling) to run HermiT over
  **merged graph + bridge + full pinned BFO + full pinned IAO**. The current
  gate reasons over an import-free graph, so it structurally cannot see the
  clash the bridge could create. Needs the BFO/IAO artifacts fetched by
  checksum from `external-vocabularies.yaml`, cached or vendored so CI stays
  offline-capable, matching how `tooling/validate.py` already validates the
  contract "without network access".
- Add **negative probes** for the two rejected axioms: a software sensor typed
  `sosa:Sensor` + `hcm-tech:Software`, and a physical specimen reached through
  `sosa:hasResult`. Both must stay consistent under the adopted bridge. If the
  group adopts the unsound axioms anyway, these same probes become the
  executable statement of the cost accepted. The repo already uses this
  pattern — see the injected process-cycle probe in `tooling/validate.py`
  step 4 and `examples/abox-inferred-invalid.ttl`.
- Add the entailment checks the bridge is supposed to buy: every observation
  class entails `BFO:0000015`; `hcm-tech:Actuator` entails exactly one BFO
  top-level branch.
- Wire into `.github/workflows/reason.yml`.

Gate: `python tooling/reason.py` (extended) plus `python tooling/validate.py`.

### 3.4 Phase 4 — deprecate `hcm-tech:Actuator` · ~0.5–1 day

Only if the dedup scope in [§2.4](#24-the-deduplication-rationale-holds-for-one-class-of-the-four)
is approved.

- `owl:deprecated true` + `dcterms:isReplacedBy sosa:Actuator` on
  `hcm-tech:Actuator`, with the HCM scoping preserved as a comment. Never
  delete: `AGENTS.md` safety rail.
- Re-point `hcm-tech:hasActuator`'s range and the two union domains.
- Add the migration row to `hcm-compat.ttl` and the replacement to the
  migration guide.
- Update `examples/` and `ontology/context.jsonld`.
- `### Renamed` changelog section, as `hcm-tech:Actuator -> sosa:Actuator`.

Gate: `python tooling/build.py && python tooling/validate.py`.

### 3.5 Phase 5 — presentation and documentation · ~1–1.5 days

This is where the user-facing complaint is actually answered, and per
[§2.6](#26-what-this-means-for-the-vote) it is still needed after the bridge,
because `Sensor`, `Result`, and `EnvironmentalProperty` stay double-parented.

- **5a.** Split the `docs/ALIGNMENTS.md` claim-strength table by reuse kind —
  annotation property, class, object property, data property — per
  [§2.1](#21-part-1-is-right-and-should-be-adopted-regardless-of-the-vote).
  Carry the same split into the paper's reuse claims. Adopt regardless of the
  vote on part 2.
- `docs/UPPER-LEVEL-VIEW.md` — add the reconciliation rule: what a consumer
  does when a class sits under both trees, which tree the default release
  renders, and what loading the bridge changes.
- `docs/ALIGNMENTS.md` SOSA section — the per-axiom verdicts and the two
  registry-only pairs. If Phase 0 scoped PROV-O in, update that row; if it
  scoped PROV-O out, say so explicitly so the divergence is deliberate.
- `docs/decisions/ADR-0002-SEMTS-SOSA-EDITION-POLICY.md` — add a pointer to
  ADR-0005. Do not edit its accepted decision text.
- `docs/README.md` — index the new ADR.
- WIDOCO output (`docs/widoco/`, `.github/workflows/docs.yml`) and the
  `webapp/` class browser — check how each renders a class with two named
  parents and what the bridge changes. This is the "misleads users in
  practice" part of the objection, and it needs eyes on rendered output, not a
  passing test.

Gate: `python tooling/docs.py` if it regenerates anything; visual check of the
WIDOCO pages and the webapp tree.

### 3.6 Phase 6 — shapes, examples, competency questions · ~0.5–1 day

- Check `shapes/hcm-shapes.ttl` for constraints targeting `sosa:` or `BFO:`
  classes whose behaviour changes under RDFS inference with the bridge loaded —
  `tooling/validate.py` runs pySHACL with inference enabled, so a new
  superclass edge can change which shapes apply. The three shapes targeting
  `hcm-tech:Sensor` are the ones to check first.
- Re-run the five manifest examples, the ISA/STATO evidence graph, and the
  round-trip fixture.
- Confirm the eleven `queries/cq-*.rq` still return the reviewed rows in
  `queries/competency_questions.yaml`. A new superclass edge can widen a
  `rdfs:subClassOf*` pattern and change an exact-answer row.
- Add one CQ only the bridge can answer — e.g. "which HCMO observation classes
  are BFO processes" — otherwise the bridge has no executable justification in
  the repository.

Gate: `python tooling/validate.py`.

### 3.7 Phase 7 — manuscript · ~0.5 day

- `docs/paper/` Results — the upper-level design currently describes dual
  anchoring without a reconciliation rule.
- Connects to meeting item 3: TBox/ABox/CBox is exactly the vocabulary for
  "the bridge is a TBox alignment, the SSSOM rows are a registry, neither is
  imported into the ABox evidence."
- Keep the claim at "implemented selective alignment" in the
  `docs/ALIGNMENTS.md` table. A bridge module is not formal profile
  conformance and must not be written up as one.

### 3.8 Phase 8 — release · ~0.5 day

- `CHANGELOG.md`: `### Added` for the bridge and ADR; `### Renamed` only if
  Phase 4 runs.
- Version: an opt-in bridge leaving `dist/` byte-identical is additive and
  needs no `owl:versionIRI` bump. Phase 4 changes a shipped class and **does**
  need a bump from `…/hcm/0.3.0`, coordinated with the release DOI.
- Commit `dist/` alongside the modules; CI fails on a stale `dist/`.

### Summary

| Phase | Work | Est. |
| --- | --- | --- |
| 0 | Decision package, put the two unsound axioms to Philippe, scope questions | 0.5 d |
| 1 | ADR-0005 | 0.5 d |
| 2 | Bridge module, SSSOM rows, external-vocab contract | 1–1.5 d |
| 3 | Reasoner gate over full BFO closure + two negative probes | 1 d |
| 4 | Deprecate `hcm-tech:Actuator` (if scoped in) | 0.5–1 d |
| 5 | Reuse-kind table split, UPPER-LEVEL-VIEW, ALIGNMENTS, WIDOCO, webapp | 1–1.5 d |
| 6 | Shapes, examples, CQs | 0.5–1 d |
| 7 | Manuscript | 0.5 d |
| 8 | Changelog, version, release | 0.5 d |
| | **Total after the vote** | **~6–7.5 days** |

Phase 3 is the critical path and the difference between a bridge that is safe
for downstream users and one that is not.

---

## 4. If the vote goes another way

| Option | Work | Relative cost |
| --- | --- | --- |
| **(a)/(d) as narrowed in [§2.6](#26-what-this-means-for-the-vote)** | As above. Two axioms, opt-in bridge, one deprecation, reconciliation rule still published. | ~6–7.5 d |
| **(a) unnarrowed** | Adds the two unsound axioms. Costs the same to build but ships a known inconsistency for software sensors and physical samples, and needs an explicit, recorded acceptance of that. | ~6–7.5 d, higher risk |
| **(b) accept double annotation, document reconciliation** | Phases 0, 1, 5, 7, 8. No bridge module, no new reasoner closure, no risk to consumers. Answers the "misleads users" objection with a published rule. The §1.2 gap and part 1 still need deciding on their own merits. | ~2.5–3 d |
| **(c) commit to one hierarchy** | Most invasive. Dropping SOSA parents breaks the `sosa:hasResult` / `hasFeatureOfInterest` / `observedProperty` restrictions the obs module is built on and contradicts ADR-0002; dropping BFO parents strands the five-anchor presentation and the developer profile. Either way it is a semantic change to shipped classes needing deprecations, a version bump, and a rewrite of the paper's SOSA section. | ~8–10 d, highest risk |

Note that part 1 of the proposal ([§2.1](#21-part-1-is-right-and-should-be-adopted-regardless-of-the-vote))
is orthogonal to all four and should be adopted whatever happens.

---

## 5. Motion text for the vote

> **Motion 1 (reporting).** HCMO reports external reuse split by reuse kind —
> annotation properties used for ontology metadata, versus classes, object
> properties, and data properties used in HCM semantics — in
> `docs/ALIGNMENTS.md` and in the resource paper.
>
> **Motion 2 (bridge).** HCMO adopts a directional BFO/SOSA bridge in a
> dedicated opt-in module with its own ontology IRI, asserting
> `sosa:Observation ⊑ BFO:0000015` and `sosa:Actuator ⊑ BFO:0000040`. HCMO does
> **not** assert `sosa:Sensor ⊑ BFO:0000040` or `sosa:Result ⊑ IAO:0000030`,
> because the pinned 2017 SOSA Recommendation defines a Sensor as a "device,
> agent (including humans), or software" and a Result as including the physical
> specimen produced by an act of Sampling; both pairs are recorded as SSSOM
> `closeMatch` rows instead, and the corresponding HCMO classes keep their
> existing BFO/IAO and SOSA parents. No `owl:equivalentClass` axiom is asserted
> between a SOSA class and a BFO/IAO class. A reasoner gate over the full
> pinned BFO and IAO closure, with negative probes for the software-sensor and
> physical-sample cases, is a precondition of merging.
>
> **Motion 3 (deduplication) — corrected 2026-09-24.** Duplicate terms are
> decided by meaning, not by name. `hcm-tech:Actuator`, `hcm-tech:Sensor`,
> `hcm-obs:ObservationResult`, and `hcm-env:EnvironmentalProperty` are all
> narrower than their SOSA counterparts and carry HCMO commitments, so all are
> retained and documented; no HCMO class is deprecated (see A05).
>
> **Open to the floor:** whether `sosa:ObservableProperty ⊑ BFO:0000020` is
> added, and whether the decision extends to the BFO/PROV-O dual anchors.

---

## 6. Open questions the plan cannot settle

1. Whether Philippe accepts the two unsound-axiom findings in
   [§2.2](#22-part-2-axiom-by-axiom-against-the-pinned-source), or intends
   those axioms knowingly.
2. Default release or opt-in profile. Affects the version bump and every
   downstream consumer.
3. Whether `sosa:ObservableProperty ⊑ BFO:0000020` is added — it puts a sixth
   anchor into a presentation deliberately designed around five.
4. How far the deduplication goes beyond `hcm-tech:Actuator`.
5. Whether PROV-O dual anchors are in scope.
6. Whether the disjointness remark referred to the SOSA/SSN 2023 Edition. If
   so, that reopens ADR-0002 and belongs in a separate decision.
