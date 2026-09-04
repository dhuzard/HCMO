# 3. Requirements and competency questions

> **Status:** full draft aligned with the published HCMO 0.3.0 competency-question
> index. Exact answers are reported in §6. ~1 pp.

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

- **R1 — Context-aware observations.** An observation must remain linkable,
  where applicable, to its feature of interest, observed property, time,
  procedure, sensor, and result. The standard shapes enforce fields per profiled
  observation subtype rather than imposing one biologically inappropriate
  completeness rule on every SOSA observation.
- **R2 — Separation of device, observation, and result.** A sensor (a technical
  device), an observation (the measurement event in context), and a result (the
  produced value/interpretation) must be modelled distinctly, preserving the
  chain *device → observation → result/interpretation*. HCM outputs are
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
- **R7 — Standards reuse and interoperability.** Where a suitable standard
  exists, it must be reused rather than re-minted. Candidate standards include
  SOSA/SSN, OWL-Time, BFO/IAO, PROV-O, and reviewed quantity/unit
  vocabularies; each mapping strength must be justified separately.
- **R8 — Data-quality checking.** The model must support consistency and
  completeness checks (e.g. a numeric value without a unit, an animal not assigned
  to an enclosure over an interval).

**Competency questions.** Selected retrieval aspects of the requirements are
operationalised as executable SPARQL questions \cite{noy2001,lot2022}; structural
requiredness is tested separately with SHACL. The release index contains eleven questions.
They retrieve assignments by enclosure and at a reference time; missing enclosure
dimensions; environment specifications paired with observed QUDT quantities;
time-bounded operational and calibration evidence; husbandry provisioning gaps;
sensor-captured properties; observations lasting at least 24 hours under a stated
condition; and three ISA/STATO provenance paths. Complete expected bindings are
versioned with the queries, including the intentionally empty missing-dimensions
answer. Section 6 reports their exact results. Five additional queries exercise
the isolated 2 × 2 round-trip fixture for housing history, factor assignments,
repeated observations, statistical result/file-fragment separation, and the
Source-to-Sample derivation.
