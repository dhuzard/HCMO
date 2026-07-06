# HCMO v2 — re-modularised draft (for co-author review)

**Status: DRAFT for review. Not yet canonical.** The live ontology is still
`ontology/modules/` (wired into `hcmo.yaml`, `build.py`, CI, and `dist/`). This
folder is a **parallel proposal** implementing the re-modularisation decided in
[`docs/paper/MODULE-MAP.md`](../../docs/paper/MODULE-MAP.md) (HITL Round 5,
2026-07-03). Nothing here is imported by the build; the current version is
untouched so both can be compared. **Promote only after co-author validation**,
then delete `ontology/modules/` and repoint the tooling (see *Promotion* below).

## What changed vs the current 4-module version

**5 modules** (was core/bio/env/obs): `hcm` **core = enclosure only** · `bio` ·
`obs` (observations **+** results) · `env` · **`tech`** (new).

| Decision | Effect |
|----------|--------|
| Results → obs (Q20) | `ObservationResult`, `QuantityValue`, `CategoricalResult`, `BehaviorResult`, `LocationResultTable` now live in `obs`. Core no longer holds results. |
| `tech` own module (Q19) | `Sensor`, `Hardware`, `Software`, `TimeSeries` + device props → `…/hcm/tech#` (**new IRIs**). |
| HousingAssignment → bio | + `assignedToEnclosure`. |
| StudyFactors → bio | dropped the bogus `⊑ MonitoredEnclosure` axiom. |
| EnclosureDimensions → core | + its dimension props `hasHeight/Length/Width/DimUnit`. |
| `Structural&LocationTable` → **`LocationResultTable`** (obs) | fixed the illegal `&` IRI and legacy label. |
| Dropped cruft | `OWL-Timeintervaltable`, `ns:objectProperty`, `xsd:boolean/integer`-as-property, empty `hcm-obs:#` property, duplicate `UNKNOWN:hasName`. |
| Unit dedup (M4) | the two `hasUnit` merged into one `hcm:hasUnit` **stub** — pending replacement by QUDT/OM (Q21, still open). |

## Layout

```
ontology/v2/
  modules/
    hcm-core.ttl          # MonitoredEnclosure hub + reused-vocab scaffolding + ontology header (7 ORCIDs)
    hcm-bio.ttl           # Subject, ExperimentalGroup, HousingAssignment, StudyFactors
    hcm-obs.ttl           # observations + ALL results
    hcm-env.ttl           # profiles, specs, environmental properties
    hcm-tech.ttl          # Sensor/Hardware/Software/TimeSeries (NEW namespace …/hcm/tech#)
    hcm-placeholders.ttl  # 15 UNKNOWN:/ns: terms still awaiting definition-or-drop (T4/T5)
  hcmo-v2-merged.ttl      # merged graph (595 triples) for quick review
  README.md               # this file
```

Term counts (HCMO + reused scaffolding): core 6 cls / bio 4 / obs 10 / env 6 /
tech 4; 15 placeholders isolated. All files parse clean.

## Still pending (not addressed by re-modularisation)

- **Units**: `hcm:hasUnit` is a temporary stub — replace with **QUDT/OM** once the
  vocabulary is chosen (Q21). `hasValue`/`hasNumericValue` are follow-on candidates.
- **15 placeholders** in `hcm-placeholders.ttl` — define or drop (T4), then add
  `rdfs:comment` definitions to every term (T5).
- **Branding**: the v2 ontology header now uses HCMO; reconcile the remaining repository-level branding separately (T7b).
- **Device-manufacturer** property (M5 split) not yet minted; enclosure keeps
  `hcm:hasManufacturer`.

## Promotion (after co-author sign-off)

1. Replace `ontology/modules/` with `ontology/v2/modules/`.
2. Add the `tech` module to `hcmo.yaml`; update the README module-sub-namespace list.
3. `python tooling/build.py` → regenerate `dist/`; `python tooling/validate.py`.
4. Re-author `shapes/`, `examples/`, `queries/` against the new terms (T6).
5. Cut the release + refreshed DOI (T9) — do the breaking `…/hcm/tech#` IRI moves before tagging.
