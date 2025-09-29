import app from "../server.js";

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

const base = "https://mfg.example.com/hcm/id/";
const jsonldDoc = {
  "@context": [baseContext["@context"], { "label": "http://www.w3.org/2000/01/rdf-schema#label" }],
  "@graph": [
    {
      "@id": `${base}System_A`,
      "@type": "System",
      "label": "System A (rack 3, cage 12)",
      "hasEnclosure": { "@id": `${base}Enc_01` },
      "hasHardware": { "@id": `${base}HW_01` },
      "hasSoftware": { "@id": `${base}SW_01` },
      "producedBy": { "@id": `${base}SupplierAcme` },
      "collectsInfoOn": { "@id": `${base}Mouse_1` },
      "hasSensor": [{ "@id": `${base}IR_Sensor_1` }],
      "hasActuator": [{ "@id": `${base}Feeder_1` }]
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
      "@id": `${base}Mouse_1`,
      "@type": "Animal",
      "label": "Mouse 1 (study cohort alpha)",
      "livesIn": { "@id": `${base}Enc_01` },
      "requiresToThrive": { "@id": `${base}Enc_01_Needs` },
      "displays": { "@id": `${base}Behav_Rec_1` }
    },
    {
      "@id": `${base}Behav_Rec_1`,
      "@type": "BehaviorAndPhysiology",
      "label": "Exploration bouts (24h window)",
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
      "hasProperty": { "@id": `${base}TI_24h_LHI` }
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