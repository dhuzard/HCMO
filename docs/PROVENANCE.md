# HCMO Development Provenance

HCMO developed through four stages:

1. The community-developed [COST TEATIME Olog](https://www.cost-teatime.org/about/hcm-definition/)
   established structured terminology for the home-cage monitoring domain and
   is the closest conceptual precursor to HCMO.
2. During the first half of 2025, Damien Huzard began translating the broader
   domain need into a machine-actionable ontology through Metadatapp's
   semantic-development work and related grant preparation.
3. A COST mobility grant (€750) awarded to Damien Huzard for *Mapping the
   Home-Cage Monitoring Ontology to Device Metadata* supported limited
   preliminary device-metadata mapping, project scoping, and publication of an
   early GitHub version in September 2025, with contributions from Leonardo
   Restivo and Benoit Girard.
4. An Exogene grant (€23,000), administered by the Pôle Universitaire
   d'Innovation of the University of Montpellier and awarded to Metadatapp to
   support collaboration between Damien Huzard and Konstantin Todorov, supported
   the comprehensive redesign and formal evaluation from October 2025 to
   October 2026. As part of the Exogene-funded Master's project, Cyril Gilbert
   redesigned and implemented the HCMO version presented in the article, with
   the other authors contributing as recorded in the CRediT statement.

## Non-author contributions

- **Initial HCM profile of the TEATIME Olog:** Leonardo Restivo and Davor Virag.
- **Preparation and preliminary scoping of the COST mobility-grant project and
  early categorisation of metadata elements used in auxiliary authoring tools:**
  Benoit Girard and Leonardo Restivo.
- **Early conceptual and software architecture developed for HCMO within
  Metadatapp:** Laurent Huzard.
- **Domain expertise and feedback:** Benoit Petit-Demoulière, Vootele Voikar,
  Leonardo Restivo, Davor Virag, and Marion Rivalan.

Damien Huzard also acknowledges the INITIUM incubator team, particularly Rémi
Przybylski and Kate Rivière, as well as Frédéric Deverre, Loïc Clementz, and
Geoffrey Galibert for their contributions to the technical and business
development of Metadatapp.

## Auxiliary field-tier inventory

The preliminary project work by Benoit Girard and Leonardo Restivo included an
early categorisation of metadata elements used in auxiliary authoring tools.
Damien Huzard subsequently introduced a Mandatory/Recommended/Optional inventory
into the repository and revised it. The current inventory differs substantially
from the earlier historical repository inventory. Because the original
field-level classification supplied during preliminary scoping is not available
in the repository, the precise continuity of individual assignments and
rationales cannot be reconstructed from version history alone.

The current inventory is documentation and input to the optional authoring
workbench. Its tiers are not encoded as distinctions in the OWL ontology or the
canonical SHACL shapes, and they were not evaluated as part of the scientific
contribution reported in the HCMO article.

### Repository evidence

- Commit `3f2fc24` (30 September 2025), authored by Damien Huzard, introduced
  Mandatory/Recommended/Optional markers in the authoring interface.
- Commit `a421285` (3 October 2025), authored by Damien Huzard, introduced the
  field-tier document used by the device-agnostic blueprint workbench.
- Commit `af52605` (6 October 2025), authored by Damien Huzard, reintroduced and
  expanded `docs/FIELD-TIERS.md`; later revisions remain visible in its Git
  history.
- The earlier repository inventory, `ontology/hcmo-field-inventory.tsv`, had 30
  entries: 14 Mandatory, 12 Recommended, and 4 Optional. The current
  `docs/FIELD-TIERS.md` has 36 entries: 20 Mandatory, 11 Recommended, and 5
  Optional. Numerous fields were removed, added, split, or assigned a different
  tier.
- No commit message or tracked field-level source attributes either repository
  inventory to Benoit Girard or Leonardo Restivo. Their preliminary contribution
  is recorded in the project-provenance statement, while Git history establishes
  only when and by whom the repository artifacts were committed and revised.
