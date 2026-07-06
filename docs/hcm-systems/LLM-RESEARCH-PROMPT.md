# LLM research prompt

A reusable prompt to research one HCM system at a time. It is tuned to surface the
facts HCMO needs to author faithful ABox instances and mock datasets: what the
system measures, at what rate, in what file format, with what schema, for which
subjects/enclosures, and where real data or manuals live.

**How to use:** replace `{{SYSTEM}}` and `{{VENDOR}}`. Use a web-enabled model
(citations required). Paste the answer into the system folder's `README.md` and keep
the `## Sources` block. Run it once per system in [`CATALOG.md`](CATALOG.md).

---

## Prompt (copy from here)

```
You are helping build validation data for HCMO, an OWL ontology for home-cage
monitoring (HCM) of laboratory rodents. HCMO models: monitored enclosures, subjects
and experimental groups, the environment and its measurements, observations and
results, and the sensors / hardware / software that produce the data.

Research the HCM system "{{SYSTEM}}" (vendor/authors: {{VENDOR}}). Use current,
citable web sources — vendor pages, manuals/spec sheets, peer-reviewed papers,
preprints, code repos, and public datasets. Do NOT guess: if a fact is unavailable,
write "unknown — not found" rather than inventing it. Cite a URL for every factual
claim.

Return the answer as GitHub-flavored Markdown with exactly these sections:

1. Overview — one paragraph: what it is, who makes it, commercial vs open-source,
   maturity, and the modality (video / RFID / EMF / load cell / telemetry / metabolic
   / environmental / acoustic-USV / operant / other).

2. Monitored entities — species supported; single- vs group-housing; cage/rack type
   and whether it retrofits standard cages or is a bespoke enclosure.

3. Sensors & actuators — each physical sensor/actuator, what it transduces, sampling
   rate, and range/resolution if published.

4. Measured & derived parameters — a table: | parameter | unit | raw or derived |
   sampling rate | notes |. Include environmental variables if any.

5. Data output — THE MOST IMPORTANT SECTION. File formats (CSV/HDF5/JSON/proprietary/
   API), one concrete example of the record/column schema (field names + types +
   units), typical file/volume size per cage or subject per day, timestamp format and
   timezone handling, and any published data dictionary. Quote real column headers if
   you can find them.

6. Software & interoperability — acquisition/analysis software, export options, open
   API / TTL / standard schemas, and integration with other HCM systems.

7. Public data & documentation — direct links to: downloadable sample datasets
   (repositories, OSF/Zenodo/Figshare/GitHub), user manuals or API docs (PDF/URL),
   and the 2–3 most relevant papers (with DOIs). Flag whether each artifact is freely
   redistributable (license) or link-only.

8. HCMO mapping notes — which HCMO modules/classes/properties this system's data would
   populate (e.g. hcm:Sensor, hcm-env measurements, hcm-obs observations/results,
   hcm-bio subjects/groups), and any concept the current ontology seems to lack.

9. Mock-data recipe — a short spec for a synthetic dataset that mimics the real output:
   columns, value ranges, sampling, duration, and number of subjects/cages — enough to
   generate a believable file for `datasets/mock/`.

## Sources
- (bulleted list of every URL used)
```

---

## Batch / triage variant

To decide where to invest first, run this once over the whole catalog:

```
For each system in the list below, return one row: | system | modality |
commercial/open-source | is a public sample dataset available? (URL or "no") | is a
public manual/spec or data dictionary available? (URL or "no") | best single paper
(DOI) | 1-line note on data-output format |. Do not invent links; use "no" when
unknown. Prioritise finding downloadable datasets and documented output schemas.

Systems: {{PASTE THE CATALOG.md SYSTEM NAMES}}
```

## Tips

- Prefer sources that show **real column headers / file formats** — those are what let
  us mock faithfully and validate SHACL shapes.
- For commercial systems, the **user manual / integration guide** is often the only
  place the data schema is documented; ask specifically for it.
- Open-source systems usually ship an example dataset in their GitHub repo or the
  paper's supplement — always ask for that link.
- Keep vendor-copyrighted PDFs out of git unless redistribution is permitted; store a
  link in `papers/links.md` instead.
