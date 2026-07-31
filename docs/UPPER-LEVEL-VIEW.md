# HCMO upper-level views

HCMO exposes a small upper-level view by default while retaining a more
precise ontology-developer view as an optional profile. Both views use
canonical BFO and IAO IRIs. HCMO does not mint replacement upper-level terms
and does not assert equivalence with PROV-O, SIO, SULO, or ONTOP.

## Default end-user view

The generated release (`dist/hcmo.*`) presents five anchors:

```text
Thing
└── Entity
    ├── Material entity
    ├── Information entity
    ├── Quality / property
    └── Process / event
```

The labels “information entity”, “quality / property”, and “process / event”
are navigation language for users. Their canonical logical anchors are,
respectively, IAO information content entity, BFO quality, and BFO process.
The aliases do not collapse distinct upper-ontology categories.

The main HCMO placement is:

- Material entity: enclosures, enrichment, subjects, experimental groups,
  actuators, hardware, and sensors.
- Information entity: dimensions, assignments, study factors, environmental
  profiles, specifications, results, software, and time series.
- Quality / property: environmental properties.
- Process / event: the anchor is available for navigation, but HCMO currently
  defines no local process class. Evidence events use their authoritative
  external types.

The direct links to Entity are deliberate presentation shortcuts. They are
entailed by the authoritative BFO/IAO hierarchy and make the default release
understandable without requiring users to navigate continuant and dependence
categories.

## Optional ontology-developer view

Ontology developers can additionally load
`ontology/profiles/external-upper-developer.ttl`. It restores the
source-faithful intermediate BFO/IAO hierarchy, including continuant,
occurrent, independent continuant, specifically and generically dependent
continuant, and object aggregate.

The profile also refines `ExperimentalGroup` from the default Material entity
placement to BFO object aggregate. This is an additive refinement: it does not
change the HCMO term IRI or contradict the default view.

The profile is deliberately outside `hcmo.yaml`, whose shape remains the
stable release API. Its class set, hierarchy, and group refinement are checked
by `tooling/external_vocab.py` and by the normal validation gate.
