# Cyril's tracking checklist — status mirror

**Source (Google Sheet):**
<https://docs.google.com/spreadsheets/d/1AcxwqF7L6NVEI07FE5GWx74uxTq_UACBWfGS44O7XKo/edit?gid=822209222#gid=822209222>

> This is a **repo-side mirror** of Cyril's 44-item checklist, updated with what
> has been done in `docs/paper/` and what is still left. I cannot write to the
> Google Sheet directly (read-only access), so copy the **Statut / Lien-preuve /
> Commentaire** columns below back into the sheet.
>
> **Statut legend:** ✅ Fait · 🟡 En cours · ⏸ Reporté · ⛔ Bloqué (needs clean V1 = T0) · ⬜ À faire
> **Last synced:** 2026-08-15 (`cyril/paper-submission-review`)

## Progress snapshot
| Indicateur | Valeur |
|---|---|
| Total | 44 |
| ✅ Fait | 33 |
| 🟡 En cours | 4 |
| ⏸ Reporté | 0 |
| ⛔ Bloqué (T0) | 0 |
| ⬜ À faire | 7 |
| Obligatoires restantes (non-Fait) | ~8 |

## Items

| # | Catégorie | Élément | Oblig. | Statut | Lien / preuve (repo) | Commentaire |
|:-:|:-:|---|:-:|:-:|---|---|
| 1 | Article | Choisir la cible principale | Oui | ✅ | `docs/paper/README.md`, `OPEN-QUESTIONS.md` (R1) | **ESWC 2027 Resource Track, 15 pp** (décidé). ISWC = repli. |
| 2 | Article | Plan de l'article adapté à HCMO | Oui | ✅ | `docs/paper/OUTLINE.md` | 8 sections + budget de pages + fil narratif. |
| 3 | Article | Lister les contributions | Oui | ✅ | `sections/01-introduction.md` | 4 contributions; HCMO = 1ʳᵉ ontologie HCM. |
| 4 | Article | Rédiger la motivation | Oui | ✅ | `sections/01-introduction.md` | Diversité systèmes/capteurs + manque d'interopérabilité. |
| 5 | Article | Section "Availability" prête à coller | Oui | ✅ | `sections/05-availability.md`, `metadata/resource-metadata.md` | Draft complet; items en attente marqués [pending]. |
| 6 | Article | Partie communauté d'usagers HCM | Oui | ✅ | `sections/03-requirements.md`, `sections/07-impact.md` | Parties prenantes + adoption via TEATIME. |
| 7 | Related work | 5–10 resource papers d'ontologies comparables | Oui | ✅ | `docs/paper/notes/resource-papers/README.md` | 5 resource papers comparables identifiés avec source et critères de comparaison pour HCMO : metadata, availability, figures, CQ/SPARQL, évaluation. |
| 8 | Related work | Guidelines / best practices publication ontologie | Oui | ✅ | `CALL-REQUIREMENTS.md`, `references.bib` | WIDOCO, OOPS!, FAIR, w3id, Zenodo, LOT/SAMOD. |
| 9 | Related work | Tableau critères ESWC vs ISWC | Oui | ✅ | `README.md`, `CALL-REQUIREMENTS.md` | Format, anonymat, pages, availability. |
| 10 | Ontologie | Stabiliser classes & propriétés centrales | Oui | ✅ | `ontology/modules/`, `docs/paper/MODULE-MAP.md` | Le modèle 5 modules est promu; compatibilité explicite pour les IRI 0.0.1. |
| 11 | Ontologie | Labels + commentaires entités principales | Oui | ✅ | `ontology/modules/*.ttl`, `docs/MISSING-DEFINITIONS.md` | Toutes les classes/propriétés HCMO actives ont label et définition textuelle. |
| 12 | Ontologie | Vérifier modules Turtle/OWL exportés | Oui | ✅ | `ontology/modules/`, `dist/`, `tooling/validate.py` | Build reproductible, parsing des modules/distributions et validation automatisée. |
| 13 | Ontologie | Nettoyer termes Chowlk temporaires | Oui | ✅ | `docs/paper/PLACEHOLDER-MAP.md`, `ontology/legacy/mapp-0.0.1/` | Aucun placeholder actif; source originale archivée hors manifeste. |
| 14 | Ontologie | Exemples d'instances représentatifs | Oui | ✅ | `examples/abox-minimal.ttl`, `examples/isa-hcmo-bridge.ttl`, `examples/dvc-tecniplast.ttl` | Exemples HCMO courants, cas ISA/RO-Crate et profil DVC présents. |
| 15 | Ontologie | Requêtes SPARQL des competency questions | Oui | ✅ | `queries/competency_questions.yaml`, `queries/cq-*.rq` | Onze requêtes canoniques et cinq requêtes isolées de round trip passent avec leurs réponses complètes attendues. |
| 16 | Ontologie | SHACL valides/invalides | Oui | ✅ | `shapes/hcm-shapes.ttl`, `examples/` | Les exemples positifs et négatifs sont exécutés par `tooling/validate.py`. |
| 17 | Ontologie | Lancer OOPS! + FOOPS! FAIR ontology assessment + noter problèmes | Oui | 🟡 | `docs/paper/evaluation/CANDIDATE-OOPS-FOOPS-2026-08-15.md`, `sections/06-evaluation.md` | Scan du candidat 0.3.0 archivé et trié; à relancer après les dernières corrections de métadonnées et sur l'artefact tagué. |
| 18 | Évaluation | Définir les competency questions de l'article | Oui | ✅ | `sections/03-requirements.md`, `queries/competency_questions.yaml` | Le texte décrit les onze questions canoniques et les cinq questions du fixture de round trip. |
| 19 | Évaluation | Chaque requête répond à une CQ | Oui | ✅ | `queries/competency_questions.yaml`, `tooling/validate.py` | Index, fichiers et réponses exactes sont contrôlés automatiquement; aucune requête orpheline. |
| 20 | Évaluation | Bilan OOPS!/FOOPS!/AskWol/SHACL/WIDOCO/HermiT | Oui | ✅ | `sections/06-evaluation.md`, `evaluation/ASKWOL-TRIAGE.md` | Les preuves datées sont archivées; AskWol est non bloquant avec exceptions documentées. |
| 21 | Ontologie | Documentation WIDOCO | Oui | ✅ | `README.md` → <https://dhuzard.github.io/HCMO/index-en.html> | Lien ajouté au README. |
| 22 | Availability | Dépôt GitHub propre & compréhensible | Oui | ✅ | `README.md`, `docs/README.md`, `docs/ARCHITECTURE.md` | Architecture active, sources historiques, génération et validation sont documentées. |
| 23 | Availability | Release versionnée figée | Oui | ✅ | `v0.3.0`, `RELEASE-GATE.md` | Tag, release et cinq artefacts vérifiés le 2026-08-31. |
| 24 | Availability | DOI Zenodo | Oui | ✅ | `CITATION.cff` → DOI de version 10.5281/zenodo.22208202 | Le concept DOI stable reste 10.5281/zenodo.18925284. |
| 25 | Availability | Vérifier la licence | Oui | ✅ | `LICENSE`, `README.md`, `TODO.md` | CC BY 4.0 confirmé par les coauteurs le 2026-08-31. |
| 26 | Availability | CITATION.cff | Oui | ✅ | `CITATION.cff` | Présent + ORCIDs ajoutés. |
| 27 | Availability | Namespace persistant w3id | Oui | ✅ | <https://w3id.org/hcmo/ontology/hcm>, `RELEASE-GATE.md` | Négociation vérifiée vers les artefacts 0.3.0 et la documentation HCMO le 2026-08-31, sans changer les IRI. |
| 28 | Availability | README : comment utiliser l'ontologie | Oui | ✅ | `README.md` | Quickstart + "Consuming the ontology". |
| 29 | Availability | Release/doc/DOI = même version | Oui | ✅ | `RELEASE-GATE.md`, `CITATION.cff` | Release et documentation 0.3.0; DOI de version 10.5281/zenodo.22208202. |
| 30 | Availability | Section Availability prête à coller | Oui | ✅ | `sections/05-availability.md`, `metadata/resource-metadata.md` | GitHub/DOI/licence/docs/examples/queries. |
| 31 | KGQA | Rôle du repo hcmo-kgqa-lab dans le papier | Non | ✅ | `sections/07-impact.md`, `OPEN-QUESTIONS.md` (R2) | **Outlook**, pas contribution principale (décidé). |
| 32 | KGQA | Fuseki se lance avec données d'exemple | Non | ⬜ | — | Hors périmètre principal; à tester si temps. |
| 33 | KGQA | Requêtes SPARQL du démonstrateur OK | Non | ⬜ | — | Idem (outlook). |
| 34 | KGQA | Décrire principe LLM-contraint/KGQA | Non | ✅ | `sections/07-impact.md` | Décrit en outlook (pipeline Sanou). |
| 35 | KGQA | Capture/figure du démonstrateur | Non | ⬜ | — | Seulement si utile. |
| 36 | Soumission | Format & template | Oui | ✅ | `CALL-REQUIREMENTS.md` | **LNCS** (Springer). |
| 37 | Soumission | (Non-)anonymisation | Oui | ✅ | `CALL-REQUIREMENTS.md` | **Single-anonymous** : auteurs nommés. |
| 38 | Soumission | Figures principales | Oui | ✅ | `overleaf/figures/f1.tex`, `f2.tex`, `f3.tex` | Trois figures TikZ vectorielles et sans dépendance draw.io: pipeline, modèle 5 modules et fixture de round trip. |
| 39 | Soumission | Tableau récap des ressources | Oui | ✅ | `metadata/resource-metadata.md` | GitHub/DOI/docs/examples/SHACL/queries. |
| 40 | Soumission | Relecture interne complète | Oui | ⬜ | `TODO.md` (T22) | À faire en fin de rédaction. |
| 41 | Soumission | Liste auteurs & contributions | Oui | ✅ | `metadata/authors.md` | Ordre confirmé; Gilbert, Todorov et Huzard correspondants; Todorov/Huzard co-derniers. |
| 42 | Soumission | Version soumissionnable | Oui | 🟡 | `sections/`, `overleaf/`, `tooling/build_paper.py` | Draft complet exporté; restent affiliations exactes, email correspondant de Cyril et revue collective. |
| 43 | Soumission | Archive interne (preuves & liens) | Non | ✅ | `docs/paper/` (OPEN-QUESTIONS, AUDIT, NOVELTY…) | Ce dossier sert d'archive de décisions. |
| 44 | Availability | Liens valides après soumission/publication | Oui | ⬜ | — | À revérifier avant soumission. |

## What's drafted (article) — for items 2–6, 18, 30, 36–37, 39, 41
All eight numbered article sections and the abstract have a current draft in
`docs/paper/sections/`. They were reviewed against the post-PR #26 HCMO 0.3.0
artifact on 2026-08-15. A deterministic LNCS/Overleaf export, three TikZ figures,
and a bibliography with all referenced keys are available under `overleaf/`.

## Remaining work
The ontology promotion and CQ-reconciliation blockers are cleared. Item **17**
remains partially open because archived OOPS!/FOOPS! runs target the clean-v2
precursor, not the final paper-matching release. Items **23/29/44** are final
release checks, item **27** is the w3id content-negotiation check, and items
**40/42** require co-author metadata and collective manuscript review.
