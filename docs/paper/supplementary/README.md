# Supplementary material (not part of the 15-page manuscript)

| File | Content |
| --- | --- |
| `hasse-2x2-design.tex` / `.pdf` | **Supplementary Fig. S1.** Hasse diagram of the 2 × 2 factorial design with repeated measures used by the ISA round-trip fixture (issue #35). Cited in §5 of the manuscript. |

## Hasse diagram: evaluation (issue #35, 2026-10-12)

The diagram shows the factor structure of the fixture: treatment and enrichment
crossed (four groups), eight animals nested in the groups, and seven days
crossed with animals (56 observations). Day is drawn as a design factor; the
fitted linear mixed model uses it as a linear term with a random intercept per
animal (`activity_count ~ treatment * enrichment + day`). Day interactions are
not drawn because the model does not fit them; no degrees of freedom are shown
for the same reason.

What it adds over the manuscript's figures: it makes the **experimental unit**
(the animal, for the treatment × enrichment contrast) and the **observational
unit** (an animal on a day) explicit, which is the distinction behind the
experimental-unit discussion (backlog section 2; ADR-0006 open point 2).

Decision (2026-10-12, Damien Huzard): supplementary figure S1, linked from §5
of the manuscript; not a manuscript figure (15-page budget).
