# 4. Resource description

- HCMO overview; namespace policy (w3id base + module sub-namespaces). **Use
  "HCMO" only — no MAPP framing (HITL R3).**
- Modular structure: **bio / housing / env / tech** (HITL R1; per Gilbert 2026
  report — repo currently core/bio/env/obs, to be re-modularised, T3b).
- Key classes (from report diagrams): Subject; HousingAssignment, ExperimentalGroup,
  Enclosure; environmental profile/dimensions/light-cycle; Weight/Behavior/Health/
  Environment observations + results; Sensor, Hardware, Software, TimeSeries(Segment).
- Key modelling choice: **sensor ≠ observation ≠ result** kept distinct (report
  Fig. 11), preserving the device→observation→measurement→interpretation chain.
- Standards reuse (all real in V1 — HITL R3): **SOSA/SSN, OWL-Time, UO, PROV, BFO,
  schema.org, semts**. Give the alignment axioms (cite `docs/ALIGNMENTS.md`); be
  explicit which terms are reused as-is vs specialised vs HCMO-specific.
- JSON-LD context for application developers.
- Figure F2: ontology overview (WebVOWL).
