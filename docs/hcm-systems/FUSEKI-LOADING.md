# Fuseki loading workflow

Use this workflow to build a Fuseki dataset from the ontology plus HCM systems
ABox data.

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
`examples/user-submission.ttl`.

## Suggested named graphs

Load the files into separate named graphs so ontology, catalog, and curated
submissions can be updated independently:

| Graph | File(s) | Purpose |
|---|---|---|
| `https://w3id.org/hcmo/graph/ontology` | `dist/hcmo.ttl` | Active HCMO ontology. |
| `https://w3id.org/hcmo/graph/catalog` | `docs/hcm-systems/catalog.ttl` | Sparse HCM system/product/software/component catalog. |
| `https://w3id.org/hcmo/graph/submissions` | curated submission `.ttl` files | Complete user-submitted system ABox records. |

## Example load commands

With Apache Jena command-line tools:

```powershell
tdb2.tdbloader --loc .\fuseki-data\hcmo `
  --graph=https://w3id.org/hcmo/graph/ontology dist\hcmo.ttl

tdb2.tdbloader --loc .\fuseki-data\hcmo `
  --graph=https://w3id.org/hcmo/graph/catalog docs\hcm-systems\catalog.ttl

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
