# Proposition de communication — SemWeb.Pro 2026

> Journée du 26 novembre 2026, Paris · Organisée par Logilab
> Soumission à envoyer à `contact at semweb.pro` avant le 30 juin 2026.
> Présentation orale (15 min + 5 min de questions) ou poster.

---

## Titre

**HCMO : une ontologie et des graphes de connaissances pour le monitoring en
cage des animaux de laboratoire**

## Description (≈ 360 mots)

Le monitoring en cage (*home-cage monitoring*, HCM) — l'observation
automatisée, continue et non invasive des animaux de laboratoire dans leur cage
d'hébergement — connaît un essor rapide en recherche préclinique. Il améliore la
qualité et la reproductibilité des données tout en répondant aux principes des
3R (réduction et raffinement de l'expérimentation animale). Mais chaque système
commercial produit des données propriétaires, hétérogènes et cloisonnées :
comparer, agréger ou partager les résultats entre dispositifs et entre
laboratoires reste très difficile, au détriment de la science ouverte et des
principes FAIR.

HCMO (*Home-Cage Monitoring Ontology*) propose un modèle sémantique partagé
pour ce domaine. Elle décrit les enceintes monitorées, les
sujets biologiques et groupes expérimentaux, l'environnement et ses mesures, les
observations et résultats, ainsi que les capteurs, le matériel et les logiciels
qui produisent les données. L'ontologie s'appuie sur les standards du Web
sémantique et s'aligne sur des vocabulaires établis : SOSA/SSN (capteurs et
observations), OWL-Time (temporalité), PROV (provenance) et BFO (ontologie de
haut niveau), avec une feuille de route vers QUDT/OM pour les grandeurs et
unités.

Au-delà du modèle, HCMO est livrée comme un paquet directement exploitable par
des outils : un manifeste de version stable servant de contrat aux couches en
aval, des sources Turtle modulaires, des distributions générées de façon
reproductible (TTL, OWL, JSON-LD), des formes SHACL pour la validation des
données à l'ingestion, des requêtes de compétence SPARQL, un contexte JSON-LD
pour les développeurs, une documentation HTML (WIDOCO), des IRI pérennes
(w3id.org), une licence CC BY 4.0, un DOI et une chaîne d'intégration continue
qui garantit la cohérence des artefacts.

Nous explorons par ailleurs l'apport des grands modèles de langues (LLM) à deux
niveaux : l'assistance à la construction et à l'enrichissement de l'ontologie,
et l'interrogation en langue naturelle du graphe de connaissances (couche KGQA),
afin de rendre ces données accessibles aux biologistes.

Nous présenterons la motivation et le domaine, les choix de modélisation et
d'alignement, l'organisation outillée du dépôt open source, et les leçons d'un
projet pilote — ainsi que les défis ouverts : qualité des définitions, mapping
des données constructeurs et adoption communautaire.

## Autrices et auteurs

Le projet réunit une équipe pluridisciplinaire mêlant expertise en
neurosciences et expérimentation animale et expertise en Web sémantique,
graphes de connaissances et données FAIR :

- **Damien Huzard** ([ORCID 0000-0003-4820-7951](https://orcid.org/0000-0003-4820-7951)) — neuroscientifique, porteur du projet, spécialiste du monitoring en cage.
- **Konstantin Todorov** ([ORCID 0000-0002-9116-6692](https://orcid.org/0000-0002-9116-6692)) — Web sémantique et appariement d'ontologies.
- **Pierre Larmande** ([ORCID 0000-0002-2923-9790](https://orcid.org/0000-0002-2923-9790)) — données FAIR et graphes de connaissances pour les sciences du vivant.
- **Cyril Gilbert**, **Gaoussou Sanou**, **Serge Sonfack**, **Antoine Tofano** — modélisation de l'ontologie, ingénierie des données et outillage.

> _À compléter avant l'envoi : affiliations institutionnelles et, si possible,
> ORCID manquants._

## Liens

- Dépôt de code : <https://github.com/dhuzard/HCMO>
- Espace de noms / IRI de l'ontologie : <https://w3id.org/hcmo/ontology/hcm>
- DOI (Zenodo) : <https://doi.org/10.5281/zenodo.18925285>
- Documentation HTML (WIDOCO) : <https://dhuzard.github.io/HCMO/index-en.html>
- Démo / vidéo de la couche KGQA — _à insérer si disponible avant l'envoi._

---

### Notes de soumission

- **Format** : viser la présentation orale ; un repli en poster reste pertinent,
  la conférence retenant en poster les projets encore en cours.
- **Langue** : proposition acceptée en anglais, mais **présentation en
  français** (langue de la conférence). Ce texte est rédigé en français.
- **Engagement** : au moins une personne parmi les auteurs s'engage à venir
  présenter (et à prendre une place).
- **Critères de sélection** : mettre en avant l'**usage effectif des standards**
  (OWL, SHACL, SPARQL, SOSA/SSN, PROV, OWL-Time, JSON-LD) et le caractère
  **open source et outillé** du projet ; ajouter une démo/vidéo est apprécié.
