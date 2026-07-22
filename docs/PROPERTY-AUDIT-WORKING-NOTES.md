# Property audit working notes

Status: working evidence for checklist item C01. This document is not the
approved C03 property inventory and does not authorize ontology changes.

Reviewer: Cyril Gilbert (`https://orcid.org/0009-0008-2489-8106`)

Review started: 2026-07-22

Review branch: `cyril/property-audit`

## Scope and method

The audit covers the 81 active, non-deprecated local object and datatype
properties declared in the five active source modules. The 49 deprecated
properties in `hcm-compat.ttl` will be reviewed separately. External
properties directly used in HCMO axioms, shapes, examples, or competency
queries remain in scope.

For each priority case, the review will distinguish:

- asserted domain, range, parent, inverse, and class restrictions;
- consequences inferred from isolated positive and edge-case assertions;
- use in examples, SHACL shapes, and competency questions;
- the intended domain meaning and a reviewer decision; and
- any later implementation item, which must have separate approval and tests.

`python tooling/property_audit.py` verifies the current `81 + 49` source
snapshot and executes the first rule-level entailment test with OWL RL. The
normal HermiT check remains the ontology-wide OWL DL consistency gate. OWL RL
is used here only to expose concrete inverse and domain/range consequences; it
does not replace HermiT.

The exact C03 TSV fields are still awaiting co-author validation. These notes
therefore must not be converted automatically into ontology edits or treated
as the final inventory.

## C01-01: monitoredBy and installedIn

Review status: `needs evidence`

Owning module: `ontology/modules/hcm-tech.ttl`

### Asserted semantics

| Property | Definition summary | Domain | Range | Other axiom |
| --- | --- | --- | --- | --- |
| `hcm-tech:monitoredBy` | enclosure to a sensor installed in or monitoring it | `hcm:MonitoredEnclosure` | `hcm-tech:Sensor` | inverse of `hcm-tech:installedIn` |
| `hcm-tech:installedIn` | sensor to the enclosure in which it is installed | `hcm-tech:Sensor` | `hcm:MonitoredEnclosure` | inverse entailed from the declaration above |

`hcm-tech:Sensor` also has an existential restriction requiring installation
in some monitored enclosure. This restriction is relevant to the same
portable, remote, and not-yet-deployed sensor cases, but it is a distinct axiom
that requires its own decision.

### Current use

- Positive examples assert both properties in `abox-minimal.ttl`,
  `isa-hcmo-bridge.ttl`, and `user-submission.ttl`; the DVC example also uses
  both relations.
- `hcm-shapes.ttl` requires at least one `monitoredBy` value for a monitored
  enclosure and exactly one `installedIn` value for a sensor.
- competency question `sensors-behaviors` navigates from an enclosure through
  `monitoredBy` and then through `captures`.
- no current edge-case fixture represents remote or portable monitoring.

Because the positive examples explicitly assert both directions, they do not
test whether the inverse axiom itself is correct or necessary.

### Observed inference

The executable test starts from each relation separately. With the current
axioms:

1. `cage monitoredBy sensor` entails `sensor installedIn cage`;
2. `sensor installedIn cage` entails `cage monitoredBy sensor`; and
3. each assertion also entails the declared subject and object types through
   domain and range.

The first entailment is too strong if a remote or portable sensor can monitor
an enclosure without being physically installed in it. HermiT can confirm that
the ontology is consistent, but consistency alone cannot establish that this
domain claim is true.

### Preliminary decision

Decision: `needs evidence` from domain experts and representative systems.

The definitions currently differ: `monitoredBy` explicitly permits monitoring
without installation, whereas `installedIn` is a physical placement relation.
Under the accepted C02 inverse policy, that wording does not justify an exact
inverse.

Candidate resolutions for review:

1. Keep the relations distinct and remove the inverse axiom. Reverse query
   navigation can use a SPARQL inverse path where needed.
2. Narrow `monitoredBy` to installed sensors and retain the inverse, only if all
   intended HCM systems satisfy that stronger meaning.
3. Introduce a separately justified deployment or monitoring-assignment model
   if installation and monitoring vary over time or by recording session.

No candidate is implemented by this audit note. Before a change, the project
needs at least one portable or remote sensor example, an agreed competency
question, and explicit decisions for both the inverse and the Sensor
existential restriction.

## Review queue

The next cases follow the accepted C01 order:

1. `hcm:locatedIn` against the accepted broad `schema:Place` range;
2. the seven shared environmental-property predicates;
3. `hcm-obs:hasCondition` and its open `owl:Thing` range;
4. current-state properties and housing-assignment time;
5. subject-to-observation shortcuts against SOSA; and
6. broad union domains in `hcm-bio` and `hcm-tech`.

The group-membership inverse candidate and `captures` parent relation will be
reviewed under C02 with the same evidence pattern.
