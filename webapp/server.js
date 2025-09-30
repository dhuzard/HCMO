import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';
import fs from 'fs';
import os from 'os';
import { promisify } from 'util';
import { spawn } from 'child_process';
import { v4 as uuidv4 } from 'uuid';
import jsonld from 'jsonld';
import { Parser, Writer } from 'n3';
import archiver from 'archiver';
import { PassThrough } from 'stream';

const writeFile = promisify(fs.writeFile);
const rm = promisify(fs.rm);

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, '..');
const publicDir = path.join(__dirname, 'public');
const shapesPath = path.join(repoRoot, 'shapes', 'hcm-shapes.ttl');
const blueprintInventoryPath = path.join(repoRoot, 'ontology', 'hcmo-field-inventory.tsv');
const blueprintMappingPath = path.join(repoRoot, 'reference', 'device', 'device-to-ontology-mapping.csv');

const STATUS_ICONS = {
  provided: '✅',
  partial: '⚠️',
  missing: '❌',
  unknown: '•'
};

function createApp() {
  const app = express();
  app.use(express.json({ limit: '1mb' }));
  app.use(express.static(publicDir));

  app.post('/api/export', exportHandler);
  app.get('/api/blueprint/inventory', blueprintInventoryHandler);
  app.get('/api/blueprint/examples', blueprintExamplesHandler);
  return app;
}

function parseDelimited(content, delimiter) {
  const lines = content.trim().split(/\r?\n/).filter(Boolean);
  if (!lines.length) {
    return [];
  }
  const headers = lines.shift().split(delimiter);
  return lines.map((line) => {
    const cells = line.split(delimiter);
    const record = {};
    headers.forEach((header, idx) => {
      record[header.trim()] = (cells[idx] ?? '').trim();
    });
    return record;
  });
}

function parseTsv(content) {
  return parseDelimited(content, '\t');
}

function parseCsv(content) {
  const lines = content.trim().split(/\r?\n/).filter(Boolean);
  if (!lines.length) {
    return [];
  }
  const headers = lines.shift().split(',').map((header) => header.trim());
  return lines.map((line) => {
    const cells = [];
    let current = '';
    let inQuotes = false;

    for (let i = 0; i < line.length; i += 1) {
      const char = line[i];
      if (char === '"') {
        if (inQuotes && line[i + 1] === '"') {
          current += '"';
          i += 1;
        } else {
          inQuotes = !inQuotes;
        }
      } else if (char === ',' && !inQuotes) {
        cells.push(current.trim());
        current = '';
      } else {
        current += char;
      }
    }
    cells.push(current.trim());

    const record = {};
    headers.forEach((header, idx) => {
      const value = cells[idx] ?? '';
      record[header] = value.replace(/^"|"$/g, '');
    });
    return record;
  });
}

function normalizeStatus(raw) {
  if (!raw) return 'unknown';
  const lower = raw.toLowerCase();
  if (lower.includes('provided') || raw.includes('✅')) return 'provided';
  if (lower.includes('partial') || raw.includes('⚠') || raw.includes('warning')) return 'partial';
  if (lower.includes('missing') || raw.includes('❌')) return 'missing';
  if (lower.includes('unknown')) return 'unknown';
  return lower || 'unknown';
}

async function loadBlueprintInventory() {
  const content = await fs.promises.readFile(blueprintInventoryPath, 'utf8');
  const records = parseTsv(content);
  const domains = new Map();

  records.forEach((record) => {
    const domainId = record.domain;
    if (!domains.has(domainId)) {
      domains.set(domainId, {
        id: domainId,
        label: record.domain.replace(/_/g, ' '),
        fields: []
      });
    }
    const domain = domains.get(domainId);
    domain.fields.push({
      identifier: record.identifier,
      label: record.label,
      classification: record.classification,
      ontologyIri: record.ontology_iri,
      expectedDatatype: record.expected_datatype
    });
  });

  return {
    domains: Array.from(domains.values()).sort((a, b) => a.id.localeCompare(b.id))
  };
}

async function loadBlueprintMapping() {
  try {
    const content = await fs.promises.readFile(blueprintMappingPath, 'utf8');
    const records = parseCsv(content);
    const mapping = new Map();
    records.forEach((record) => {
      const domain = record.domain;
      const field = record.blueprint_field;
      if (!domain || !field) return;
      const key = `${domain}:${field}`;
      const status = normalizeStatus(record.coverage_status);
      const deviceField = record.device_field || '';
      const transform = record.transform || '';
      const value = deviceField || transform || '';
      mapping.set(key, {
        status,
        value,
        deviceField,
        transform,
        notes: record.notes || ''
      });
    });
    return mapping;
  } catch (error) {
    // Mapping is optional; return empty map if missing.
    return new Map();
  }
}

async function loadBlueprintExamples() {
  const inventory = await loadBlueprintInventory();
  const mapping = await loadBlueprintMapping();

  const representative = {
    id: 'representative-device',
    label: 'Representative Device Export',
    description: 'Derived from reference/device/device-to-ontology-mapping.csv coverage data.',
    fields: {}
  };

  const ideal = {
    id: 'ideal-complete',
    label: 'Ideal Complete Alignment',
    description: 'All mandatory and optional fields provided with placeholder values.',
    fields: {}
  };

  inventory.domains.forEach((domain) => {
    representative.fields[domain.id] = {};
    ideal.fields[domain.id] = {};

    domain.fields.forEach((field) => {
      const key = `${domain.id}:${field.identifier}`;
      const mappingEntry = mapping.get(key);
      representative.fields[domain.id][field.identifier] = {
        status: mappingEntry?.status ?? 'missing',
        value: mappingEntry?.value ?? '',
        notes: mappingEntry?.notes ?? mappingEntry?.transform ?? '',
        transform: mappingEntry?.transform ?? ''
      };

      ideal.fields[domain.id][field.identifier] = {
        status: 'provided',
        value: `Example ${field.identifier}`,
        notes: field.classification === 'mandatory' ? 'Core metadata' : 'Recommended metadata'
      };
    });
  });

  return {
    examples: [representative, ideal]
  };
}

async function blueprintInventoryHandler(_req, res) {
  try {
    const inventory = await loadBlueprintInventory();
    res.json({ ...inventory, statusIcons: STATUS_ICONS });
  } catch (error) {
    console.error('Failed to load blueprint inventory:', error);
    res.status(500).json({ error: 'Failed to load blueprint inventory.' });
  }
}

async function blueprintExamplesHandler(_req, res) {
  try {
    const examples = await loadBlueprintExamples();
    res.json({ ...examples, statusIcons: STATUS_ICONS });
  } catch (error) {
    console.error('Failed to load blueprint examples:', error);
    res.status(500).json({ error: 'Failed to load blueprint examples.' });
  }
}

async function jsonldToTurtle(doc) {
  const nquads = await jsonld.toRDF(doc, { format: 'application/n-quads' });
  const parser = new Parser({ format: 'application/n-quads' });
  const writer = new Writer({ prefixes: { hcm: 'https://w3id.org/hcmo/ontology/hcm#' } });

  const quads = parser.parse(nquads);
  writer.addQuads(quads);

  return new Promise((resolve, reject) => {
    writer.end((error, result) => {
      if (error) {
        reject(error);
      } else {
        resolve(result);
      }
    });
  });
}

async function runPyshacl(dataPath) {
  return new Promise((resolve, reject) => {
    const args = ['-m', 'pyshacl', '-s', shapesPath, '-m', '-i', 'rdfs', '-a', '-f', 'human', dataPath];
    const proc = spawn('python', args, { cwd: repoRoot });

    let stdout = '';
    let stderr = '';

    proc.stdout.on('data', (chunk) => {
      stdout += chunk.toString();
    });

    proc.stderr.on('data', (chunk) => {
      stderr += chunk.toString();
    });

    proc.on('error', (error) => reject(error));

    proc.on('close', (code) => {
      if (stderr) {
        stdout += `\n[stderr]\n${stderr}`;
      }
      resolve({ code, report: stdout.trim() });
    });
  });
}

async function buildZip(jsonldText, turtleText, validationText) {
  return new Promise((resolve, reject) => {
    const archive = archiver('zip', { zlib: { level: 9 } });
    const stream = new PassThrough();
    const chunks = [];

    stream.on('data', (chunk) => chunks.push(chunk));
    stream.on('end', () => resolve(Buffer.concat(chunks)));
    archive.on('error', (error) => reject(error));

    archive.pipe(stream);
    archive.append(jsonldText, { name: 'export.jsonld' });
    archive.append(turtleText, { name: 'export.ttl' });
    archive.append(validationText, { name: 'validation.txt' });

    archive.finalize();
  });
}

async function exportHandler(req, res) {
  const { jsonld: jsonldDoc } = req.body || {};

  if (!jsonldDoc) {
    return res.status(400).send('Missing jsonld document in request body.');
  }

  let tempDir;
  try {
    const turtleText = await jsonldToTurtle(jsonldDoc);
    const jsonldText = JSON.stringify(jsonldDoc, null, 2);

    tempDir = await fs.promises.mkdtemp(path.join(os.tmpdir(), 'hcmo-export-'));
    const dataPath = path.join(tempDir, 'export.ttl');

    await writeFile(dataPath, turtleText, 'utf8');

    const { code, report } = await runPyshacl(dataPath);

    const zipBuffer = await buildZip(jsonldText, turtleText, report);
    const zipFilename = `hcmo-export-${uuidv4()}.zip`;

    res.json({
      conforms: code === 0,
      turtle: turtleText,
      validationReport: report,
      zipBase64: zipBuffer.toString('base64'),
      zipFilename
    });
  } catch (error) {
    console.error('Export error:', error);
    res.status(500).send(`Failed to process export: ${error.message}`);
  } finally {
    if (tempDir) {
      await rm(tempDir, { recursive: true, force: true }).catch(() => undefined);
    }
  }
}

const app = createApp();

const PORT = process.env.PORT || 3000;
if (process.argv[1] && path.resolve(process.argv[1]) === __filename) {
  app.listen(PORT, () => {
    console.log(`HCMO form server running on http://localhost:${PORT}`);
  });
}

export default app;
export { createApp };
