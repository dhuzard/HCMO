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
const fieldTiersPath = path.join(repoRoot, 'docs', 'FIELD-TIERS.md');

const STATUS_ICONS = {
  provided: '\u2713',
  partial: '\u25B3',
  missing: '\u25CB',
  unknown: '?'
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

function toIdentifier(value) {
  return value
    .replace(/`/g, '')
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '_')
    .replace(/^_+|_+$/g, '');
}

function normalizeMarkdownText(text, { collapseWhitespace = true } = {}) {
  if (!text) return '';
  let value = text.trim();
  if (value.startsWith('`') && value.endsWith('`')) {
    value = value.slice(1, -1).trim();
  }
  value = value
    .replace(/\*\*/g, '')
    .replace(/\[(.+?)\]\((.+?)\)/g, '$1');
  return collapseWhitespace ? value.replace(/\s+/g, ' ').trim() : value.trim();
}

function parseMarkdownTable(section) {
  const lines = section.split(/\r?\n/).map((line) => line.trim());
  const tableLines = lines.filter((line) => line.startsWith('|'));
  if (tableLines.length < 2) {
    return [];
  }

  const headers = tableLines[0]
    .split('|')
    .slice(1, -1)
    .map((cell) => normalizeMarkdownText(cell));

  const rows = [];
  for (let i = 2; i < tableLines.length; i += 1) {
    const line = tableLines[i];
    if (!line) continue;
    const cleaned = line.replace(/[-|:\s]/g, '');
    if (!cleaned) continue;
    const cells = line.split('|').slice(1, -1).map((cell) => cell.trim());
    const record = {};
    headers.forEach((header, idx) => {
      record[header] = cells[idx] ?? '';
    });
    rows.push(record);
  }
  return rows;
}

function parseFieldTiersMarkdown(markdown) {
  const tierMatches = [...markdown.matchAll(/##\s+(Mandatory|Recommended|Optional) Fields([\s\S]*?)(?=##\s+|$)/g)];
  return tierMatches.map((match) => {
    const tierName = match[1];
    const section = match[2];
    const rows = parseMarkdownTable(section);
    const tierId = tierName.toLowerCase();
    const fields = rows.map((row) => {
      const rawField = row.Field ?? row['Field'] ?? '';
      const identifier = toIdentifier(rawField || tierName);
      const label = normalizeMarkdownText(rawField, { collapseWhitespace: false }) || identifier;
      return {
        id: identifier,
        tierId,
        tierLabel: tierName,
        label,
        description: normalizeMarkdownText(row.Description ?? ''),
        rationale: normalizeMarkdownText(row.Rationale ?? ''),
        exampleValue: normalizeMarkdownText(row['Example Value'] ?? '', { collapseWhitespace: false }),
        validationNotes: normalizeMarkdownText(row['Validation Notes'] ?? ''),
        downstreamUtility: normalizeMarkdownText(row['Downstream Utility'] ?? '')
      };
    });
    return {
      id: tierId,
      label: `${tierName} Fields`,
      tier: tierName,
      fields
    };
  });
}

async function loadBlueprintInventory() {
  const content = await fs.promises.readFile(fieldTiersPath, 'utf8');
  const tiers = parseFieldTiersMarkdown(content);
  return { tiers };
}

function buildExampleFromTiers(tiers) {
  const minimal = {
    id: 'example-minimal-mandatory',
    label: 'Minimal Mandatory Coverage',
    description: 'Matches docs/EXAMPLES/example-minimal-mandatory.json',
    fields: {}
  };
  const extended = {
    id: 'example-extended-recommended',
    label: 'Extended Mandatory + Recommended Coverage',
    description: 'Matches docs/EXAMPLES/example-extended-recommended.yaml',
    fields: {}
  };

  tiers.forEach((tier) => {
    minimal.fields[tier.id] = {};
    extended.fields[tier.id] = {};

    tier.fields.forEach((field) => {
      if (tier.id === 'mandatory') {
        minimal.fields[tier.id][field.id] = {
          status: 'provided',
          value: field.exampleValue || '',
          notes: 'Covered in the minimal mandatory example payload.'
        };
      } else {
        minimal.fields[tier.id][field.id] = {
          status: 'missing',
          value: '',
          notes: ''
        };
      }

      if (tier.id === 'optional') {
        extended.fields[tier.id][field.id] = {
          status: 'partial',
          value: '',
          notes: 'Optional field – include when available.'
        };
      } else {
        extended.fields[tier.id][field.id] = {
          status: 'provided',
          value: field.exampleValue || '',
          notes: tier.id === 'mandatory'
            ? 'Mandatory field'
            : 'Recommended field covered in extended example.'
        };
      }
    });
  });

  return { examples: [minimal, extended] };
}

async function loadBlueprintExamples() {
  const { tiers } = await loadBlueprintInventory();
  return buildExampleFromTiers(tiers);
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

