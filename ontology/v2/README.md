# HCMO v2 — re-modularised draft (for co-author review)

**Status: DRAFT for review. Not yet canonical.** The live ontology is still
`ontology/modules/` (wired into `hcmo.yaml`, `build.py`, CI, and `dist/`). This
folder is a **parallel proposal** implementing the re-modularisation decided in
[`docs/paper/MODULE-MAP.md`](../../docs/paper/MODULE-MAP.md) (HITL Round 5,
2026-07-03). Nothing here is imported by the build; the current version is
untouched so both can be compared. **Promote only after co-author validation**,
then delete `ontology/modules/` and repoint the tooling (see *Promotion* below).

## BioPortal review files

Use the clean generated files for BioPortal submission/review. They merge the v2
source modules and exclude `hcm-placeholders.ttl`, which is now an empty
quarantine file retained only for audit/history:

- Turtle: `https://raw.githubusercontent.com/dhuzard/HCMO/main/ontology/v2/hcmo-v2-merged-clean.ttl`
- RDF/XML: `https://raw.githubusercontent.com/dhuzard/HCMO/main/ontology/v2/hcmo-v2-merged-clean.owl`

Regenerate them with:

```bash
python tooling/build_v2_clean.py
```

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
    hcm-placeholders.ttl  # empty quarantine file; no active UNKNOWN terms
  hcmo-v2-merged.ttl      # merged graph (698 triples) for quick review
  hcmo-v2-merged-clean.ttl # BioPortal Turtle graph (698 triples)
  hcmo-v2-merged-clean.owl # BioPortal RDF/XML graph (698 triples)
  README.md               # this file
```

The generated merged/clean graphs currently contain 698 triples after adding
FAIR ontology-header metadata and `rdfs:comment` definitions. Term counts (HCMO
+ reused scaffolding): core 7 cls / bio 4 / obs 10 / env 6 / tech 5. No active
`UNKNOWN:` placeholders remain in v2. All files parse clean.

## Still pending (not addressed by re-modularisation)

- **Units**: `hcm:hasUnit` is a temporary stub — replace with **QUDT/OM** once the
  vocabulary is chosen (Q21). `hasValue`/`hasNumericValue` are follow-on candidates.
- **Placeholder cleanup validation**: the former 7 remaining placeholders have
  been replaced, mapped to existing terms, or dropped in the v2 draft. Co-author
  validation is still requested before promotion.
- **Branding**: the v2 ontology header now uses HCMO; reconcile the remaining repository-level branding separately (T7b).
- **Device-manufacturer** property (M5 split) not yet minted; enclosure keeps
  `hcm:hasManufacturer`.

## Promotion (after co-author sign-off)

1. Replace `ontology/modules/` with `ontology/v2/modules/`.
2. Add the `tech` module to `hcmo.yaml`; update the README module-sub-namespace list.
3. `python tooling/build.py` → regenerate `dist/`; `python tooling/validate.py`.
4. Re-author `shapes/`, `examples/`, `queries/` against the new terms (T6).
5. Cut the release + refreshed DOI (T9) — do the breaking `…/hcm/tech#` IRI moves before tagging.
