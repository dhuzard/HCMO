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
  hcmo-mapping.tsv             ← native concept → HCMO mapping table (coverage evaluation)
  generate_hcmo_instance.py    ← builds the instance graph below (real + synthetic + declared metadata)
  ../../../../examples/dvc-tecniplast.ttl
                               ← profile-level RDF ABox graph
  ../../../../examples/systems/dvc-tecniplast.ttl
                               ← GENERATED instance graph (real cohort 7623 + synthetic B6_F + metadata)
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
- **RDF ABox profile:** [`../../../../examples/dvc-tecniplast.ttl`](../../../../examples/dvc-tecniplast.ttl)
  organizes the DVC example as explicit `rdf:type` assertions,
  instance-to-instance object-property links, and instance-to-literal data values.
  It intentionally does not assert enclosure dimensions because they are not
  recorded in this local profile.

## Instance graph for the coverage evaluation

[`generate_hcmo_instance.py`](generate_hcmo_instance.py) builds
`examples/systems/dvc-tecniplast.ttl`, which is validated against the standard
SHACL shapes and queried by the cross-system competency questions in
[`evaluation/`](../../../../evaluation/). It combines **three provenance
classes**, each marked in the graph:

1. **Real** — the cohort-7623 export (group `B6_M`, rack `AAAA`): all **24
   cages** as `hcm:MonitoredEnclosure`s at their rack positions, the real
   `INSERTED`/`REMOVED` events as `hcm:OperationalStatusRecord`s with validity
   intervals (nine cages were removed during the run; two never re-appear), and
   **720 real 1-minute activation-index bins**.
2. **Synthetic** — a second cohort (group `B6_F`, rack `BBBB`, 8 cages) written
   by [`datasets/mock/generate_dvc_traces.py`](datasets/mock/) so that the
   scenario also contains cages of females, contributing 240 further bins.
3. **Declared experimental metadata** — everything the export does *not* carry,
   supplied to make the scenario realistic and linked to a
   `mock-experimental-metadata` dataset note so it can never be mistaken for a
   measurement:

| Metadata | Value |
|---|---|
| Light programme | lights **off 19:00–07:00** (12:12) → `hcm-env:LightCycle` |
| Rack environment | temperature and relative humidity every 15 min from the **rack environmental monitor (REM)**, room targets 22 °C / 50 % RH |
| Housing | **2 mice per cage**, C57BL/6J; cages of **males** (`B6_M`) and cages of **females** (`B6_F`); 64 subjects with mock birth dates |
| Husbandry | **cage change every Wednesday, 10:00–11:00** → `prov:Activity` over the cage |
| Enrichment | nesting material in every cage |
| Hardware / software | **GM500** IVC cages, one rack controller per rack, **DVC Analytics 3.5** |

The cage-level activation index keeps the **cage group** as its feature of
interest even though the individual animals are now known, because the
capacitive board measures the cage, not an animal. The rack itself is modelled
as an `hcm:Enclosure` so that the REM readings have something to be about.

The full native-concept → HCMO table is [`hcmo-mapping.tsv`](hcmo-mapping.tsv).
Concepts documented for the DVC but absent from the available exports (Bedding
Status Index / Urination Index, the raw electrode stream) are listed as not
covered *by the export*.

## HCMO mapping (highlights)
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
