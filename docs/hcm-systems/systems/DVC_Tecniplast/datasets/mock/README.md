# Mock DVC® traces — real-schema

**Synthetic, freely redistributable** home-cage-monitoring traces shaped **exactly
like the real DVC® export** in [`../real/`](../real/). Use them to exercise HCMO
ingestion, SHACL shapes, and competency queries without touching proprietary data.
**Not real animals.**

## Files

| File | What it is |
|---|---|
| `generate_dvc_traces.py` | Deterministic, stdlib-only generator (fixed seed → identical output). |
| `mock_B6_M_animal_loc__index_smoothed.csv` | Index trace: 8 cages × 3 days × 1-min bins (4,320 rows). Same columns as the real index file. |
| `mock_B6_M_events.csv` | Matching cage-lifecycle event log (REGISTERED → … → REMOVED). |
| `reconstructed-schema/` | An **earlier** mock built before the real headers were known — a *reconstructed* wide schema (`DateTime, ActivationDensityPct, BeddingStatusIndex, …`). Kept for reference; **superseded** by the real-schema traces above. |

## Why two mock schemas?

The profile in [`../../dvc-system-profile.md`](../../dvc-system-profile.md) §5 was
written when the exact vendor CSV headers were *unknown*, so its mock
(`reconstructed-schema/`) used self-describing, reconstructed field names. The real
cohort-7623 export has since given us the **actual** headers, so the traces here
reproduce them verbatim (`day, hour, minute, relativeTime, <G>_AVG, <G>_SEM, <G>_QRT,
<G>_SAMPLES, <G>_<cageId>…`). Prefer these for validation.

## Fidelity

Reproduces the conventions verified against the real file:
- `relativeTime = day*86400 + hour*3600 + minute*60` (events add seconds).
- `<G>_AVG` = mean of online cages; `<G>_SEM` = sample SD; `<G>_QRT` = `linspace(min,max,5)+[min,max]`.
- `<G>_SAMPLES ≈ online_cages × 240` (12 electrodes @ 4 Hz × 60 s).
- Progressive cage insertion (leading empty cells), ISO-8601 timestamps with `-0400`.
- Nocturnal circadian drive (dark-phase mean ≈ 5.8 vs light ≈ 1.7 index units),
  grounded in the DVC corpus (dark-phase-dominant activity). See profile §9.

Value ranges are plausible, **not** a physiological model — the point is faithful
*shape and structure*, so parsers/validators that work here work on real exports.

## Regenerate / rescale

```bash
python3 generate_dvc_traces.py                 # defaults: B6_M, 8 cages, 3 days
python3 generate_dvc_traces.py --cages 24 --days 14   # match the real cohort size
python3 generate_dvc_traces.py --group B6_F --seed 11
```
