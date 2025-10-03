import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import { createApp } from '../server.js';

async function withServer(fn) {
  const app = createApp();
  const server = app.listen(0);
  try {
    await new Promise((resolve, reject) => {
      server.on('listening', resolve);
      server.on('error', reject);
    });
    await fn(server);
  } finally {
    await new Promise((resolve) => server.close(resolve));
  }
}

test('blueprint inventory exposes tiers and fields from FIELD-TIERS.md', async () => {
  await withServer(async (server) => {
    const { port } = server.address();
    const response = await fetch(`http://127.0.0.1:${port}/api/blueprint/inventory`);
    assert.equal(response.status, 200);
    const payload = await response.json();

    assert.ok(Array.isArray(payload.tiers), 'tiers should be an array');
    assert.equal(payload.tiers.length, 3, 'expected mandatory/recommended/optional tiers');
    payload.tiers.forEach((tier) => {
      assert.ok(Array.isArray(tier.fields), `tier ${tier.id} should have fields`);
      assert.ok(tier.fields.length > 0, `tier ${tier.id} should not be empty`);
      tier.fields.forEach((field) => {
        assert.ok(field.id, 'field id should be present');
        assert.ok(field.label, 'field label should be present');
        assert.equal(field.tierId, tier.id, 'field tier should align with parent');
      });
    });
  });
});

test('blueprint examples align with tier structure', async () => {
  await withServer(async (server) => {
    const { port } = server.address();
    const response = await fetch(`http://127.0.0.1:${port}/api/blueprint/examples`);
    assert.equal(response.status, 200);
    const payload = await response.json();

    assert.ok(Array.isArray(payload.examples), 'examples should be an array');
    const minimal = payload.examples.find((example) => example.id === 'example-minimal-mandatory');
    const extended = payload.examples.find((example) => example.id === 'example-extended-recommended');
    assert.ok(minimal, 'expected minimal mandatory example');
    assert.ok(extended, 'expected extended example');

    Object.entries(minimal.fields).forEach(([tierId, fields]) => {
      Object.entries(fields).forEach(([fieldId, entry]) => {
        if (tierId === 'mandatory') {
          assert.equal(entry.status, 'provided', `mandatory field ${fieldId} should be provided in minimal example`);
        } else {
          assert.equal(entry.status, 'missing', `non-mandatory field ${fieldId} should be missing in minimal example`);
        }
      });
    });

    Object.entries(extended.fields).forEach(([tierId, fields]) => {
      Object.entries(fields).forEach(([fieldId, entry]) => {
        if (tierId === 'optional') {
          assert.equal(entry.status, 'partial', `optional field ${fieldId} should be partial in extended example`);
        } else {
          assert.equal(entry.status, 'provided', `field ${fieldId} should be provided in extended example`);
        }
      });
    });
  });
});

test('ethics notice remains visible in public/index.html', async () => {
  const html = await fs.readFile(new URL('../public/index.html', import.meta.url), 'utf8');
  assert.match(html, /placeholder <strong>\(O\)<\/strong>/, 'ethics placeholder should be referenced in the UI');
});
