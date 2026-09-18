# Co-author meeting: manuscript reshape, double hierarchy, and ISA/STATO follow-up

Date: 2026-09-18

Participants: Cyril Gilbert, Philippe Rocca-Serra, Damien Huzard

Status: meeting record. The manuscript restructure is a decision of this
meeting. Every other item below is an open question, a proposal, or an action;
none of them is an approved ontology, claim, or generated-artifact change.

## 1. Decision: reshape the article

The manuscript moves to the following order:

1. **Introduction**
2. **Related work** — receives the COST TEATIME context (currently spread
   across the abstract, introduction, availability, impact, and conclusion),
   the home-cage monitoring state of the art, and the difficulties of
   variability and heterogeneity across HCM systems.
3. **Methodology**
4. **Results** — HCMO itself, the use cases, and the examples.
5. **Discussion and future work**

This is the only item decided in the meeting. It supersedes the current
section split in `docs/paper/sections/` (introduction, related work,
requirements, resource, availability, evaluation, impact, conclusion), and the
working outline in `docs/paper/OUTLINE.md` must be updated to match.

## 2. Open question for collegial decision: the double hierarchy

HCMO currently parents classes under both BFO and SOSA. The group must justify
this double hierarchy, because double parenting is not ideal and may mislead
users in practice.

The difficulty is that both hierarchies assert disjointness: BFO's top-level
branches are disjoint, and the SOSA parents are disjoint as well. A user
therefore has to be told how to handle a class that sits under both.

Candidate directions raised, none selected:

- define equivalences between the two hierarchies;
- accept double annotation, and document how a consumer reconciles it;
- commit to one hierarchy for annotation, either SOSA or BFO; or
- anchor SOSA inside BFO, which would bridge the OBO Foundry and W3C
  approaches.

**Action:** send Philippe's original comment to the co-authors so the decision
is taken collegially rather than inside a single branch.

## 3. Add examples for other classes, and clarify the box levels

Add worked examples covering further classes, including the OBI and STATO
usage, and make the distinction between the levels explicit in the manuscript:

- **TBox** — the normative HCMO class and property axioms;
- **ABox** — the instance/evidence graphs, where the OBI, STATO, and ISA
  identifiers actually occur; and
- **CBox** — the controlled vocabularies and value sets.

This matters because the paper already states that OBI and STATO are not
imported or formally aligned as HCMO classes. Naming the levels explicitly is
the cleanest way to keep that boundary legible to a reader.

## 4. The 2 x 2 design: explain what is tested, and link it to STATO

Explain better what the fixture actually tests and how, and mention the
seven-day repeated-measures structure alongside the 2 x 2 factorial design.
Revise the ISA example accordingly and link it to STATO.

For `examples/isa-roundtrip/`, the target to demonstrate is the chain:

```text
data/dark-phase-activity.csv  ->  ISA-Tab  ->  STATO
```

**Action:** Philippe plans to open a PR on this.

### Repository facts the PR will need

These are stated here so the revised text does not overclaim:

- The design is 2 x 2 **between subjects**: treatment (vehicle / active) x
  cage enrichment (standard / enriched), four groups, eight animals, two per
  group.
- Day is a **within-subject repeated measure**, not a third crossed factor.
  In `tooling/generate_isa_roundtrip_fixture.py`, `treatment` and `enrichment`
  are explicitly categorical, `day` is not; in
  `activity_count ~ treatment * enrichment + day` it therefore enters as a
  numeric linear covariate on one degree of freedom, and additively rather
  than crossed. Describing the fixture as "2 x 2 x 7" would promise
  interaction cells the pinned model never estimates.
- Accurate wording is therefore **"2 x 2 factorial with repeated measures,
  seven daily observations per animal"** (56 observations in total). If the
  group instead wants day fit as a seven-level factor, that is a real change
  to the generator, to the reported contrast, and to the expected answers in
  `examples/isa-roundtrip/competency_questions.yaml`.
- The current native ISA-Tab projection deliberately stops at the
  animal-8 Source-to-tissue-Sample path, and the repeated-observation
  structure and the semantic STATO result IRIs are declared controlled losses
  in `examples/isa-roundtrip/loss/isa-tab.yaml`. Carrying
  `dark-phase-activity.csv` through ISA-Tab to STATO therefore touches those
  declared losses and is the substantive part of the proposed PR.

## 5. ISA plus JSON-LD

Show how to build the bridge between HCMO and ISA through a JSON-LD context
file, and how to construct JSON-LD from ISA. Open question: deposit the result
on Zenodo?

## 6. For the Discussion: heterogeneity and the experimental unit

Add to the discussion the difficulty that different HCM systems have in
representing each other: they vary widely in capability and in what they can
record, which is exactly the heterogeneity HCMO has to absorb.

The statistical layer is the sharpest example. HCMO cannot currently define
the experimental unit unambiguously:

- some systems only produce measurements at the **group** (cage) level; while
- others resolve the **individual subject**.

This drives the open questions of how to link either case to ISA, and how to
make the two reusable and mutually compatible. The group considered this an
important point and a good illustration of both HCMO's value and the real
limitations still to be solved, so it should be explained very clearly rather
than compressed.

## 7. Other actions raised

| Item | Note | Owner |
| --- | --- | --- |
| Hasse diagram for the experimental design | Proposed, to be evaluated as a figure | open |
| SPARQL queries to be validated | Ask Gaoussou Sanou for a PR? | Gaoussou, to be confirmed |
| SKOS Collection for file formats | Build a SKOS collection covering the file formats of the different systems and providers. A SKOS collection is directly usable as a controlled term list in dropdown menus: builder, system, version, file formats, metadata, and similar fields. | open |

## Summary of actions

1. Restructure the manuscript to the five-part order in section 1, and update
   `docs/paper/OUTLINE.md`. — Damien
2. Circulate Philippe's original double-hierarchy comment to all co-authors for
   a collegial decision. — Damien
3. Add OBI/STATO class examples and the TBox/ABox/CBox clarification to the
   manuscript. — open
4. PR on the 2 x 2 fixture: explain what is tested, state the repeated-measures
   structure correctly, and carry `dark-phase-activity.csv` through ISA-Tab to
   STATO. — Philippe
5. Draft the HCMO-ISA JSON-LD context and the ISA-to-JSON-LD build; decide on a
   Zenodo deposit. — open
6. Write the heterogeneity and experimental-unit discussion. — open
7. Decide on the Hasse diagram, the SPARQL query validation PR, and the SKOS
   collection for system/provider file formats. — open
