# HCMO validation profile — Tecniplast Digital Ventilated Cage (DVC®)

> **System:** Digital Ventilated Cage (DVC®) · **Vendor:** Tecniplast S.p.A. (Buguggiate, Italy), with the DVC Analytics cloud platform.
> **Purpose of this file:** structured, source-cited validation data for the **HCMO** ontology (an OWL model for home-cage monitoring of laboratory rodents — monitored enclosures, subjects/groups, environment + measurements, observations + results, and the sensors/hardware/software producing the data). HCMO is the "ontology of home cage" strand of the **COST Action CA20135 "TEATIME"** effort to standardise HCM. [TEATIME](https://www.cost-teatime.org/) · [TEATIME HCM definition](https://www.cost-teatime.org/about/hcm-definition/)
>
> **Evidence rule:** every factual claim carries a URL. Where a fact is not available from a citable source it is written **"unknown — not found"** rather than guessed. The exact vendor CSV export headers and any downloadable public DVC dataset were **not** locatable from open sources this session and are flagged as such in §5 and §7.

---

## 1. Overview

The DVC® is a **commercial, non-intrusive, capacitance-based** home-cage monitoring platform from **Tecniplast**. A sensing board carrying a grid of capacitive electrodes is mounted **externally, underneath each standard individually ventilated cage (IVC)** on the rack; it detects animal position and movement through changes in electrical capacitance — **no cameras, no tethers, no implants, no animal handling**. Because the sensor lives at the rack, the system scales to facility level and runs 24/7, capturing the dark (active) phase that conventional daytime testing misses. [Tecniplast DVC product page](https://digitalcage-tecniplast.com/en/products/dvc-digital-ventilated-cage-for-digital-vivarium.html) · [Iannello 2019, Heliyon](https://doi.org/10.1016/j.heliyon.2019.e01454)

- **Modality:** electrical-capacitance (electric-field) proximity sensing — *not* video, *not* RFID, *not* infrared beam-break. [Iannello 2019](https://doi.org/10.1016/j.heliyon.2019.e01454)
- **Commercial vs open-source:** **commercial/proprietary hardware + cloud software (DVC Analytics)**. The raw-capacitance → Animal Locomotion Index / Bedding Status Index computation inside DVC Analytics is **proprietary and undocumented from primary sources**. [Tir 2025, Sci Rep](https://doi.org/10.1038/s41598-025-87530-6)
- **Vendor / key authors:** Tecniplast S.p.A.; core technology and validation papers are co-authored by Tecniplast scientists (F. Iannello, M. Rigamonti, S. Gaburro). [Iannello 2019](https://doi.org/10.1016/j.heliyon.2019.e01454)
- **Regulatory/safety posture:** the electronics generate only extremely low-intensity EMF, with no adverse clinicopathological effects over 12 months of housing. [Recordati 2019, Toxicol Pathol](https://doi.org/10.1177/0192623319852353)

---

## 2. Monitored entities

- **Species:** **mouse** (*Mus musculus*) is the documented species across the entire peer-reviewed corpus. A targeted literature sweep found **no** primary DVC rat studies — apparent "DVC + rat" hits are abbreviation collisions (dorsal vagal complex, etc.). **Rat support: unknown — not found** as a validated, published use; treat as an evidence gap. [Pernold 2019, PLoS One](https://doi.org/10.1371/journal.pone.0211063) (internal corpus: `knowledge/dvc-literature.md`)
- **Single vs group housing:** **both.** The capacitance signal is intrinsically **cage-level**. *Amount / rhythm / region* metrics (activation/ALI, rest-bout split, RDI, circadian parameters, spatial region metrics) stay valid for **group-housed cages of any numerosity**; only metrics that reconstruct an **individual trajectory** (distance walked, per-animal bout decomposition, ~1 mm centroid) require **single housing**. [Pernold 2023, PLoS One](https://doi.org/10.1371/journal.pone.0280416) · [Sun 2024, Front Neurosci](https://doi.org/10.3389/fnins.2024.1456307)
- **Retrofit vs bespoke enclosure:** **retrofit.** The sensing board mounts under **standard Tecniplast GM500 / DGM "green-line" IVCs**; the cage itself is untouched. A black-cage variant with in-built per-cage LED lighting ("Leddy") turns each cage into an independent light-controlled chamber. [Iannello 2019](https://doi.org/10.1016/j.heliyon.2019.e01454) · [Tir 2025](https://doi.org/10.1038/s41598-025-87530-6)
- **Individual identity:** DVC has **no native RFID**; individual-animal attribution in a group cage is a **contested divide-by-occupancy derivation**, not a direct per-animal measurement. [Sun 2024](https://doi.org/10.3389/fnins.2024.1456307)

---

## 3. Sensors & actuators

| Component | Transduces | Sampling / rate | Range / resolution | Source |
|---|---|---|---|---|
| Capacitive electrode board (12 electrodes, 4×3 planar grid) | Animal presence/position/movement via dielectric (capacitance) change | **4 Hz — every 250 ms**, per electrode, 24/7 | 12 electrodes; centroid ≈ **1 mm** spatial resolution (single-housed); activation is binary per electrode above a noise threshold | [Iannello 2019](https://doi.org/10.1016/j.heliyon.2019.e01454) · [Tir 2025](https://doi.org/10.1038/s41598-025-87530-6) · [Pernold 2023](https://doi.org/10.1371/journal.pone.0280416) |
| Same electrode board (environmental channel) | **Bedding moisture** as a decline in electromagnetic-field strength → **Bedding Status Index (BSI)** | derived from the same 4 Hz stream | arbitrary units; BSI ∝ inverse of moisture | [Brachs 2025, Lab Anim (NY)](https://doi.org/10.1038/s41684-025-01648-8) |
| DVC Rack Environmental Monitor | Rack **temperature** and **relative humidity** | continuous (exact rate: **unknown — not found**) | operating context ~**55 ± 10 % RH** logged | [Brachs 2025](https://doi.org/10.1038/s41684-025-01648-8) |
| "Leddy" per-cage LED lighting (actuator) | Programmable light delivery per cage | programmable LD schedules | **~100 photopic lux** at rack level 22 (70 melanopic / 75 rhodopic lux); **no in-cage light sensor** (stated limitation) | [Tir 2025](https://doi.org/10.1038/s41598-025-87530-6) |
| GYM500 running wheel (optional add-on) | Wheel rotation → running distance/speed | read by the same 12-electrode board; logged per hour | cumulative running distance; non-runner cut-off < 500 m/peak-hour | [Hopkins 2025, In Vivo](https://doi.org/10.21873/invivo.14120) |

---

## 4. Measured & derived parameters

| Parameter | Unit | Raw/Derived | Rate | Notes |
|---|---|---|---|---|
| Electrode capacitance (per electrode) | arbitrary (capacitance) | **raw** | 4 Hz | The atomic signal; 12 channels/cage. [Iannello 2019](https://doi.org/10.1016/j.heliyon.2019.e01454) |
| Electrode activation | binary (0/1) per electrode | derived | per sample | Activates when \|Δ capacitance\| exceeds empty-cage noise threshold (λ=1.25 in Pernold recipe). [Pernold 2023](https://doi.org/10.1371/journal.pone.0280416) |
| Activation Density (AD) / Electrode Activation Density (EAD) | ratio 0–1 | derived | per second → binned | activations ÷ (interval × #electrodes). EAD vs tracking distance rₛ > 0.95. [Iannello 2019](https://doi.org/10.1016/j.heliyon.2019.e01454) · [Pernold 2023](https://doi.org/10.1371/journal.pone.0280416) |
| **Animal Locomotion Index (ALI)** / "…Smoothed" | **% (0–100)** | derived (proprietary) | binned (1 min / 1 h export) | Proportion of the 12 electrodes active in a bin; the **default DVC Analytics activity readout**. [Tir 2025](https://doi.org/10.1038/s41598-025-87530-6) |
| Distance walked | metres | derived | per bout/day | Single-housed only; ~**330 m/day** baseline (C57BL/6J). [Pernold 2023](https://doi.org/10.1371/journal.pone.0280416) |
| Rest / activity bouts (long rest ≥40 s, MOTS, locomotion) | count / seconds | derived | per day | ~**7,100 bouts/day**; ~67 % time in long rest. Single-housed. [Pernold 2023](https://doi.org/10.1371/journal.pone.0280416) |
| **Regularity Disruption Index (RDI)** | dimensionless (sample entropy) | derived | per light/dark phase | Butterworth band-pass + sample entropy (m=2, r=0.2) on minute-binned activity; transdiagnostic biomarker. [Golini 2020, Front Neurosci](https://doi.org/10.3389/fnins.2020.00896) |
| Circadian parameters (period, IS, IV, RA, onsets) | h / dimensionless | derived | per day(s) | chi-square periodogram + Witting equations. [Tir 2025](https://doi.org/10.1038/s41598-025-87530-6) |
| Spatial: frontality, wall activity (thigmotaxis), Gini | % / index | derived | per bin/day | From the 12-electrode geometry; group-housed-friendly. [Fuochi 2023, Sci Rep](https://doi.org/10.1038/s41598-023-37464-8) |
| **Bedding Status Index (BSI)** | arbitrary units | derived | binned | Higher = drier; drives cage-change decisions. [Collins 2025, JAALAS](https://doi.org/10.30802/AALAS-JAALAS-24-151) |
| Urination Index (UI) | UI (≈1.4 UI per mL) | derived (deterministic transform of BSI) | cumulative | Metabolic biomarker; flags hyperglycaemia days early. [Brachs 2025](https://doi.org/10.1038/s41684-025-01648-8) |
| Rack temperature / relative humidity | °C / % RH | raw | continuous | Environmental context. [Brachs 2025](https://doi.org/10.1038/s41684-025-01648-8) |
| Wheel running distance (GYM500) | metres | derived | per hour | Optional add-on. [Hopkins 2025](https://doi.org/10.21873/invivo.14120) |

---

## 5. Data output — MOST IMPORTANT

### 5.1 Formats and pipeline
- The **raw stream** is 12 electrodes × 4 Hz ≈ 48 readings/s/cage ≈ **~2.5 MB/cage/day**. Mice (~70 % water) raise local capacitance. [Pernold 2023](https://doi.org/10.1371/journal.pone.0280416) · [Iannello 2019](https://doi.org/10.1016/j.heliyon.2019.e01454)
- **DVC Analytics (cloud)** handles acquisition, visualisation and export, and computes the proprietary **ALI** and **BSI**. Data are **exported as CSV**, typically binned to **1-minute or 1-hour** intervals; downstream statistical analysis is done in R/Python/Prism. [Tir 2025](https://doi.org/10.1038/s41598-025-87530-6) · internal corpus `knowledge/dvc-literature.md`
- The open-source **UrinatoR** R/Shiny app consumes exported DVC **BSI CSVs** to compute the Urination Index — the only public, runnable DVC analysis pipeline located. [UrinatoR (GitHub, MIT)](https://github.com/Mortendall/UrinatoR)

### 5.2 Concrete record/column schema
> ⚠️ **Provenance caveat:** the **exact vendor header strings and timestamp format used by DVC Analytics are NOT publicly documented** (proprietary export). The schema below is the **documented-variable set** — timestamp, cage identity, ALI, BSI, environment at 1-min/1-h bins — expressed with **reconstructed, self-describing field names**. It is the schema of the accompanying mock file `dvc_activity_mock.csv`, and should be treated as a faithful *shape*, not as verbatim vendor headers. Variables and their existence/units are source-backed; the header strings are illustrative.

One row **per cage per time-bin** (long format). Real header row from `dvc_activity_mock.csv`:

```
DateTime,UnixTimeMillis,RackId,CagePosition,CageId,Strain,Sex,HousingDensity,LightPhase,DaysSinceCageChange,ActivationDensityPct,BeddingStatusIndex,RackTemperatureC,RackHumidityPct
2026-03-02T09:00:00+01:00,1772438400000,RACK-A1,C03,DVC-A1-C03,C57BL/6J,male,1,light,0.0,12.77,99.89,22.36,54.6
```

| Field | Type | Unit | Source-backed variable? |
|---|---|---|---|
| `DateTime` | string (ISO 8601 + offset) | — | timestamp exists; **exact vendor format unknown — not found** (ISO 8601 chosen) |
| `UnixTimeMillis` | integer | ms since epoch (UTC) | convenience key; not vendor-verified |
| `RackId` | string | — | rack identity (documented concept) |
| `CagePosition` | string | — | slot on rack (documented concept) |
| `CageId` | string | — | logical cage id |
| `Strain` | string | — | metadata (must be joined; not in raw stream) |
| `Sex` | string | — | metadata |
| `HousingDensity` | integer | animals/cage | cage-level signal driver [Sun 2024](https://doi.org/10.3389/fnins.2024.1456307) |
| `LightPhase` | string | light\|dark | derivable from light programme |
| `DaysSinceCageChange` | float | days | needed to exclude cage-change effects [Fuochi 2023](https://doi.org/10.1038/s41598-023-37464-8) |
| `ActivationDensityPct` | float | % (0–100) | **ALI** [Tir 2025](https://doi.org/10.1038/s41598-025-87530-6) |
| `BeddingStatusIndex` | float | arbitrary | **BSI** [Collins 2025](https://doi.org/10.30802/AALAS-JAALAS-24-151) |
| `RackTemperatureC` | float | °C | env channel [Brachs 2025](https://doi.org/10.1038/s41684-025-01648-8) |
| `RackHumidityPct` | float | % RH | env channel [Brachs 2025](https://doi.org/10.1038/s41684-025-01648-8) |

- **Volume per cage/subject/day:** **~2.5 MB/cage/day** raw (12×4 Hz); the binned CSV export is far smaller — at **1-min bins, 1,440 rows/cage/day** (this file: 4 cages × 7 days = 40,320 rows, ~4.6 MB). [Pernold 2023](https://doi.org/10.1371/journal.pone.0280416)
- **Timestamp format + timezone:** **unknown — not found** for the native vendor export; papers report per-facility local time. This profile adopts **ISO 8601 with explicit UTC offset** (`+01:00`, Europe/Rome-like) plus a UTC unix-ms mirror, and states the timezone explicitly — the FAIR-correct convention the vendor format does not guarantee.
- **Data dictionary link:** no public vendor data dictionary was located (**unknown — not found**); this table + `datasets/mock/dvc/README.md` serve as the dictionary for the mock file.

---

## 6. Software & interoperability

- **DVC Analytics** (cloud) is the acquisition/visualisation/export layer and computes ALI + BSI; the raw→ALI/BSI step is **proprietary**. [Tir 2025](https://doi.org/10.1038/s41598-025-87530-6)
- **Export:** CSV of binned metrics (1-min / 1-h). Raw capacitance is exportable in principle but arrives **without the metadata** (strain, sex, age, housing density + configuration, cage-change schedule, light programme, intervention timestamps) that every analysis recipe depends on — the binding reuse constraint is **metadata, not maths**. (Neuronautix synthesis, grounded in `knowledge/dvc-literature.md`)
- **Open API / TTL / standard schemas:** **unknown — not found.** No public REST API spec, no RDF/TTL export, and no adoption of a community standard schema (e.g. SOSA/SSN, ISA, or an HCM ontology) were located from open sources. This is precisely the gap HCMO + a FAIR export convention would fill. [Fuochi 2024, Front Big Data (standards call)](https://doi.org/10.3389/fdata.2024.1390467)
- **Open downstream tooling:** [UrinatoR](https://github.com/Mortendall/UrinatoR) (R/Shiny, MIT) for the Urination Index; all other core metrics (EAD, centroid tracking, RDI, spatial/Gini, circadian) must be **reimplemented from published formulas** — no shipped code. (internal corpus)

---

## 7. Public data & documentation

- **Downloadable sample datasets:** **unknown — not found.** No open DVC dataset on Zenodo/figshare/OSF was locatable this session; several papers state "data available on request" and only UrinatoR ships per-figure Source Data. Treat "public raw DVC dataset" as an evidence gap. [UrinatoR](https://github.com/Mortendall/UrinatoR)
- **Manuals / API docs:** the official Tecniplast catalogue and spec pages (`digitalcage-tecniplast.com`) are the vendor source; note the scientific-papers catalogue pages have been repeatedly **Cloudflare-blocked (HTTP 403)** to automated fetch. [DVC product page](https://digitalcage-tecniplast.com/en/products/dvc-digital-ventilated-cage-for-digital-vivarium.html) · [Tecniplast USA shop listing](https://shop.tecniplastusa.com/products/tecniplast-digital-ventilated-caging-dvc)
- **Key papers (DOIs):**
  1. **Iannello 2019**, *Heliyon* — foundational technology; capacitance sensing ≈ video. [10.1016/j.heliyon.2019.e01454](https://doi.org/10.1016/j.heliyon.2019.e01454)
  2. **Pernold 2023**, *PLoS One* — rest/activity bout budget; the raw-signal recipe. [10.1371/journal.pone.0280416](https://doi.org/10.1371/journal.pone.0280416)
  3. **Tir 2025**, *Sci Rep* — DVC for circadian phenotyping; per-cage LED; ALI. [10.1038/s41598-025-87530-6](https://doi.org/10.1038/s41598-025-87530-6)
  4. **Brachs 2025**, *Lab Anim (NY)* — BSI → Urination Index metabolic biomarker (pairs with UrinatoR). [10.1038/s41684-025-01648-8](https://doi.org/10.1038/s41684-025-01648-8)
- **License / redistributability:** the papers are open-access (CC-BY variants — check each). **DVC raw data / exports are proprietary to the generating facility**; there is no vendor-blessed open license for DVC data. The **mock file in this directory is synthetic** and freely redistributable — that is its purpose.

---

## 8. HCMO mapping notes

Mapping the DVC data to HCMO's described modules (monitored enclosures; subjects & experimental groups; environment & measurements; observations & results; sensors/hardware/software):

- **Monitored enclosure:** one DVC cage = an **individually ventilated cage (GM500/DGM)** instance, sited at a `RackId` + `CagePosition`; **retrofit**, not bespoke. Populates an *Enclosure/Cage* class with a *rack-position* property and a *ventilation-type* = IVC.
- **Subjects & experimental groups:** `HousingDensity` distinguishes a **single Subject** (density 1, individually attributable) from an **ExperimentalGroup** (density > 1, cage-level aggregate). `Strain`/`Sex` are Subject/Group attributes that **must be joined from metadata** — they are not in the raw sensor stream.
- **Environment & measurements:** `RackTemperatureC`, `RackHumidityPct`, and the **light programme** (Leddy) are *Environment* properties/measurements; `BeddingStatusIndex` is an environmental measurement that **doubles as a physiological biomarker** (Urination Index) — a dual-classification case for the ontology.
- **Observations & results:** each row is an **Observation** (a `DateTime`) yielding **Results** — `ActivationDensityPct` (ALI) and `BeddingStatusIndex` — following a sensor→observation→result pattern (compatible with SOSA/SSN framing).
- **Sensors / hardware / software:** the **12-electrode capacitive board**, the **Rack Environmental Monitor**, the **Leddy LED** actuator, the optional **GYM500 wheel**, and the **DVC Analytics** software (which *derives* ALI/BSI) — a Device/Software provenance chain from raw capacitance to derived metric.

**Gaps in the ontology this system stresses:**
1. **Cage-level vs individual attribution.** DVC's signal is a cage aggregate; HCMO must represent an Observation whose `hasFeatureOfInterest` is a **Group** (or Cage), not a Subject — and represent the *contested* divide-by-occupancy derivation as an explicit, flagged transformation, not a silent per-Subject fact. [Sun 2024](https://doi.org/10.3389/fnins.2024.1456307)
2. **Proprietary derivation provenance.** ALI/BSI are computed by closed software; HCMO needs a way to state "derived, algorithm proprietary/opaque" in the provenance chain. [Tir 2025](https://doi.org/10.1038/s41598-025-87530-6)
3. **Dual-role channels.** BSI is simultaneously an *environmental* measurement and the input to a *physiological/metabolic* biomarker — the ontology should allow one raw channel to feed multiple observation types. [Brachs 2025](https://doi.org/10.1038/s41684-025-01648-8)
4. **Missing-metadata as a first-class concern.** The reuse-blocking fact is that raw exports lack strain/sex/density/cage-change/light metadata; HCMO's value is precisely in mandating these as required properties. [Fuochi 2024](https://doi.org/10.3389/fdata.2024.1390467)
5. **No native individual ID.** No RFID → HCMO cannot assume a Subject-level identifier exists for grouped DVC cages.

---

## 9. Mock-data recipe

Reproducible generator: **`generate_dvc_mock.py`** (stdlib only, seeded → deterministic). Output: **`dvc_activity_mock.csv`**.

- **Columns:** as in §5.2 (14 fields; one row per cage per 1-min bin).
- **Subjects / cages:** **4 cages** on one rack — 2 single-housed **C57BL/6J males** (density 1, individually attributable) + 2 group-housed **BALB/cAnNCrl females** (density 4, cage-level aggregate).
- **Duration & sampling:** **7 days**, **1-min bins** (10,080 bins/cage; 40,320 rows total). Study starts at a **cage change (Mon 09:00 local, UTC+01:00)**.
- **Value ranges & structure (grounded in the corpus):**
  - `ActivationDensityPct` (ALI, 0–100 %): circadian drive with **dark-phase peak** (single-housed ~19 % dark vs ~3 % light; group aggregate ~44 % dark, scaled **sub-linearly** with density — 4 animals ≈ 2.3×, not 4×), plus discrete high-activity bouts, long rests, a 2-day acclimatisation lift, and a transient post-cage-change handling bump. [Pernold 2023](https://doi.org/10.1371/journal.pone.0280416) · [Sun 2024](https://doi.org/10.3389/fnins.2024.1456307)
  - `BeddingStatusIndex` (BSI): starts ~100 (fresh), **declines over the week** (faster at higher density), resets at cage change. [Collins 2025](https://doi.org/10.30802/AALAS-JAALAS-24-151)
  - `RackTemperatureC`: ~22 °C ± diurnal 0.5 °C. `RackHumidityPct`: ~55 % RH, drifting up as bedding soils. [Brachs 2025](https://doi.org/10.1038/s41684-025-01648-8)
  - **Light programme:** 12:12 LD, lights on 07:00–19:00 → `LightPhase`.
- **To regenerate:** `python3 generate_dvc_mock.py` (add `--days N` to shorten).

---

## Sources

- https://www.cost-teatime.org/
- https://www.cost-teatime.org/about/hcm-definition/
- https://digitalcage-tecniplast.com/en/products/dvc-digital-ventilated-cage-for-digital-vivarium.html
- https://shop.tecniplastusa.com/products/tecniplast-digital-ventilated-caging-dvc
- https://doi.org/10.1016/j.heliyon.2019.e01454 (Iannello 2019, Heliyon)
- https://doi.org/10.1371/journal.pone.0211063 (Pernold 2019, PLoS One)
- https://doi.org/10.1177/0192623319852353 (Recordati 2019, Toxicol Pathol)
- https://doi.org/10.1038/s41598-025-87530-6 (Tir 2025, Sci Rep)
- https://doi.org/10.1371/journal.pone.0280416 (Pernold 2023, PLoS One)
- https://doi.org/10.1038/s41598-023-37464-8 (Fuochi 2023, Sci Rep)
- https://doi.org/10.3389/fnins.2024.1456307 (Sun 2024, Front Neurosci)
- https://doi.org/10.3389/fnins.2020.00896 (Golini 2020, Front Neurosci)
- https://doi.org/10.30802/AALAS-JAALAS-24-151 (Collins 2025, JAALAS)
- https://doi.org/10.1038/s41684-025-01648-8 (Brachs 2025, Lab Anim NY)
- https://doi.org/10.21873/invivo.14120 (Hopkins 2025, In Vivo)
- https://doi.org/10.3389/fdata.2024.1390467 (Fuochi 2024, Front Big Data)
- https://github.com/Mortendall/UrinatoR
