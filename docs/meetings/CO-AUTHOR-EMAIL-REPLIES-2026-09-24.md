# Co-author email replies: restructure, 2 x 2 wording, BFO/SOSA, authorship

Recorded: 2026-09-24

Replies received from: Konstantin Todorov, Cyril Gilbert, Pierre Larmande,
Gaoussou Sanou (to Damien's update email following the
[2026-09-18 meeting](CO-AUTHOR-MEETING-2026-09-18.md)).

Not yet replied in this thread: Serge Sonfack Sounchio, Antoine Toffano.
Philippe Rocca-Serra is the author of the option (a) proposal and did not cast
a separate vote in this thread.

Status: a record of the replies and of the decisions taken from them
(section 4). Apart from the 2 × 2 wording (D2), no manuscript prose, ontology axiom,
term IRI, or generated artifact changed.

## 1. Tally by topic

| Topic | Konstantin | Cyril | Pierre | Gaoussou | Outcome so far |
| --- | --- | --- | --- | --- | --- |
| Restructure the paper | Agrees; a resource paper need not follow the research-paper structure, what matters is covering the call's required elements | Agrees; same caveat about strict traditional structure | Agrees; sent a further example paper | Agrees | **Agreed (4/4)**, with the caveat that the call's required elements come first |
| Describe the fixture as 2 x 2 factorial with repeated measures (not 2 x 2 x 7) | — | Agrees | Agrees | — | **Agreed** by those who answered; no objection |
| Q3 BFO/SOSA double hierarchy | **(a)** equivalences | **(a)**, if each equivalence is semantically justified and tested for unintended reasoning consequences | **(a)** first, or **(d)**; agrees with Philippe's proposal | **(a)**; fall back on elements of **(d)** where no proper equivalent exists | **(a) preferred (4/4)**, with (d) as the accepted fallback (2/4 name it explicitly) |
| Authorship decision (additional co-author) | No objection; leaves it to Damien | No objection | Agrees | — | **No objection** from those who answered |

Options (a)–(d) are those listed in section 2 of the
[2026-09-18 meeting record](CO-AUTHOR-MEETING-2026-09-18.md): (a) define
equivalences between the two hierarchies; (b) accept double annotation and
document how a consumer reconciles it; (c) commit to one hierarchy; (d) anchor
SOSA inside BFO.

## 2. What the Q3 vote means for the plan

> **Superseded by [section 4.2](#42-provisional--awaiting-philippes-confirmation).**
> The analysis below predates the Prudhomme et al. alignment route and is kept
> for the record.

The group's mandate is option (a), and two replies explicitly attach
conditions that matter:

- Cyril: every equivalence must be **semantically justified** and **tested for
  unintended reasoning consequences**.
- Gaoussou and Pierre: where a strict equivalence cannot be established, use
  **(d)**.

The per-axiom review in
[`BFO-SOSA-DOUBLE-HIERARCHY-PLAN.md`](../BFO-SOSA-DOUBLE-HIERARCHY-PLAN.md)
§2 found that no SOSA class can correctly be declared `owl:equivalentClass` to
a BFO/IAO class, and that two of Philippe's four subclass statements
(`sosa:Sensor ⊑ material entity`, `sosa:Result ⊑ information entity`) fail the
justification test against the pinned SOSA 2017 definitions. Under the
conditions the co-authors themselves set, the vote therefore resolves to the
narrowed Motion 2 in §5 of the plan: (a) delivered as a directional (d)-style
bridge for the two sound statements, with SSSOM `closeMatch` rows for the other
two and a reasoner gate before merging.

**Not yet confirmed by the co-authors:** they voted on "(a) equivalences" as
described in the meeting, not on the narrowed motion text. The narrowing, the
two rejected statements, and the default-release-versus-opt-in question
(plan §6, item 2) still need to be put back to the group — Philippe first,
since the two rejected statements are his. The PROV-O route in
[`PHILIPPE-PROV-BFO-REPLY-2026-09-23.md`](PHILIPPE-PROV-BFO-REPLY-2026-09-23.md)
bears on the `sosa:Sensor` case and should go out with that follow-up.

## 3. Replies as received

### Konstantin Todorov

> Hi all,
>
> Thanks for the updates Damien.
>
> Great for restructuring the paper if it helps reduce redundancies. A quick
> remark though - since this is a resource paper, it is common that it does not
> exactly follow the typical research papers structure (cf. for ex. Gaoussou's
> KG paper published at ISWC :
> https://iswc2022.semanticweb.org/wp-content/uploads/2022/11/978-3-031-19433-7_36.pdf).
> By all means, what matters is that the paper contains all the elements that
> are requested by the call for such kind of papers (which was the case when I
> read it).
>
> Regarding question 3, very good point indeed. I'd go for option a) define
> equivalences between the two hierarchies - to me this is both technically
> clean and doesn't imply "erasing" one of the resources in favor of the other.
>
> Regarding the additional co-author - no objection on my side, I'll let you
> judge Damien since you know the background and context of your collaboration.
>
> Cheers,
>
> Konstantin

### Cyril Gilbert

> Hi,
>
> I agree with the restructuring, although I am not sure that a resource paper
> needs to follow a strictly traditional structure.
>
> I also agree with describing the example as a 2 × 2 factorial design with
> repeated measures, rather than a 2 × 2 × 7 design.
>
> Regarding BFO/SOSA, I don't have sufficient expertise to decide between the
> options. Option (a) seems clear, as long as each equivalence is semantically
> justified and tested for unintended reasoning consequences.
>
> Of course, I have no objection regarding the proposed authorship decision.
>
> Best,
> Cyril

### Pierre Larmande

> Dear all,
>
> Sorry for the late reply.
> For the structure of the paper, more examples bellow to give you an overview.
>
> I agree to describe the example as a 2 × 2 factorial design with repeated
> measures.
>
> For BFO - SOSA I agree with Philippe proposal and would vote for a first or d.
>
> I agree with the authorship decision
> Link: https://iswc2023.semanticweb.org/wp-content/uploads/2023/11/142660151.pdf
>
> Best regards
>
> Pierre

### Gaoussou Sanou

> Hello everyone,
> Thank you, Damien, for the updates. The restructuring looks good to me.
> Regarding question 3, the simplest and cleanest solution is, to me,
> Konstantin and Cyril's suggestion (option a: creating equivalence). However,
> since establishing a strict equivalent can sometimes be challenging, option d
> is also worth considering (as Pierre pointed out).
> My vote goes to option a), but if we cannot find a proper equivalent, we
> could potentially incorporate elements of option d.
> Best regards,
>
> Gaoussou

## 4. Decisions (2026-09-24)

### 4.1 Settled — work can proceed

| # | Decision | Basis | Status |
| --- | --- | --- | --- |
| D1 | **Restructure the paper.** Follow the seven-section resource-paper layout in [`docs/paper/OUTLINE.md`](../paper/OUTLINE.md). It implements the five-part reshape agreed on 2026-09-18, with "Results" split into HCMO, interoperability use cases, and metrics/evaluation/impact. The governing rule, per Konstantin and Cyril, is that every element required by the call is covered; the classic research-paper structure is not a constraint. Models: the OntoPFAS and SemTS ESWC 2026 papers already in `OUTLINE.md`, plus Gaoussou's ISWC 2022 paper and the ISWC 2023 paper sent by Pierre. | Agreed 4/4 | **Settled** — T20b unblocked |
| D2 | **Describe the example as a 2 × 2 factorial design with repeated measures** (seven daily observations per animal, 56 in total), never as 2 × 2 × 7. | Agreed by Cyril and Pierre; no objection | **Settled** — applied to manuscript §§4 and 6 (Markdown and LaTeX) on 2026-09-24 |
| D3 | **Authorship: add the proposed additional co-author.** | No objection from any reply | **Settled** — name, ORCID, affiliation, CRediT roles and position still to be entered in `docs/paper/metadata/authors.md` |

Paper sources:
- Gaoussou's ISWC 2022 KG paper: <https://iswc2022.semanticweb.org/wp-content/uploads/2022/11/978-3-031-19433-7_36.pdf>
- ISWC 2023 example from Pierre: <https://iswc2023.semanticweb.org/wp-content/uploads/2023/11/142660151.pdf>

### 4.2 Provisional — awaiting Philippe's confirmation

The BFO/SOSA decision (Q3) is **provisional**. The working position below
**replaces the conclusion of section 2** (the narrowed Motion 2 with Sensor
rejected), because the Prudhomme et al. 2025 alignment paper that Philippe
shared on 2026-09-23 gives a published route
([notes](../PROV-BFO-ALIGNMENT-PAPER-NOTES.md)). The paper is by Prudhomme
et al.; Philippe is not an author. Refer to it as "the Prudhomme et al.
alignment paper".

| # | Provisional position | Pending |
| --- | --- | --- |
| P1 | **No direct equivalence.** The examined SOSA classes are not asserted equivalent to the proposed BFO classes, because SOSA's semantics are intentionally broad. BFO placements are obtained through one-way links: W3C SOSA→PROV-O (SSN Rec. §6.5), then PROV-O→BFO (Prudhomme et al.), e.g. `sosa:Observation ⊑ prov:Activity ≡ BFO process`. | Philippe |
| P2 | **Reuse, don't author.** An HCMO alignment profile imports the two published alignments. HCMO adds a direct link only where an HCMO-specific requirement cannot be obtained compositionally. | Philippe Q2 |
| P3 | **Opt-in.** The profile is not part of the default release; its status may be reconsidered once it proves stable. | Philippe Q3 |
| P4 | **Software sensors.** Accept the entailed `sosa:Sensor ⊑ material entity`, modelling a software sensor as running software, which concretises the code (an information entity). Documented as a commitment introduced by the BFO alignment, not by SOSA. | Philippe Q1 |
| P5 | **Duplicate terms by meaning, not name.** Retire `hcm-tech:Actuator` in favour of `sosa:Actuator` if it adds no narrower meaning. Keep `hcm-tech:Sensor`, `hcm-obs:ObservationResult`, and `hcm-env:EnvironmentalProperty` as documented specialisations. **Conflict found 2026-09-24:** decision A05 in `docs/PHILIPPE-ROCCA-SERRA-HUMAN-REVIEW-CHECKLIST.md` (accepted) already retains `hcm-tech:Actuator` as the *physical*, home-cage-specific subclass of `sosa:Actuator`, because the SOSA class also covers software and other systems. By the meaning-not-name criterion it is therefore narrower and should be kept; the email's point 4 premise ("adds nothing beyond `sosa:Actuator`") is wrong and should be corrected with Philippe. | Philippe Q4 |
| P6 | **Exact versions.** Test against the pinned SOSA 2017 artifact and its matching W3C alignment, with versions recorded in the profile metadata and CI; do not carry over conclusions from the 2023 edition. Our BFO pin differs slightly from the release the paper targets; test it, don't assume. | Philippe Q5 (edition of the disjointness remark) |
| P7 | **Tested alignment module.** CI checks: satisfiability; consistency of `examples/` and targeted probes; conservativity (no change inside the HCMO, SOSA or BFO hierarchies, materialised and compared as in the paper); any new cross-derived disjointness listed and reviewed; provenance and rationale recorded for each mapping (SSSOM). The chain's BFO entailments are listed and documented; it is **not** presented as a complete BFO interpretation of SOSA. | Cyril's condition; no dissent |

Nothing in 4.2 authorises a module change. After confirmation, the outcome is
recorded in ADR-0005 (plan §3.1) before any implementation.

## 5. Reply to the co-authors (draft, 2026-09-24)

Status: draft prepared for Damien; send status not recorded here. It
supersedes the unsent
[`PHILIPPE-PROV-BFO-REPLY-2026-09-23.md`](PHILIPPE-PROV-BFO-REPLY-2026-09-23.md),
which remains as the detailed technical background.

**Subject:** Re: HCMO paper — decisions from your replies, and one confirmation for Philippe

> Dear all,
>
> Thank you all for your quick and clear replies. Here is where we stand.
>
> **1. Paper structure — agreed.** We restructure to reduce repetition. As Konstantin and Cyril pointed out, a resource paper doesn't need to follow the classic research-paper layout. The rule I'll follow is to cover every element the call requires. I'll use the example papers you sent (Gaoussou's ISWC 2022 paper, and the ISWC 2023 paper from Pierre) as models.
>
> **2. The example design — agreed.** We'll describe it as a *2 × 2 factorial design with repeated measures (seven daily observations per animal)*, not as 2 × 2 × 7.
>
> **3. Authorship — agreed.** No objections, so [name] joins the author list. I'll update the metadata.
>
> **4. BFO/SOSA — option (a) preferred by everyone, with (d) as the fallback.**
> Konstantin, Cyril, Pierre and Gaoussou all prefer (a): link the two hierarchies without dropping either one. Pierre and Gaoussou would fall back on (d) where a strict equivalence doesn't hold. Cyril asked that every link be justified and tested for unwanted reasoning effects.
>
> When we checked the proposed links one by one, the SOSA classes we examined should **not** be declared *equivalent* to the proposed BFO classes. SOSA is deliberately broad. For example, a SOSA "Sensor" can be a device, a human or a piece of software, and a SOSA "Result" can be a physical sample. What works are one-way "is a kind of" links. In practice, that is Gaoussou's "(a), with elements of (d)".
>
> The paper Philippe shared yesterday (Prudhomme et al. 2025, *Sci Data* 12:282) gives us a clean way to do this. The authors publish a peer-reviewed alignment of PROV-O to BFO. The W3C already publishes a one-way alignment of SOSA to PROV-O. Put together, the two give BFO placements for SOSA terms **without anyone declaring them equivalent**. For example, an Observation is a kind of PROV Activity (W3C), and a PROV Activity is the same as a BFO process (the paper), so an Observation is inferred to be a BFO process.
>
> We ran that combination through a reasoner against HCMO:
>
> - Our four observation classes (Behavior, Weight, Health Status, Environment) currently have no BFO place. They get one (process) without any edit to our modules.
> - Observation and Actuator land where Philippe proposed.
> - Result is placed only as a "continuant", so physical samples remain valid.
> - Sensor is placed under "material entity". This holds if we treat a software sensor as the *running* software, with the code as a separate information entity, which is the paper's own position.
> - All our examples stay consistent.
>
> This doesn't give SOSA a complete BFO reading. It gives a set of consequences that follow from two published alignments, and we'll list and document each of them rather than present the chain as a general SOSA–BFO equivalence.
>
> **Proposed plan** (building on Cyril's condition):
>
> - **Reuse, don't author.** HCMO imports the two published alignments in a separate profile, rather than writing its own statements about W3C terms. HCMO adds a direct link only where it needs one that the chain can't provide.
> - **Opt-in, not default.** The core ontology doesn't force BFO commitments on users who only need the home-cage model or SOSA compatibility. We can reconsider once the profile has proved stable.
> - **Tested, not just asserted.** We adopt the paper's own checks in our validation: no class is left without possible members; our example data stays consistent; loading the alignment changes nothing inside the HCMO, SOSA or BFO hierarchies; and any new disjointness the alignment adds is listed and reviewed. Each link is recorded with its source and rationale.
> - **Exact versions.** We test against exactly the SOSA 2017 file we pin and the matching W3C alignment, and record those versions in the profile and the tests. Our BFO version differs slightly from the one the paper aligned to, so we'll check that rather than assume it.
>
> **Philippe, could you confirm these five points (yes/no, or a correction):**
>
> 1. **Software sensors.** We accept the Sensor link, with a software sensor modelled as the running software and the code as a separate information entity. We document this as a choice that comes from the BFO alignment, not something SOSA itself requires.
> 2. **Reuse over authoring.** The profile imports the published alignments, and HCMO adds only the direct links it strictly needs.
> 3. **Opt-in.** The profile is optional for now and is not part of the default release.
> 4. **Duplicate terms.** We decide by meaning, not by name. `hcm-tech:Actuator` adds nothing beyond `sosa:Actuator`, so we retire it in favour of the SOSA term. Our Sensor, Observation Result and Environmental Property classes are narrower than SOSA's, so we keep them and document what they add.
> 5. **SOSA edition.** Your remark about disjointness: was it about the 2017 Recommendation or the 2023 edition? The published chain relies on 2017, which is what we pin, and we won't carry conclusions over from the 2023 work without re-testing.
>
> Once you confirm, I'll write it up as a formal decision record and then build and test the profile.
>
> Serge and Antoine, if you have any comments on any of these four points, they're very welcome.
>
> Many thanks again,
> Damien

## 6. Follow-ups

1. Send the reply in section 5 (fill in the new co-author's name).
2. Get Philippe's answers to Q1–Q5; then record the outcome and participants
   in ADR-0005 and mark 4.2 as decided.
3. Ask Serge and Antoine for their replies.
4. Collect the new co-author's name, ORCID, affiliation, CRediT roles and
   position in the author order (D3).
5. Start the restructure (D1, T20b) in `docs/paper/sections/`, then mirror it
   into `docs/paper/overleaf/`.
