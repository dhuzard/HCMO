# Cyril's tracking checklist — status mirror

**Source (Google Sheet):**
<https://docs.google.com/spreadsheets/d/1AcxwqF7L6NVEI07FE5GWx74uxTq_UACBWfGS44O7XKo/edit?gid=822209222#gid=822209222>

> This is a **repo-side mirror** of Cyril's 44-item checklist, updated with what
> has been done in `docs/paper/` and what is still left. I cannot write to the
> Google Sheet directly (read-only access), so copy the **Statut / Lien-preuve /
> Commentaire** columns below back into the sheet.
>
> **Statut legend:** ✅ Fait · 🟡 En cours · ⏸ Reporté · ⛔ Bloqué (needs clean V1 = T0) · ⬜ À faire
> **Last synced:** 2026-07-09 (branch `main`)

## Progress snapshot
| Indicateur | Valeur |
|---|---|
| Total | 44 |
| ✅ Fait | 25 |
| 🟡 En cours | 8 |
| ⏸ Reporté | 1 |
| ⛔ Bloqué (T0) | 3 |
| ⬜ À faire | 7 |
| Obligatoires restantes (non-Fait) | ~16 |

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
| 10 | Ontologie | Stabiliser classes & propriétés centrales | Oui | 🟡 | `ontology/v2/`, `docs/paper/MODULE-MAP.md` | v2 5 modules construit et placeholders nettoyés; reste à promouvoir officiellement puis traiter unités/définitions. |
| 11 | Ontologie | Labels + commentaires entités principales | Oui | 🟡 | `ontology/v2/modules/*.ttl`, `docs/paper/FOOPS-REPORT-2026-07-09.md` | v2: 111/111 termes évalués par FOOPS ont maintenant un `rdfs:comment`; revue co-auteurs + promotion live encore nécessaires. |
| 12 | Ontologie | Vérifier modules Turtle/OWL exportés | Oui | ✅ | `ontology/v2/README.md`, `ontology/v2/hcmo-v2-merged-clean.owl`, `docs/paper/PROTEGE-REASONER.md` | Modules v2 + clean OWL parsés; HermiT passe avec 33 classes et 0 classe incohérente. Live build/CI à repointer à la promotion. |
| 13 | Ontologie | Nettoyer termes Chowlk temporaires | Oui | ✅ | `docs/paper/PLACEHOLDER-MAP.md`, `ontology/v2/modules/hcm-placeholders.ttl` | Placeholders actifs v2 réduits à 0; cleanup final appliqué et documenté. Validation co-auteurs encore utile avant promotion. |
| 14 | Ontologie | Exemples d'instances représentatifs | Oui | 🟡 | `examples/user-submission.ttl`, `examples/dvc-tecniplast.ttl`, `docs/hcm-systems/FORM-FIELD-MAPPING.md` | Formulaire + DVC organisés en triples RDF: `rdf:type`, liens instance-instance, et valeurs littérales. Il reste à produire les exemples SHACL v2 complets après promotion. |
| 15 | Ontologie | Requêtes SPARQL des competency questions | Oui | ⛔ | `sections/03-requirements.md` | CQ1–CQ6 définies; requêtes après T0 (renvoient 0 actuellement). |
| 16 | Ontologie | SHACL valides/invalides | Oui | ⏸ | `docs/paper/PROTEGE-REASONER.md` | Reporté après décision de réunion: d'abord raisonneur OWL dans Protégé sur v2; SHACL seulement après gel/promotion des termes v2. |
| 17 | Ontologie | Lancer OOPS! + FOOPS! FAIR ontology assessment + noter problèmes | Oui | 🟡 | `docs/paper/FOOPS-REPORT-2026-07-09.md`, `docs/paper/evaluation/OOPS-REPORT-2026-07-10.md`, `sections/06-evaluation.md` | FOOPS v0.4.0 lancé sur le clean v2: score 0.49444446 → 1.0 après métadonnées, définitions et logo. OOPS! relancé post-FOOPS; P04/P08/P12/P34 corrigés, P11 réduit de 94 à 87, P10/P11/P13/P22 documentés. |
| 18 | Évaluation | Définir les competency questions de l'article | Oui | ✅ | `sections/03-requirements.md` | CQ1–CQ6 + mapping R1–R8. |
| 19 | Évaluation | Chaque requête répond à une CQ | Oui | ⛔ | — | Bloqué T0 (besoin de la V1 + requêtes). |
| 20 | Évaluation | Bilan OOPS!/FOOPS!/SHACL/WIDOCO/HermiT | Oui | 🟡 | `sections/06-evaluation.md`, `docs/paper/PROTEGE-REASONER.md`, `docs/paper/FOOPS-REPORT-2026-07-09.md`, `docs/paper/evaluation/OOPS-REPORT-2026-07-10.md` | WIDOCO ✅; HermiT ✅; FOOPS ✅ (1.0); OOPS! ✅ report archived, safe fixes applied, P11 reduced to 87; SHACL reporté jusqu'au gel/promotion des termes v2. |
| 21 | Ontologie | Documentation WIDOCO | Oui | ✅ | `README.md` → <https://dhuzard.github.io/HCMO/index-en.html> | Lien ajouté au README. |
| 22 | Availability | Dépôt GitHub propre & compréhensible | Oui | 🟡 | `README.md`, `ontology/v2/README.md`, `docs/paper/TODO.md` | README enrichi; v2 documentée; nettoyage global et promotion restent en cours. |
| 23 | Availability | Release versionnée figée | Oui | ⬜ | `TODO.md` (T9) | À cadrer sur la version citée. |
| 24 | Availability | DOI Zenodo | Oui | ✅ | `CITATION.cff` → 10.5281/zenodo.18925285 | Existe; à refigers sur la release du papier (T9). |
| 25 | Availability | Vérifier la licence | Oui | ✅ | `LICENSE`, `README.md` | CC BY 4.0 (fichier vérifié). ⚠ **Consentement des co-auteurs à confirmer** (CC BY 4.0 vs CC0) — voir OPEN-QUESTIONS Q19 / TODO T23b. |
| 26 | Availability | CITATION.cff | Oui | ✅ | `CITATION.cff` | Présent + ORCIDs ajoutés. |
| 27 | Availability | Namespace persistant w3id | Oui | 🟡 | <https://github.com/perma-id/w3id.org/pull/6261>, <https://w3id.org/hcmo/ontology/hcm> | Namespace HCMO live depuis le 2026-06-30. Follow-up ajouté: mettre à jour le w3id pour la version v2/release promue, sans changer l'IRI de base. |
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
| 38 | Soumission | Figures principales | Oui | 🟡 | `sources/figures/`, `version_rapport.drawio` | Figures candidates importées depuis le rapport; source draw.io/TTL harmonisée sur HCMO + `LocationResultTable`. Reste à choisir les figures finales et régénérer les PNG si nécessaire. |
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
only sections still incomplete; §6 now has HermiT, FOOPS, and OOPS evidence,
while final SHACL/CQ claims still depend on v2 promotion.

## The remaining blocker
Items **15, 19, 42** still wait on the promoted clean ontology and the
paper-ready v2 release alignment. Item **11** now has v2 definitions but still
needs co-author review and promotion. Item **13** is done, HermiT, FOOPS, and
OOPS evidence are recorded, and item **17** remains in progress for the
remaining OOPS modeling-policy findings. Item **27 (w3id)** is live but reopened
as a v2 release follow-up.
