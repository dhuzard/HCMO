# HCMO public SPARQL reference endpoint: Apache Jena Fuseki serving read-only
# TDB2 databases that are loaded while the image is BUILT. The image is
# immutable: a restart never empties it and no volume is needed.
#
# Build context = repository root (see /.dockerignore):
#   docker build -f deploy/fuseki/Dockerfile -t hcmo-sparql .
#   docker run --rm -p 3030:3030 hcmo-sparql
#
# Stages:
#   loader   downloads + verifies Fuseki and Jena, runs load.sh (tdb2.tdbloader)
#   runtime  JRE + Fuseki + config + databases only (no Jena tools, no sources)

ARG JAVA_IMAGE=eclipse-temurin:21-jre

# ---------------------------------------------------------------------------
FROM ${JAVA_IMAGE} AS loader

# Pinned versions and SHA-512 of the release tarballs (values from the .sha512
# files on archive.apache.org). Bump them together.
ARG FUSEKI_VERSION=5.6.0
ARG JENA_VERSION=5.6.0
ARG FUSEKI_SHA512=53dfe13cdd5f6387a0c62917e275fde2cd2e2f2052bfe7515384934f24915228b8512a2dd2b50b7060cc300c976254349d991fcea239484cae48e0a59d67cd54
ARG JENA_SHA512=220ff50c3b6803c2cdade5479f8812700b281f4153fd73cdb83277b30f3d2c9e8a4a49d09717cfa7dde4fe5c7132a2aaaeeef3fbc474a6773b3d9deb5d63cbaa
# archive.apache.org keeps every release (downloads.apache.org drops old ones).
ARG APACHE_DIST=https://archive.apache.org/dist/jena/binaries

RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends ca-certificates curl; \
    rm -rf /var/lib/apt/lists/*

# Download, verify, unpack. Independent of the RDF sources, so this layer stays
# cached when only the data changes.
RUN set -eux; \
    cd /tmp; \
    curl -fsSL --retry 5 --retry-delay 5 -o fuseki.tar.gz \
        "${APACHE_DIST}/apache-jena-fuseki-${FUSEKI_VERSION}.tar.gz"; \
    echo "${FUSEKI_SHA512}  fuseki.tar.gz" | sha512sum -c -; \
    curl -fsSL --retry 5 --retry-delay 5 -o jena.tar.gz \
        "${APACHE_DIST}/apache-jena-${JENA_VERSION}.tar.gz"; \
    echo "${JENA_SHA512}  jena.tar.gz" | sha512sum -c -; \
    mkdir -p /opt/fuseki /opt/jena; \
    tar -xzf fuseki.tar.gz -C /opt/fuseki --strip-components=1; \
    tar -xzf jena.tar.gz -C /opt/jena --strip-components=1; \
    rm -f fuseki.tar.gz jena.tar.gz; \
    test -f /opt/fuseki/fuseki-server.jar; \
    test -x /opt/jena/bin/tdb2.tdbloader

ENV JENA_HOME=/opt/jena

# Only the files load.sh reads (the .dockerignore keeps the context to these).
COPY hcmo.yaml                    /src/hcmo.yaml
COPY dist/hcmo.ttl                /src/dist/hcmo.ttl
COPY examples/                    /src/examples/
COPY vocabularies/                /src/vocabularies/
COPY docs/hcm-systems/catalog.ttl /src/docs/hcm-systems/catalog.ttl
COPY deploy/fuseki/load.sh deploy/fuseki/config.ttl.in /src/deploy/fuseki/

# Read the HCMO version, render config.ttl, load the TDB2 databases into
# /build/fuseki (the future $FUSEKI_BASE). CRs are stripped in case of a
# Windows checkout; `sh` avoids depending on the file's executable bit.
RUN set -eux; \
    sed -i 's/\r$//' /src/deploy/fuseki/load.sh; \
    sh /src/deploy/fuseki/load.sh /src /build/fuseki

# ---------------------------------------------------------------------------
FROM ${JAVA_IMAGE} AS runtime

ARG FUSEKI_VERSION=5.6.0
LABEL org.opencontainers.image.title="hcmo-sparql" \
      org.opencontainers.image.description="Read-only SPARQL endpoint (Apache Jena Fuseki ${FUSEKI_VERSION}) for the HCMO ontology and examples" \
      org.opencontainers.image.source="https://github.com/dhuzard/HCMO"

# curl: HEALTHCHECK only (usually already in the Temurin image).
# User: uid/gid 1000 "fuseki". Ubuntu 24.04-based Temurin images already ship
# an "ubuntu" user/group with id 1000, so whatever holds id 1000 is removed first.
RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends curl; \
    rm -rf /var/lib/apt/lists/*; \
    u="$(getent passwd 1000 | cut -d: -f1)"; \
    if [ -n "$u" ]; then userdel -r "$u" || true; fi; \
    g="$(getent group 1000 | cut -d: -f1)"; \
    if [ -n "$g" ]; then groupdel "$g"; fi; \
    groupadd -g 1000 fuseki; \
    useradd -u 1000 -g 1000 -d /fuseki -M -s /usr/sbin/nologin fuseki; \
    mkdir -p /opt/fuseki /fuseki; \
    chown 1000:1000 /fuseki

# FUSEKI_HOME: Fuseki distribution (read-only). FUSEKI_BASE: run area, must be
# writable by the server user (Fuseki creates logs/, backups/, ... at start).
ENV FUSEKI_HOME=/opt/fuseki \
    FUSEKI_BASE=/fuseki \
    JAVA_OPTIONS=-Xmx512m \
    FUSEKI_PORT=3030

# Fuseki: launcher, server jar (UI included), logging config, licences.
COPY --from=loader /opt/fuseki/fuseki-server /opt/fuseki/fuseki-server.jar \
                   /opt/fuseki/log4j2.properties /opt/fuseki/LICENSE /opt/fuseki/NOTICE \
                   /opt/fuseki/
# Rendered config.ttl, HCMO_VERSION and databases/{hcmo,hcm-systems}.
COPY --from=loader --chown=1000:1000 /build/fuseki/ /fuseki/
COPY --chown=1000:1000 deploy/fuseki/shiro.ini /fuseki/shiro.ini
COPY deploy/fuseki/entrypoint.sh /opt/fuseki/entrypoint.sh
RUN set -eux; \
    sed -i 's/\r$//' /opt/fuseki/entrypoint.sh; \
    chmod 0755 /opt/fuseki/entrypoint.sh /opt/fuseki/fuseki-server; \
    test -f /fuseki/config.ttl; \
    test -d /fuseki/databases/hcmo; \
    test -d /fuseki/databases/hcm-systems

USER 1000:1000
WORKDIR /fuseki
EXPOSE 3030

# Liveness: /$/ping is anonymous (shiro.ini). The start period covers the JVM
# start; $FUSEKI_PORT is expanded by the shell at check time.
HEALTHCHECK --interval=30s --timeout=5s --start-period=40s --retries=3 \
    CMD curl -fsS "http://localhost:${FUSEKI_PORT}/\$/ping" > /dev/null || exit 1

ENTRYPOINT ["/opt/fuseki/entrypoint.sh"]
