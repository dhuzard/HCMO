# HCMO SPARQL reference endpoint (Fuseki)

This folder packages a public, read-only SPARQL endpoint for HCMO: Apache Jena
Fuseki 5.6.0 in a Docker image whose TDB2 databases are loaded **at build time**
from the files of a release. The image is meant to be deployed on Clever Cloud,
but it runs anywhere Docker does.

## Design

- **Immutable image.** `deploy/fuseki/Dockerfile` loads `dist/hcmo.ttl`, the
  examples and the vocabularies into TDB2 while the image is built. A restart
  starts from the same data, so no persistent volume (FS Bucket) is needed and no
  loader runs at start-up. To change the data, build and deploy a new image.
- **Read-only and anonymous.** The datasets expose the query and graph-store
  read services only; there is no update endpoint, and no password exists.
- **Union default graph.** Each dataset sets `tdb2:unionDefaultGraph`, so a
  query without `GRAPH` sees the union of all named graphs (the form
  `tooling/validate.py` evaluates), and `GRAPH ?g { ... }` still shows where a
  triple comes from.
- **Three datasets.**
  - `/hcmo`: the reference evaluation graph of the twelve competency questions
    (`queries/competency_questions.yaml`), that is what `tooling/validate.py`
    evaluates (the ontology and the three positive examples), plus the six SKOS
    vocabularies, which the questions do not touch:
    - `https://w3id.org/hcmo/graph/ontology` (`dist/hcmo.ttl`)
    - `https://w3id.org/hcmo/graph/examples/hcmo-abox-minimal`,
      `…/examples/hcmo-user-submission`, `…/examples/hcmo-isa-hcmo-bridge` (the
      three positive examples)
    - `https://w3id.org/hcmo/graph/vocab/{file-format,data-access-method,vendor,system,modality,sensor-technology}`
  - `/hcmo-<version>` (today `/hcmo-0.4.1`): the same database under a
    version-qualified, citable name, so a query written against `/hcmo-0.4.1`
    states which release it was run on. The image serves the release it was
    built from, under both names; it does not carry earlier releases (see
    "Release procedure").
  - `/hcm-systems`: an exploration dataset for the HCM systems catalogue: the
    ontology, `…/graph/catalog` (`docs/hcm-systems/catalog.ttl`),
    `…/graph/examples/dvc-tecniplast`, `…/graph/submissions`
    (`examples/user-submission.ttl`) and the six vocabularies. It is not the
    reference graph: competency-question answers differ here.
- **Why not the Metadatapp store?** The Metadatapp Fuseki on Clever Cloud loads
  its data at runtime and runs without an FS Bucket, so it is empty after every
  restart until a rebuild runs (see "Deploying on Clever Cloud" in
  `docs/guide/self-hosting/knowledge-graph.md` of the Metadatapp repository). It
  also mixes HCMO with other projects' graphs and holds the HCMO examples as
  named-only graphs. A dedicated, immutable image gives a stable, citable
  reference that does not depend on Metadatapp's loading state.

## Security model

- The bundled Fuseki UI is public: YASQE (editor) and YASR (results) work
  against the datasets without sign-in.
- The admin API `/$/**` is restricted to localhost by Fuseki's default
  `localhostFilter`. From outside, `/#/manage` does not work. `/$/ping`,
  `/$/server`, `/$/stats` and `/$/metrics` answer anonymously; every other
  `/$/` path answers 403.
- The query timeout is 30 s. Fuseki itself does not rate-limit; add that in
  front (Cloudflare or Clever Cloud) if abuse appears.
- Environment variables: `JAVA_OPTIONS` (default `-Xmx512m`) and `FUSEKI_PORT`
  (default `3030`). No secret is baked into the image.

## Run locally

From the repository root (the build context is the repository root):

```bash
docker compose -f deploy/fuseki/docker-compose.yml up --build
# or, without compose
docker build -f deploy/fuseki/Dockerfile -t hcmo-sparql .
docker run --rm -p 3030:3030 hcmo-sparql
```

Then open `http://localhost:3030/`, and check the reference graph:

```bash
curl http://localhost:3030/$/ping
python tooling/run_cqs.py --endpoint http://localhost:3030/hcmo/sparql
```

The twelve questions are expected to return 12/12.

## URLs

`<host>` is the deployment host: `sparql.hcmo.metadatapp.net` in production
(HTTPS), `localhost:3030` locally. `https://w3id.org/hcmo/sparql` redirects to
the production endpoint once the w3id rule is merged
([perma-id/w3id.org#7018](https://github.com/perma-id/w3id.org/pull/7018)): a
GET keeps its query string (302), a POST is repeated with its body (307), and a
browser without a query lands on the query page of `/hcmo`.

| What | URL |
|---|---|
| UI | `http://<host>/` |
| UI, query page of a dataset | `http://<host>/#/dataset/hcmo/query` |
| SPARQL endpoint, reference graph | `http://<host>/hcmo/sparql` |
| SPARQL endpoint, frozen release | `http://<host>/hcmo-0.4.1/sparql` |
| SPARQL endpoint, systems catalogue | `http://<host>/hcm-systems/sparql` |
| Graph store (read), per dataset | `http://<host>/<dataset>/get` |
| Health | `http://<host>/$/ping` |
| Server and statistics | `http://<host>/$/server`, `http://<host>/$/stats` |

## Clever Cloud: first-time setup

Done on 2026-10-29: the application **PROD hcmo-sparql**
(`app_d4c7adac-9dbc-4c4c-98f1-d9d048b0f37b`, organisation Metadatapp, region
`par`, flavor XS) serves `sparql.hcmo.metadatapp.net`. The steps below are kept
to recreate it.

A maintainer creates the application once, from the repository root, with the
`clever` CLI, in the existing organisation. The commands adapt the Metadatapp
ones, minus the FS Bucket and the admin password:

```bash
clever create --type docker "PROD hcmo-sparql" --alias prod-hcmo-sparql --region par --org <org-id>
clever scale --alias prod-hcmo-sparql --flavor XS     # S for -Xmx1g
clever env set --alias prod-hcmo-sparql CC_DOCKERFILE deploy/fuseki/Dockerfile
clever env set --alias prod-hcmo-sparql CC_DOCKER_EXPOSED_HTTP_PORT 3030
clever env set --alias prod-hcmo-sparql CC_HEALTH_CHECK_PATH '/$/ping'
clever env set --alias prod-hcmo-sparql JAVA_OPTIONS -- -Xmx512m   # "--": the value starts with a dash
clever deploy --alias prod-hcmo-sparql
```

| Variable | Value |
|---|---|
| `CC_DOCKERFILE` | `deploy/fuseki/Dockerfile` |
| `CC_DOCKER_EXPOSED_HTTP_PORT` | `3030` |
| `CC_HEALTH_CHECK_PATH` | `/$/ping` |
| `JAVA_OPTIONS` | `-Xmx512m` on XS (1 GB), `-Xmx1g` on S (2 GB) |

Do not set `CC_FS_BUCKET`: Metadatapp saw deployments stop at *Mounting
bucket …* with it, and this image does not need it.

Then:

1. Add the custom domain with
   `clever domain add --alias prod-hcmo-sparql sparql.hcmo.metadatapp.net`, and
   the DNS record Clever Cloud shows (`clever domain diag`): a CNAME
   `sparql.hcmo` to `domain.par.clever-cloud.com.` in the `metadatapp.net` zone
   (Cloudflare), **DNS only**, so Clever Cloud can issue the Let's Encrypt
   certificate. The certificate arrived a few minutes after the record.
2. Add a w3id rule `https://w3id.org/hcmo/sparql` to that domain in
   `ids/hcmo/.htaccess` of perma-id/w3id.org (opened as
   [perma-id/w3id.org#7018](https://github.com/perma-id/w3id.org/pull/7018)).
3. Check the deployment (below).

### GitHub configuration

The workflow `.github/workflows/sparql-deploy.yml` deploys with
`47ng/actions-clever-cloud@v2.1.0`, in the GitHub environment `production`.

| Kind | Name | Value |
|---|---|---|
| Secret (environment `production`) | `CLEVER_TOKEN` | Clever Cloud API token |
| Secret (environment `production`) | `CLEVER_SECRET` | Clever Cloud API secret |
| Variable | `CLEVER_SPARQL_APP_ID` | the application id (`app_…`, from `.clever.json` or the console); today `app_d4c7adac-9dbc-4c4c-98f1-d9d048b0f37b` |
| Variable | `CLEVER_SPARQL_URL` | public base URL, used for the post-deploy check; today `https://sparql.hcmo.metadatapp.net` |

The token and secret in place come from a maintainer's `clever login` and
expire on 2027-10-30. Renew them (or replace them with a dedicated API token)
before then, or deployments fail at the Clever Cloud step.

`.github/workflows/sparql-image.yml` builds the image on every change to its
inputs and runs `tooling/run_cqs.py` against the container (12/12 expected on
`/hcmo` and `/hcmo-<version>`). It needs no secret.

## Release procedure

1. Release HCMO as usual (tag `v0.5.0`, GitHub release published).
2. The `release: published` event triggers `sparql-deploy.yml`, which builds
   the image on Clever Cloud from the tagged sources. `/hcmo` and `/hcmo-0.5.0`
   now hold the 0.5.0 data; `/hcmo-0.4.1` is no longer served by this image.
3. The workflow then runs the post-deploy check against `CLEVER_SPARQL_URL`.
4. After the release, `/hcmo` answers with 0.5.0 data; `/hcmo-0.5.0` is the
   citable name of that release.

Keeping earlier releases online next to the current one (`/hcmo-0.4.1` after
0.5.0) is a deliberate follow-up, not something this image does: it would load
each earlier release's `hcmo.ttl` and examples from that release's GitHub
assets at build time, which needs a per-release manifest of those files. Until
then, a published version stays reproducible from its tag (`docker build` on
the tag gives the same image) and from its Zenodo archive.

A manual deployment is possible from the Actions tab (`workflow_dispatch`) or
with `clever deploy --alias prod-hcmo-sparql`.

## Troubleshooting

- **Is it up?** `curl -i https://<host>/$/ping` must return `200`. A restart
  loop usually means the health check fails or the JVM is out of memory.
- **Logs:** `clever logs --alias prod-hcmo-sparql` (add `--since 1h`).
- **Memory:** `OutOfMemoryError` or a killed container: raise the flavor to S
  and set `JAVA_OPTIONS` to `-Xmx1g`. Keep the heap well under the instance
  memory, TDB2 maps its files outside the heap.
- **Queries fail with a timeout:** the 30 s limit applies; narrow the query with
  a `GRAPH` clause or `LIMIT`.
- **Wrong answers for the competency questions:** run
  `python tooling/run_cqs.py --endpoint https://<host>/hcmo/sparql`. `/hcm-systems`
  holds extra graphs and is expected to differ.
- **`/#/manage` or `/$/datasets` refuse:** expected, the admin API is
  localhost-only.
- **Data looks stale:** the image only changes when a new one is deployed; check
  the last deployment in the Actions tab and `clever status`.
