# ROBOT Report (Annotation Completeness)

This report checks for missing `rdfs:label`, `IAO:0000115`, and `dcterms:source`
on core ontology entities (classes, object properties, datatype properties).

## Commands

```bash
# From repo root
robot report \
  --input ontology/hcm.ttl \
  --profile tooling/robot-report.tsv \
  --output reports/robot-report.tsv
```

## Expected output format

`reports/robot-report.tsv` is a TSV with the following columns:

```
ID	LEVEL	LABEL	MESSAGE	ENTITY
```

Example rows:

```
missing_definition	ERROR	Missing definition	Entity is missing IAO:0000115	https://w3id.org/hcmo/ontology/hcm#SomeEntity
missing_provenance	WARN	Missing provenance	Entity is missing dcterms:source	https://w3id.org/hcmo/ontology/hcm#AnotherEntity
```

If there are no findings, the file contains only the header row.
