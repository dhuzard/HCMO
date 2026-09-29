# HCMO validation profile — Live Mouse Tracker (LMT)

> **Evidence rule:** every fact carries a source. **[site]** is the LMT home page
> <https://micecraft.org/lmt/>; **[paper]** is de Chaumont et al. 2019
> (<https://doi.org/10.1038/s41551-019-0396-1>); **[db]** means the fact was read
> directly from the public sample database (see §7), which was inspected on
> 2026-09-29; **[authors]** marks information given by the HCMO authors on
> 2026-09-29. Where a fact is not available it is written **"unknown — not found"**.

## 1. Overview

Live Mouse Tracker is an open-source system for long-term tracking of mice or
rats with automatic annotation of individual and social behaviour, over periods
from hours to months **[site]**. A depth camera tracks the animals and RFID
antennas under the arena keep their identities over time **[site] [paper]**.

- **Authors:** de Chaumont et al. **[paper]**
- **Type:** open-source (tracker and analysis scripts downloadable) **[site]**
- **Licence:** GNU GPL v3 **[authors]**; the analysis repository declares
  GPL-3.0 (<https://github.com/fdechaumont/lmt-analysis/blob/master/LICENSE>).

## 2. Monitored entities

- **Species:** mice or rats **[site]**.
- **Housing:** group-housed; the sample contains 4 animals **[db]**.
- **Identity:** each animal carries an RFID tag (ISO FDX-B, 134.2 kHz) **[site]**,
  stored in `ANIMAL.RFID` **[db]**.

## 3. Sensors & actuators

| Component | Transduces | Sampling rate | Notes |
|---|---|---|---|
| Depth camera (Kinect) | Depth image of the arena from above | 30 frames/s (sample: 23,890 frames over 796 s) **[db]** | Mounted at a calibrated 63 cm height **[site]** |
| RFID antennas | Glass PIT tags (APT12, FDX) at 134.2 kHz | unknown — not found | Used to match tracks to identities **[site]**; `RFID MATCH` / `RFID MISMATCH` events **[db]** |
| Video recorder | Arena video | — | MP4 in 10-minute segments **[site]** |

No actuators.

## 4. Measured & derived parameters

| Parameter | Raw/derived | Where stored | Notes |
|---|---|---|---|
| Mass-centre, front and back points (x, y, z) | Derived per frame from depth | `DETECTION.MASS_*`, `FRONT_*`, `BACK_*` **[db]** | Pixels **[authors]**; x/y range 96–416 and 58–362, z 0–128 in the sample **[db]** |
| Rearing, looking up, looking down | Derived per frame | `DETECTION.REARING`, `LOOK_UP`, `LOOK_DOWN` (0/1) **[db]** | |
| Behavioural events | Derived intervals | `EVENT` **[db]** | 62 distinct names in the sample, see §5.3 |
| Identity matching | Derived | `EVENT` (`RFID MATCH`, `RFID MISMATCH`, `RFID ASSIGN ANONYMOUS TRACK`) **[db]** | |

## 5. Data output

### 5.1 Formats and pipeline

- **Experiment database:** one standalone SQLite file per experiment **[site]**
  (HCMO concept `ff:live-mouse-tracker-sqlite`).
- **Video:** MP4 files in 10-minute segments, synchronised with frame numbers
  and timestamps **[site]** (HCMO concept `ff:mp4`).
- **Background depth images** of the enclosure **[site]**.
- **Post-processing:** Python analysis scripts in
  <https://github.com/fdechaumont/lmt-analysis> read the database and write event
  tables back into it **[site]**. The sample's `LOG` table records such runs
  (`Build Event Oral Oral Contact`, `Build Event Move`, …) dated 2022-09-08 and
  2022-12-20, i.e. years after the 2018 recording **[db]**.

### 5.2 Database schema **[db]**

| Table | Rows in sample | One row per | Key columns |
|---|---|---|---|
| `ANIMAL` | 4 | animal | `ID` (integer key), `RFID` (text), `GENOTYPE` (text, empty in sample), `NAME` (`A`–`D`) |
| `FRAME` | 23,890 | video frame | `FRAMENUMBER` (key), `TIMESTAMP` (Unix epoch, milliseconds), `NUMPARTICLE`, `PAUSED` |
| `DETECTION` | 95,281 | animal × frame | `FRAMENUMBER` → `FRAME`, `ANIMALID` → `ANIMAL`, mass/front/back x-y-z, `REARING`, `LOOK_UP`, `LOOK_DOWN`, `DATA` (XML with the same values plus the segmentation mask) |
| `EVENT` | 67,976 | event interval | `NAME`, `DESCRIPTION`, `STARTFRAME`, `ENDFRAME`, `IDANIMALA`–`IDANIMALD` → `ANIMAL`, `METADATA` (JSON text) |
| `RFIDEVENT` | 0 | RFID read | `RFID`, `TIME`, `X`, `Y` |
| `LOG` | 142 | processing run | `process`, `version`, `date`, `tmin`, `tmax` |

Time is carried by frame numbers; `FRAME.TIMESTAMP` converts them to absolute
time. The sample starts at 2018-01-10 07:55:02 UTC and lasts 13 min 16 s.

### 5.3 Events in the sample **[db]**

Events involve one animal (20,549), two (46,898), three (516) or four (11), or
none (2). The 62 names fall into these groups:

- **Individual behaviour:** `Move isolated`, `Stop isolated`, `Rearing`,
  `Rear isolated`, `Rear at periphery`, `Rear in centerWindow`, `Look down`,
  `WallJump`, `Stop`, `SAP` (stretch attend posture **[authors]**), …
- **Dyadic social behaviour:** `Contact`, `Oral-oral Contact`,
  `Oral-genital Contact`, `Side by side Contact`, `Approach`, `Social approach`,
  `Follow`, `Escape`, `Social escape`, `Get away`, `Break contact`, `Train2`
  (a train of two mice following each other **[authors]**), …
- **Group configurations:** `Group2`, `Group3`, `Group4`, `Group 3 make`,
  `Group 3 break`, `Nest3_`, …
- **Zones:** `Center Zone`, `Periphery Zone`, `Water Zone`, `Water Stop`.
- **Identity and quality control:** `RFID MATCH`, `RFID MISMATCH`, `badIdentity`,
  `badOrientation`, `badSegmentation`, `Detection`, `Head detected`.
- **Manual annotations:** `manualContact`, `manualOralGenital`,
  `manualOralOralContact`, `manualSideSideOpposite`, `manualSideSideSame`.
- **Other:** `MACHINE LEARNING ASSOCIATION`, sequence events
  (`seq oral oral - oral genital`), and `coucou`, probably a test label
  **[authors]**.

## 6. Software & interoperability

- Tracker: Windows application, current build "June 2026 — build 1271" **[site]**.
- Official analysis: <https://github.com/fdechaumont/lmt-analysis> **[site]**.
- Third-party tools listed on the site: LMT-toolkit
  (<https://github.com/ntorquet/lmt_toolkit_analysis>), LMT-Easy, LMT Widget
  Tools, MouseKing, Tripping Rats **[site]**.
- Data access: file export (the SQLite file is the primary output); HCMO concept
  `dam:file-export`.

## 7. Public data & documentation

- **Sample experiment:**
  <https://micecraft.org/lmt/download/20180110_validation_4_ind_Experiment_6644_e.sqlite>
  — 141,179,904 bytes, SHA-256
  `0d96d4d9d0141ac19acdc25b29f0a6577a7c2f86889080f7095df46ec3cba6b6` (downloaded
  2026-09-29). Not committed to this repository because of its size.
- Analysis tutorial and troubleshooting guides are linked from the home page **[site]**.

## 8. HCMO mapping

Multi-animal events follow the HCMO pattern adopted on 2026-09-29: the feature
of interest of a behavior observation is either one `hcm-bio:Subject` or an
`hcm-bio:InteractingGroup` whose members are stated with `hcm-bio:hasMember`;
directed behaviors add `hcm-obs:hasInitiator` and `hcm-obs:hasRecipient`.

| LMT | HCMO pattern |
|---|---|
| The database file | `hcm-tech:TimeSeries` with `hcm-tech:hasFileFormatConcept ff:live-mouse-tracker-sqlite`, `hcm-tech:hasFileFormat "application/vnd.sqlite3"`, `hcm-tech:hasDataAccessMethod dam:file-export` |
| Depth camera, RFID antennas | `hcm-tech:Sensor` |
| `ANIMAL` row | `hcm-bio:Subject`, with the RFID as identifier |
| `EVENT` with one animal | `hcm-obs:BehaviorObservation`; feature of interest = the subject |
| `EVENT` with two to four animals | `hcm-obs:BehaviorObservation`; feature of interest = an `hcm-bio:InteractingGroup` whose members are `IDANIMALA`–`IDANIMALD` |
| Directed `EVENT` | additionally `hcm-obs:hasInitiator` = `IDANIMALA`, `hcm-obs:hasRecipient` = `IDANIMALB` |
| `EVENT.NAME` | `hcm-obs:hasBehaviorType` on the `hcm-obs:BehaviorResult` |
| `STARTFRAME`, `ENDFRAME` | `sosa:phenomenonTime` interval, via `FRAME.TIMESTAMP` |
| `DETECTION` rows | `hcm-obs:LocationResultTable` |

**Still to confirm** against the lmt-analysis code: which events are directed,
and that `IDANIMALA` is always the initiator. Likely directed: `Approach`,
`Social approach`, `Approach contact`, `Approach rear`, `Follow`, `FollowZone`,
`Escape`, `Social escape`, `Get away`, `Oral-genital Contact`, `Train2`. Likely
symmetric (group only): `Contact`, `Oral-oral Contact`, `Side by side Contact`,
`Side by side Contact, opposite way`, `Group2`, `Group3`, `Group4`.

## Sources

- LMT home page: <https://micecraft.org/lmt/> (read 2026-09-29).
- de Chaumont F. et al. (2019) Real-time analysis of the behaviour of groups of
  mice via a depth-sensing camera and machine learning. *Nature Biomedical
  Engineering* 3:930–942. <https://doi.org/10.1038/s41551-019-0396-1>
- Sample database, inspected with SQLite (see §7).
