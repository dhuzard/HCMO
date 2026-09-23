# Reply to Philippe Rocca-Serra — PROV-O → BFO paper (2026-09-23)

**Status:** draft reply, kept for reuse. Not yet sent.
Background and evidence:
[`../PROV-BFO-ALIGNMENT-PAPER-NOTES.md`](../PROV-BFO-ALIGNMENT-PAPER-NOTES.md).
Decisions referenced:
[`../BFO-SOSA-DECISIONS-TO-TAKE.md`](../BFO-SOSA-DECISIONS-TO-TAKE.md).

---

**Subject:** Re: PROV-O → BFO paper (Prudhomme et al. 2025) — what it gives HCMO

Hi Philippe,

Thanks for the paper, it arrived at exactly the right moment. Their PROV→BFO alignment, combined with the W3C's own SOSA→PROV alignment (SSN Rec. §6.5), gives us a **published SOSA→BFO route**. That route bears directly on the double-hierarchy decisions. We ran the combination through HermiT with HCMO 0.3.0 and our pinned BFO and SOSA. Full notes are in `docs/PROV-BFO-ALIGNMENT-PAPER-NOTES.md`. Here is what it could do for us, with concrete examples.

**1. A BFO anchor for our observation classes, with no change to HCMO.**
Once the chain is loaded, Behavior, Weight, Health Status and Environment Observation are all inferred to be BFO processes. That fixes Decision 7 with no edits to our modules. In practice, one query for "every process mouse X took part in" would return both OBI/ISA assays and HCM observations. Today it returns only the assays.

**2. A bridge without us making claims about W3C terms.**
Instead of HCMO asserting `sosa:Actuator ⊑ material entity` and similar statements, an opt-in profile would import two published artifacts: the authors' CC0 files and the W3C alignment. HCMO itself would say nothing about `sosa:*`, which answers the hijacking concern. It also follows the paper's own advice to reuse existing alignments rather than mint new ones.

**3. Mistakes in data that SOSA alone lets through.**
The authors found errors in the W3C PROV examples this way. Our tests found two HCM cases that pass today but are flagged under the chain:

- **A behavioural bout (a process) used as the feature of interest.** The chain gives `hasFeatureOfInterest ⊑ prov:used ⊑ has participant`, so the feature of interest must be a continuant. The correct target is the mouse; the bout should be the observed phenomenon.
- **A `hcm-tech:Software` individual typed directly as `sosa:Sensor`.** This clashes because software is an information entity and a sensor is inferred to be material. It shows up only with the developer upper-level profile loaded, because the default view files information entities directly under "entity". That is a reason to always test bridges under that profile.

**4. A citable answer for software sensors (Decision 3).**
The chain entails `sosa:Sensor ⊑ material entity`, the statement we were about to reject. The paper's position is that a software agent is *running* software, i.e. material. For a video-tracking pipeline that gives:

```turtle
ex:deeplabcut-v2.3   a hcm-tech:Software .                     # the code (information)
ex:tracker-run-cage7 a hcm-tech:Sensor ;                        # the deployed, running instance
    obo:RO_0000059   ex:deeplabcut-v2.3 .                       # concretizes
ex:obs42 a hcm-obs:BehaviorObservation ;
    sosa:madeBySensor ex:tracker-run-cage7 .
```

This is consistent under the chain. The Result statement is different: the chain gives only `sosa:Result ⊑ continuant`, which supports rejecting "Result is information" (physical samples stay valid).

**5. Provenance without extra modelling.**
Because `sosa:hasResult ⊑ prov:generated` and `sosa:madeBySensor ⊑ prov:wasAssociatedWith`, every HCM observation also becomes a PROV record. Calibration Activity → Sensor → Observation → Result → derived Time Series (`prov:wasDerivedFrom`, which the chain places under RO *causally influenced by*) forms a single graph. The ISA recording-provenance query could follow it without extra HCMO properties. It also means our Operational Assessment and Calibration Activity double parents (`BFO:0000015` and `prov:Activity`) become redundant rather than conflicting. That changes how Decision 8 should be justified: "already resolved by a published alignment", not "PROV is an orthogonal view".

**6. Their QA method in our CI.**
Whatever we decide, I'd like to adopt their checks for any bridge profile:

- **No hierarchy changes:** SOSA's own subclass tree and HCMO's must be the same with and without the bridge.
- **Example consistency:** `examples/` plus targeted probe instances like the ones above must stay consistent under the bridge.
- **Mapping records:** each bridge axiom gets a written justification and a label, exported as SSSOM (`semapv:ManualMappingCuration`) to `mappings/semantic/`.

**Caveats.** The SOSA→PROV alignment is non-normative. Their BFO release differs slightly from our pin. Our run used only the BFO file, without the CCO/RO files or the SWRL location rules.

**Three questions for you:**

1. Is the running-software pattern acceptable to you as the answer to the software-sensor objection? That decides whether the whole chain can be adopted, including the Sensor statement.
2. Are you comfortable with an opt-in profile that imports their alignment rather than HCMO asserting SOSA→BFO axioms itself?
3. (Still open from the decision sheet) Was your exclusivity remark about SOSA 2017 or the 2023 edition? The chain relies on the 2017 alignment, which matches our pin.

Best,
Damien
