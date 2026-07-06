<!-- Copy this folder to `../<system-slug>/` and fill in. Slug = lowercase-hyphenated. -->
# {{System name}}

- **Vendor / authors:** {{vendor or lab}}
- **Type:** commercial | open-source | DIY
- **Modality:** video | RFID | EMF | load cell | telemetry | metabolic | environmental | acoustic (USV) | operant | other
- **Status:** {{active / discontinued / prototype}}
- **Chapter reference:** Huzard et al. 2026, Sect. {{2.x}}

## Overview
{{One paragraph — what it is and what it monitors.}}

## Monitored entities
- **Species:** {{mouse / rat / …}}
- **Housing:** single | group ({{n}} per cage)
- **Enclosure:** {{retrofit standard cage / bespoke arena / rack-level}}

## Sensors & actuators
| Component | Transduces | Sampling rate | Range / resolution |
|---|---|---|---|
| | | | |

## Measured & derived parameters
| Parameter | Unit | Raw/derived | Rate | Notes |
|---|---|---|---|---|
| | | | | |

## Data output  ⟵ key for mocking
- **Format(s):** {{CSV / HDF5 / JSON / proprietary / API}}
- **Example schema:** {{field names + types + units, or a sample header row}}
- **Volume:** {{~X MB per cage/subject per day}}
- **Timestamps:** {{format + timezone}}
- **Data dictionary:** {{link or "unknown — not found"}}

## Software & interoperability
{{acquisition/analysis software, export options, open API / TTL / standard schemas.}}

## HCMO mapping notes
{{Which HCMO classes/properties this populates; gaps found. Link ABox in ../../../examples/ once authored.}}

## Files in this folder
- `docs/` — {{manuals / brochures / spec sheets}}
- `papers/` — {{PDFs, or links.md}}
- `datasets/real/` — {{real exports, de-identified}}
- `datasets/mock/` — {{synthetic data matching the real schema}}

## Sources
- {{URL}}
