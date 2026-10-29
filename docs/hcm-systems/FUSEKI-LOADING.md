# Fuseki loading workflow

Use this workflow to build a Fuseki dataset from the ontology plus HCM systems
ABox data.

## Recommended: `deploy/fuseki/`

The maintained, reproducible way to get these graphs into Fuseki is
[`deploy/fuseki/`](../../deploy/fuseki/README.md): a Docker image (Apache Jena
Fuseki 5.6.0) that loads the graphs below into TDB2 at build time and serves
three read-only datasets (`/hcmo`, `/hcmo-<version>`, `/hcm-systems`; the last
one holds the catalogue and submissions). Run it locally with
`docker compose -f deploy/fuseki/docker-compose.yml up --build`. The manual
`tdb2.tdbloader` workflow below remains the alternative, for example to load
into an existing Fuseki.

## Generate RDF artifacts

From the repository root:

```powershell
python tooling/build.py
python tooling/export_hcm_catalog.py
python tooling/validate.py
```

`dist/hcmo.ttl` is the ontology graph. `docs/hcm-systems/catalog.ttl` is the
generated sparse catalog graph. User submissions are Turtle files generated from
the contribution form or curated into the same pattern as
`examples/user-submission.ttl`. The DVC worked example has a profile-level ABox at
`examples/dvc-tecniplast.ttl`; it is source-backed RDF instance data, but it is
not yet a full SHACL submission because the local profile does not assert cage
dimensions.

## Suggested named graphs

Load the files into separate named graphs so ontology, catalog, and curated
submissions can be updated independently:

| Graph | File(s) | Purpose |
|---|---|---|
| `https://w3id.org/hcmo/graph/ontology` | `dist/hcmo.ttl` | Active HCMO ontology. |
| `https://w3id.org/hcmo/graph/catalog` | `docs/hcm-systems/catalog.ttl` | Sparse HCM system/product/software/component catalog. |
| `https://w3id.org/hcmo/graph/examples/dvc-tecniplast` | `examples/dvc-tecniplast.ttl` | Source-backed DVC system profile ABox. |
| `https://w3id.org/hcmo/graph/submissions` | curated submission `.ttl` files | Complete user-submitted system ABox records. |
| `https://w3id.org/hcmo/graph/examples/hcmo-abox-minimal` | `examples/abox-minimal.ttl` | Positive example, part of the competency-question evaluation graph. |
| `https://w3id.org/hcmo/graph/examples/hcmo-user-submission` | `examples/user-submission.ttl` | Positive example, part of the evaluation graph. |
| `https://w3id.org/hcmo/graph/examples/hcmo-isa-hcmo-bridge` | `examples/isa-hcmo-bridge.ttl` | Positive example, part of the evaluation graph. |
| `https://w3id.org/hcmo/graph/vocab/<name>` | `vocabularies/<file>.ttl` | The six SKOS vocabularies: `file-format` (`file-formats.ttl`), `data-access-method` (`data-access-methods.ttl`), `vendor` (`vendors.ttl`), `system` (`systems.ttl`), `modality`, `sensor-technology`. |

`deploy/fuseki/` loads the `/hcmo` dataset from the ontology, the three `examples/hcmo-*`
graphs and the vocabularies; `/hcm-systems` from the ontology, catalog,
`dvc-tecniplast`, submissions and vocabularies.

## Example load commands

With Apache Jena command-line tools:

```powershell
tdb2.tdbloader --loc .\fuseki-data\hcmo `
  --graph=https://w3id.org/hcmo/graph/ontology dist\hcmo.ttl

tdb2.tdbloader --loc .\fuseki-data\hcmo `
  --graph=https://w3id.org/hcmo/graph/catalog docs\hcm-systems\catalog.ttl

tdb2.tdbloader --loc .\fuseki-data\hcmo `
  --graph=https://w3id.org/hcmo/graph/examples/dvc-tecniplast examples\dvc-tecniplast.ttl

tdb2.tdbloader --loc .\fuseki-data\hcmo `
  --graph=https://w3id.org/hcmo/graph/submissions examples\user-submission.ttl
```

With a running Fuseki server, use `s-post` or the Fuseki UI and select the same
named graph IRIs.

## Validation rule

Validate complete user submissions against `shapes/hcm-shapes.ttl` before loading
them into the submissions graph. The generated catalog is intentionally sparse and
should be treated as a reference graph, not as a complete `hcm:System`
submission.

```powershell
python -m pyshacl -s shapes\hcm-shapes.ttl -i rdfs -a -f human examples\user-submission.ttl
```

## Competency questions against a hosted endpoint

`tooling/validate.py` runs the twelve `queries/cq-*.rq` on an in-memory graph.
To run the same questions against a SPARQL endpoint (a local or hosted Fuseki,
the Metadatapp public endpoint) and compare the rows with the reviewed
`expected_answers`, use:

```powershell
python tooling/run_cqs.py --endpoint http://localhost:3030/hcmo/sparql
python tooling/run_cqs.py --endpoint https://<host>/hcmo/sparql --user admin --password ...
python tooling/run_cqs.py --endpoint https://<host>/hcmo/sparql --no-compare   # rows only
```

The expected rows hold only when the dataset's default graph is the union of the files of the
validator's evaluation graph (`python tooling/run_cqs.py --print-files`:
`dist/hcmo.ttl` plus the positive examples) and queries see their union, so
either load them into the default graph or enable `tdb2:unionDefaultGraph`.
A dataset that also holds the catalog, submissions, or other releases returns
extra rows; `--no-compare` shows them without failing, and `--graph <iri>`
(repeatable, sent as `default-graph-uri`) restricts the query to the named
graphs. On the Metadatapp public endpoint, which loads the ontology as
`https://w3id.org/hcmo/graph/ontology` and the three positive examples as
named-only graphs `https://w3id.org/hcmo/graph/examples/hcmo-<name>`:

```powershell
python tooling/run_cqs.py --endpoint https://api.metadatapp.net/api/v1/public/sparql `
  --graph https://w3id.org/hcmo/graph/ontology `
  --graph https://w3id.org/hcmo/graph/examples/hcmo-abox-minimal `
  --graph https://w3id.org/hcmo/graph/examples/hcmo-user-submission `
  --graph https://w3id.org/hcmo/graph/examples/hcmo-isa-hcmo-bridge
```

## Minimal SPARQL checks

List submitted systems and their suppliers:

```sparql
PREFIX hcm: <https://w3id.org/hcmo/ontology/hcm#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?system ?label ?supplierLabel WHERE {
  GRAPH <https://w3id.org/hcmo/graph/submissions> {
    ?system a hcm:System ;
      rdfs:label ?label ;
      hcm:producedBy/rdfs:label ?supplierLabel .
  }
}
```

List catalog records by category:

```sparql
PREFIX hcm: <https://w3id.org/hcmo/ontology/hcm#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?record ?label ?category WHERE {
  GRAPH <https://w3id.org/hcmo/graph/catalog> {
    ?record rdfs:label ?label ;
      hcm:hasCategory ?category .
  }
}
ORDER BY ?category ?label
```
