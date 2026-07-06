# Tecniplast DVC® — HCMO reference example

**First worked example** for HCMO validation: a commercial, capacitance-based
home-cage monitoring platform, with a **source-cited system profile**, a **real
export** (cohort 7623), and **synthetic look-alike traces** that mirror the real
schema exactly.

| | |
|---|---|
| **System** | Digital Ventilated Cage (DVC®) |
| **Vendor** | Tecniplast S.p.A. (Buguggiate, Italy) + DVC Analytics cloud |
| **Modality** | EMF / electrical-capacitance proximity sensing (no camera, no RFID, no implant) |
| **Sensor** | 12 capacitive electrodes (4×3 grid) under each IVC, 4 Hz, 24/7 |
| **Key outputs** | Activation/Locomotion Index (activity), Bedding Status Index, rack temp/humidity |
| **Housing** | Single **and** group (signal is cage-level) |
| **Species** | Mouse (rat use: not found in the literature) |

## Contents

```
DVC_Tecniplast/
  README.md                    ← this file
  dvc-system-profile.md        ← full source-cited profile (9 sections + Sources)
  datasets/
    real/                      ← real cohort-7623 export + data dictionary
      Cohort7623_animal_loc__index_smoothed.csv
      Cohort7623_events.csv
      README.md
    mock/                      ← synthetic traces matching the REAL schema (+ generator)
      generate_dvc_traces.py
      mock_B6_M_animal_loc__index_smoothed.csv
      mock_B6_M_events.csv
      reconstructed-schema/    ← earlier mock (headers guessed); superseded
      README.md
```

- **Start here:** [`dvc-system-profile.md`](dvc-system-profile.md) — what the system is,
  its sensors, every measured/derived parameter, the data-output analysis, and full
  citations.
- **Real data + schema:** [`datasets/real/README.md`](datasets/real/README.md).
- **Mock traces + generator:** [`datasets/mock/README.md`](datasets/mock/README.md).

## HCMO mapping (highlights)

From the profile §8 — how a DVC export populates HCMO:

- **Enclosure:** one DVC cage = an IVC (GM500/DGM) at a `rack` + `position` (retrofit).
- **Subjects vs groups:** housing density 1 → an individually-attributable **Subject**;
  density > 1 → a cage-level **ExperimentalGroup**. Strain/sex are joined metadata, not
  in the raw stream.
- **Observations & results:** each 1-min bin is an **Observation** yielding **Results**
  (activation index; bedding/temperature/humidity) — a sensor → observation → result
  chain compatible with SOSA/SSN.
- **Sensors/software:** capacitive board + rack environmental monitor + DVC Analytics
  (which *derives* the indices) form a device/software provenance chain.

**Gaps this system stresses in the ontology** (design fodder for v2):
1. **Cage-level vs individual attribution** — the feature of interest is often a Group/Cage, not a Subject.
2. **Proprietary derivation provenance** — indices are computed by closed software; provenance must say "derived, algorithm opaque".
3. **Dual-role channels** — Bedding Status Index is both an *environmental* measurement and a *physiological* biomarker (Urination Index).
4. **Missing-metadata as first-class** — raw exports lack strain/sex/density/cage-change/light metadata; HCMO's value is mandating them.
5. **No native individual ID** — no RFID, so no assumed Subject-level identifier for grouped cages.

## Provenance & licensing

The profile and mock data are synthetic/derived and freely redistributable. The
**real** cohort-7623 files are contributor-provided for HCMO validation — see
[`datasets/real/README.md`](datasets/real/README.md) before redistributing. All factual
claims in the profile carry a source URL; unavailable facts are marked
"unknown — not found" rather than guessed.
