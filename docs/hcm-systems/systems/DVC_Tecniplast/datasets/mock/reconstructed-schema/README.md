# Mock DVC® dataset — HCMO validation (reconstructed schema)

> **⚠️ Superseded.** This mock was built **before** the real DVC export headers were
> known, so its columns are a *reconstruction* (`DateTime, ActivationDensityPct,
> BeddingStatusIndex, …`). The real cohort-7623 export has since revealed the actual
> headers — use the **real-schema** traces one level up in [`../`](../) for validation.
> This folder is kept for reference only.
>
> The `dvc-system-profile.md` referenced below now lives at the system-folder root:
> [`../../../dvc-system-profile.md`](../../../dvc-system-profile.md).

Synthetic, redistributable home-cage-monitoring data shaped like a **Tecniplast Digital
Ventilated Cage (DVC®)** export, for validating the **HCMO** ontology. **Not real data.**

## Files
| File | What it is |
|---|---|
| `generate_dvc_mock.py` | Deterministic, stdlib-only generator (fixed seed → identical output). |
| `dvc_activity_mock.csv` | **Not committed** (4.7 MB, regenerable). Run the generator to produce it: 4 cages × 7 days × 1-min bins = 40,320 rows. |
| `README.md` | This file (data dictionary + provenance). |

## Data dictionary (`dvc_activity_mock.csv`)
One row **per cage per 1-minute bin**. 14 columns:

| Column | Type | Unit | Meaning |
|---|---|---|---|
| `DateTime` | ISO 8601 + offset | — | Bin start, facility local time (UTC+01:00). |
| `UnixTimeMillis` | int | ms (UTC) | Same instant, epoch milliseconds. |
| `RackId` | str | — | Rack identifier. |
| `CagePosition` | str | — | Slot on the rack. |
| `CageId` | str | — | Logical cage identifier. |
| `Strain` | str | — | Mouse strain (joined metadata). |
| `Sex` | str | — | male \| female. |
| `HousingDensity` | int | animals | Animals in cage (1 = single-housed). |
| `LightPhase` | str | light\|dark | 12:12 LD, lights on 07:00–19:00. |
| `DaysSinceCageChange` | float | days | Days since last cage change. |
| `ActivationDensityPct` | float | % (0–100) | Animal Locomotion Index (ALI). |
| `BeddingStatusIndex` | float | arbitrary | Higher = drier bedding. |
| `RackTemperatureC` | float | °C | Rack environmental monitor. |
| `RackHumidityPct` | float | % RH | Rack environmental monitor. |

## Fidelity & caveats
- **The exact vendor CSV headers and timestamp format are not publicly documented.** These
  header strings are a **reconstruction** consistent with the documented DVC variables
  (ALI, BSI, environment, 1-min bins). Faithful *shape*, not verbatim vendor headers. See
  `dvc-system-profile.md` §5.
- Value ranges are grounded in the peer-reviewed DVC corpus (dark-phase-dominant circadian
  activity; sub-linear group scaling; BSI decline between cage changes). See profile §9.
- Regenerate: `python3 generate_dvc_mock.py` (`--days N` to shorten).
