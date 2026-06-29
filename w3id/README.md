# w3id.org redirect config

These files are **not** used by this repository's build or CI. They are the
content-negotiation config for the persistent IRI base `https://w3id.org/hcmo/`.

To take effect they must be contributed to the community registry:

1. Fork <https://github.com/perma-id/w3id.org>.
2. Copy `hcmo/.htaccess` from here into `hcmo/.htaccess` there.
3. Open a PR. Once merged, `https://w3id.org/hcmo/...` resolves per the rules.

## What `hcmo/.htaccess` does

Two `Accept`-header negotiation blocks over the ontology IRI:

| Request | Resolves to |
| --- | --- |
| `/ontology/hcm` (+ `/bio`, `/env`, `/obs` modules) | the **latest** GitHub Release artifacts, or the WIDOCO docs site for browsers |
| `/ontology/hcm/<version>` (e.g. `0.9`) | the **`v<version>`** GitHub Release artifacts, or that release's page for browsers |

The version block matches only version-shaped segments (`\d+\.\d+(?:\.\d+)?`,
e.g. `0.9` or `0.0.1`) so it never shadows the `bio`/`env`/`obs` module
namespaces.

Per-version artifacts come from `release.yml`, which attaches
`hcmo.ttl` / `hcmo.owl` / `hcmo.json` to each `v*` tag release. The Release
assets are served with correct RDF media types (`text/turtle`,
`application/rdf+xml`, `application/json`), which is why these rules dereference
to Releases rather than `raw.githubusercontent.com` (which serves `text/plain`).

> **Note:** `hcmo.yaml` currently declares `version: 0.0.1`, but the latest
> published release is `v0.9`. Until the manifest version and the release tag
> agree, the version IRI `…/hcm/0.0.1` will 303 to a `v0.0.1` release that does
> not exist. Reconcile the manifest/tag before relying on per-version IRIs.
