# Noldus PhenoTyper + EthoVision XT — HCMO coverage example (synthetic export)

- **Vendor:** Noldus Information Technology (Wageningen, Netherlands)
- **Type:** commercial
- **Modality:** video (integrated home-cage arena with top-unit camera) +
  EthoVision XT tracking and behaviour recognition
- **Status:** active
- **Chapter reference:** Huzard et al. 2026, commercial platforms (PhenoTyper)
- **Data provenance:** **synthetic, schema-faithful.** No PhenoTyper recording
  could be redistributed, so the three files under `datasets/mock/` are generated
  by [`generate_hcmo_instance.py`](generate_hcmo_instance.py) with a fixed seed.
  They reproduce the *shape* of EthoVision XT exports (header block, unit row,
  column names); the values are not recorded data.

## Overview

The PhenoTyper is a 30 × 30 cm home cage with a top unit holding an
infrared-sensitive camera, white and infrared LED units and optional stimuli.
EthoVision XT tracks the animal's centre point (and nose/tail points) from the
video, derives distance, velocity, zone occupancy (e.g. the shelter) and
movement states per time bin, and its Behavior Recognition module classifies
grooming, rearing, eating and sniffing bouts.

## Monitored entities

- **Species:** mouse (rat version exists)
- **Housing:** single (one animal per arena in the mock); group tracking possible
- **Enclosure:** PhenoTyper 3000, 30 × 30 × 35 cm (vendor specification), with shelter

## Sensors & actuators

| Component | Transduces | Sampling | Modelled as |
|---|---|---|---|
| top-unit IR-sensitive camera | video → centre-point coordinates | 25 samples/s | `hcm-tech:Sensor` (`installedIn` arena, 25 Hz) |
| white light LED unit | day/night illumination (EthoVision schedule) | — | `hcm-tech:Actuator` |
| infrared LED unit | illumination for dark-phase tracking | — | `hcm-tech:Actuator` |

## Measured & derived parameters

| Parameter | Unit | Raw/derived | Export |
|---|---|---|---|
| X center, Y center | cm | raw track | track export (25 Hz) |
| Distance moved, Velocity | cm, cm/s | derived per sample / per bin | track + time-bin exports |
| In zone(Shelter), Movement(Moving) durations | s | derived per bin | time-bin export |
| Behavior (grooming, rearing supported/unsupported, eating, sniffing) | event | derived (classifier) | behaviour event export |

## Data output

- `ethovision_track_sample_arena1.csv` — EthoVision "Export raw data" shape: a
  header block (`Number of header lines`, trial, arena, subject, start time,
  sample rate, video file), a column row, a unit row, then one row per sample
  (20 s at 25 samples/s = 500 rows in the mock).
- `ethovision_time_bins.csv` — "Statistics & Charts" shape: one row per arena per
  1-min bin (2 arenas × 120 bins).
- `ethovision_behavior_events.csv` — behaviour events with start/stop seconds
  (53 events in the mock).
- **Timestamps:** trial-relative seconds; converted to absolute time from the
  trial start (2026-06-02 18:00, UTC+02:00). The run spans the light→dark
  transition (dark from 19:00 under the top-unit LED schedule).

## HCMO mapping

The complete mapping is [`hcmo-mapping.tsv`](hcmo-mapping.tsv) (24 concepts).
Highlights:

- **Native subtypes fit:** recognised behaviours → `hcm-obs:BehaviorObservation`
  with `hcm-obs:BehaviorResult`/`hasBehaviorType`; the raw centre-point track →
  `hcm-obs:LocationResultTable` with SemTS `segmentDimension`s for X and Y; the
  LEDs → `hcm-tech:Actuator`; the shelter → `hcm:Enrichment`.
- **Generic pattern (partial):** per-bin distance, velocity, shelter time and
  moving time are `sosa:Observation`s with `hcm-obs:QuantityValue` results and a
  `sosa:usedProcedure` (centre-point tracking); HCMO has no locomotion subtype.
- **Not covered:** the trial entity, per-sample shape descriptors
  (Area/Areachange/Elongation) and the video file itself.

**Gaps exposed:** zone semantics ("in shelter") live only in the observable
property's label; there is no HCMO notion of an arena zone or of a trial;
EthoVision exports no classifier confidence, so `hasConfidenceScore` stays
unused.

## Files in this folder

- `generate_hcmo_instance.py` — writes the three mock exports and
  `../../../../examples/systems/noldus-phenotyper.ttl`
- `hcmo-mapping.tsv` — native concept → HCMO mapping table
- `datasets/mock/` — synthetic exports

## Sources

- Noldus, PhenoTyper and EthoVision XT product documentation: https://www.noldus.com/
- Grieco et al. 2021, *Front. Behav. Neurosci.* 15:735387 (PhenoTyper home-cage monitoring)
- Huzard et al. 2026, *Technologies for Home Cage Monitoring in Preclinical Research*,
  https://doi.org/10.1007/978-3-032-19781-8_7
