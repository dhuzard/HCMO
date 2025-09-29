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

function createApp() {
  const app = express();
  app.use(express.json({ limit: '1mb' }));
  app.use(express.static(publicDir));

  app.post('/api/export', exportHandler);
  return app;
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