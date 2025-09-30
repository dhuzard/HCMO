#!/usr/bin/env node
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const statusWeights = {
  provided: 1,
  partial: 0.5,
  missing: 0,
  unknown: 0,
};

function parseCsv(content) {
  const lines = content.trim().split(/\r?\n/);
  const [header, ...rows] = lines;
  const columns = header.split(",");
  return rows.map((row) => {
    const cells = row.split(/,(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)/).map((cell) => cell.replace(/^\"|\"$/g, ""));
    const record = {};
    columns.forEach((col, idx) => {
      record[col.trim()] = cells[idx]?.trim() ?? "";
    });
    return record;
  });
}

function scoreChecklist(records) {
  const domains = new Map();
  for (const record of records) {
    const domain = record.domain;
    if (!domains.has(domain)) {
      domains.set(domain, { total: 0, weighted: 0, mandatory: 0, mandatoryProvided: 0 });
    }
    const data = domains.get(domain);
    data.total += 1;
    const weight = statusWeights[record.coverage_status] ?? 0;
    data.weighted += weight;
    if (record.classification === "mandatory") {
      data.mandatory += 1;
      if (record.coverage_status === "provided") {
        data.mandatoryProvided += 1;
      }
    }
  }
  const summary = [];
  for (const [domain, data] of domains.entries()) {
    const coverage = data.total ? (data.weighted / data.total) * 100 : 0;
    const mandatoryCoverage = data.mandatory ? (data.mandatoryProvided / data.mandatory) * 100 : 0;
    summary.push({ domain, items: data.total, coverage: coverage.toFixed(1), mandatoryCoverage: mandatoryCoverage.toFixed(1) });
  }
  return summary.sort((a, b) => a.domain.localeCompare(b.domain));
}

function main() {
  const inputPath = process.argv[2] ?? "docs/hcmo-blueprint-checklist.csv";
  const csvPath = resolve(process.cwd(), inputPath);
  const content = readFileSync(csvPath, "utf8");
  const records = parseCsv(content);
  const summary = scoreChecklist(records);
  const overall = summary.reduce((acc, item) => acc + Number(item.coverage), 0) / summary.length;
  console.log("Blueprint coverage summary (weighted by provided=1, partial=0.5):");
  for (const item of summary) {
    console.log(`- ${item.domain}: coverage ${item.coverage}% | mandatory provided ${item.mandatoryCoverage}%`);
  }
  console.log(`Overall coverage (simple mean): ${overall.toFixed(1)}%`);
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}
