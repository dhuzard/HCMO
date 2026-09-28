# Independent review of the multi-system mappings

**Status (2026-09-28):** planned; no review has started.
**Owner:** Damien Huzard.

## Why this review is needed

The coverage figures in [`reports/coverage.md`](reports/coverage.md) are
provisional, for three reasons:

1. **Single annotator.** One person wrote every `hcmo-mapping.tsv`. For most
   systems the same person also designed the synthetic export from public
   documentation, so the export, the concept list and the mapping share one
   reading of the system. The test is partly circular.
2. **No recorded data.** All six exports are synthetic, including DVC cohort
   7623. Whether each export reproduces what the system really writes has not
   been checked by anyone who runs the system.
3. **The concept list sets the denominator.** A missing or split concept moves
   the percentage. Only the system's developers can say whether the list is
   complete.

The review fixes this in two phases: first the six systems already mapped,
then an open call to the HCM community.

## Phase 1 — the six mapped systems

Each system gets two independent reviewers:

- a **system expert** (developer or long-term user), who judges the export
  schema and the concept list;
- an **HCMO co-author** who was not the first annotator, who re-maps the
  concepts to HCMO terms.

| System | System expert(s) to invite | HCMO co-author | Status |
|---|---|---|---|
| Tecniplast DVC | Giorgio, Lorenzo, Guido or Mara (Tecniplast) | to assign | not contacted |
| TSE PhenoMaster | contact at TSE Systems to identify | to assign | not contacted |
| Noldus PhenoTyper + EthoVision XT | contact at Noldus to identify | to assign | not contacted |
| FED3 | Lex Kravitz | to assign | not contacted |
| Live Mouse Tracker | Fabrice de Chaumont or Nicolas Torquet | to assign | not contacted |
| BEATBox | Eric or Lizbeth | to assign | not contacted |

A seventh system, **MIROSlav** (Davor), is a candidate. It has no profile,
export or mapping yet; adding it would follow the contribution path in
[`docs/hcm-systems/contribute/`](../docs/hcm-systems/contribute/).

### What each system expert is asked

1. **Export schema.** Does the synthetic export under
   `docs/hcm-systems/systems/<system>/datasets/mock/` match what the system
   writes: file layout, column names, units, time base, identifiers? List every
   difference.
2. **A recorded sample, if possible.** A small de-identified export would
   replace the mock, go under `datasets/real/`, and change the `data` field in
   [`multi-system.yaml`](multi-system.yaml). This is optional; the review is
   useful without it.
3. **Concept list.** Is every concept the system exposes listed once in the
   `native_concept` column? Which are missing, merged or wrongly split?
4. **Gaps.** Are the partial and not-covered rows fair descriptions of what the
   system does?

### What each HCMO co-author does (blind re-mapping)

1. Take the concept list only: the `native_concept`, `source` and
   `description` columns of `hcmo-mapping.tsv`, with the mapping columns removed.
2. Independently assign `module`, `mapping` (hcmo / external / partial /
   not-covered) and `hcmo_target`, using the ontology documentation, without
   looking at the first mapping.
3. Save the result as `hcmo-mapping.<reviewer-initials>.tsv` next to the
   original.

### Agreement and adjudication

- Report **Cohen's κ** on the four-way mapping kind per system and pooled, the
  raw percentage agreement, and agreement on the target term for rows both
  annotators mapped as `hcmo`.
- Resolve disagreements in a short adjudication call. The adjudicated table
  replaces `hcmo-mapping.tsv`; both independent tables stay in the repository.
- Record the outcome in `multi-system.yaml` under `mapping_review`: status,
  reviewers, date, κ.
- Regenerate the graphs and reports. The coverage report then states the
  reviewed figures.

Agreement tooling (κ from the two TSV files) is not written yet; add it to
`tooling/evaluate.py` when the first independent table arrives.

## Phase 2 — open call

When all six systems are reviewed, invite COST Action TEATIME members and the
wider HCM community to contribute further systems with the existing
contribution form
([`docs/hcm-systems/contribute/`](../docs/hcm-systems/contribute/)). Each new
system follows the same path: profile, export (recorded if possible), mapping,
blind second mapping, adjudication.

## To confirm now: declared DVC experimental metadata

The DVC graph adds metadata that a DVC export does not carry. All of it is
assumed; each node links to the `mock-experimental-metadata` dataset note.
Damien to confirm or correct each value:

| Item | Value in the graph | Confirmed? |
|---|---|---|
| Light programme | 12:12, lights off 19:00–07:00 | |
| Rack environment | temperature and relative humidity from the rack environmental monitor every 15 min; room targets 22 °C / 50 % RH | |
| Housing density | 2 mice per cage | |
| Strain and sex | C57BL/6J; males in `B6_M` (rack AAAA), females in `B6_F` (rack BBBB) | |
| Dates of birth | mock values per subject | |
| Husbandry | cage change every Wednesday, 10:00–11:00 | |
| Enrichment | nesting material in every cage | |
| Cage model | GM500 IVC, 391 × 199 × 160 mm external | |
| Software | DVC Analytics 3.5 (cloud) | |
| Time zone | UTC−04:00 | |
| Materialised window | cohort 7623: 4 cages × 180 min from 2025-10-14 11:00; B6_F: 2 cages × 120 min from 18:00 | |

Cohort 7623 itself is mock. Its folder is still called `datasets/real/` because
`examples/dvc-tecniplast.ttl` on `main` references that path. Rename the folder
in a separate change on `main`.
