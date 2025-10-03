import app from "../server.js";

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

const base = "https://mfg.example.com/hcm/id/";
const jsonldDoc = {
  "@context": [baseContext["@context"], { "label": "http://www.w3.org/2000/01/rdf-schema#label" }],
  "@graph": [
    {
      "@id": `${base}hcmo-system-001`,
      "@type": "System",
      "label": "System 001 (rack 3, cage 12)",
      "hasEnclosure": { "@id": `${base}Enc_01` },
      "hasHardware": { "@id": `${base}HW_01` },
      "hasSoftware": { "@id": `${base}SW_01` },
      "producedBy": { "@id": `${base}SupplierAcme` },
      "collectsInfoOn": { "@id": `${base}S-00123` },
      "followsProtocol": { "@id": `${base}Proto_HCM` },
      "hasSensor": [{ "@id": `${base}IR_Sensor_1` }],
      "hasActuator": [{ "@id": `${base}Feeder_1` }]
    },
    {
      "@id": `${base}Proto_HCM`,
      "@type": "Protocol",
      "label": "Minimal disturbance protocol",
      "protocolReference": "doi:10.1234/hcmo-protocol"
    },
    {
      "@id": `${base}HW_01`,
      "@type": "Hardware",
      "label": "HW control board 01",
      "communicatesWith": { "@id": `${base}SW_01` }
    },
    {
      "@id": `${base}SW_01`,
      "@type": "Software",
      "label": "Telemetry service 01"
    },
    {
      "@id": `${base}SupplierAcme`,
      "@type": "Supplier",
      "label": "Acme supply partners"
    },
    {
      "@id": `${base}Enc_01_Needs`,
      "@type": "NeedsSequence",
      "hasFood": true,
      "hasWater": true,
      "hasSocialContacts": true,
      "hasSafetyFromThreat": true,
      "hasEnvironmentalEnrichment": true
    },
    {
      "@id": `${base}Enc_01_Dims`,
      "@type": "Dimensions",
      "width": 30,
      "length": 45,
      "height": 20,
      "unit": "cm"
    },
    {
      "@id": `${base}Enc_01`,
      "@type": "Enclosure",
      "label": "Enclosure 01 (Rack 3 Cage 12)",
      "provides": { "@id": `${base}Enc_01_Needs` },
      "hasDimensions": { "@id": `${base}Enc_01_Dims` }
    },
    {
      "@id": `${base}S-00123`,
      "@type": "Animal",
      "label": "Subject S-00123",
      "livesIn": { "@id": `${base}Enc_01` },
      "requiresToThrive": { "@id": `${base}Enc_01_Needs` },
      "displays": { "@id": `${base}Behav_Rec_1` }
    },
    {
      "@id": `${base}Behav_Rec_1`,
      "@type": "BehaviorAndPhysiology",
      "label": "Exploration bouts (24h)",
      "isDisplayedInside": { "@id": `${base}Enc_01` },
      "hasCircadianRhythm": { "@id": `${base}Behav_Rec_1_CR` },
      "extendsEnoughToCapture": { "@id": `${base}TI_24h` }
    },
    {
      "@id": `${base}Behav_Rec_1_CR`,
      "@type": "CircadianRhythm",
      "label": "Nocturnal peak"
    },
    {
      "@id": `${base}TI_24h`,
      "@type": "TimeInterval",
      "label": "24-hour observation window",
      "durationHours": 24,
      "isExtendable": true,
      "hasProperty": { "@id": `${base}TI_24h_LHI` },
      "hasBeginning": { "@id": `${base}TI_24h_Start` },
      "hasEnd": { "@id": `${base}TI_24h_End` }
    },
    {
      "@id": `${base}TI_24h_Start`,
      "@type": "time:Instant",
      "inXSDDateTime": { "@value": "2025-09-20T20:00:00Z", "@type": "xsd:dateTime" }
    },
    {
      "@id": `${base}TI_24h_End`,
      "@type": "time:Instant",
      "inXSDDateTime": { "@value": "2025-09-21T20:00:00Z", "@type": "xsd:dateTime" }
    },
    {
      "@id": `${base}TI_24h_LHI`,
      "@type": "LimitedInteractionWithHumans",
      "label": "Minimal human contact"
    },
    {
      "@id": `${base}IR_Sensor_1`,
      "@type": "Sensor",
      "label": "IR beam sensor (left wall)",
      "captures": { "@id": `${base}Behav_Rec_1` }
    },
    {
      "@id": `${base}Feeder_1`,
      "@type": "Actuator",
      "label": "Feeder 1 (pellet dispenser)",
      "elicits": { "@id": `${base}Behav_Rec_1` }
    }
  ]
};

const server = app.listen(0, async () => {
  const { port } = server.address();
  const response = await fetch(`http://127.0.0.1:${port}/api/export`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ jsonld: jsonldDoc })
  });

  const payload = await response.json();
  console.log(JSON.stringify({ status: response.status, conforms: payload.conforms }, null, 2));
  server.close();
});
