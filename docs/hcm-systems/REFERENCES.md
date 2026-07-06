# References to dig into

Extracted from the reference list of **Huzard et al. (2026), "Technologies for Home
Cage Monitoring in Preclinical Research"** (Springer,
https://doi.org/10.1007/978-3-032-19781-8_7). Grouped by relevance to feeding HCMO
with data. ⭐ = high priority for finding **actual datasets or data schemas** to mock.

## System / dataset papers (best sources of real data schemas)

### Video & pose
- ⭐ **de Chaumont F, et al. (2019).** Real-time analysis of the behaviour of groups of mice via a depth-sensing camera and machine learning. *Nat Biomed Eng* 3(11):930–942. — *Live Mouse Tracker (LMT).*
- ⭐ **Salem G, et al. (2024).** MouseVUER: video based open-source system for laboratory mouse home-cage monitoring. *Sci Rep* 14:2662.
- **Guzman M, et al. (2024).** Highly accurate and precise determination of mouse mass using computer vision. *Patterns* 5(9):101039.
- **Lapp HE, et al. (2023).** Automated maternal behavior (AMBER) pipeline. *Sci Rep* 13:18277.
- **Pennington ZT, et al. (2021).** EzTrack — a step-by-step guide to behavior tracking. *Curr Protoc* 1(10):e255.
- **Grieco F, et al. (2021).** Measuring behavior in the home cage: study design, applications, challenges, and perspectives. *Front Behav Neurosci* 15:735387. — *Noldus PhenoTyper context.*

### RFID
- ⭐ **Habedank A, et al. (2022).** O mouse, where art thou? The Mouse Position Surveillance System (MoPSS) — an RFID-based tracking system. *Behav Res Methods* 54(2):676–689.
- ⭐ **Mieske P, et al. (2021).** Roaming in a land of milk and honey: life trajectories and metabolic rate of female inbred mice in a semi-naturalistic environment. *Animals* 11(10):3002. — *29 antennas / 20 mice / 186k points / 10.1 MB.*
- **Winn CB, et al. (2021).** Automated monitoring of respiratory rate as a novel humane endpoint. *PLoS One* 16(9):e0257694. — *Pfizer RFID + HCM.*
- **Sass F, et al. (2024).** NK2R control of energy expenditure and feeding to treat metabolic diseases. *Nature* 635:987–1000. — *RFID thermogenesis in group-housed mice.*
- **Huzard D, et al. (2022).** Impact of C-tactile low-threshold mechanoreceptors on affective touch and social interactions in mice. *Sci Adv* 8(26):eabo7566. — *LMT use.*

### EMF (Tecniplast DVC)
- ⭐ **Iannello F (2019).** Non-intrusive high throughput automated data collection from the home cage. *Heliyon* 5(4):e01454. — *DVC technical basis.*
- **Voikar V, Gaburro S (2020).** Three pillars of automated home-cage phenotyping of mice. *Front Behav Neurosci* 14:575434.
- **Brachs S, et al. (2025).** Robust non-invasive detection of hyperglycemia... the novel urination index biomarker. *bioRxiv* 10.1101/2025.04.02.646666.

### Load cells
- ⭐ **Virag D, et al. (2021).** Repurposing a digital kitchen scale for neuroscience research: a complete hardware and software cookbook for **PASTA**. *Sci Rep* 11:2963.
- **Huzard D, et al. (2024).** Primary sensory neuron dysfunction underlying mechanical itch... Shank3 mouse. *bioRxiv* 10.1101/2024.12.29.630575. — *LABORAS scratching.*
- **Sommer R (2005).** Simultaneous collection of behavioural and physiological data in mice: integration of LABORAS with Dataquest. *Measuring Behavior.*

### Telemetry
- ⭐ **Kramer K, Hachtman S, Girand M, Stiedl O (2021).** Applications of implantable radio telemetry in small laboratory animals. In *Handbook of Laboratory Animal Science*, 4th edn, ch. 15. CRC Press. — *DSI-style signals, sample rates, file sizes.*
- **Pedraza P, et al. (2025).** Validation of the SoHo™ telemetry system for continuous body temperature monitoring in socially housed mice. *Am Physiol Summit* A40(S1):2078.
- **Ouyang W, et al. (2024).** An implantable device for wireless monitoring of diverse physio-behavioral characteristics in freely behaving small animals and groups. *Neuron* 112(11):1764–1777.e5.
- **Mills PA (2000).** A new method for measurement of blood pressure, heart rate, and activity in the mouse by radiotelemetry. *J Appl Physiol* 88:1537–1544.
- **Martin S (2024).** Long-term, high-resolution telemetry monitoring of circadian rhythmicity... socially housed mice. *Australas Neurosci Soc Annu Sci Meet* 21878.

### Metabolic
- **Škop V, et al. (2020).** Mouse thermoregulation: the thermoneutral point. *Cell Rep* 31(2):107501.
- **Škop V, et al. (2023).** The metabolic cost of physical activity in mice... *Mol Metab* 71:101699.
- **Rubio WB, et al. (2023).** Indirect calorimetry to assess energy balance in mice: measurement and data analysis. *Methods Mol Biol* 2662:103–115.
- **Speakman JR (2013).** Measuring energy metabolism in the mouse. *Front Physiol* 4:34.
- **Eynaud A, et al. (2024).** Adapting indirect calorimetry to measure metabolic status of healthy and septic neonatal mice. *bioRxiv* 10.1101/2024.05.23.595520.
- **Gallage S, et al. (2024).** A 5:2 intermittent fasting regimen ameliorates NASH... *Cell Metab* 36(6):1371–1393.e7. — *TSE PhenoMaster use.*
- **Hu D, et al. (2023).** TMEM135 links peroxisomes to Brown fat... *Nat Commun* 14:6099.

### Environmental
- ⭐ **Virag D, et al. (2024).** My friend MIROSLAV: a hackable open-source hardware/software platform for high-throughput rodent activity monitoring in the home cage. *bioRxiv* 10.1101/2024.06.25.600592.
- ⭐ **Virag D, et al. (2025).** My friend MIROSLAV (peer-reviewed). *Behav Res Methods* 57(7):1–19.
- ⭐ **Vidva R, et al. (2025).** MyVivarium: a cloud-based lab-animal colony management application with real-time ambient sensing. *Comput Struct Biotechnol J* 27:612–623.

### Acoustic (USV)
- **Coffey KR, et al. (2019).** DeepSqueak. *Neuropsychopharmacology* 44(5):859–868.
- **de Chaumont F, et al. (2021).** LMT USV toolbox. *Front Behav Neurosci* 15:735920.
- **Waidmann EN, et al. (2024).** Mountable miniature microphones to identify and assign mouse USVs. *bioRxiv* 10.1101/2024.02.05.579003.

### Operant
- ⭐ **Matikainen-Ankney BA, et al. (2021).** An open-source device for measuring food intake and operant behavior in rodent home-cages (**FED3**). *eLife* 10:e66173. 10.7554/eLife.66173.
- ⭐ **Petersen N, et al. (2023).** LIQ HD: an open-source tool for recording undisturbed two-bottle drinking. *eNeuro* 10(4):ENEURO.0506-22.2023.
- **Bruinsma B, et al. (2019).** An automated home-cage-based 5-choice serial reaction time task. *Psychopharmacology* 236(7):2015–2026.
- **Augier E, et al. (2017).** A method for evaluating the reinforcing properties of ethanol in rats without water deprivation. *J Vis Exp* 119:e53305.

### Beam-break / activity
- **Czekajewski JA, Hill HL, Kober KJ (1982).** Animal activity monitor and behavior processor. US Patent 4,337,726. — *Columbus Instruments basis.*
- **Goulding EH, et al. (2008).** A robust automated system elucidates mouse home cage behavioral structure. *PNAS* 105(52):20575–20582.
- **Keenan BT, et al. (2020).** High-throughput sleep phenotyping in diversity outbred mice. *Sleep* 43(5):zsz278.
- **Pack AI, et al. (2007).** Novel method for high-throughput phenotyping of sleep in mice. *Physiol Genomics* 28(2):232–238.

## Metadata / interoperability / standards (directly relevant to HCMO)
- ⭐ **Bains RS, Huzard D, McCutcheon JE, Boguszewski P, Virag D, Restivo L, Lewejohann L, et al. (2025).** Too big to lose — a FAIR repository for biomedical data derived from home-cage monitoring. *OSF*. 10.31219/osf.io/fsg83_v1. — *HCM definition Olog + FAIR data model; core input for HCMO alignment.*
- **TEATIME** (COST Action CA20135): HCM definition — https://www.cost-teatime.org/about/hcm-definition/ ; behaviour database — thebehaviourdatabase.org
- **Metadatapp (MAPP)** — https://www.metadatapp.net

## AI / method references (for derived observations & mock keypoint data)
- Mathis A, et al. (2018) DeepLabCut. *Nat Neurosci* 21(9):1281–1289.
- Nath T, et al. (2019) DeepLabCut 3D. *Nat Protoc* 14(7):2152–2176.
- Lauer J, et al. (2022) Multi-animal DeepLabCut. *Nat Methods* 19(4):496–504.
- Insafutdinov E, et al. (2016) DeeperCut. *arXiv* 1605.03170.
- Pereira TD, et al. (2022) SLEAP. *Nat Methods* 19(4):486–495.
- Redmon J, et al. (2015) YOLO. *arXiv* 1506.02640.
- Kirillov A, et al. (2023) Segment Anything. *arXiv* 2304.02643.
- Bradski G (2000) The OpenCV library. *Dr Dobb's J* 25(11):120–123.
- Karashchuk P, et al. (2021) Anipose. *Cell Rep* 36(13):109730.
- Dunn TW, et al. (2021) DANNCE — 3D kinematic profiling. *Nat Methods* 18(5):564–573.
- Klibaite U, et al. (2025) s-DANNCE — Mapping the landscape of social behavior. *Cell* 188(8):2249–2266.
- Hsu AI, Yttri EA (2021) B-SOiD. *Nat Commun* 12:5188.
- Luxem K, et al. (2022) VAME. *Commun Biol* 5:1267.
- von Ziegler LM, et al. (2024) Behavioral flow / BehaviorFlow. *Nat Methods* 21(12):2376–2387.
- Weinreb C, et al. (2024) Keypoint-MoSeq. *Nat Methods* 21(7):1329–1339.
- Vaswani A, et al. (2017) Attention is all you need. *arXiv* 1706.03762.

> Full author lists and the remaining physiology/telemetry-surgery references are in
> the source PDF's reference section (pp. 205–210).
