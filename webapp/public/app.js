const baseContext = {
  "@context": {
    "@vocab": "https://w3id.org/hcmo/ontology/hcm#",
    "hcm": "https://w3id.org/hcmo/ontology/hcm#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "time": "http://www.w3.org/2006/time#",
    "width": { "@id": "hcm:width", "@type": "xsd:decimal" },
    "length": { "@id": "hcm:length", "@type": "xsd:decimal" },
    "height": { "@id": "hcm:height", "@type": "xsd:decimal" },
    "unit": { "@id": "hcm:unit" },
    "durationHours": { "@id": "hcm:durationHours", "@type": "xsd:decimal" },
    "isExtendable": { "@id": "hcm:isExtendable", "@type": "xsd:boolean" },
    "followsProtocol": "hcm:followsProtocol",
    "protocolReference": "hcm:protocolReference",
    "hasEnclosure": "hcm:hasEnclosure",
    "hasHardware": "hcm:hasHardware",
    "hasSoftware": "hcm:hasSoftware",
    "producedBy": "hcm:producedBy",
    "collectsInfoOn": "hcm:collectsInfoOn",
    "livesIn": "hcm:livesIn",
    "requiresToThrive": "hcm:requiresToThrive",
    "provides": "hcm:provides",
    "displays": "hcm:displays",
    "isDisplayedInside": "hcm:isDisplayedInside",
    "hasCircadianRhythm": "hcm:hasCircadianRhythm",
    "extendsEnoughToCapture": "hcm:extendsEnoughToCapture",
    "hasProperty": "hcm:hasProperty",
    "captures": "hcm:captures",
    "elicits": "hcm:elicits",
    "hasSensor": "hcm:hasSensor",
    "hasActuator": "hcm:hasActuator",
    "communicatesWith": "hcm:communicatesWith",
    "hasDimensions": "hcm:hasDimensions",
    "hasFood": "hcm:hasFood",
    "hasWater": "hcm:hasWater",
    "hasSocialContacts": "hcm:hasSocialContacts",
    "hasSafetyFromThreat": "hcm:hasSafetyFromThreat",
    "hasEnvironmentalEnrichment": "hcm:hasEnvironmentalEnrichment",
    "hasBeginning": { "@id": "time:hasBeginning", "@type": "@id" },
    "hasEnd": { "@id": "time:hasEnd", "@type": "@id" },
    "inXSDDateTime": { "@id": "time:inXSDDateTime", "@type": "xsd:dateTime" }
  }
};
const form = document.querySelector('#hcmo-form');
const resultsSection = document.querySelector('#results');
const statusLine = document.querySelector('#status-line');
const jsonldOutput = document.querySelector('#jsonld-output');
const turtleOutput = document.querySelector('#turtle-output');
const validationOutput = document.querySelector('#validation-output');
const downloadJsonldBtn = document.querySelector('#download-jsonld');
const downloadTurtleBtn = document.querySelector('#download-turtle');
const downloadZipBtn = document.querySelector('#download-zip');

const sensorList = document.querySelector('[data-sensor-list]');
const actuatorList = document.querySelector('[data-actuator-list]');
const addSensorButton = document.querySelector('#add-sensor');
const addActuatorButton = document.querySelector('#add-actuator');

const tabButtons = document.querySelectorAll('.tab-button');
const panels = document.querySelectorAll('.panel');
const blueprintPanel = document.querySelector('#blueprint-panel');
const blueprintFieldsContainer = document.querySelector('#blueprint-fields');
const blueprintSummaryContainer = document.querySelector('#blueprint-summary');
const blueprintExampleSelect = document.querySelector('#blueprint-example-select');
const blueprintExampleDescription = document.querySelector('#blueprint-example-description');
const blueprintLoading = document.querySelector('#blueprint-loading');
const blueprintApplyButton = document.querySelector('#blueprint-apply-example');
const blueprintResetButton = document.querySelector('#blueprint-reset');

const DEFAULT_STATUS_ICONS = {
  provided: '\u2713',
  partial: '\u25B3',
  missing: '\u25CB',
  unknown: '?'
};

const blueprintState = {
  inventory: null,
  examples: [],
  statusIcons: { ...DEFAULT_STATUS_ICONS },
  fieldMap: new Map(),
  tierSummaries: new Map(),
  initialised: false
};

const titleCase = (value) => value.charAt(0).toUpperCase() + value.slice(1);

function formatTierLabel(id) {
  return id.replace(/_/g, ' ').replace(/\b\w/g, (char) => char.toUpperCase());
}
function showPanel(panelId) {
  panels.forEach((panel) => {
    const matches = panel.dataset.panel === panelId;
    panel.classList.toggle('panel--active', matches);
    panel.toggleAttribute('hidden', !matches);
  });
}

tabButtons.forEach((button) => {
  button.addEventListener('click', () => {
    const target = button.dataset.panelTarget;
    tabButtons.forEach((btn) => btn.classList.toggle('tab-button--active', btn === button));
    showPanel(target);
    if (target === 'blueprint-panel' && blueprintPanel && !blueprintState.initialised) {
      initBlueprintPanel();
    }
  });
});

async function fetchJson(url) {
  const response = await fetch(url);
  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `Request failed (${response.status})`);
  }
  return response.json();
}

function ensureTrailing(base) {
  if (!base) return base;
  return /[\/#]$/.test(base) ? base : `${base}/`;
}
function buildRow(container, prefix, defaults = {}) {
  const wrapper = document.createElement('div');
  wrapper.className = 'item-row';
  wrapper.innerHTML = `
    <label>${titleCase(prefix)} ID
      <input type="text" name="${prefix}Id[]" value="${defaults.id ?? ''}" required>
    </label>
    <label>${titleCase(prefix)} Label
      <input type="text" name="${prefix}Label[]" value="${defaults.label ?? ''}">
    </label>
    <button type="button" class="remove-item">Remove</button>
  `;

  wrapper.querySelector('.remove-item').addEventListener('click', () => {
    wrapper.remove();
    updateBlueprintSummary();
  });

  container.appendChild(wrapper);
}

function collectRepeated(container, prefix) {
  const entries = [];
  container.querySelectorAll('.item-row').forEach((row) => {
    const idInput = row.querySelector(`input[name="${prefix}Id[]"]`);
    const labelInput = row.querySelector(`input[name="${prefix}Label[]"]`);
    const id = idInput?.value.trim();
    if (id) {
      entries.push({ id, label: labelInput?.value.trim() || '' });
    }
  });
  return entries;
}

function toNumber(value) {
  if (value === undefined || value === null || value === '') return undefined;
  const number = Number(value);
  return Number.isNaN(number) ? undefined : number;
}

function toBoolean(value) {
  if (typeof value === 'boolean') return value;
  if (typeof value === 'string') {
    return value.toLowerCase() === 'true';
  }
  return Boolean(value);
}

function dateTimeToIso(value) {
  if (!value) return undefined;
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return undefined;
  return date.toISOString();
}
function gatherFormData() {
  const formData = new FormData(form);
  const sensors = collectRepeated(sensorList, 'sensor');
  const actuators = collectRepeated(actuatorList, 'actuator');

  const ingestedAtIso = dateTimeToIso(formData.get('ingestedAt'));
  const sessionStartIso = dateTimeToIso(formData.get('sessionStart'));
  const sessionEndIso = dateTimeToIso(formData.get('sessionEnd'));

  return {
    baseIri: formData.get('baseIri').trim(),
    systemId: formData.get('systemId').trim(),
    systemLabel: formData.get('systemLabel').trim(),
    hardwareId: formData.get('hardwareId').trim(),
    hardwareLabel: formData.get('hardwareLabel').trim(),
    softwareId: formData.get('softwareId').trim(),
    softwareLabel: formData.get('softwareLabel').trim(),
    supplierId: formData.get('supplierId').trim(),
    supplierLabel: formData.get('supplierLabel').trim(),
    protocolId: formData.get('protocolId').trim(),
    protocolLabel: formData.get('protocolLabel').trim(),
    enclosureId: formData.get('enclosureId').trim(),
    enclosureLabel: formData.get('enclosureLabel').trim(),
    width: formData.get('width'),
    length: formData.get('length'),
    height: formData.get('height'),
    unit: formData.get('unit').trim(),
    needs: {
      food: formData.get('needFood') === 'on',
      water: formData.get('needWater') === 'on',
      social: formData.get('needSocial') === 'on',
      safety: formData.get('needSafety') === 'on',
      enrichment: formData.get('needEnrichment') === 'on'
    },
    animalId: formData.get('animalId').trim(),
    animalLabel: formData.get('animalLabel').trim(),
    behaviorId: formData.get('behaviorId').trim(),
    behaviorLabel: formData.get('behaviorLabel').trim(),
    circadianLabel: formData.get('circadianLabel').trim(),
    operatorContact: formData.get('operatorContact').trim(),
    dataProductLinks: formData.get('dataProductLinks').trim(),
    intervalId: formData.get('intervalId').trim(),
    intervalLabel: formData.get('intervalLabel').trim(),
    durationHours: formData.get('durationHours'),
    isExtendable: formData.get('isExtendable'),
    limitedInteractionLabel: formData.get('limitedInteractionLabel').trim(),
    sessionInterval: {
      start: sessionStartIso,
      end: sessionEndIso
    },
    sensors,
    actuators,
    ingestedAt: ingestedAtIso
  };
}
function buildGraph(data) {
  const {
    baseIri,
    systemId,
    systemLabel,
    hardwareId,
    hardwareLabel,
    softwareId,
    softwareLabel,
    supplierId,
    supplierLabel,
    protocolId,
    protocolLabel,
    enclosureId,
    enclosureLabel,
    width,
    length,
    height,
    unit,
    needs,
    animalId,
    animalLabel,
    behaviorId,
    behaviorLabel,
    circadianLabel,
    operatorContact,
    dataProductLinks,
    intervalId,
    intervalLabel,
    durationHours,
    isExtendable,
    limitedInteractionLabel,
    sessionInterval,
    sensors,
    actuators,
    ingestedAt
  } = data;

  const base = ensureTrailing(baseIri);

  const systemIri = `${base}${systemId}`;
  const hardwareIri = `${base}${hardwareId}`;
  const softwareIri = `${base}${softwareId}`;
  const supplierIri = `${base}${supplierId}`;
  const protocolIri = `${base}${protocolId}`;
  const enclosureIri = `${base}${enclosureId}`;
  const needsIri = `${base}${enclosureId}_Needs`;
  const dimensionsIri = `${base}${enclosureId}_Dims`;
  const operatorContactIri = operatorContact ? `${base}${systemId}_Contact` : undefined;
  const dataProductsIri = dataProductLinks ? `${base}${systemId}_DataProducts` : undefined;
  const animalIri = `${base}${animalId}`;
  const behaviorIri = `${base}${behaviorId}`;
  const circadianIri = `${base}${behaviorId}_CR`;
  const intervalIri = `${base}${intervalId}`;
  const limitedInteractionIri = `${base}${intervalId}_LHI`;
  const intervalStartIri = sessionInterval.start ? `${intervalIri}_Start` : undefined;
  const intervalEndIri = sessionInterval.end ? `${intervalIri}_End` : undefined;

  const graph = [];

  const optionalLabel = (label) => (label ? { label } : {});

  const systemNode = {
    '@id': systemIri,
    '@type': 'System',
    ...optionalLabel(systemLabel),
    hasEnclosure: { '@id': enclosureIri },
    hasHardware: { '@id': hardwareIri },
    hasSoftware: { '@id': softwareIri },
    producedBy: { '@id': supplierIri },
    collectsInfoOn: { '@id': animalIri },
    followsProtocol: { '@id': protocolIri },
    hasSensor: sensors.map((sensor) => ({ '@id': `${base}${sensor.id}` })),
    hasActuator: actuators.map((actuator) => ({ '@id': `${base}${actuator.id}` }))
  };

  if (ingestedAt) {
    systemNode.ingestedAt = { '@value': ingestedAt, '@type': 'xsd:dateTime' };
  }

  graph.push(systemNode);
  graph.push({
    '@id': protocolIri,
    '@type': 'Protocol',
    ...optionalLabel(protocolLabel),
    protocolReference: protocolId
  });

  graph.push({
    '@id': hardwareIri,
    '@type': 'Hardware',
    ...optionalLabel(hardwareLabel),
    communicatesWith: { '@id': softwareIri }
  });

  graph.push({
    '@id': softwareIri,
    '@type': 'Software',
    ...optionalLabel(softwareLabel)
  });

  const supplierNode = {
    '@id': supplierIri,
    '@type': 'Supplier',
    ...optionalLabel(supplierLabel)
  };
  if (operatorContactIri) {
    supplierNode.hasProperty = { '@id': operatorContactIri };
  }
  graph.push(supplierNode);

  graph.push({
    '@id': needsIri,
    '@type': 'NeedsSequence',
    hasFood: needs.food,
    hasWater: needs.water,
    hasSocialContacts: needs.social,
    hasSafetyFromThreat: needs.safety,
    hasEnvironmentalEnrichment: needs.enrichment
  });

  graph.push({
    '@id': dimensionsIri,
    '@type': 'Dimensions',
    width: toNumber(width),
    length: toNumber(length),
    height: toNumber(height),
    unit
  });

  const enclosureNode = {
    '@id': enclosureIri,
    '@type': 'Enclosure',
    ...optionalLabel(enclosureLabel),
    provides: { '@id': needsIri },
    hasDimensions: { '@id': dimensionsIri }
  };
  if (dataProductsIri) {
    enclosureNode.hasProperty = { '@id': dataProductsIri };
  }
  graph.push(enclosureNode);

  graph.push({
    '@id': animalIri,
    '@type': 'Animal',
    ...optionalLabel(animalLabel),
    livesIn: { '@id': enclosureIri },
    requiresToThrive: { '@id': needsIri },
    displays: { '@id': behaviorIri }
  });

  graph.push({
    '@id': behaviorIri,
    '@type': 'BehaviorAndPhysiology',
    ...optionalLabel(behaviorLabel),
    isDisplayedInside: { '@id': enclosureIri },
    hasCircadianRhythm: { '@id': circadianIri },
    extendsEnoughToCapture: { '@id': intervalIri }
  });

  graph.push({
    '@id': circadianIri,
    '@type': 'CircadianRhythm',
    ...optionalLabel(circadianLabel)
  });

  const intervalNode = {
    '@id': intervalIri,
    '@type': 'TimeInterval',
    ...optionalLabel(intervalLabel),
    durationHours: toNumber(durationHours),
    isExtendable: toBoolean(isExtendable),
    hasProperty: { '@id': limitedInteractionIri }
  };

  if (intervalStartIri) {
    intervalNode.hasBeginning = { '@id': intervalStartIri };
    graph.push({
      '@id': intervalStartIri,
      '@type': 'time:Instant',
      inXSDDateTime: { '@value': sessionInterval.start, '@type': 'xsd:dateTime' }
    });
  }

  if (intervalEndIri) {
    intervalNode.hasEnd = { '@id': intervalEndIri };
    graph.push({
      '@id': intervalEndIri,
      '@type': 'time:Instant',
      inXSDDateTime: { '@value': sessionInterval.end, '@type': 'xsd:dateTime' }
    });
  }

  graph.push(intervalNode);

  graph.push({
    '@id': limitedInteractionIri,
    '@type': 'LimitedInteractionWithHumans',
    ...optionalLabel(limitedInteractionLabel)
  });

  sensors.forEach((sensor) => {
    graph.push({
      '@id': `${base}${sensor.id}`,
      '@type': 'Sensor',
      ...optionalLabel(sensor.label),
      captures: { '@id': behaviorIri }
    });
  });

  actuators.forEach((actuator) => {
    graph.push({
      '@id': `${base}${actuator.id}`,
      '@type': 'Actuator',
      ...optionalLabel(actuator.label),
      elicits: { '@id': behaviorIri }
    });
  });

  if (operatorContactIri && operatorContact) {
    graph.push({
      '@id': operatorContactIri,
      '@type': 'ContactPoint',
      label: operatorContact
    });
  }

  if (dataProductsIri && dataProductLinks) {
    graph.push({
      '@id': dataProductsIri,
      '@type': 'DataProduct',
      label: dataProductLinks
    });
  }

  return { graph, base };
}
function buildJsonLdDocument(data) {
  const { graph, base } = buildGraph(data);

  const contextArray = [baseContext['@context'], {
    label: 'http://www.w3.org/2000/01/rdf-schema#label'
  }];

  if (data.ingestedAt) {
    contextArray.push({
      ingestedAt: { '@id': `${base}ingestedAt`, '@type': 'xsd:dateTime' }
    });
  }

  return {
    '@context': contextArray,
    '@graph': graph
  };
}

function saveBlob(data, mime, filename, isBase64 = false) {
  const blob = isBase64
    ? new Blob([Uint8Array.from(atob(data), (c) => c.charCodeAt(0))], { type: mime })
    : new Blob([data], { type: mime });

  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

function enableDownloads(jsonldText, turtleText, zipBuffer, zipFilename) {
  downloadJsonldBtn.disabled = false;
  downloadJsonldBtn.onclick = () => saveBlob(jsonldText, 'application/ld+json', 'hcmo-export.jsonld');

  downloadTurtleBtn.disabled = false;
  downloadTurtleBtn.onclick = () => saveBlob(turtleText, 'text/turtle', 'hcmo-export.ttl');

  if (zipBuffer) {
    downloadZipBtn.disabled = false;
    downloadZipBtn.onclick = () => saveBlob(zipBuffer, 'application/zip', zipFilename || 'hcmo-package.zip', true);
  }
}

function normalizeCoverageStatus(raw) {
  if (!raw) return 'unknown';
  const value = String(raw).toLowerCase();
  if (value.includes('provided') || String(raw).includes(DEFAULT_STATUS_ICONS.provided)) return 'provided';
  if (value.includes('partial') || String(raw).includes(DEFAULT_STATUS_ICONS.partial)) return 'partial';
  if (value.includes('missing') || String(raw).includes(DEFAULT_STATUS_ICONS.missing)) return 'missing';
  if (value.includes('unknown')) return 'unknown';
  return value || 'unknown';
}

function decodeIcon(value) {
  if (!value) return DEFAULT_STATUS_ICONS.unknown;
  return value.replace(/\\u([0-9a-f]{4})/gi, (_, code) => String.fromCharCode(parseInt(code, 16)));
}

function statusIcon(status) {
  const raw = blueprintState.statusIcons[status] ?? DEFAULT_STATUS_ICONS[status] ?? DEFAULT_STATUS_ICONS.unknown;
  return decodeIcon(raw);
}

function createStats() {
  return {
    provided: 0,
    partial: 0,
    missing: 0,
    unknown: 0,
    total: 0,
    mandatoryTotal: 0,
    mandatoryProvided: 0
  };
}

function setFieldStatus(fieldState, status, options = {}) {
  const normalized = normalizeCoverageStatus(status);
  fieldState.status = normalized;
  if (typeof options.manual === 'boolean') {
    fieldState.manualStatus = options.manual;
  }
  const select = fieldState.elements.statusSelect;
  if (select && select.value !== normalized) {
    select.value = normalized;
  }
  const iconChar = statusIcon(normalized);
  fieldState.elements.statusIcon.textContent = iconChar;
  fieldState.elements.statusIcon.title = `${titleCase(normalized)} status`;
}
function updateTierSummary(tierId, stats) {
  const summary = blueprintState.tierSummaries.get(tierId);
  if (!summary) return;
  const mandatoryNote = summary.mandatoryTotal
    ? ` · Mandatory ${stats.mandatoryProvided}/${summary.mandatoryTotal}`
    : '';
  summary.element.textContent = `${statusIcon('provided')} ${stats.provided} · ${statusIcon('partial')} ${stats.partial} · ${statusIcon('missing')} ${stats.missing}${mandatoryNote}`;
}

function updateBlueprintSummary() {
  if (!blueprintSummaryContainer) return;
  if (!blueprintState.fieldMap.size) {
    blueprintSummaryContainer.innerHTML = '<p class="blueprint-description">Blueprint inventory not loaded yet.</p>';
    return;
  }

  const tierStats = new Map();
  const totals = createStats();

  blueprintState.fieldMap.forEach((fieldState) => {
    const stats = tierStats.get(fieldState.tierId) ?? createStats();
    if (stats[fieldState.status] !== undefined) {
      stats[fieldState.status] += 1;
    }
    stats.total += 1;
    if (fieldState.field.tierId === 'mandatory') {
      stats.mandatoryTotal += 1;
      if (fieldState.status === 'provided') {
        stats.mandatoryProvided += 1;
      }
    }
    tierStats.set(fieldState.tierId, stats);

    if (totals[fieldState.status] !== undefined) {
      totals[fieldState.status] += 1;
    }
    totals.total += 1;
    if (fieldState.field.tierId === 'mandatory') {
      totals.mandatoryTotal += 1;
      if (fieldState.status === 'provided') {
        totals.mandatoryProvided += 1;
      }
    }
  });

  blueprintSummaryContainer.innerHTML = '';

  const weightedCoverage = totals.total
    ? (((totals.provided + 0.5 * totals.partial) / totals.total) * 100).toFixed(1)
    : '0.0';
  const mandatoryCoverage = totals.mandatoryTotal
    ? ((totals.mandatoryProvided / totals.mandatoryTotal) * 100).toFixed(1)
    : '0.0';

  const overallCard = document.createElement('div');
  overallCard.className = 'blueprint-summary-card';
  overallCard.innerHTML = `
    <h4>Overall</h4>
    <div class="blueprint-summary-metrics">
      <span class="status-chip status-chip--provided">${statusIcon('provided')} ${totals.provided}</span>
      <span class="status-chip status-chip--partial">${statusIcon('partial')} ${totals.partial}</span>
      <span class="status-chip status-chip--missing">${statusIcon('missing')} ${totals.missing}</span>
    </div>
    <p class="blueprint-description">Weighted coverage ${weightedCoverage}% · Mandatory provided ${mandatoryCoverage}%</p>
  `;
  blueprintSummaryContainer.appendChild(overallCard);

  const tiersInOrder = blueprintState.inventory?.tiers ?? [];
  tiersInOrder.forEach((tier) => {
    const stats = tierStats.get(tier.id) ?? createStats();
    const mandatoryProvided = stats.mandatoryProvided || 0;
    const mandatoryTotal = stats.mandatoryTotal || 0;
    const mandatoryPercent = mandatoryTotal
      ? ((mandatoryProvided / mandatoryTotal) * 100).toFixed(1)
      : '0.0';

    const tierCard = document.createElement('div');
    tierCard.className = 'blueprint-summary-card';
    tierCard.innerHTML = `
      <h4>${tier.tier}</h4>
      <div class="blueprint-summary-metrics">
        <span class="status-chip status-chip--provided">${statusIcon('provided')} ${stats.provided}</span>
        <span class="status-chip status-chip--partial">${statusIcon('partial')} ${stats.partial}</span>
        <span class="status-chip status-chip--missing">${statusIcon('missing')} ${stats.missing}</span>
      </div>
      <p class="blueprint-description">Mandatory provided ${mandatoryProvided}/${mandatoryTotal} (${mandatoryPercent}%)</p>
    `;
    blueprintSummaryContainer.appendChild(tierCard);

    updateTierSummary(tier.id, stats);
  });
}
function createBlueprintFieldRow(tierId, field) {
  const row = document.createElement('tr');
  const fieldKey = `${tierId}:${field.id}`;

  const titleCell = document.createElement('th');
  titleCell.scope = 'row';
  const title = document.createElement('div');
  title.className = 'blueprint-field__title';
  title.textContent = field.label;
  const description = document.createElement('div');
  description.className = 'blueprint-field__meta';
  description.textContent = field.description || 'Description pending';
  titleCell.appendChild(title);
  titleCell.appendChild(description);

  const classificationCell = document.createElement('td');
  const badge = document.createElement('span');
  badge.className = `badge badge--${field.tierId}`;
  badge.textContent = field.tierLabel;
  classificationCell.appendChild(badge);

  const valueCell = document.createElement('td');
  const textarea = document.createElement('textarea');
  textarea.className = 'blueprint-input';
  textarea.placeholder = field.exampleValue ? `Example: ${field.exampleValue}` : 'Enter mapping value or notes';
  valueCell.appendChild(textarea);

  const metaList = document.createElement('dl');
  metaList.className = 'blueprint-field__details';
  metaList.innerHTML = `
    <dt>Rationale</dt><dd>${field.rationale || '—'}</dd>
    <dt>Validation</dt><dd>${field.validationNotes || '—'}</dd>
    <dt>Downstream</dt><dd>${field.downstreamUtility || '—'}</dd>
  `;
  valueCell.appendChild(metaList);

  const notes = document.createElement('div');
  notes.className = 'blueprint-notes';
  notes.hidden = true;
  valueCell.appendChild(notes);

  const statusCell = document.createElement('td');
  const statusControl = document.createElement('div');
  statusControl.className = 'status-control';
  const icon = document.createElement('span');
  icon.className = 'status-icon';
  icon.textContent = statusIcon('missing');
  icon.title = 'Missing status';
  const select = document.createElement('select');
  select.className = 'blueprint-status';
  ['provided', 'partial', 'missing', 'unknown'].forEach((status) => {
    const option = document.createElement('option');
    option.value = status;
    option.textContent = `${statusIcon(status)} ${titleCase(status)}`;
    select.appendChild(option);
  });
  select.value = 'missing';
  statusControl.appendChild(icon);
  statusControl.appendChild(select);
  statusCell.appendChild(statusControl);

  row.appendChild(titleCell);
  row.appendChild(classificationCell);
  row.appendChild(valueCell);
  row.appendChild(statusCell);

  const state = {
    tierId,
    field,
    status: 'missing',
    value: '',
    manualStatus: false,
    elements: {
      textarea,
      statusSelect: select,
      statusIcon: icon,
      notes
    }
  };

  blueprintState.fieldMap.set(fieldKey, state);

  textarea.addEventListener('input', () => {
    state.value = textarea.value.trim();
    if (!state.manualStatus) {
      const autoStatus = state.value ? 'provided' : 'missing';
      setFieldStatus(state, autoStatus, { manual: false });
    } else if (!state.value && state.status === 'provided') {
      setFieldStatus(state, 'missing', { manual: true });
    }
    updateBlueprintSummary();
  });

  select.addEventListener('change', () => {
    state.manualStatus = true;
    setFieldStatus(state, select.value, { manual: true });
    updateBlueprintSummary();
  });

  return row;
}

function buildBlueprintUI(tiers) {
  if (!blueprintFieldsContainer) return;
  blueprintFieldsContainer.innerHTML = '';
  blueprintState.fieldMap.clear();
  blueprintState.tierSummaries.clear();

  if (!tiers.length) {
    blueprintFieldsContainer.innerHTML = '<p class="blueprint-description">No blueprint tiers available.</p>';
    return;
  }

  tiers.forEach((tier) => {
    const card = document.createElement('section');
    card.className = 'card blueprint-tier';

    const header = document.createElement('div');
    header.className = 'blueprint-tier__header';
    const title = document.createElement('h3');
    title.className = 'blueprint-tier__title';
    title.textContent = tier.label;
    const summary = document.createElement('div');
    summary.className = 'blueprint-tier__summary';
    header.appendChild(title);
    header.appendChild(summary);

    const table = document.createElement('table');
    table.className = 'blueprint-table';
    const tbody = document.createElement('tbody');
    (tier.fields || []).forEach((field) => {
      const row = createBlueprintFieldRow(tier.id, field);
      tbody.appendChild(row);
    });
    table.appendChild(tbody);

    card.appendChild(header);
    card.appendChild(table);
    blueprintFieldsContainer.appendChild(card);

    const mandatoryTotal = (tier.fields || []).filter((field) => field.tierId === 'mandatory').length;
    blueprintState.tierSummaries.set(tier.id, {
      element: summary,
      mandatoryTotal
    });
  });

  updateBlueprintSummary();
}
function applyBlueprintExample(exampleOrId) {
  const example = typeof exampleOrId === 'string'
    ? blueprintState.examples.find((item) => item.id === exampleOrId)
    : exampleOrId;
  if (!example) return;

  if (blueprintExampleSelect && blueprintExampleSelect.value !== example.id) {
    blueprintExampleSelect.value = example.id;
  }

  blueprintState.fieldMap.forEach((fieldState) => {
    const entry = example.fields?.[fieldState.tierId]?.[fieldState.field.id];
    const value = entry?.value ?? '';
    const note = entry?.notes ?? '';

    fieldState.value = value;
    fieldState.manualStatus = Boolean(entry?.status);
    fieldState.elements.textarea.value = value;
    if (note) {
      fieldState.elements.notes.textContent = note;
      fieldState.elements.notes.hidden = false;
    } else {
      fieldState.elements.notes.textContent = '';
      fieldState.elements.notes.hidden = true;
    }

    const status = entry?.status ?? (value ? 'provided' : 'missing');
    setFieldStatus(fieldState, status, { manual: Boolean(entry?.status) });
  });

  if (blueprintExampleDescription) {
    blueprintExampleDescription.textContent = example.description || '';
  }

  updateBlueprintSummary();
}

function populateBlueprintExamples(examples) {
  if (!blueprintExampleSelect) return;
  blueprintExampleSelect.innerHTML = '';
  const placeholder = document.createElement('option');
  placeholder.value = '';
  placeholder.textContent = 'Select example…';
  blueprintExampleSelect.appendChild(placeholder);

  examples.forEach((example) => {
    const option = document.createElement('option');
    option.value = example.id;
    option.textContent = example.label;
    blueprintExampleSelect.appendChild(option);
  });

  if (examples.length) {
    applyBlueprintExample(examples[0]);
  } else if (blueprintExampleDescription) {
    blueprintExampleDescription.textContent = 'No predefined examples available yet.';
  }
}

function resetBlueprintFields() {
  blueprintState.fieldMap.forEach((fieldState) => {
    fieldState.value = '';
    fieldState.manualStatus = false;
    fieldState.elements.textarea.value = '';
    fieldState.elements.notes.textContent = '';
    fieldState.elements.notes.hidden = true;
    setFieldStatus(fieldState, 'missing', { manual: false });
  });

  if (blueprintExampleSelect) {
    blueprintExampleSelect.value = '';
  }
  if (blueprintExampleDescription) {
    blueprintExampleDescription.textContent = 'Fields cleared. Enter values to compute coverage.';
  }

  updateBlueprintSummary();
}

async function initBlueprintPanel() {
  if (!blueprintPanel || blueprintState.initialised) return;

  blueprintState.initialised = true;

  if (blueprintLoading) {
    blueprintLoading.textContent = 'Loading blueprint metadata...';
    blueprintLoading.hidden = false;
    blueprintLoading.classList.remove('status--error');
  }

  try {
    const [inventory, examples] = await Promise.all([
      fetchJson('/api/blueprint/inventory'),
      fetchJson('/api/blueprint/examples')
    ]);

    blueprintState.inventory = inventory;
    blueprintState.statusIcons = { ...DEFAULT_STATUS_ICONS, ...(inventory.statusIcons || {}) };
    blueprintState.examples = examples.examples || [];

    buildBlueprintUI(inventory.tiers || []);
    populateBlueprintExamples(blueprintState.examples);

    if (blueprintLoading) {
      blueprintLoading.textContent = 'Loaded blueprint tiers. Load an example or enter values to update coverage.';
    }
  } catch (error) {
    if (blueprintLoading) {
      blueprintLoading.textContent = `Failed to load blueprint metadata: ${error.message}`;
      blueprintLoading.classList.add('status--error');
    }
  }
}
async function handleSubmit(event) {
  event.preventDefault();
  statusLine.classList.remove('status--error');
  statusLine.textContent = 'Building payload...';

  const data = gatherFormData();

  if (!data.sensors.length) {
    statusLine.textContent = 'Add at least one sensor.';
    statusLine.classList.add('status--error');
    return;
  }
  if (!data.actuators.length) {
    statusLine.textContent = 'Add at least one actuator.';
    statusLine.classList.add('status--error');
    return;
  }
  if (!data.sessionInterval.start || !data.sessionInterval.end) {
    statusLine.textContent = 'Provide start and end timestamps for the session interval.';
    statusLine.classList.add('status--error');
    return;
  }
  if (new Date(data.sessionInterval.start) >= new Date(data.sessionInterval.end)) {
    statusLine.textContent = 'Session end must be later than the start timestamp.';
    statusLine.classList.add('status--error');
    return;
  }

  const jsonldDocument = buildJsonLdDocument(data);
  const jsonldText = JSON.stringify(jsonldDocument, null, 2);

  statusLine.textContent = 'Submitting for validation...';

  try {
    const response = await fetch('/api/export', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ jsonld: jsonldDocument })
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(errorText || 'Server error');
    }

    const result = await response.json();

    resultsSection.hidden = false;
    jsonldOutput.value = jsonldText;
    turtleOutput.value = result.turtle;
    validationOutput.value = result.validationReport;

    statusLine.textContent = result.conforms ? 'Validation succeeded (Conforms).' : 'Validation completed with issues.';
    if (!result.conforms) {
      statusLine.classList.add('status--error');
    }

    enableDownloads(jsonldText, result.turtle, result.zipBase64, result.zipFilename);
  } catch (error) {
    resultsSection.hidden = false;
    statusLine.textContent = `Error: ${error.message}`;
    statusLine.classList.add('status--error');
    jsonldOutput.value = jsonldText;
    turtleOutput.value = '';
    validationOutput.value = '';
    downloadJsonldBtn.disabled = true;
    downloadTurtleBtn.disabled = true;
    downloadZipBtn.disabled = true;
  }
}

form.addEventListener('submit', handleSubmit);
addSensorButton.addEventListener('click', () => buildRow(sensorList, 'sensor'));
addActuatorButton.addEventListener('click', () => buildRow(actuatorList, 'actuator'));

// Seed defaults
buildRow(sensorList, 'sensor', { id: 'IR_Sensor_1', label: 'IR beam sensor (left wall)' });
buildRow(actuatorList, 'actuator', { id: 'Feeder_1', label: 'Feeder (pellet dispenser)' });

if (blueprintApplyButton) {
  blueprintApplyButton.addEventListener('click', () => {
    const selected = blueprintExampleSelect?.value;
    if (selected) {
      applyBlueprintExample(selected);
    }
  });
}

if (blueprintResetButton) {
  blueprintResetButton.addEventListener('click', () => {
    resetBlueprintFields();
  });
}

if (blueprintExampleSelect) {
  blueprintExampleSelect.addEventListener('change', () => {
    const selected = blueprintExampleSelect.value;
    const example = blueprintState.examples.find((item) => item.id === selected);
    if (blueprintExampleDescription) {
      blueprintExampleDescription.textContent = example?.description ?? '';
    }
  });
}

showPanel('export-panel');

if (blueprintPanel) {
  initBlueprintPanel();
}










