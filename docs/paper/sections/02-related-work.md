# 2. Related work

> **Status:** full draft (artifact-independent). Positioning per `NOVELTY.md`:
> HCMO is the first HCM ontology; reuses standards; differentiates from adjacent
> biomedical/animal ontologies. ~1 pp.

**Home-Cage Monitoring and data sharing.** HCM is an active and rapidly growing
field, with recent surveys of systems, sensing technologies, and applications
\cite{kiryk2026,huzard2026tech,duarte2026diy}. The community has begun to address
data sharing and metadata explicitly \cite{forrest2026} and to frame data quality
as part of animal welfare through the WellFAIR perspective \cite{petit2026wellfair}.
These efforts establish *requirements* — rich, standardised metadata that travel
with the measurements — but stop short of a shared, machine-actionable semantic
model. To our knowledge, no ontology models the HCM acquisition chain (animal
subject ↔ housing ↔ environment ↔ device ↔ observation ↔ result) end-to-end.

**Standards reused, not duplicated.** HCMO builds on W3C and community
vocabularies. SOSA provides the sensor/observation backbone \cite{sosa}; OWL-Time
models temporal entities and intervals \cite{owltime}; BFO and IAO provide
upper-level anchors \cite{bfo}; and SEMTS contributes selected time-series terms.
UO, QUDT/OM, and PROV are relevant candidates for units and richer provenance,
but are not claimed as active semantic dependencies of version 0.2.0. HCMO
contributes the HCM-specific concepts and relations that bind the reused patterns.

**Adjacent biomedical and laboratory-animal ontologies.** Several resources cover
neighbouring concerns. The Ontology for Biomedical Investigations (OBI) models
investigations, protocols, instruments, materials, and data \cite{obi}; the
Ontology of Laboratory Animal Medicine (OLAM) provides laboratory-animal
terminology; and the Mouse Experimental Design Ontology (MEDO) standardises
experimental-design descriptions, overlapping HCMO's housing/experimental-group
notions. Reporting guidelines such as ARRIVE \cite{arrive} prescribe *what* to
report about in-vivo experiments but are not machine-readable ontologies. None of
these model continuous in-cage acquisition; HCMO is complementary to them and can
bridge to OBI and MEDO where appropriate.

**Ontology engineering.** Methodologically, HCMO follows an incremental,
competency-question-driven process in the spirit of LOT \cite{lot2022} and SAMOD
\cite{samod2017}, with requirements expressed as competency questions
\cite{noy2001}. The current version was conceptualised graphically in
diagrams.net and exported to OWL/Turtle with Chowlk \cite{chowlk2022}; LinkML was
explored as an alternative serialisation \cite{linkml2021}. Documentation is
produced with WIDOCO \cite{widoco2017}, and quality is assessed with OOPS!
\cite{oops2012} and, for FAIRness, FOOPS! \cite{foops}, complemented by reasoning
and SHACL validation \cite{gangemi2006}. Positioned this way, HCMO is the first
ontology dedicated to HCM, designed to interoperate with — rather than replace —
the surrounding standards and biomedical ontologies.
