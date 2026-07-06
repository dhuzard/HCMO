# HCM systems catalog

Systems, platforms, and companies extracted from **Huzard et al. (2026),
"Technologies for Home Cage Monitoring in Preclinical Research"** (in *Home Cage
Monitoring in Rodents: A Global Effort*, eds. Gaburro & Mandillo, Springer,
https://doi.org/10.1007/978-3-032-19781-8_7). Source PDF:
[`../paper/sources/articles/HCM-technologies_SpringerBook.pdf`](../paper/sources/articles/HCM-technologies_SpringerBook.pdf).

Each is a candidate for a per-system folder. **Priority** is a rough suggestion for
where to start feeding data: **P1** = commercial system with a chapter co-author
and/or well-documented data output; **P2** = open-source system with a published
dataset or code; **P3** = component/toolchain useful for context or mocks.

`slug` = suggested folder name. Fill profiles using [`LLM-RESEARCH-PROMPT.md`](LLM-RESEARCH-PROMPT.md).

## Commercial HCM platforms

| System | Vendor | Modality | Key measured parameters | Data / links | Prio | slug |
|---|---|---|---|---|---|---|
| **DVC® (Digital Ventilated Cage)** | Tecniplast S.p.A. | EMF (capacitive electrode array under cage) | Activity, rest/wake bouts, social/aggression proxy, urination/wetness, polyuria; rack-level room conditions | ~4 MB/cage/day @ 4 Hz; monitors 10,000+ cages. Iannello 2019; Voikar & Gaburro 2020; Brachs et al. 2025 | P1 | `tecniplast-dvc` |
| **Telemetry implants (PhysioTel / HD)** | Data Sciences International (DSI), Harvard Bioscience | Implantable telemetry | ECG, BP, EEG, EMG, glucose, temperature, activity; 600–1000 Hz | ~1.5 GB/subject/7 days. Kramer et al. 2021 | P1 | `dsi-telemetry` |
| **Oxymax / CLAMS** (Comprehensive Lab Animal Monitoring System) | Columbus Instruments | Indirect calorimetry + IR beam-break + plethysmography | VO₂, VCO₂, RER, energy expenditure, activity, feeding, (respiratory freq.) | Czekajewski et al. 1982 (activity patent); Škop et al. 2020/2023 | P1 | `columbus-clams` |
| **PhenoMaster / AnimalGate** | TSE Systems | Metabolic (calorimetry) + feeding/drinking + body-weight gate | VO₂/VCO₂/RER, food/water intake, body weight, activity | Gallage et al. 2024 | P1 | `tse-phenomaster` |
| **LABORAS** | Metris | Load cells / vibration (Laboratory Animal Behaviour Observation Registration & Analysis System) | Locomotion, rearing, grooming, **scratching**, feeding/drinking | Sommer 2005 (integration w/ Dataquest); Huzard et al. 2024 | P1 | `metris-laboras` |
| **PhenoTyper (2)** | Noldus | Video (integrated arena) + EthoVision | Locomotion, social, behavior classification; environmental control | Grieco et al. 2021 | P1 | `noldus-phenotyper` |
| **Cage-lid retrofit modules** | Olden Labs | Video (retrofit on standard shoebox cages) | Behavior/activity; layers onto commercial racks | https://oldenlabs.com/ | P1 | `olden-labs` |
| **RFID temperature / multi-sensor implants** | UID (Unified Information Devices) / micetracking.com | RFID (LF, ISO 11784/85 FDX-B) + temp/accel/PPG | Individual ID, body temperature; newer chips add accelerometer, photoplethysmograph (HR, SpO₂, resp) | https://www.uidevices.com/laboratory-animal-temperature/ ; https://micetracking.com/ | P1 | `uid-rfid` |
| **Promethion** ("Sable Promotion" in text) | Sable Systems | Metabolic (calorimetry) | VO₂/VCO₂/RER, activity, feeding | (named only) | P2 | `sable-promethion` |
| **SoHo™ telemetry** | (see Pedraza et al. 2025) | Telemetry, socially housed | Body temperature, activity in group housing | Pedraza et al. 2025 | P2 | `soho-telemetry` |
| **iMouse** | — | Retrofit camera system | Video monitoring on standard racks | https://imouse.info/ | P2 | `imouse` |
| **Pallidus** | Pallidus.io | Environmental (cage-top units → cloud) | Activity, humidity, temperature | Pallidus.io | P2 | `pallidus` |
| **2D-Neuro** | 2D-Neuro | Wireless optogenetic implants (neuro toolchain) | Pattern-locked optogenetic stimulation in home cage | https://2dneuro.com/ | P3 | `2d-neuro` |
| **IntelliCage** | (TSE / New Behavior) | Operant / cognitive, group-housed | Learning, reversal, rule-switch, activity via RFID corners | (named only) | P2 | `intellicage` |
| **UltraVox XT** | Noldus | Acoustic (USV) | Ultrasonic vocalization detection/analysis | (named only) | P3 | `noldus-ultravox` |
| **Avisoft** | Avisoft Bioacoustics | Acoustic (USV) | USV recording + analysis | (named only) | P3 | `avisoft` |
| **Sonotrack** | Metris | Acoustic (USV) | USV multi-channel recording | (named only) | P3 | `sonotrack` |
| **Dodotronic** | Dodotronic | Acoustic (USV mics) | Ultrasonic microphones | (named only) | P3 | `dodotronic` |
| **BatSound / Pettersson M500-USB** | Pettersson | Acoustic (USV, low-cost) | USV via "bat microphone" + Audacity | https://batsound.com/product-category/usbmicrophones/ | P3 | `batsound-pettersson` |
| **Metadatapp (MAPP)** | Metadatapp / Neuronautix | Metadata management (not a sensor) | Unified metadata across project/mouse/data-publication | https://www.metadatapp.net | P2 | `metadatapp` |

## Open-source / DIY systems

| System | Authors | Modality | Key measured parameters | Data / links | Prio | slug |
|---|---|---|---|---|---|---|
| **Live Mouse Tracker (LMT)** | de Chaumont et al. | Video (IR depth) + RFID | Group social behavior, individual ID, trajectories | https://micecraft.org/lmt/ ; de Chaumont et al. 2019; Huzard et al. 2022 | P1 | `live-mouse-tracker` |
| **MIROSLAV + EnviroSLAV** | Virag et al. | PIR activity + environment | Activity per cage; illumination/temp/humidity | Virag et al. 2024 (bioRxiv), 2025 (Behav Res Methods) | P1 | `miroslav` |
| **FED3** | Matikainen-Ankney et al. | Operant (nose-poke) + food intake | Pellet retrieval, operant events; SD-card logging | eLife 2021, 10.7554/eLife.66173 | P1 | `fed3` |
| **MouseVUER** | Salem et al. | Video (open-source home-cage) | Home-cage video monitoring | Sci Rep 2024, 14:2662 | P2 | `mousevuer` |
| **MoPSS** (Mouse Position Surveillance System) | Habedank et al. | RFID tunnel reader (Arduino) | Cage-to-cage position / preference test | Behav Res Methods 2022 | P2 | `mopss` |
| **MyVivarium** | Vidva et al. | IoT / Raspberry Pi | Colony management + real-time ambient sensing (cloud) | Comput Struct Biotechnol J 2025 | P2 | `myvivarium` |
| **LIQ HD** (Lick Instance Quantifier Home-cage Device) | Petersen et al. | Lickometer (two-bottle) | Undisturbed two-bottle drinking, live lick counts | eNeuro 2023 | P2 | `liq-hd` |
| **PASTA** (Platform for Acoustic STArtle) | Virag et al. | Load cell (repurposed kitchen scale) | Startle response, periodic breathing (DIY) | Sci Rep 2021, 11:2963 | P3 | `pasta` |
| **AMBER** (Automated Maternal Behavior during Early life in Rodents) | Lapp et al. | Video pipeline | Maternal behavior classification | Sci Rep 2023 | P3 | `amber` |
| **PsiBox** | — | Operant (sensory discrimination) | Tone/frequency discrimination, sequence learning | (named only) | P3 | `psibox` |

## AI / computer-vision toolchains (software layers, not cage hardware)

Useful for understanding **derived** observations/results and for generating mock
keypoint/behavior data. Group under a single `ai-toolchains/` folder if preferred.

| Tool | Task | Reference |
|---|---|---|
| **DeepLabCut** / DeepLabCut 3D | Markerless pose estimation (2D/3D) | Mathis et al. 2018; Nath et al. 2019; Lauer et al. 2022 (multi-animal) |
| **DeeperCut** | Multi-person pose (basis for DLC) | Insafutdinov et al. 2016 |
| **SLEAP** | Multi-animal pose tracking | Pereira et al. 2022 |
| **YOLO** | Real-time object/animal detection | Redmon et al. 2015 |
| **Segment Anything (SAM)** | Zero-shot segmentation | Kirillov et al. 2023 |
| **OpenCV** | Undistortion / stereo triangulation | Bradski 2000 |
| **Anipose** | Multi-camera 3D calibration + triangulation | Karashchuk et al. 2021 |
| **DANNCE / s-DANNCE** | 3D volumetric pose, social behavior | Dunn et al. 2021; Klibaite et al. 2025 |
| **B-SOiD** | Unsupervised behavior segmentation | Hsu & Yttri 2021 |
| **VAME** | Latent movement motifs (VAE) | Luxem et al. 2022 |
| **BehaviorFlow** | Behavioral state-transition analysis | von Ziegler et al. 2024 |
| **Keypoint-MoSeq** | Motion sequencing / behavioral modules | Weinreb et al. 2024 |
| **DeepSqueak** | USV detection/analysis | Coffey et al. 2019 |
| **LMT USV Toolbox** | USV in behavioral context | de Chaumont et al. 2021 |
| **EzTrack** | Single-animal video tracking | Pennington et al. 2021 |

## Sensor components & standards (context for environmental/RFID mocks)

| Item | Type | Note |
|---|---|---|
| Sensirion **SHT45** | Temp/humidity sensor | Cage-level environmental monitoring |
| ams OSRAM **TSL25721** | Light sensor | Illumination monitoring |
| **Telaire T6713** | CO₂ (NDIR) | Calibration-free long life |
| **Aqara / AirGradient / Apollo AIR-1 / Sonoff** | Home-automation air-quality | Repurposable COTS sensors |
| **Kinect** | IR/depth camera | Used in LMT-style depth sensing |
| **FLIR** | Thermal camera | Body-temperature / physiology from video |
| **ISO 11784 / 11785 (FDX-B, 134.2 kHz)** | RFID standard | LF animal-ID standard used across RFID systems |
| **TEATIME** (COST Action CA20135) | Consortium / HCM definition + database | https://www.cost-teatime.org/about/hcm-definition/ ; thebehaviourdatabase.org |
| **OSF FAIR repository** ("Too big to lose") | Data repository / metadata effort | Bains et al. 2025, 10.31219/osf.io/fsg83_v1 |

See [`REFERENCES.md`](REFERENCES.md) for full citations and DOIs.
