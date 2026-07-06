# Real DVC® export — cohort 7623

Real Tecniplast **Digital Ventilated Cage (DVC®)** export contributed for HCMO
validation. Group `B6_M` (C57BL/6, males — per the group label), **24 cages**, one
rack, **14 days** at 1-minute resolution, starting **2025-10-14 10:16 (UTC−04:00)**.

> **Provenance & use:** contributed by the HCMO team for ontology validation. Cage
> identifiers are the facility's internal codes; the files carry no personnel names
> or animal-identifying information. DVC raw data/exports are normally proprietary to
> the generating facility — treat these files as shared **for HCMO validation** and
> check with the contributor before redistributing outside the project. The synthetic
> look-alikes in [`../mock/`](../mock/) are freely redistributable.

## Files

| File | Rows | What it is |
|---|---|---|
| `Cohort7623_animal_loc__index_smoothed.csv` | 18,464 | Smoothed activation/locomotion index, one row per 1-min bin, cages as columns. |
| `Cohort7623_events.csv` | 216 | Cage-lifecycle event log (registration → insertion → updates → removal). |

## `…_animal_loc__index_smoothed.csv` — schema

One row **per 1-minute bin**. 9 metadata columns + one column per cage (24 here).
`<G>` is the group prefix (`B6_M`).

| Column | Type | Unit | Meaning |
|---|---|---|---|
| `day` | int | days | Days since day 0 (calendar-day counter, increments at local midnight). |
| `hour`, `minute` | int | — | Local wall-clock time of the bin. |
| `relativeTime` | int | s | Seconds since local midnight of day 0 = `day*86400 + hour*3600 + minute*60`. |
| `<G>_TIMESTAMP` | string | — | ISO 8601 with millis and numeric offset, e.g. `2025-10-14T10:16:00.000-0400`. |
| `<G>_AVG` | float | index | Mean activation index across the online cages in the bin. |
| `<G>_SEM` | float | index | Dispersion across cages — in this export equals the **sample SD** (ddof=1). |
| `<G>_QRT` | JSON array | index | 7 numbers = `linspace(min,max,5)` then `min,max` appended. Quoted. |
| `<G>_SAMPLES` | int | count | Raw sub-samples aggregated in the bin ≈ `online_cages × 240` (12 electrodes @ 4 Hz × 60 s). |
| `<G>_<cageId>` | float | index | Per-cage smoothed activation index. **Empty** until that cage is INSERTED. |

Notes:
- The activation index is the DVC's capacitance-derived locomotion readout (see the
  profile's ALI/Activation-Density discussion in [`../../dvc-system-profile.md`](../../dvc-system-profile.md) §4).
- Cages come online progressively in the first minutes → leading empty cells, and the
  count of populated cells drives `SAMPLES`.

## `…_events.csv` — schema

One row **per cage-lifecycle event**.

| Column | Type | Meaning |
|---|---|---|
| `group` | string | Group label (`B6_M`). |
| `day`, `hour`, `minute` | int | Local time of the event. |
| `relativeTime` | int (s) | `day*86400 + hour*3600 + minute*60 + seconds` (includes seconds, unlike the index file). |
| `timestamp` | string | ISO 8601 with real sub-second millis + offset. |
| `cage` | string | Cage identifier. |
| `rack` | string | Rack id (e.g. `AAAA`); empty for non-placement events. |
| `position` | string | Slot on the rack (e.g. `A6`); empty for non-placement events. |
| `event` | enum | `REGISTERED`, `ADDED`, `CAGE_ONLINE`, `INSERTED`, `UPDATED`, `REMOVED`. |

Typical lifecycle: `REGISTERED → ADDED → CAGE_ONLINE → INSERTED (rack+position)` at
start, `UPDATED` pings during the run, and `REMOVED` (+ a fresh `INSERTED`) at a
cage change.

See [`../mock/`](../mock/) for a deterministic generator that reproduces both file
shapes as synthetic data.
