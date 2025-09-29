const baseContext = {
  "@context": {
    "@vocab": "https://w3id.org/hcmo/ontology/hcm#",
    "hcm": "https://w3id.org/hcmo/ontology/hcm#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "width": { "@id": "hcm:width", "@type": "xsd:decimal" },
    "length": { "@id": "hcm:length", "@type": "xsd:decimal" },
    "height": { "@id": "hcm:height", "@type": "xsd:decimal" },
    "unit":   { "@id": "hcm:unit" },
    "durationHours": { "@id": "hcm:durationHours", "@type": "xsd:decimal" },
    "isExtendable":  { "@id": "hcm:isExtendable",  "@type": "xsd:boolean" },
    "hasEnclosure":  "hcm:hasEnclosure",
    "hasHardware":   "hcm:hasHardware",
    "hasSoftware":   "hcm:hasSoftware",
    "producedBy":    "hcm:producedBy",
    "collectsInfoOn":"hcm:collectsInfoOn",
    "livesIn":       "hcm:livesIn",
    "requiresToThrive": "hcm:requiresToThrive",
    "provides":      "hcm:provides",
    "displays":      "hcm:displays",
    "isDisplayedInside": "hcm:isDisplayedInside",
    "hasCircadianRhythm": "hcm:hasCircadianRhythm",
    "extendsEnoughToCapture": "hcm:extendsEnoughToCapture",
    "hasProperty":   "hcm:hasProperty",
    "captures":      "hcm:captures",
    "elicits":       "hcm:elicits",
    "hasSensor":     "hcm:hasSensor",
    "hasActuator":   "hcm:hasActuator",
    "communicatesWith": "hcm:communicatesWith",
    "hasDimensions": "hcm:hasDimensions",
    "hasFood": "hcm:hasFood",
    "hasWater": "hcm:hasWater",
    "hasSocialContacts": "hcm:hasSocialContacts",
    "hasSafetyFromThreat": "hcm:hasSafetyFromThreat",
    "hasEnvironmentalEnrichment": "hcm:hasEnvironmentalEnrichment"
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

const titleCase = (value) => value.charAt(0).toUpperCase() + value.slice(1);

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
    container.removeChild(wrapper);
    if (container.children.length === 0) {
      buildRow(container, prefix);
    }
  });
  container.appendChild(wrapper);
}

function collectRepeated(container, prefix) {
  return Array.from(container.querySelectorAll('.item-row')).map((row) => {
    const id = row.querySelector(`input[name="${prefix}Id[]"]`).value.trim();
    const label = row.querySelector(`input[name="${prefix}Label[]"]`).value.trim();
    return { id, label };
  }).filter((item) => item.id);
}

function toBoolean(value) {
  return String(value).toLowerCase() === 'true';
}

function toNumber(value) {
  const num = Number(value);
  return Number.isFinite(num) ? num : undefined;
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
    intervalId,
    intervalLabel,
    durationHours,
    isExtendable,
    limitedInteractionLabel,
    sensors,
    actuators,
    ingestedAt
  } = data;

  const base = ensureTrailing(baseIri);

  const systemIri = `${base}${systemId}`;
  const hardwareIri = `${base}${hardwareId}`;
  const softwareIri = `${base}${softwareId}`;
  const supplierIri = `${base}${supplierId}`;
  const enclosureIri = `${base}${enclosureId}`;
  const needsIri = `${base}${enclosureId}_Needs`;
  const dimensionsIri = `${base}${enclosureId}_Dims`;
  const animalIri = `${base}${animalId}`;
  const behaviorIri = `${base}${behaviorId}`;
  const circadianIri = `${base}${behaviorId}_CR`;
  const intervalIri = `${base}${intervalId}`;
  const limitedInteractionIri = `${base}${intervalId}_LHI`;

  const graph = [];

  const optionalLabel = (label) => label ? { label } : {};

  const systemNode = {
    '@id': systemIri,
    '@type': 'System',
    ...optionalLabel(systemLabel),
    hasEnclosure: { '@id': enclosureIri },
    hasHardware: { '@id': hardwareIri },
    hasSoftware: { '@id': softwareIri },
    producedBy: { '@id': supplierIri },
    collectsInfoOn: { '@id': animalIri },
    hasSensor: sensors.map((sensor) => ({ '@id': `${base}${sensor.id}` })),
    hasActuator: actuators.map((actuator) => ({ '@id': `${base}${actuator.id}` }))
  };

  if (ingestedAt) {
    systemNode.ingestedAt = { '@value': ingestedAt, '@type': 'xsd:dateTime' };
  }

  graph.push(systemNode);

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

  graph.push({
    '@id': supplierIri,
    '@type': 'Supplier',
    ...optionalLabel(supplierLabel)
  });

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

  graph.push({
    '@id': enclosureIri,
    '@type': 'Enclosure',
    ...optionalLabel(enclosureLabel),
    provides: { '@id': needsIri },
    hasDimensions: { '@id': dimensionsIri }
  });

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

  graph.push({
    '@id': intervalIri,
    '@type': 'TimeInterval',
    ...optionalLabel(intervalLabel),
    durationHours: toNumber(durationHours),
    isExtendable: toBoolean(isExtendable),
    hasProperty: { '@id': limitedInteractionIri }
  });

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

  return { graph, base, needsIri, dimensionsIri };
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
    intervalId: formData.get('intervalId').trim(),
    intervalLabel: formData.get('intervalLabel').trim(),
    durationHours: formData.get('durationHours'),
    isExtendable: formData.get('isExtendable'),
    limitedInteractionLabel: formData.get('limitedInteractionLabel').trim(),
    sensors,
    actuators,
    ingestedAt: ingestedAtIso
  };
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