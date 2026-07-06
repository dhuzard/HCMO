# 3. Requirements and competency questions

> **Status:** full draft (artifact-independent), from Gilbert (2026) §4. The CQ
> *answers/results* are artifact-dependent and deferred to §6 (parked on T0). ~1 pp.

**Stakeholders and use cases.** HCMO is intended for several roles: researchers
comparing or aggregating behavioural and physiological data across studies and
laboratories; facility managers and welfare committees auditing housing and
husbandry; data engineers ingesting heterogeneous device exports; and, in the
longer term, downstream AI consumers querying the resulting knowledge graph. These
roles share one need — to interpret a measurement together with the full context
of its production.

**Requirements from domain analysis.** Analysis of the HCM domain
\cite{kiryk2026,huzard2026tech,forrest2026} yields the following requirements,
which drive the model (forward references to §4):

- **R1 — Context-complete observations.** Every observation must record the
  concerned subject, the observed property, the time, the procedure, and, where
  available, the result, so that no measurement is stranded without context.
- **R2 — Separation of device, observation, and result.** A sensor (a technical
  device), an observation (the measurement event in context), and a result (the
  produced value/interpretation) must be modelled distinctly, preserving the
  chain *device → observation → measurement → interpretation*. HCM outputs are
  often signals later transformed by software into inferred behaviours.
- **R3 — Temporal housing assignment.** Membership of an animal in an enclosure is
  time-bounded, not permanent, and must be represented as an assignment over an
  interval, linked to experimental groups and study factors.
- **R4 — Environment as interpretable context.** Enclosure dimensions, enrichment,
  light cycles, and measurable conditions (temperature, humidity, gas, light) must
  be representable, distinguishing a *property* from the *values* observed for it.
- **R5 — Technical provenance.** Hardware, sensors, software, and their
  organisation of data into time series/segments must be captured without
  conflating technical provenance with biological interpretation.
- **R6 — Rich, machine-readable metadata.** Species, strain, sex, age, housing,
  enrichment, device configuration, sampling rate, software, and protocol must be
  first-class, supporting FAIR reuse \cite{fair,forrest2026}.
- **R7 — Standards reuse and interoperability.** Where a suitable standard exists
  (SOSA/SSN, OWL-Time, UO, PROV, BFO), it must be reused rather than re-minted.
- **R8 — Data-quality checking.** The model must support consistency and
  completeness checks (e.g. a numeric value without a unit, an animal not assigned
  to an enclosure over an interval).

**Competency questions.** Requirements are operationalised as competency questions
that the ontology must be able to answer \cite{noy2001,lot2022}. Representative
examples (from the domain analysis):

- **CQ1.** Which enclosure is `Subject_001` assigned to at time *T*? *(R1, R3)*
- **CQ2.** Which subjects are currently housed in `Room_101`? *(R3)*
- **CQ3.** What is the latest recorded weight of `Subject_001`? *(R1)*
- **CQ4.** Which subjects were exposed to a temperature above 25 °C? *(R4)*
- **CQ5.** Which sensors monitor `Enclosure_A2`? *(R5)*
- **CQ6.** Are there observations with numeric values but no units? *(R8)*

Each CQ maps onto a requirement and onto the module that satisfies it (CQ1–CQ3 →
*bio*/*housing*; CQ4 → *env*; CQ5 → *tech*; CQ6 → cross-cutting data quality via
SHACL). §6 reports, for the released artifact, the SPARQL realisation of these
questions and their results over example data. *(Deferred: runnable CQ results and
coverage figures depend on the clean V1 artifact — TODO T6, parked on T0.)*
