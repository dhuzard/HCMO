# HCMO Development Provenance

HCMO developed through four stages:

1. The community-developed [COST TEATIME Olog](https://www.cost-teatime.org/about/hcm-definition/)
   established structured terminology for the home-cage monitoring domain and
   is the closest conceptual precursor to HCMO. Its deposited source is archived
   as Zenodo version DOI
   [10.5281/zenodo.22646369](https://doi.org/10.5281/zenodo.22646369), with
   concept DOI [10.5281/zenodo.22646368](https://doi.org/10.5281/zenodo.22646368).
2. From early March 2025, Damien Huzard developed an earlier machine-actionable
   ontology, HCM-D, published on BioPortal
   (<https://bioportal.bioontology.org/ontologies/HCM-D>, no longer active),
   through Metadatapp's semantic-development work and related grant
   preparation. Leonardo Restivo confirmed this date (2026-09-24) and followed
   the development through the CEDAR user list.
3. A Virtual Mobility Grant (€750) of COST Action CA20135 (TEATIME), awarded
   to Damien Huzard for the project *Mapping the Home-Cage Monitoring Ontology
   to Device Metadata*, supported preliminary mapping and implementation work
   on HCMO, including project scoping and publication of an early GitHub
   version in September 2025. The project was initiated by Benoît Girard, who
   wrote the proposal, with contributions from Leonardo Restivo. Benoît Girard
   is a co-author of the HCMO article
   (decided 2026-09-24) and is credited there in the CRediT statement rather
   than in the acknowledgements. His Conceptualization role is qualified as
   *initial project framing* (agreed 2026-09-29): it covers the early-stage
   conceptual framework of this stage, not the later development and
   conceptualization of HCMO in stage 4.
4. An Exogene grant (€23,000), administered by the Pôle Universitaire
   d'Innovation of the University of Montpellier and awarded to Metadatapp to
   support collaboration between Damien Huzard and Konstantin Todorov, supported
   the comprehensive redesign and formal evaluation from October 2025 to
   October 2026. As part of the Exogene-funded Master's project (internship
   started January 2026), Cyril Gilbert
   redesigned and implemented the HCMO version presented in the article, with
   the other authors contributing as recorded in the CRediT statement.

## Non-author contributions

These entries follow the non-author contributions paragraph of the HCMO article.

- **HCM Definition:** COST Action TEATIME (CA20135), particularly Working
  Group 2, as its collective producer. Leonardo Restivo introduced the Olog
  approach and facilitated its community-based development.
- **Semantic-components model of Bains et al.:** Leonardo Restivo and Davor
  Virag.
- **Preliminary scoping of the COST mobility-grant project:** Leonardo Restivo.
- **Early conceptual and software architecture developed for HCMO within
  Metadatapp:** Laurent Huzard.
- **Participation in project discussions (January–March 2026):** Antoine
  Toffano.
- **Domain expertise and feedback:** Benoit Petit-Demoulière, Vootele Voikar,
  Leonardo Restivo, Davor Virag, and Marion Rivalan.

Damien Huzard also acknowledges the INITIUM incubator team, particularly Rémi
Przybylski, Noelline Meslin, and Kate Rivière, as well as Frédéric Deverre,
Loïc Clementz, and Geoffrey Galibert for their contributions to the technical and business
development of Metadatapp.

## Clarifications from contributors

- **Davor Virag** (email to Damien Huzard, recorded 2026-09-24): he expressed interest in the COST
  mobility-grant project on 7 September 2025 but was not included in its
  submission, through an unintentional omission by the submitter. He was
  invited to work on HCMO in April 2026 and again expressed interest; he
  followed up on 14 July 2026, and scheduling conflicts have so far prevented
  joint work. He did not decline to take part for lack of time. His credit in
  the article (the Bains et al. semantic-components model, and domain
  expertise and feedback) is unchanged.

## Auxiliary field-tier inventory

The source classification document for the repository's
Mandatory/Recommended/Optional field tiers is Benoît Girard's email to Damien
Huzard of 2 October 2025. It set out a fourteen-item
Mandatory/Recommended/Optional classification of metadata elements, with a
scientific rationale for each item, together with the argument for a
device-agnostic conceptual blueprint. The field-tier document and the
device-agnostic blueprint workbench introduced the next day (commit
`a421285`, 3 October 2025) drew on that email, including several of its
formulations. The inventory was then expanded and revised in the repository.

The current inventory is documentation and input to the optional authoring
workbench. Its tiers are not encoded as distinctions in the OWL ontology or the
canonical SHACL shapes, and they were not evaluated as part of the scientific
contribution reported in the HCMO article.

### Repository history

- Commit `3f2fc24` (30 September 2025) introduced Mandatory/Recommended/Optional
  markers in the authoring interface.
- Commit `a421285` (3 October 2025) introduced the field-tier document used by
  the device-agnostic blueprint workbench, following the 2 October 2025 email.
- Commit `af52605` (6 October 2025) reintroduced and expanded
  `docs/FIELD-TIERS.md`; later revisions remain visible in its Git history.
- The earlier repository inventory, `ontology/hcmo-field-inventory.tsv`, had 30
  entries: 14 Mandatory, 12 Recommended, and 4 Optional. The current
  `docs/FIELD-TIERS.md` has 36 entries: 20 Mandatory, 11 Recommended, and 5
  Optional.

Contributions to HCMO are recorded from the project record (emails, proposal
documents, meetings and manuscript work), not inferred from commit authorship
or pull requests; most contributors never committed to this repository.
