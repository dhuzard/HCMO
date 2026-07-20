# Artifact audit — committed repo vs. Gilbert 2026 report

> **Historical audit, resolved in HCMO 0.2.0.** The discrepancy below describes
> the repository on 2026-06-29. The reviewed five-module model has since been
> promoted to `ontology/modules/`; placeholders were removed, definitions added,
> and the original export archived under `ontology/legacy/`.

**Date:** 2026-06-29 · **Trigger:** HITL Round 1, Q4 ("artifact state: needs audit").

## Original finding (resolved): the repo and the report described different artifacts

| | Committed repo (`dist/` v0.0.1) | Gilbert 2026 report (V1) |
|---|---|---|
| Classes | **32** | ~45 |
| Object properties | **38** | (part of ~46) |
| Datatype properties | **73** | (part of ~46) |
| Terms with `rdfs:comment` | **0** | clean labels in diagrams |
| Placeholder/erroneous terms | **43** (`UNKNOWN:*`×39, `ns:Class2`, `ns:objectProperty`, `xsd:boolean/integer` as properties) | none visible |
| Modules | `core / bio / env / obs` | `bio / housing / env / tech` |
| Reused classes / props | not separated | 6 / 17 |
| Prefixes | — | 12 |

**Conclusion:** the committed `dist/hcmo.ttl` is an **older, raw Chowlk export**.
The report's diagrams (figs 7–10) show a **newer, cleaner V1** (different
modularisation, sensible counts, no placeholders) that is **not in the repo**.

## Original implications for the paper
1. **The clean V1 must be obtained and committed** before any quality claims.
   The committed artifact cannot pass a Resources-Track availability/quality bar.
2. The paper's canonical structure is **bio/housing/env/tech** (Round 1) → the
   repo must be **re-modularised** away from core/bio/env/obs, OR the clean V1's
   own modularisation imported wholesale.
3. The 73 datatype vs 38 object properties split in the repo is a Chowlk artefact
   (many should be object properties / restructured) — the clean V1 likely already
   fixes this.

## Resolution
- **T0 is closed.** The active release uses five domain modules
  (`core/bio/env/obs/tech`) plus `hcm-compat.ttl`; `hcmo.yaml`, `dist/`, SHACL,
  examples, queries, and documentation now target HCMO 0.2.0.
- The table above must be cited only as provenance for the cleanup decision, not
  as the current state or term inventory of HCMO.
