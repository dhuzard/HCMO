# ADR-0006: Behaviour observations involving several animals

- Status: proposed — implemented on branch `feat/skos-file-formats`, pending
  co-author review
- Date: 2026-09-29

## Context

HCMO 0.3.0 required exactly one `hcm-bio:Subject` as the feature of interest of
an `hcm-obs:BehaviorObservation`. Home-cage systems that track groups record
behaviours involving two to four animals. In the public Live Mouse Tracker
sample, 70 % of the 67,976 events involve at least two animals (for example
"A approaches B", contacts, groups of three). Such events had no correct HCMO
representation. `hcm-bio:ExperimentalGroup` does not fit: it is defined by the
study design, whereas these groups exist only while the behaviour lasts. This
is one instance of the experimental-unit question raised at the 2026-09-18
co-author meeting.

Three options were compared:

1. **Group feature of interest plus roles** (chosen).
2. One observation per participating animal, linked by a shared interaction
   node: no change to `BehaviorObservation`, but two to four times as many
   observations and duplicated results.
3. Several subjects as feature of interest: no new terms, but who acted on whom
   is lost.

## Decision

- A multi-animal behaviour is **one** `hcm-obs:BehaviorObservation`. Its feature
  of interest is an `hcm-bio:InteractingGroup`: a transient group of two or more
  subjects defined by the observed behaviour. Members are stated with
  `hcm-bio:hasMember`, whose domain now also covers interacting groups.
- The `BehaviorObservation` restriction is loosened from `hcm-bio:Subject` to
  `hcm-bio:Subject` or `hcm-bio:InteractingGroup`. Existing data remain valid.
- Directed behaviours add `hcm-obs:hasInitiator` and `hcm-obs:hasRecipient`
  (sub-properties of `hcm-obs:involvesSubject`). Symmetric behaviours state the
  group only.
- SHACL requires at least two members per group, role holders who are members
  of the observation's group, and distinct initiator and recipient.

For Live Mouse Tracker, per the HCMO authors: an event involves several animals
when `IDANIMALB` is filled; `IDANIMALA` initiates and `IDANIMALB` receives;
`Group2`–`Group4` are symmetric. Symmetric events, which LMT stores in every
ordering of the animals, collapse into one observation. The per-event table is
`docs/hcm-systems/systems/live-mouse-tracker/event-mapping.csv`.

## Consequences

- Queries for an animal's behaviour must look at both paths: the animal as
  feature of interest, and the animal as member of an interacting group. The
  competency question `social-interaction-partners` shows the pattern.
- Group-level results are not attributed to individuals. Deriving per-animal
  measures (for example, time in contact per mouse) is an analysis step, not an
  ontology inference.
- Behaviour names stay free text in `hcm-obs:hasBehaviorType`. Whether a
  behaviour is directed or symmetric is recorded per source system (the LMT
  table), not in the ontology; a future SKOS behaviour vocabulary could carry
  it.

## Open points for the co-authors

1. Accept option 1, including the loosened `BehaviorObservation` axiom.
2. Should group housing measured only at cage level (no individual resolution)
   use `InteractingGroup`, `ExperimentalGroup`, or the enclosure as feature of
   interest? This ADR does not decide it.
3. Confirm the six LMT rows still marked "to confirm" in `event-mapping.csv`:
   the five manual annotations and `Nest4_`. All other rows are backed by the
   authors' rules, `EVENT.DESCRIPTION`, or the lmt-analysis event-building code.
