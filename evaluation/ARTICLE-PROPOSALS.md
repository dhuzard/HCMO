# Candidate additions to the HCMO article

**Status (2026-09-28):** proposals only. The article on `HCMO-draft-v4` is the
source of truth; nothing here has been added to it. Decide item by item.

**Page budget.** The draft is already about one page over the provisional
15-page limit (`docs/paper/CALL-REQUIREMENTS.md`), so every addition needs an
equal cut. Each proposal gives its approximate cost.

**Gate.** Present the numbers as provisional until the review in
[`CONTRIBUTOR-REVIEW.md`](CONTRIBUTOR-REVIEW.md) has produced adjudicated
mappings and a κ value. Until then, every figure below must carry both
limits: synthetic exports and a single annotator.

## What the evaluation answers

It answers the reviewer question "can HCMO describe the outputs of real,
heterogeneous home-cage systems, and where does it fail?" It does **not** show
anything about animals: every value in the six graphs is generated.

## Honest figures (from `reports/coverage.md`)

| | HCMO-native [95% CI] | + external terms | + partial patterns |
|---|---|---|---|
| All six systems, 170 concepts | 77/170 = 45% [38–53] | 101/170 = 59% | 147/170 = 86% |

| Module (pooled) | HCMO-native [95% CI] | Expressible at all |
|---|---|---|
| core | 17/21 = 81% [60–92] | 20/21 |
| tech | 27/37 = 73% [57–85] | 32/37 |
| env | 11/15 = 73% [48–89] | 15/15 |
| bio | 13/22 = 59% [39–77] | 22/22 |
| obs | **9/62 = 15% [8–25]** | 58/62 |

Per system, HCMO-native ranges from 34% (BEATBox) to 58% (DVC). The intervals
overlap, so the ranking between systems is descriptive only.

**Main finding:** enclosure, device and environment concepts map natively.
Observation-level concepts mostly do not: they fit only through generic SOSA
observations, reused terms or lossy patterns. The next modelling effort
belongs in `hcm-obs`.

## Proposals

### P1. Evaluation (§6): a coverage paragraph (recommended)

Cost: about 0.3 page. Draft text:

> **Coverage of heterogeneous HCM systems.** To test coverage beyond the
> development examples, we listed the documented outputs of six HCM systems —
> a capacitive cage rack (Tecniplast DVC), indirect calorimetry (TSE
> PhenoMaster), video tracking (Noldus PhenoTyper with EthoVision XT),
> group-housed depth video with RFID (Live Mouse Tracker), and two open
> operant devices (FED3, BEATBox) — and mapped each of 170 native concepts to
> HCMO. 45% [95% CI 38–53] were expressed with HCMO's own terms, 59% with
> HCMO plus reused external terms, and 86% at all once generic or lossy
> patterns were accepted. Native coverage was high for enclosure (81%),
> technical (73%) and environmental (73%) concepts and low for observation
> concepts (15%). Exports were synthetic, built from public documentation;
> mappings were made by one annotator and independently reviewed by [N]
> system developers (κ = [..]). Mapping tables, generators and instance
> graphs are in the repository.

Replace the bracketed values after the review. If the review is not done by
submission, drop the last-but-one sentence and say "by one annotator".

### P2. Figure: coverage by system and by module (recommended with P1)

Cost: about 0.4 page; it can replace a table.

- **Panel A:** one horizontal stacked bar per system (hcmo / external /
  partial / not covered), sorted by native share, labelled with n, with a
  Wilson 95% whisker on the native share.
- **Panel B:** a heatmap of systems × modules, cell = native share, annotated
  "k/n". It shows the weak observation row at a glance.

Generate both from the TSV files with a script under `evaluation/` so they stay
reproducible, like the reports.

### P3. Discussion (§7): gaps as the 0.4.0 roadmap (recommended)

Cost: about 0.2 page. A ranked list, each gap naming the systems that hit it:

1. No task / trial / session vocabulary (BEATBox, FED3, Noldus).
2. No n-ary behavioural event with participant roles (LMT).
3. No observation subtype for numeric activity, metabolic or operant results
   (DVC, TSE, Noldus, FED3, BEATBox).
4. No genotype property (LMT).
5. `ExperimentalGroup` cannot carry strain or sex (DVC and other cage-level
   systems).
6. `hcm:locatedIn` and arena zones have no history (DVC, Noldus, LMT).
7. No subject identifier property; `dcterms:identifier` is reused (TSE,
   Noldus, FED3, LMT, BEATBox).

A small dot matrix of gaps × systems can replace the list if space allows.

### P4. Competency questions (§6): one sentence, no table

> Sixteen further questions, fourteen of which join several systems, run over
> the union of the six instance graphs; their complete expected answers are
> checked in CI.

State that these are regression checks written by the authors, not an
independent test. Do not quote any answer value: counts, accuracies and
latencies come from the generators.

### P5. SHACL (§6): one clause after a mutation study (optional)

Now: the six graphs conform, and 24 injected faults (four fault types × six
graphs) are rejected. Before citing this, extend it to a systematic mutation
study, for example 50 mutations per fault type, and report the detection rate
per type, listing any type the shapes deliberately do not catch.

### P6. Availability: one line (recommended)

Point to `evaluation/` and `docs/hcm-systems/systems/` as the reproducible
evaluation material.

## Statistics: use and avoid

**Use:**
- Wilson 95% intervals on every coverage share.
- Pooled and per-module shares.
- Cohen's κ between the independent annotators (after the review).
- The detection rate per fault type (after the mutation study).

**Avoid:**
- Hypothesis tests between systems: with n = 24–36 concepts per system they
  are underpowered, and the concept lists were not sampled.
- Any statistic or plot of values in the graphs (activity, calorimetry,
  accuracy per strain, behaviour counts). They are synthetic.
- "% mapped" as a headline: it counts lossy mappings as success.

## Not proposed

- The DVC sensor → observation → result figure from the first version of this
  branch: `HCMO-draft-v4` already uses Fig. 4, and the bin it showed is mock.
- The full sixteen-question table and the per-module metrics table: keep them
  in the repository.
