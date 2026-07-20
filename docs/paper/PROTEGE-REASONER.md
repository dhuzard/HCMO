# Protégé and HermiT consistency check

Status: the automated reasoner targets the active HCMO release artifacts. The
pre-promotion v2 results remain recorded below as historical evidence.

## Active release protocol

1. Run `python tooling/build.py`.
2. Open `dist/hcmo.owl` in Protégé.
3. Confirm the ontology IRI is `https://w3id.org/hcmo/ontology/hcm` and the
   version IRI matches `hcmo.yaml`.
4. Run HermiT and record consistency, unsatisfiable classes, and warnings.
5. Run the reproducible command-line check:

```bash
pip install -r tooling/reasoning-requirements.txt
python tooling/reason.py --java-memory 2000
```

On local 32-bit Java, use `--java-memory 512`.

The command reads the generated RDF/XML and Turtle paths from `hcmo.yaml`,
checks both serializations, rejects properties typed as both object and
datatype properties, rejects active `UNKNOWN:` IRIs, and fails when HermiT
reports an inconsistent class.

SHACL remains a separate data-quality gate and is run by
`python tooling/validate.py` against the positive and negative ABox examples.

## Active 0.2.0 result

The command-line check was repeated on 2026-07-20 against `dist/hcmo.owl` from
the tagged 0.2.0 lineage. The graph contained 1,252 triples; HermiT loaded 56
HCMO classes and reported zero inconsistent classes. The pre-check found 57
object properties, 73 datatype properties, and no active `UNKNOWN:` IRI.

## Historical v2 review result

Before promotion, Protégé Desktop 5.6.9 and the command-line HermiT check were
run on `ontology/v2/hcmo-v2-merged-clean.owl`. That snapshot contained 700 RDF
triples and 32 declared classes; it loaded successfully, contained no active
`UNKNOWN:` IRI, and HermiT reported zero inconsistent classes. The v2 files are
now historical snapshots and are not build inputs.

The earlier dry-run evidence is archived in
`docs/paper/PROTEGE-DRY-RUN-2026-07-06.md`.
