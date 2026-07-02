# Cyril's tracking checklist — status mirror

**Source (Google Sheet):**
<https://docs.google.com/spreadsheets/d/1AcxwqF7L6NVEI07FE5GWx74uxTq_UACBWfGS44O7XKo/edit?gid=822209222#gid=822209222>

> This is a **repo-side mirror** of Cyril's 44-item checklist, updated with what
> has been done in `docs/paper/` and what is still left. I cannot write to the
> Google Sheet directly (read-only access), so copy the **Statut / Lien-preuve /
> Commentaire** columns below back into the sheet.
>
> **Statut legend:** ✅ Fait · 🟡 En cours · ⛔ Bloqué (needs clean V1 = T0) · ⬜ À faire
> **Last synced:** 2026-06-29 (branch `claude/resource-paper-draft`)

## Progress snapshot
| Indicateur | Valeur |
|---|---|
| Total | 44 |
| ✅ Fait | 22 |
| 🟡 En cours | 4 |
| ⛔ Bloqué (T0) | 11 |
| ⬜ À faire | 7 |
| Obligatoires restantes (non-Fait) | ~20 |

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
| 10 | Ontologie | Stabiliser classes & propriétés centrales | Oui | ⛔ | `AUDIT.md` | **Bloqué T0** : dépôt = export Chowlk obsolète. |
| 11 | Ontologie | Labels + commentaires entités principales | Oui | ⛔ | `AUDIT.md` | **0 `rdfs:comment`** dans le dépôt actuel → V1. |
| 12 | Ontologie | Vérifier modules Turtle/OWL exportés | Oui | 🟡 | `AUDIT.md` | Audit fait (mismatch repo↔rapport); correctif = T0. |
| 13 | Ontologie | Nettoyer termes Chowlk temporaires | Oui | ⛔ | `AUDIT.md` | **43 placeholders** (`UNKNOWN:*`, `ns:Class2`…) → V1. |
| 14 | Ontologie | Exemples d'instances représentatifs | Oui | ⛔ | `sections/03-requirements.md` | Scénario HCM complet; ABox synthétiques après T0. |
| 15 | Ontologie | Requêtes SPARQL des competency questions | Oui | ⛔ | `sections/03-requirements.md` | CQ1–CQ6 définies; requêtes après T0 (renvoient 0 actuellement). |
| 16 | Ontologie | SHACL valides/invalides | Oui | ⛔ | — | Bloqué T0 (shapes ciblent les termes legacy). |
| 17 | Ontologie | Lancer OOPS! + noter problèmes | Oui | ⛔ | — | Bloqué T0. |
| 18 | Évaluation | Définir les competency questions de l'article | Oui | ✅ | `sections/03-requirements.md` | CQ1–CQ6 + mapping R1–R8. |
| 19 | Évaluation | Chaque requête répond à une CQ | Oui | ⛔ | — | Bloqué T0 (besoin de la V1 + requêtes). |
| 20 | Évaluation | Bilan OOPS!/SHACL/WIDOCO | Oui | 🟡 | `sections/06-evaluation.md` | WIDOCO ✅; OOPS!/SHACL bloqués T0. |
| 21 | Ontologie | Documentation WIDOCO | Oui | ✅ | `README.md` → <https://dhuzard.github.io/HCMO/index-en.html> | Lien ajouté au README. |
| 22 | Availability | Dépôt GitHub propre & compréhensible | Oui | 🟡 | `README.md` | README enrichi; nettoyage global en cours. |
| 23 | Availability | Release versionnée figée | Oui | ⬜ | `TODO.md` (T9) | À cadrer sur la version citée. |
| 24 | Availability | DOI Zenodo | Oui | ✅ | `CITATION.cff` → 10.5281/zenodo.18925285 | Existe; à refigers sur la release du papier (T9). |
| 25 | Availability | Vérifier la licence | Oui | ✅ | `LICENSE`, `README.md` | CC BY 4.0. |
| 26 | Availability | CITATION.cff | Oui | ✅ | `CITATION.cff` | Présent + ORCIDs ajoutés. |
| 27 | Availability | Namespace persistant w3id | Oui | ✅ | <https://github.com/perma-id/w3id.org/pull/6261>, <https://w3id.org/hcmo/ontology/hcm> | PR w3id merged le 2026-06-30 ; namespace HCMO accepté. À vérifier ensuite avec la release finale. |
| 28 | Availability | README : comment utiliser l'ontologie | Oui | ✅ | `README.md` | Quickstart + "Consuming the ontology". |
| 29 | Availability | Release/doc/DOI = même version | Oui | ⬜ | `TODO.md` (T9) | À faire au moment de la release. |
| 30 | Availability | Section Availability prête à coller | Oui | ✅ | `sections/05-availability.md`, `metadata/resource-metadata.md` | GitHub/DOI/licence/docs/examples/queries. |
| 31 | KGQA | Rôle du repo hcmo-kgqa-lab dans le papier | Non | ✅ | `sections/07-impact.md`, `OPEN-QUESTIONS.md` (R2) | **Outlook**, pas contribution principale (décidé). |
| 32 | KGQA | Fuseki se lance avec données d'exemple | Non | ⬜ | — | Hors périmètre principal; à tester si temps. |
| 33 | KGQA | Requêtes SPARQL du démonstrateur OK | Non | ⬜ | — | Idem (outlook). |
| 34 | KGQA | Décrire principe LLM-contraint/KGQA | Non | ✅ | `sections/07-impact.md` | Décrit en outlook (pipeline Sanou). |
| 35 | KGQA | Capture/figure du démonstrateur | Non | ⬜ | — | Seulement si utile. |
| 36 | Soumission | Format & template | Oui | ✅ | `CALL-REQUIREMENTS.md` | **LNCS** (Springer). |
| 37 | Soumission | (Non-)anonymisation | Oui | ✅ | `CALL-REQUIREMENTS.md` | **Single-anonymous** : auteurs nommés. |
| 38 | Soumission | Figures principales | Oui | 🟡 | `sources/figures/`, rapport de stage | Figures candidates importées depuis le rapport. Sélection proposée pour l’article : F1 = contexte HCM/Olog ou paramètres HCM ; F2 = vue modules HCMO bio/housing/env/tech ; F3 = chaîne capteur → observation → résultat/provenance. Reste à choisir avec Damien lesquelles garder et à nettoyer les versions finales. |
| 39 | Soumission | Tableau récap des ressources | Oui | ✅ | `metadata/resource-metadata.md` | GitHub/DOI/docs/examples/SHACL/queries. |
| 40 | Soumission | Relecture interne complète | Oui | ⬜ | `TODO.md` (T22) | À faire en fin de rédaction. |
| 41 | Soumission | Liste auteurs & contributions | Oui | ✅ | `metadata/authors.md` | Gilbert 1ᵉʳ; Todorov & Huzard co-corresp. |
| 42 | Soumission | Version soumissionnable (objectif fin juillet) | Oui | ⛔ | — | Bloqué T0 (§4 & §6 manquent). |
| 43 | Soumission | Archive interne (preuves & liens) | Non | ✅ | `docs/paper/` (OPEN-QUESTIONS, AUDIT, NOVELTY…) | Ce dossier sert d'archive de décisions. |
| 44 | Availability | Liens valides après soumission/publication | Oui | ⬜ | — | À revérifier avant soumission. |

## What's drafted (article) — for items 2–6, 18, 30, 36–37, 39, 41
Abstract + §1 Introduction + §2 Related work + §3 Requirements + §5
Engineering/Availability + §7 Impact + §8 Conclusion are **drafted** in
`docs/paper/sections/`. **§4 Resource description** and **§6 Evaluation** are the
only sections still missing — both **blocked on the clean V1 (T0)**.

## The one blocker driving most ⛔ items
Items **10–17, 19, 42** all wait on the **clean V1 ontology** (see `AUDIT.md` and
the co-author email `emails/request-clean-v1.md`). Unblocking T0 clears 9+ items.
Item **27 (w3id)** and **23/29 (release)** are independent and can proceed now.
