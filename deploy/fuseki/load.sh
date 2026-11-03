#!/bin/sh
# Build-time loader for the HCMO SPARQL image (runs in the Dockerfile's loader
# stage, never at container start).
#
#   load.sh SRC_DIR OUT_DIR
#
# SRC_DIR  repository files copied into the build (hcmo.yaml, dist/, examples/,
#          vocabularies/, docs/hcm-systems/catalog.ttl, deploy/fuseki/).
# OUT_DIR  becomes $FUSEKI_BASE in the runtime image: receives config.ttl and
#          the TDB2 databases under databases/<name>.
#
# Needs JENA_HOME (Apache Jena binary distribution, for tdb2.tdbloader).
# Graph IRIs are a published convention: do not rename them.
set -eu

SRC=${1:?usage: load.sh SRC_DIR OUT_DIR}
OUT=${2:?usage: load.sh SRC_DIR OUT_DIR}
: "${JENA_HOME:?JENA_HOME must point to the Apache Jena distribution}"
LOADER="$JENA_HOME/bin/tdb2.tdbloader"
G=https://w3id.org/hcmo/graph

die() { echo "load.sh: $*" >&2; exit 1; }

[ -x "$LOADER" ] || die "tdb2.tdbloader not found or not executable: $LOADER"

# --- HCMO version: first top-level `version:` of hcmo.yaml (quotes and
# trailing comment stripped). The build fails if it is missing or odd.
[ -f "$SRC/hcmo.yaml" ] || die "$SRC/hcmo.yaml not found"
VERSION=$(sed -n 's/^version:[[:space:]]*["'\'']\{0,1\}\([^"'\''#[:space:]]*\).*$/\1/p' "$SRC/hcmo.yaml" | head -n 1)
[ -n "$VERSION" ] || die "no 'version:' found in hcmo.yaml"
case "$VERSION" in
  *[!0-9A-Za-z.+-]*) die "unexpected version '$VERSION' in hcmo.yaml" ;;
esac
echo "load.sh: HCMO version $VERSION"

mkdir -p "$OUT/databases"

# --- config.ttl from the template (@HCMO_VERSION@ -> version).
sed "s/@HCMO_VERSION@/$VERSION/g" "$SRC/deploy/fuseki/config.ttl.in" > "$OUT/config.ttl"
if grep -q '@HCMO_VERSION@' "$OUT/config.ttl"; then die "placeholder left in config.ttl"; fi
grep -q "\"hcmo-$VERSION\"" "$OUT/config.ttl" || die "service hcmo-$VERSION missing from config.ttl"
# Record the version served (handy for `docker run ... cat /fuseki/HCMO_VERSION`).
echo "$VERSION" > "$OUT/HCMO_VERSION"

# load DB GRAPH_IRI FILE: one named graph into a TDB2 database.
load() {
  [ -s "$SRC/$3" ] || die "missing or empty input file: $3"
  echo "load.sh: $1 <$2> <- $3"
  "$LOADER" --loc="$OUT/databases/$1" --graph="$2" "$SRC/$3"
}

# The six controlled vocabularies, shared by both databases.
load_vocabs() {
  load "$1" "$G/vocab/file-format"        vocabularies/file-formats.ttl
  load "$1" "$G/vocab/data-access-method" vocabularies/data-access-methods.ttl
  load "$1" "$G/vocab/vendor"             vocabularies/vendors.ttl
  load "$1" "$G/vocab/system"             vocabularies/systems.ttl
  load "$1" "$G/vocab/modality"           vocabularies/modality.ttl
  load "$1" "$G/vocab/sensor-technology"  vocabularies/sensor-technology.ttl
}

# --- /hcmo (and /hcmo-<version>): the validator's evaluation graph (the
# ontology plus the positive examples of hcmo.yaml, i.e. what
# `python tooling/run_cqs.py --print-files` lists) plus the SKOS vocabularies,
# which the competency questions do not touch. Adding any other file changes
# the reviewed answers (the catalog and the DVC profile do: see /hcm-systems).
load hcmo "$G/ontology"                              dist/hcmo.ttl
load hcmo "$G/examples/hcmo-abox-minimal"            examples/abox-minimal.ttl
load hcmo "$G/examples/hcmo-user-submission"         examples/user-submission.ttl
load hcmo "$G/examples/hcmo-isa-hcmo-bridge"         examples/isa-hcmo-bridge.ttl
load_vocabs hcmo

# --- /hcm-systems: exploration dataset for the HCM systems catalogue.
load hcm-systems "$G/ontology"                       dist/hcmo.ttl
load hcm-systems "$G/catalog"                        docs/hcm-systems/catalog.ttl
load hcm-systems "$G/examples/dvc-tecniplast"        examples/dvc-tecniplast.ttl
load hcm-systems "$G/submissions"                    examples/user-submission.ttl
load_vocabs hcm-systems

echo "load.sh: done ($OUT)"
