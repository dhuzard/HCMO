# Authors & front matter (HITL Round 4)

**Decision (confirmed 2026-08-31):** Cyril Gilbert is **first author**. The
middle-author order is Gaoussou Sanou, Serge Sonfack Sounchio, Antoine Toffano,
Pierre Larmande, and Philippe Rocca-Serra. Konstantin Todorov and Damien Huzard
are **co-last**; Damien remains the final listed author. Cyril Gilbert,
Konstantin Todorov, and Damien Huzard are the three corresponding authors.

| # | Author | Role | ORCID | Affiliation |
|---|--------|------|-------|-------------|
| 1 | **Cyril Gilbert** | **First / corresponding ✉** | 0009-0008-2489-8106 | LIRMM, Université de Montpellier, CNRS, Montpellier, France |
| 2 | Gaoussou Sanou | contributing author | 0000-0003-2204-2466 | IMGT®, IGH, Université de Montpellier, CNRS, Montpellier, France |
| 3 | Serge Sonfack Sounchio | contributing author | 0000-0002-6085-6818 | Production Engineering Laboratory/UFTMiP, France |
| 4 | Antoine Toffano | contributing author | 0009-0008-0575-8490 | LIRMM, Université de Montpellier, CNRS, Montpellier, France |
| 5 | Pierre Larmande | contributing author | 0000-0002-2923-9790 | DIADE, Université de Montpellier, IRD, CIRAD, Montpellier, France |
| 6 | Philippe Rocca-Serra | contributing author | 0000-0001-9853-5668 | Oxford e-Research Centre, Department of Engineering Science, University of Oxford, Oxford OX1 3QG, United Kingdom |
| 7 | **Konstantin Todorov** | **Co-last / corresponding ✉** | 0000-0002-9116-6692 | LIRMM, Université de Montpellier, CNRS, Montpellier, France |
| 8 | **Damien Huzard** | **Co-last / corresponding ✉; final listed author** | 0000-0003-4820-7951 | Neuronautix, Montpellier, France |

> ✉ = corresponding author. Single-anonymous track → authors are **named** in
> the submission. Equal-contribution/co-last wording still needs to be adapted
> to the selected venue's supported author-note format.
>
> **Name corrections (per ORCID records, 2026-06-29):** "Sonfack" → **Sonfack
> Sounchio**; "Tofano" → **Toffano**. Applied to `CITATION.cff` + README. The
> ontology header and citation metadata use the corrected names and ORCID IRIs.
>
> Detailed acknowledgements and non-author contributions are recorded below and
> in `docs/PROVENANCE.md`.

## CRediT author statement

- **Cyril Gilbert:** Conceptualization, Investigation, Methodology, Software,
  Validation, Visualization, Writing — original draft, Writing — review &
  editing.
- **Pierre Larmande:** Validation, Writing — review & editing.
- **Philippe Rocca-Serra:** Conceptualization, Methodology, Validation, Writing
  — review & editing.
- **Gaoussou Sanou:** Conceptualization, Methodology, Visualization, Writing —
  review & editing.
- **Serge Sonfack Sounchio:** Methodology, Validation, Writing — review &
  editing.
- **Antoine Toffano:** Validation, Writing — review & editing.
- **Konstantin Todorov:** Conceptualization, Methodology, Supervision,
  Validation, Writing — review & editing.
- **Damien Huzard:** Conceptualization, Funding acquisition, Methodology,
  Project administration, Software, Supervision, Validation, Writing — original
  draft, Writing — review & editing.

## Acknowledgements and non-author contributions

The authors acknowledge the TEATIME Olog and the COST Action TEATIME community
as sources of domain terminology, expertise, and feedback.

- **Initial HCM profile of the TEATIME Olog:** Leonardo Restivo and Davor Virag.
- **Preparation and preliminary scoping of the COST mobility-grant project and
  early categorisation of metadata elements used in auxiliary authoring tools:**
  Benoit Girard and Leonardo Restivo.
- **Early conceptual and software architecture developed for HCMO within
  Metadatapp:** Laurent Huzard.
- **Domain expertise and feedback:** Benoit Petit-Demoulière, Vootele Voikar,
  Leonardo Restivo, Davor Virag, and Marion Rivalan.

Damien Huzard also thanks the INITIUM incubator team, particularly Rémi
Przybylski and Kate Rivière, as well as Frédéric Deverre, Loïc Clementz, and
Geoffrey Galibert for their contributions to the technical and business
development of Metadatapp.

## To provide before submission (T-author)
- [x] ORCIDs for Gilbert, Sanou, Sonfack Sounchio, Toffano. *(provided 2026-06-29)*
- [x] Author order and three corresponding authors. *(updated 2026-09-04)*
- [x] Exact submission affiliations for all 8 authors confirmed and recorded in
      `CITATION.cff` and the repository README. *(confirmed 2026-09-04)*
- [x] Corresponding emails confirmed 2026-08-31: Cyril Gilbert
      (`cyril.gilbert8@gmail.com`), Konstantin Todorov
      (`konstantin.todorov@lirmm.fr`), and Damien Huzard
      (`damien.huzard@gmail.com`).
- [ ] Add Philippe Rocca-Serra between Larmande and Todorov in the published
      Zenodo creator metadata. Preserve the existing Git tag and archived
      ontology graph; this is a metadata-only correction.
- [x] Development provenance, funding/acknowledgement, and Damien Huzard
      conflict-of-interest facts supplied; final prose is in the Overleaf
      manuscript.

## Development provenance, funding, and conflict-of-interest facts

- HCMO developed through four stages:
  1. The community-developed [COST TEATIME Olog](https://www.cost-teatime.org/about/hcm-definition/)
     established structured domain terminology and is the closest conceptual
     precursor to HCMO.
  2. During the first half of 2025, Damien Huzard began translating the broader
     domain need into a machine-actionable ontology through Metadatapp's
     semantic-development work and related grant preparation.
  3. A COST mobility grant (€750) awarded to Damien Huzard for *Mapping the
     Home-Cage Monitoring Ontology to Device Metadata* supported limited
     preliminary device-metadata mapping, project scoping, and publication of
     an early GitHub version in September 2025, with contributions from Leonardo
     Restivo and Benoit Girard.
  4. An Exogene grant (€23,000), administered by the Pôle Universitaire
     d'Innovation of the University of Montpellier and awarded to Metadatapp to
     support collaboration between Damien Huzard and Konstantin Todorov,
     supported the comprehensive redesign and formal evaluation from October
     2025 to October 2026. As part of the Exogene-funded Master's project, Cyril
     Gilbert redesigned and implemented the HCMO version presented in the
     article, with Pierre Larmande, Serge Sonfack Sounchio, Gaoussou Sanou, and
     Antoine Toffano contributing as recorded in the CRediT statement.
- Metadatapp, formerly Damien Huzard's entrepreneurial venture, is now an
  open-source software program.
- Damien Huzard provides consultancy services in preclinical research and
  research metadata through Neuronautix. The other authors declare no competing
  interests.
