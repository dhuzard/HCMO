# BFO / SOSA double hierarchy — decisions to take

**Working document for the co-authors.** Nothing here has been implemented.

> **2026-09-24 update:** vote received — option (a) preferred by all four
> respondents, with (d) as fallback. Provisional position and the five points
> put to Philippe:
> [`meetings/CO-AUTHOR-EMAIL-REPLIES-2026-09-24.md`](meetings/CO-AUTHOR-EMAIL-REPLIES-2026-09-24.md) §4.2.
This is the list of choices that need a collective answer, written for readers
who are not ontology engineers.

The technical evidence behind every claim is in
[`BFO-SOSA-DOUBLE-HIERARCHY-PLAN.md`](BFO-SOSA-DOUBLE-HIERARCHY-PLAN.md).
This document is the decision sheet; that one is the workings.

Origin: Philippe Rocca-Serra's comment, recorded in
[`meetings/CO-AUTHOR-MEETING-2026-09-18.md`](meetings/CO-AUTHOR-MEETING-2026-09-18.md)
section 2.

---

## Plain-language background

### The two classification systems we use

HCMO describes home-cage monitoring. To make our terms understandable to other
systems, we hang them under two existing vocabularies:

- **BFO** (Basic Formal Ontology) is the top-level scheme used across
  biomedical ontologies — the OBO Foundry world that OBI, STATO, and most
  life-science ontologies live in. It sorts everything into a handful of
  buckets that **cannot overlap**: physical objects, information, qualities,
  and processes. A thing is in exactly one of them.
- **SOSA** is a W3C web standard for sensors, observations, and results. It
  comes from the engineering and web-of-things world. It is deliberately
  loose: it says almost nothing about what its terms are, so that anyone can
  use them.

So HCMO speaks to two communities at once, which is intentional and is part of
the resource's value.

### What "double parenting" means, and why Philippe flagged it

"Parent" here means "is a kind of". Four of our classes currently declare two
parents, one from each scheme:

| Our class | is a kind of… (BFO) | …and a kind of (SOSA) |
| --- | --- | --- |
| Environmental Property | quality | Observable Property |
| Observation Result | information | Result |
| Actuator | physical object | Actuator |
| Sensor | physical object | Sensor |

When someone opens HCMO in a browsing tool (Protégé, WebVOWL, our WIDOCO
pages), these classes appear **twice**, in two unconnected family trees, with
no explanation of how the two views relate. That is Philippe's objection, and
it is a fair one: a user has no published rule for reading it.

### The thing that was assumed but turns out not to be true

The meeting discussed this as a *logical* problem: both schemes declare their
branches mutually exclusive, so a class in two of them should be a
contradiction.

We checked the actual files. **SOSA declares no exclusivity at all** — the
pinned 2017 SOSA file is 345 statements with zero exclusivity rules, and its
core classes have no parents of their own. And **HCMO itself ships no
exclusivity rules either**. So there is no contradiction in HCMO today, and
none appears even when someone loads the full BFO alongside it. Our automated
logic checker passes, and would keep passing if we changed nothing.

**But the concern was right about the future.** The fix that was proposed — put
the SOSA classes underneath BFO buckets — is *precisely* what would make BFO's
exclusivity rules apply to SOSA terms for the first time. So the worry was a
correct prediction of what adopting the fix would do, not a description of
today.

The practical upshot: **doing nothing is logically safe; it is the fix that
carries the risk.** That inverts how this was framed in the meeting, and it is
why each proposed statement below has to be checked one at a time.

### What "breaking" actually looks like

If we assert something that isn't true of a shared vocabulary, an automated
reasoner concludes the data contradicts itself. Downstream tools can then
reject the **entire** dataset, not just the offending part. And because these
statements would be about W3C's terms rather than ours, the breakage would
reach people who use SOSA and have never heard of HCMO — as long as they load
our file.

That is manageable (see Decision 5), but it is why "just add the four lines"
isn't safe as written.

---

## The proposal on the table

Philippe's option (a) has two separate parts. They should be voted separately,
because one is easy and one is not.

**Part 1 — how we report our reuse.** Distinguish vocabularies we use for
*bookkeeping about the ontology file* (who wrote it, who contributed — the
`dcterms` and `schema.org` terms) from vocabularies we use for *the actual
science* (classes and relations that constrain real data).

**Part 2 — four new statements:**

1. SOSA Actuator is a kind of physical object
2. SOSA Sensor is a kind of physical object
3. SOSA Observation is a kind of process
4. SOSA Result is a kind of information

**The reason given:** avoid having two web addresses for the same thing — both
`sosa:Actuator` and our own `hcm-tech:Actuator` exist, which is duplication.

---

## The decisions

Nine decisions. Three are quick, six need discussion. Recommendations are mine
and are open to being overruled — the point is that each gets answered
explicitly rather than by default.

---

### Decision 1 — Adopt the reporting split? (Part 1)

**Question.** Do we report "vocabulary used for file metadata" separately from
"vocabulary used for scientific meaning"?

**Context in lay terms.** Our alignments table currently lists Schema.org
contributor terms in the same breath as our BFO and SOSA class commitments.
Those are very different promises. Using `schema:creator` to record who wrote
the ontology commits us to nothing about mice, cages, or sensors. Putting our
Sensor class under SOSA's Sensor constrains every dataset anyone ever
publishes with HCMO. Reporting them the same way overstates the first and
undersells the care taken over the second.

**Options.** Adopt / don't adopt.

**Recommendation: adopt.** It is a documentation change with no effect on any
axiom, it makes the paper's reuse claims more precise, and it is independent
of everything else on this list. Under a day of work.

---

### Decision 2 — Do we build the bridge at all?

**Question.** Do we go ahead with the general approach of anchoring SOSA
terms inside BFO (options a/d), or do we instead simply document how to read
the double parenting (option b), or drop one of the two schemes (option c)?

**Context in lay terms.** The user-visible complaint is "this is confusing and
unexplained." There are two ways to answer that: *explain it*, or *restructure
it so there is less to explain*. Since we established there is no logical
problem to fix today, explaining is a genuinely complete answer to the
objection as stated, and it is a third of the cost.

The case for restructuring anyway: it genuinely bridges the OBO Foundry and
W3C worlds, which is a contribution the paper can claim, and it fixes a real
gap (see Decision 7). The case against: it commits us to statements about
someone else's vocabulary, permanently.

**Options.**

| | What it means | Cost | Risk |
| --- | --- | --- | --- |
| **a/d — build the bridge** | Anchor the sound SOSA terms under BFO, in a separate opt-in file | ~6–7.5 days | Medium; see Decisions 3–5 |
| **b — document only** | Publish the reconciliation rule, change no axioms | ~2.5–3 days | None |
| **c — drop one scheme** | Commit to BFO or SOSA alone | ~8–10 days | High — breaks our observation model or our upper-level presentation |

**Recommendation: a/d, but narrowed** as per Decisions 3 and 4. Note that
option (c) is not really available: dropping SOSA would break the
`sosa:hasResult` / `hasFeatureOfInterest` / `observedProperty` machinery the
whole observation module is built on, and contradicts ADR-0002. If the group
wants the cheapest honest answer, (b) is defensible and I would not argue hard
against it.

**Note either way:** the bridge does *not* remove the double parenting for
Sensor, Result, and Environmental Property (see Decision 3). So the
reconciliation rule from option (b) has to be written regardless. We are
choosing whether to do (b), or (b) *plus* the bridge.

---

### Decision 3 — Which of the four statements do we actually assert?

**This is the substantive one.** We checked each against the official SOSA
file.

**Two are correct and can be adopted:**

- ✅ **SOSA Actuator is a physical object.** SOSA defines an actuator as "a
  device", full stop. Safe.
- ✅ **SOSA Observation is a process.** An observation is something that
  happens over time. Safe, and it fixes a real gap — see Decision 7.

**Two are incorrect and would break real data:**

- ❌ **SOSA Sensor is a physical object.** SOSA explicitly defines a sensor as
  a *"Device, agent (**including humans**), or **software (simulation)**"*. A
  software sensor is information, not a physical object, and BFO says a thing
  cannot be both. This is not hypothetical for us: HCMO already declares its
  own `Software` class to be information, so an HCM video-tracking component
  that performs sensing would become self-contradictory **in our own
  ontology**.
- ❌ **SOSA Result is information.** SOSA says a Result includes the result of
  *an act of sampling*, and that a sample "is the result from an act of
  Sampling" and that "physical samples are sometimes known as specimens" — its
  own example is crushing a rock in a ball mill. A physical specimen is a
  physical object, not information. Anyone recording a tissue sample this way
  would break.

**Why the two failures share a pattern.** In both cases *our* class is narrower
than SOSA's. Our Sensor really is a physical HCM device; our Observation Result
really is information. The BFO statement is true **of our class** and false of
SOSA's more general one. So the claim cannot be lifted up to the SOSA term —
and keeping our current double parenting is the *correct* modelling for those
two, not a defect.

**Options.**

| | |
| --- | --- |
| **Adopt the two sound statements only** | Record the other two as non-binding "close match" notes in our mapping registry |
| **Adopt all four** | Accept that software sensors and physical samples break, and record that we accepted it |
| **Adopt none** | Falls back to Decision 2 option (b) |

**Recommendation: the two sound statements only.**

**Before we vote, Philippe should see this directly.** He may have a reason
we've missed, or may take the view that HCMO needn't serve people who type
software as a sensor. That is a legitimate call for the group — but it should
be made knowingly and written into the decision record, not discovered after
release.

---

### Decision 4 — What about the fourth class, Environmental Property?

**Question.** The list of four statements doesn't mention SOSA's *Observable
Property*, so our Environmental Property class stays double-parented whatever
we do. Do we add a statement for it?

**Context in lay terms.** If we do, the right BFO bucket is **not** "quality"
(what we use today) but the broader "specifically dependent continuant" —
because SOSA's observable property also covers things like *capacities* and
*tendencies*, which BFO treats as a different kind of thing from a quality.

The snag: that broader bucket is not one of the five headings in our
user-facing simplified view. Adding it means either a sixth heading in a view
we deliberately designed around five, or keeping this statement in the
developer-only file.

**Options.** Add it with the broader bucket, as a sixth heading / add it but
keep it developer-only / leave it out.

**Recommendation: add it, developer-only.** Keeps the simplified view at five
headings and avoids re-opening a presentation decision already taken in July.

---

### Decision 5 — Does the bridge ship by default, or as an optional extra?

**Question.** When someone downloads HCMO, do these new statements come with
it automatically, or only if they ask?

**Context in lay terms.** These statements are about **W3C's** terms, not ours.
If we ship them in the main file, everyone who loads HCMO silently inherits
our opinion about how SOSA relates to BFO — including people using SOSA for
something unrelated. In the linked-data world this is called *ontology
hijacking*, and it's considered bad manners at best.

We already have exactly the right precedent: the developer upper-level profile
is a separate file, outside the main release, that people load deliberately.

**Options.** Ship in the main release / ship as an opt-in file.

**Recommendation: opt-in.** Also cheaper — an opt-in file leaves the generated
artifacts byte-identical, so no version bump and no new DOI coordination. A
default-release bridge changes what everyone gets and needs a version bump
from 0.3.0.

---

### Decision 6 — How far does the de-duplication go?

**Question.** Philippe's rationale is that having both `sosa:Actuator` and
`hcm-tech:Actuator` is two addresses for one thing. Which of our classes do we
retire in favour of the SOSA ones?

**Context in lay terms.** The argument is strong for Actuator and weak for the
rest, because the others aren't actually duplicates — they carry real HCMO
machinery that would have to be re-pointed at a W3C class:

| Our class | Is it really a duplicate? | What retiring it would cost |
| --- | --- | --- |
| **Actuator** | **Yes, essentially** | Almost nothing — no sub-classes, not used as the subject of any relation |
| Sensor | No — ours is an HCM device, SOSA's includes humans and software | Used by 7 relations, 3 validation rules, 7 example datasets, and the ISA package |
| Observation Result | No | Has 4 sub-classes of its own |
| Environmental Property | No | Used by 7 relations |

Retiring a term never means deleting it — our rules require marking it
obsolete with a pointer to the replacement, so existing data keeps working.

**Options.** Actuator only / Actuator + Observation Result / all four / none.

**Recommendation: Actuator only.** It's the one case where the duplication
argument actually holds, and it's a half-day of work including the migration
note. Retiring Sensor would mean re-pointing seven relations and three
validation rules onto a W3C class *and* losing the narrowing that makes our
BFO statement true in the first place.

---

### Decision 7 — The gap nobody has mentioned yet

**Question.** Four of our observation classes — Behavior, Environment, Health
Status, and Weight Observation — are declared as SOSA Observations and as
**nothing at all** in BFO. They have no OBO-side anchor. Do we fix this, and
how?

**Context in lay terms.** This is the opposite of the reported problem. The
complaint was "too many parents"; the reality is that our four most important
observation classes are missing one entirely. Our own upper-level
documentation already half-admits it: it says the "Process" heading exists for
navigation but that HCMO "defines no local process class" — which is only true
because these four were never anchored there.

This is worth fixing on its own merits, whatever happens to the rest.

**Options.**

- **Via the bridge.** Adopting "SOSA Observation is a process" (Decision 3)
  fixes all four automatically, with no change to our own files. Free, if
  Decision 3 passes.
- **Directly.** Anchor the four classes to "process" ourselves. Works even if
  the bridge is rejected, but it is a change to shipped classes and needs its
  own changelog entry.
- **Leave it.** Document the gap honestly instead.

**Recommendation: via the bridge if Decision 3 passes; directly if it doesn't.**
This is, to me, the single best argument for building the bridge at all — it
buys a real repair, not just a tidier diagram.

---

### Decision 8 — Does this cover PROV-O too?

**Question.** Two other classes — Operational Assessment and Calibration
Activity — sit under both BFO and PROV-O (the provenance vocabulary). Same
structural situation. Is it in scope?

**Context in lay terms.** Our alignments document already answers this case the
*other* way: PROV-O is described as "a cross-cutting view" that deliberately
coexists with BFO rather than being merged into it. If we decide BFO/SOSA in
isolation, the repository ends up with two contradictory policies for what is
visibly the same modelling situation, and a reviewer will notice.

**Options.** Same treatment for PROV-O / explicitly out of scope, with the
reason written down.

**Recommendation: explicitly out of scope, and say why.** The PROV-O case is
genuinely different — provenance is a orthogonal view of the same entities,
not a competing classification. But the difference has to be *stated*, not
left as an inconsistency for someone to find.

---

### Decision 9 — A question for Philippe, not a vote

**Question.** Was the remark about SOSA declaring its branches mutually
exclusive about the **2023 edition** rather than the 2017 one we use?

**Context in lay terms.** The 2017 version we pin declares no exclusivity
whatsoever — we verified this against the exact file and its checksum. If the
concern was based on the newer 2023 edition, that's a much bigger question:
changing SOSA editions would re-open a decision we took in July (ADR-0002),
require a new pinned source, and affect far more than the double parenting.

**Recommendation: ask, and if yes, split it into its own decision.** It should
not be folded into this vote.

---

## Summary sheet

| # | Decision | Recommendation | Needs debate? |
| --- | --- | --- | --- |
| 1 | Split reuse reporting: metadata vs. science | **Adopt** | No — quick yes |
| 2 | Build the bridge, document only, or drop a scheme | **Build, narrowed** (b is a defensible cheaper answer) | **Yes** |
| 3 | Which of the four statements to assert | **Actuator and Observation only; not Sensor or Result** | **Yes — the main one** |
| 4 | Environmental Property / Observable Property | **Add, developer-only, broader bucket** | Some |
| 5 | Default release or opt-in file | **Opt-in** | Some |
| 6 | How far de-duplication goes | **Actuator only** | **Yes** |
| 7 | The four observation classes with no BFO anchor | **Fix — free if 3 passes** | No — clear yes |
| 8 | PROV-O in scope | **Out of scope, reason recorded** | No |
| 9 | Which SOSA edition was meant | **Ask Philippe; split if 2023** | Question, not a vote |

**Blocking order.** Decision 2 gates 3–7. Decision 3 gates 7. Decisions 1, 8,
and 9 are independent and can be settled now.

**Cost by outcome.** Documentation only: ~2.5–3 days. Narrowed bridge: ~6–7.5
days. Unnarrowed (all four statements): same effort but ships a known breakage.
Dropping a scheme: ~8–10 days and high risk.

---

## Suggested sequence

1. **Now, without a meeting:** settle Decisions 1, 8, and 9 by email. Send
   Philippe the Decision 3 evidence at the same time.
2. **After Philippe replies:** put Decisions 2, 3, and 6 to the co-authors,
   since his answer may change the shape of 3.
3. **Once 2 and 3 land:** Decisions 4, 5, and 7 follow quickly — they are
   mostly consequences.
4. **Then:** write the decision record (ADR-0005) and start Phase 2 of
   [the plan](BFO-SOSA-DOUBLE-HIERARCHY-PLAN.md).

Formal motion text, ready to be put to a vote, is in section 5 of the plan.
