# BFO / SOSA double hierarchy — decision package and work plan

Status: **proposal for the co-author vote.** Nothing here is an approved
ontology, claim, or generated-artifact change. No module under
`ontology/modules/` is modified on this branch.

Raised by: Philippe Rocca-Serra. Recorded in
[`meetings/CO-AUTHOR-MEETING-2026-09-18.md`](meetings/CO-AUTHOR-MEETING-2026-09-18.md)
section 2, action 2.

Scope of this document: (1) the verified current state, because two premises of
the meeting discussion turn out not to hold for the pinned artifacts;
(2) what option **(a) define equivalences between the two hierarchies** would
actually require, since that is the option expected to be put to the vote; and
(3) the work breakdown, gates, and fallbacks.

---

## 1. Verified current state

Every number below is reproducible from a clean checkout. The commands are in
[§1.5](#15-reproduction).

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

**Any** of the four options has to say what happens to these four classes.
Under (a) and (d) they gain a BFO process anchor by entailment; under (b) they
gain one by assertion or stay as they are, documented; under (c) with BFO
chosen they must be anchored by hand.

### 1.3 A second, identical question exists for PROV-O

`hcm:OperationalAssessment` and `hcm-tech:CalibrationActivity` are both
`BFO:0000015` **and** `prov:Activity`. Structurally this is the same question
as the SOSA one, and `docs/ALIGNMENTS.md` already answers it — "PROV-O remains
a cross-cutting provenance view," no equivalence asserted.

The vote must state whether the decision covers only BFO/SOSA or all external
dual anchors. Deciding BFO/SOSA in isolation leaves the repository with two
contradictory policies for the same modelling situation.

### 1.4 The disjointness premise does not hold for the pinned artifacts

This is the finding that should change the discussion.

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

**Consequences.**

- There is **no logical conflict in HCMO today**, and none appears even if a
  consumer loads full BFO 2020 and IAO alongside it. BFO's disjointness is
  real, but it cannot clash with SOSA classes that carry no axioms. The
  HermiT gate (`.github/workflows/reason.yml` → `tooling/reason.py`) passes
  for exactly this reason, and it would keep passing if we did nothing.
- The problem Philippe identified is therefore **presentational and
  pragmatic, not logical**: a class appears in two disconnected root trees in
  Protégé, WebVOWL, and the WIDOCO pages, and HCMO publishes no rule telling a
  consumer how to read that. That objection stands on its own and is worth
  fixing. It just is not the inconsistency risk it was discussed as.
- The direction of risk is **inverted** from the meeting's assumption. Doing
  nothing is logically safe. Asserting the bridge is what can introduce an
  inconsistency — see [§2.2](#22-the-load-bearing-risk).

### 1.5 Reproduction

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

## 2. What option (a) actually commits us to

### 2.1 Literal `owl:equivalentClass` is not defensible for any of the four pairs

Taking "define equivalences" at face value means asserting
`hcm-tech:Sensor owl:equivalentClass sosa:Sensor`, or
`sosa:Sensor owl:equivalentClass BFO:0000040`, or similar. Per pair:

| Pair | Verdict | Why |
| --- | --- | --- |
| `sosa:Sensor` ≡ `BFO:0000040` material entity | **False both ways** | SOSA defines a Sensor as a "Device, agent (including humans), or **software (simulation)**". A software sensor is an IAO information content entity, disjoint from material entity in BFO. Conversely a rock is a material entity and no sensor. |
| `sosa:Actuator` ≡ `BFO:0000040` | **False (⊒ direction)** | SOSA's Actuator is device-only, so `sosa:Actuator ⊑ BFO:0000040` is sound; the converse is not. Subsumption, not equivalence. |
| `sosa:ObservableProperty` ≡ `BFO:0000019` quality | **False** | SOSA's "observable quality (property, characteristic)" covers BFO dispositions, functions, and realizable entities generally, not just qualities. BFO qualities include unobservable ones. |
| `sosa:Result` ≡ `IAO:0000030` ICE | **False (⊒ direction)** | `sosa:Result` ⊑ ICE is defensible; ICE covers documents, plans, and specifications that are no observation result. |
| `hcm-tech:Sensor` ≡ `sosa:Sensor` | **False** | HCMO's Sensor is an HCM device; `sosa:Sensor` includes human eyes and simulations. |

So option (a), read literally, has no correct instantiation. Anyone
implementing it would have to either assert something false or silently
downgrade to subsumption.

### 2.2 The load-bearing risk

An equivalence or a downward subsumption from `sosa:Sensor` into
`BFO:0000040` does not just describe HCMO — it constrains **every** consumer
graph that uses SOSA, including graphs that have nothing to do with HCMO but
load our bridge. A consumer that types a video-tracking analysis pipeline as
`sosa:Sensor` (legitimate under the Recommendation) and as
`IAO:0000030`/`hcm-tech:Software` would become **inconsistent** the moment
full BFO is in the closure, because material entity and ICE are disjoint.

This inverts the current safety property. Today HCMO cannot make a downstream
graph inconsistent. Under a naive (a) it can. That risk is manageable — see
[§3.2](#32-phase-2--the-bridge-module) — but it must be stated in the motion,
not discovered after the release.

### 2.3 The defensible reading, and what it implies for the vote

The version of (a) that survives review is: **a separate, opt-in bridge module
asserting the strongest relation each pair actually supports** — which for all
four pairs is directional subsumption plus a SKOS mapping annotation, never
`owl:equivalentClass`.

Written out, the candidate axiom set is:

```turtle
# strength: subsumption, entailed by the source definitions
sosa:Actuator          rdfs:subClassOf BFO:0000040 .   # device-only definition
sosa:Result            rdfs:subClassOf IAO:0000030 .
sosa:Observation       rdfs:subClassOf BFO:0000015 .   # also fixes §1.2
sosa:ObservableProperty rdfs:subClassOf BFO:0000020 .  # SDC, not quality

# strength: NOT assertable — annotation only
sosa:Sensor            skos:closeMatch BFO:0000040 .   # software sensors excluded
```

Note what this means procedurally: **(a) as the group can actually implement it
is (d) "anchor SOSA inside BFO" with mapping annotations attached.** If the
co-authors vote (a), the implementer will deliver (d) plus an SSSOM row set. The
motion text in [§5](#5-motion-text-for-the-vote) says this explicitly so the
vote is not later read as authorising equivalence axioms that were never
written.

Note also `sosa:ObservableProperty ⊑ BFO:0000020` (specifically dependent
continuant), **not** `BFO:0000019` (quality). `BFO:0000020` is already in the
developer profile and the pinned BFO `used_terms`, but **not** in the
five-class default presentation, so the default upper view gains a sixth anchor
or the bridge stays developer-only. That is a genuine decision, not a detail.

---

## 3. Work breakdown

Phases 0–1 precede the vote. Phases 2–8 are conditional on (a) or (d) passing.
"Gate" means the command that must pass before the phase is done.

### 3.0 Phase 0 — decision package (before the vote) · ~0.5 day

1. Circulate Philippe's original comment verbatim, as the meeting action says,
   together with §1 of this document so the vote is taken against the verified
   artifact state rather than the remembered one.
2. Get an explicit answer to the three scope questions:
   - does the decision cover BFO/PROV dual anchors ([§1.3](#13-a-second-identical-question-exists-for-prov-o)) or only BFO/SOSA?
   - do the four SOSA-only observation classes get a BFO anchor ([§1.2](#12-the-observation-classes-are-sosa-only--the-current-state-is-not-even-consistently-double))?
   - does the bridge ship in the default release, or as an opt-in profile
     next to `external-upper-developer.ttl`?
3. Ask Philippe to confirm the disjointness finding in §1.4. If he was
   describing the SOSA/SSN 2023 Edition rather than the pinned 2017
   Recommendation, that is a separate and larger question — it would reopen
   ADR-0002's edition policy, and it should be split out rather than folded
   into this vote.

Owner: Damien. **No repository change.**

### 3.1 Phase 1 — ADR-0005 · ~0.5 day

Write `docs/decisions/ADR-0005-BFO-SOSA-BRIDGE-POLICY.md` following the shape
of ADR-0002: context, numbered decision, consequences. It must record the
mapping strength per pair, the explicit refusal of `owl:equivalentClass`, the
scope answers from Phase 0, and the vote itself (date, participants, outcome).

Gate: none (docs only). Blocks every later phase.

### 3.2 Phase 2 — the bridge module · ~1–1.5 days

New file `ontology/profiles/sosa-bfo-bridge.ttl`, its own
`owl:Ontology` IRI under `https://w3id.org/hcmo/ontology/external/`, following
the `external-upper.ttl` pattern: canonical IRIs only, source-faithful labels,
`dcterms:source` provenance per term.

- Assert the four/five subsumptions agreed in Phase 1. Do **not** re-mint any
  IRI, do **not** assert `owl:equivalentClass`, do **not** touch
  `hcm-*` term IRIs — the HCMO classes keep both parents, which become
  redundant-but-harmless once the bridge is loaded.
- Record every pair as an SSSOM row in
  `mappings/semantic/hcmo-external.sssom.tsv` with `predicate_id`,
  `mapping_justification`, `confidence`, and `review_status`, matching the
  existing rows. The `sosa:Sensor` pair is registry-only.
- Register the file and its terms in `external-vocabularies.yaml` under a new
  `sosa_bfo_bridge:` key, mirroring `developer_upper_profile:`. This requires
  a matching change in `tooling/external_vocab.py`, which checks the declared
  class set and hierarchy.
- Decide default vs. opt-in per Phase 0. Opt-in means the file is **excluded**
  from `hcmo.yaml` `modules:` — and note that `hcmo.yaml`'s shape is the
  downstream API, so adding a new top-level key there is itself a contract
  change and should be avoided; follow the developer-profile precedent of
  living outside the manifest.

Gate: `python tooling/build.py` produces no `dist/` diff if the bridge is
opt-in, or a reviewed diff if it is default.

### 3.3 Phase 3 — consistency and entailment gates · ~1 day

This phase is what buys down the [§2.2](#22-the-load-bearing-risk) risk, and it
is the part most likely to be skipped under time pressure. It should not be.

- Extend `tooling/reason.py` (or add a sibling) to run HermiT over
  **merged graph + bridge + full pinned BFO + full pinned IAO**, not just over
  `dist/hcmo.owl`. The current gate reasons over an import-free graph, so it
  cannot see the clash the bridge could create. Needs the BFO/IAO artifacts
  fetched by checksum from `external-vocabularies.yaml`; the fetch must be
  cached or vendored so CI stays offline-capable, matching how
  `tooling/validate.py` already validates the contract "without network
  access".
- Add a **negative probe** fixture: a software sensor typed
  `sosa:Sensor` + `hcm-tech:Software`, asserted to be inconsistent under the
  bridge and consistent without it. This is the executable statement of the
  cost we are accepting. The repo already uses this pattern — see the injected
  process-cycle probe in `tooling/validate.py` step 4 and the
  `abox-inferred-invalid.ttl` negative example.
- Add the entailment checks that the bridge is supposed to buy: every
  observation class entails `BFO:0000015`; `hcm-tech:Sensor` entails exactly
  one BFO top-level branch.
- Wire into `.github/workflows/reason.yml`.

Gate: `python tooling/reason.py` (extended) plus `python tooling/validate.py`.

### 3.4 Phase 4 — the four unanchored observation classes · ~0.5 day

If Phase 0 answers yes: either let `sosa:Observation ⊑ BFO:0000015` in the
bridge supply the anchor by entailment (preferred — no HCMO module changes), or
assert `BFO:0000015` directly on the four classes in `hcm-obs.ttl` if the
anchor must hold in the default release without the bridge loaded.

The second route is a semantic change to shipped classes and needs its own
`CHANGELOG.md` `### Changed` entry. The first does not.

Gate: `python tooling/build.py && python tooling/validate.py`, plus the
entailment check from Phase 3.

### 3.5 Phase 5 — presentation and documentation · ~1–1.5 days

This is where the user-facing complaint is actually answered.

- `docs/UPPER-LEVEL-VIEW.md` — add the reconciliation rule: what a consumer
  should do when a class sits under both trees, which tree the default
  release renders, and what loading the bridge changes. Resolve the
  `BFO:0000020` sixth-anchor question from [§2.3](#23-the-defensible-reading-and-what-it-implies-for-the-vote).
- `docs/ALIGNMENTS.md` — update the SOSA section and the claim-strength table.
  If Phase 0 scoped PROV-O in, update the PROV-O row too; if it scoped PROV-O
  out, say so explicitly so the divergence is deliberate.
- `docs/decisions/ADR-0002-SEMTS-SOSA-EDITION-POLICY.md` — add a pointer to
  ADR-0005. Do not edit its accepted decision text.
- `docs/README.md` — index the new ADR.
- WIDOCO output (`docs/widoco/`, `.github/workflows/docs.yml`) and the
  `webapp/` class browser — check how each renders a class with two named
  parents, and whether the bridge changes the rendered tree. This is the
  "misleads users in practice" part of the objection and it is the one that
  needs eyes on rendered output, not a passing test.

Gate: `python tooling/docs.py` if it regenerates anything; visual check of the
WIDOCO pages and the webapp tree.

### 3.6 Phase 6 — shapes, examples, competency questions · ~0.5–1 day

- Check `shapes/hcm-shapes.ttl` for constraints that target `sosa:` or `BFO:`
  classes and would change behaviour under RDFS inference with the bridge
  loaded — `tooling/validate.py` runs pySHACL with `inference` enabled, so a
  new superclass edge can change which shapes apply.
- Re-run the five manifest examples plus the ISA/STATO evidence graph and the
  round-trip fixture.
- Confirm the eleven `queries/cq-*.rq` still return the reviewed rows in
  `queries/competency_questions.yaml`. A new superclass edge can widen a
  `rdfs:subClassOf*` pattern and change an exact-answer row.
- Consider one new CQ that only the bridge can answer, e.g. "which HCMO
  observation classes are BFO processes" — otherwise the bridge has no
  executable justification in the repository.

Gate: `python tooling/validate.py`.

### 3.7 Phase 7 — manuscript · ~0.5 day

- `docs/paper/` — the Results section presents the upper-level design. It
  currently describes dual anchoring without stating a reconciliation rule.
- This connects to meeting item 3: the TBox/ABox/CBox distinction is exactly
  the vocabulary needed to say "the bridge is a TBox alignment, the SSSOM rows
  are a registry, neither is imported into the ABox evidence."
- Keep the claim at "implemented selective alignment" in the
  `docs/ALIGNMENTS.md` table. A bridge module is not formal profile
  conformance and must not be written up as one.

### 3.8 Phase 8 — release · ~0.5 day

- `CHANGELOG.md` entry. `### Added` for the bridge and ADR; `### Changed` only
  if Phase 4 took the assertion route. No `### Renamed` — nothing moves.
- Version: an opt-in bridge that leaves `dist/` byte-identical is additive and
  needs no `owl:versionIRI` bump. A default-release bridge changes the shipped
  entailments and **does** need a bump from `…/hcm/0.3.0`, coordinated with the
  release DOI.
- Commit `dist/` alongside the modules if anything regenerated; CI fails on a
  stale `dist/`.

### Summary

| Phase | Work | Est. |
| --- | --- | --- |
| 0 | Decision package, scope questions, confirm §1.4 with Philippe | 0.5 d |
| 1 | ADR-0005 | 0.5 d |
| 2 | Bridge module, SSSOM rows, external-vocab contract | 1–1.5 d |
| 3 | Reasoner gate over full BFO closure + negative probe | 1 d |
| 4 | Anchor the four observation classes | 0.5 d |
| 5 | UPPER-LEVEL-VIEW, ALIGNMENTS, WIDOCO, webapp | 1–1.5 d |
| 6 | Shapes, examples, CQs | 0.5–1 d |
| 7 | Manuscript | 0.5 d |
| 8 | Changelog, version, release | 0.5 d |
| | **Total after the vote** | **~5.5–7 days** |

Phase 3 is the critical path and the one that makes the difference between a
bridge that is safe for downstream users and one that is not.

---

## 4. If the vote goes another way

| Option | Work | Relative cost |
| --- | --- | --- |
| **(a) equivalences** | As above. Delivered as (d) + SSSOM annotations, since no pair supports literal equivalence. | ~5.5–7 d |
| **(b) accept double annotation, document reconciliation** | Phases 0, 1, 5, 7, 8 only. No bridge module, no new reasoner closure, no risk to consumers. Answers the "misleads users" objection with a published rule. Phase 4 still needs deciding on its own merits. | ~2.5–3 d |
| **(c) commit to one hierarchy** | The most invasive. Dropping SOSA parents breaks the `sosa:hasResult` / `sosa:hasFeatureOfInterest` / `sosa:observedProperty` restrictions the obs module is built on and contradicts ADR-0002; dropping BFO parents strands the five-anchor presentation and the developer profile. Either way it is a semantic change to shipped classes, needs deprecation handling, a version bump, and a rewrite of the SOSA section of the paper. | ~8–10 d, highest risk |
| **(d) anchor SOSA inside BFO** | Identical to (a) as implemented, minus the SSSOM annotation rows. | ~5–6.5 d |

**(b) is the cheapest option that fully answers the objection as stated**,
because the objection is presentational and §1.4 shows there is no logical
problem to fix. It is worth putting that on the table before the vote rather
than after it.

---

## 5. Motion text for the vote

> HCMO adopts a directional BFO/SOSA bridge. Where the pinned source
> definitions support it, SOSA classes are asserted as subclasses of canonical
> BFO/IAO classes in a dedicated bridge module with its own ontology IRI. No
> `owl:equivalentClass` axiom is asserted between a SOSA class and a BFO/IAO
> class, because no such pair is coextensive under the pinned 2017 SOSA
> Recommendation; pairs that cannot bear subsumption are recorded as SSSOM
> mapping rows only. HCMO class IRIs do not change and no term is deprecated.
> The bridge ships as **[default / opt-in — Phase 0]**. The decision covers
> **[BFO/SOSA only / all external dual anchors including PROV-O — Phase 0]**.
> A reasoner gate over the full pinned BFO and IAO closure, including a
> negative probe for the software-sensor case, is a precondition of merging.

---

## 6. Open questions the plan cannot settle

1. Default release or opt-in profile. Affects the version bump and every
   downstream consumer.
2. `sosa:ObservableProperty ⊑ BFO:0000020` adds a sixth anchor to a
   presentation deliberately designed around five.
3. Whether the four unanchored observation classes get their BFO anchor by
   entailment or by assertion.
4. Whether PROV-O is in scope.
5. Whether Philippe's disjointness remark referred to the SOSA/SSN 2023
   Edition. If so, that reopens ADR-0002 and belongs in a separate decision.
