#!/usr/bin/env node
import { readFileSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";

function parseArgs(argv) {
  const args = { format: "jsonld", out: null, inventory: "ontology/hcmo-field-inventory.tsv" };
  for (let i = 2; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === "--format" && argv[i + 1]) {
      args.format = argv[i + 1];
      i += 1;
    } else if (arg === "--out" && argv[i + 1]) {
      args.out = argv[i + 1];
      i += 1;
    } else if (arg === "--inventory" && argv[i + 1]) {
      args.inventory = argv[i + 1];
      i += 1;
    } else if (arg === "--help") {
      console.log("Usage: node tooling/metadata_entry_tool.mjs [--format jsonld|csv] [--out path] [--inventory file]");
      process.exit(0);
    }
  }
  return args;
}

function loadInventory(path) {
  const content = readFileSync(path, "utf8");
  const lines = content.trim().split(/\r?\n/);
  const [header, ...rows] = lines;
  const columns = header.split("\t");
  const entries = rows.map((row) => {
    const cells = row.split("\t");
    const entry = {};
    columns.forEach((col, idx) => {
      entry[col] = (cells[idx] ?? "").trim();
    });
    return entry;
  });
  const domains = new Map();
  for (const entry of entries) {
    const domain = entry.domain;
    if (!domains.has(domain)) {
      domains.set(domain, []);
    }
    domains.get(domain).push(entry);
  }
  return domains;
}

function buildJsonLd(domains) {
  const metadata = {};
  for (const [domain, entries] of domains.entries()) {
    metadata[domain] = {};
    for (const entry of entries) {
      metadata[domain][entry.identifier] = "";
    }
  }
  return {
    "@context": "https://w3id.org/hcmo/ontology/context.jsonld",
    metadata,
  };
}

function buildCsv(domains) {
  const rows = ["domain,field,value,notes"];
  for (const [domain, entries] of domains.entries()) {
    for (const entry of entries) {
      const note = `${entry.classification} | ${entry.ontology_iri}`.replace(/"/g, "'");
      rows.push(`${domain},${entry.identifier},,${note}`);
    }
  }
  return rows.join("\n");
}

function main() {
  const args = parseArgs(process.argv);
  const inventoryPath = resolve(process.cwd(), args.inventory);
  const domains = loadInventory(inventoryPath);
  let output;
  if (args.format === "jsonld") {
    output = JSON.stringify(buildJsonLd(domains), null, 2);
  } else if (args.format === "csv") {
    output = buildCsv(domains);
  } else {
    console.error(`Unsupported format: ${args.format}`);
    process.exit(1);
  }
  if (args.out) {
    const outPath = resolve(process.cwd(), args.out);
    writeFileSync(outPath, output, "utf8");
    console.log(`Wrote ${args.format} template to ${outPath}`);
  } else {
    process.stdout.write(output + "\n");
  }
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}
