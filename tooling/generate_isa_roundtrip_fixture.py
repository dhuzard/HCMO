#!/usr/bin/env python3
"""Generate the reviewed HCMO/ISA/STATO 2 x 2 interoperability fixture.

The fixture is deliberately generated from one data table so that canonical
HCMO RDF, RO-Crate JSON-LD, and the two CSV data entities cannot silently
diverge. It is evidence for round-trip testing, not a formal conformance claim.
"""
from __future__ import annotations

import csv
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf
from rdflib import DCTERMS, RDF, RDFS, XSD, Graph, Literal, Namespace, URIRef

if os.environ.get("PYTHONHASHSEED") != "0":
    os.environ["PYTHONHASHSEED"] = "0"
    os.execv(sys.executable, [sys.executable] + sys.argv)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "examples" / "isa-roundtrip"

EX = Namespace("https://example.org/hcmo/isa-roundtrip/")
HCM = Namespace("https://w3id.org/hcmo/ontology/hcm#")
HCM_BIO = Namespace("https://w3id.org/hcmo/ontology/hcm/bio#")
HCM_OBS = Namespace("https://w3id.org/hcmo/ontology/hcm/obs#")
HCM_TECH = Namespace("https://w3id.org/hcmo/ontology/hcm/tech#")
SCHEMA = Namespace("http://schema.org/")
BIOSCHEMAS = Namespace("https://bioschemas.org/")
BIOSCHEMAS_PROP = Namespace("https://bioschemas.org/properties/")
PROV = Namespace("http://www.w3.org/ns/prov#")
SOSA = Namespace("http://www.w3.org/ns/sosa/")
TIME = Namespace("http://www.w3.org/2006/time#")
OBI = Namespace("http://purl.obolibrary.org/obo/OBI_")
STATO = Namespace("http://purl.obolibrary.org/obo/STATO_")
QUDT = Namespace("http://qudt.org/schema/qudt/")
UNIT = Namespace("http://qudt.org/vocab/unit/")

CORE_PROFILE = URIRef("https://w3id.org/ro/crate/1.2")

GROUPS = [
    ("vehicle-standard", "vehicle", "standard"),
    ("vehicle-enriched", "vehicle", "enriched"),
    ("active-standard", "active", "standard"),
    ("active-enriched", "active", "enriched"),
]

ANIMAL_EFFECTS = (-2, 2, -1, 1, -2, 2, -1, 1)
WITHIN_ANIMAL_NOISE = (
    (-1, 0, 1, -2, 2, 0, 1),
    (1, -1, 0, 2, -2, 1, 0),
    (0, 1, -1, 2, 0, -2, 1),
    (-1, 2, 0, -1, 1, 0, -2),
    (2, -1, 1, 0, -2, 1, -1),
    (0, -2, 2, 1, -1, 0, 1),
    (1, 0, -2, 2, -1, 1, 0),
    (-2, 1, 0, -1, 2, 0, 1),
)
MODEL_FORMULA = "activity_count ~ treatment * enrichment + day; random intercept: animal"


def lit_datetime(value: datetime) -> Literal:
    return Literal(value.isoformat().replace("+00:00", "Z"), datatype=XSD.dateTime)


def add_named(g: Graph, node: URIRef, rdf_type: URIRef, name: str) -> None:
    g.add((node, RDF.type, rdf_type))
    g.add((node, SCHEMA.name, Literal(name)))


def add_interval(g: Graph, assignment: URIRef, key: str, start: datetime, end: datetime) -> None:
    interval = EX[f"interval-{key}"]
    g.add((assignment, TIME.hasTime, interval))
    add_interval_bounds(g, interval, key, start, end)


def add_interval_bounds(g: Graph, interval: URIRef, key: str, start: datetime, end: datetime) -> None:
    beginning = EX[f"instant-{key}-begin"]
    ending = EX[f"instant-{key}-end"]
    g.add((interval, RDF.type, TIME.Interval))
    g.add((interval, TIME.hasBeginning, beginning))
    g.add((interval, TIME.hasEnd, ending))
    g.add((beginning, RDF.type, TIME.Instant))
    g.add((beginning, TIME.inXSDDateTime, lit_datetime(start)))
    g.add((ending, RDF.type, TIME.Instant))
    g.add((ending, TIME.inXSDDateTime, lit_datetime(end)))


def fit_mixed_model(observations: list[dict[str, str | int]]) -> dict[str, str]:
    """Fit the declared repeated-measures model and return stable text values."""
    frame = pd.DataFrame(observations)
    frame[["treatment", "enrichment"]] = frame["group"].str.split("-", n=1, expand=True)
    frame["treatment"] = pd.Categorical(frame["treatment"], categories=["vehicle", "active"])
    frame["enrichment"] = pd.Categorical(frame["enrichment"], categories=["standard", "enriched"])
    fitted = smf.mixedlm(
        "activity_count ~ treatment * enrichment + day",
        frame,
        groups=frame["animal"],
    ).fit(reml=False, method="lbfgs", disp=False)
    if not fitted.converged:
        raise RuntimeError("the pinned mixed model did not converge")
    term = "treatment[T.active]"
    bounds = fitted.conf_int().loc[term]
    return {
        "formula": MODEL_FORMULA,
        "estimate": f"{fitted.params[term]:.4f}",
        "ci_lower": f"{bounds.iloc[0]:.4f}",
        "ci_upper": f"{bounds.iloc[1]:.4f}",
        "p_value": f"{fitted.pvalues[term]:.6g}",
        "fixed_effects": "treatment, enrichment, treatment:enrichment, day",
        "random_effect": "animal random intercept",
    }


def build_graph() -> tuple[Graph, list[dict[str, str | int]]]:
    g = Graph()
    for prefix, ns in {
        "ex": EX,
        "hcm": HCM,
        "hcm-bio": HCM_BIO,
        "hcm-obs": HCM_OBS,
        "hcm-tech": HCM_TECH,
        "schema": SCHEMA,
        "bioschemas": BIOSCHEMAS,
        "bioschemas-prop": BIOSCHEMAS_PROP,
        "prov": PROV,
        "sosa": SOSA,
        "time": TIME,
        "obi": OBI,
        "stato": STATO,
    }.items():
        g.bind(prefix, ns)

    root = URIRef("./")
    study = URIRef("studies/hcmo-2x2/")
    assay = URIRef("assays/activity/")
    creator = EX["damien-huzard"]
    descriptor = URIRef("ro-crate-metadata.json")

    add_named(g, root, SCHEMA.Dataset, "HCMO ISA/STATO 2 x 2 interoperability fixture")
    g.add((root, SCHEMA.additionalType, Literal("Investigation")))
    g.add((root, SCHEMA.identifier, Literal("HCMO-ISA-ROUNDTRIP-001")))
    g.add((root, SCHEMA.description, Literal("A generated evidence fixture for animal identity, housing, factorial design, repeated observations, and statistical-result provenance.")))
    g.add((root, SCHEMA.license, URIRef("https://creativecommons.org/publicdomain/zero/1.0/")))
    g.add((root, SCHEMA.datePublished, Literal("2026-07-31T00:00:00Z")))
    g.add((root, SCHEMA.creator, creator))
    g.add((root, SCHEMA.hasPart, study))
    g.add((root, SCHEMA.hasPart, assay))

    add_named(g, creator, SCHEMA.Person, "Damien Huzard")
    g.add((creator, SCHEMA.givenName, Literal("Damien")))
    g.add((creator, SCHEMA.familyName, Literal("Huzard")))

    add_named(g, study, SCHEMA.Dataset, "Treatment by enrichment home-cage study")
    g.add((study, SCHEMA.additionalType, Literal("Study")))
    g.add((study, SCHEMA.identifier, Literal("HCMO-2X2")))
    g.add((study, SCHEMA.description, Literal("A structural 2 x 2 design fixture; it is not a claim of adequate statistical power.")))
    g.add((study, SCHEMA.hasPart, assay))

    add_named(g, assay, SCHEMA.Dataset, "Repeated dark-phase activity assay")
    g.add((assay, SCHEMA.additionalType, Literal("Assay")))
    g.add((assay, SCHEMA.identifier, Literal("HCMO-2X2-ACTIVITY")))
    g.add((assay, SCHEMA.description, Literal("Seven repeated daily dark-phase activity outcomes per individually housed animal.")))

    # Study-design specifications and factor levels.
    factor_nodes = {
        "treatment": EX["factor-treatment"],
        "enrichment": EX["factor-enrichment"],
    }
    for key, label in (("treatment", "Treatment"), ("enrichment", "Cage enrichment")):
        node = factor_nodes[key]
        add_named(g, node, HCM_BIO.StudyFactors, f"{label} study factor")
        g.add((node, RDF.type, OBI["0000750"]))
        g.add((root, SCHEMA.mentions, node))
        g.add((study, SCHEMA.mentions, node))

    level_nodes: dict[str, URIRef] = {}
    for key, factor_key, label in (
        ("vehicle", "treatment", "Vehicle"),
        ("active", "treatment", "Active treatment"),
        ("standard", "enrichment", "Standard cage"),
        ("enriched", "enrichment", "Enriched cage"),
    ):
        node = EX[f"level-{key}"]
        level_nodes[key] = node
        add_named(g, node, SCHEMA.PropertyValue, label)
        g.add((node, RDF.type, STATO["0000265"]))
        g.add((node, SCHEMA.additionalType, Literal("FactorValue")))
        g.add((node, SCHEMA.propertyID, factor_nodes[factor_key]))
        g.add((node, SCHEMA.value, Literal(label)))

    dependent_variable = EX["dependent-variable-dark-phase-activity"]
    add_named(g, dependent_variable, SCHEMA.PropertyValue, "Daily dark-phase activity count")
    g.add((dependent_variable, RDF.type, OBI["0000751"]))
    g.add((dependent_variable, SCHEMA.unitText, Literal("activity counts per dark phase")))
    g.add((assay, SCHEMA.variableMeasured, dependent_variable))

    dimensions = EX["standard-cage-dimensions"]
    g.add((dimensions, RDF.type, HCM.EnclosureDimensions))
    for property_iri, key, value in (
        (HCM.hasWidthQuantity, "width", "20.0"),
        (HCM.hasLengthQuantity, "length", "36.0"),
        (HCM.hasHeightQuantity, "height", "18.0"),
    ):
        quantity = EX[f"standard-cage-{key}-quantity"]
        g.add((dimensions, property_iri, quantity))
        g.add((quantity, RDF.type, QUDT.QuantityValue))
        g.add((quantity, QUDT.numericValue, Literal(value, datatype=XSD.decimal)))
        g.add((quantity, QUDT.hasUnit, UNIT.CentiM))
    rack_sensor = EX["rack-activity-sensor"]
    add_named(g, rack_sensor, HCM_TECH.Sensor, "Rack activity sensor")
    g.add((rack_sensor, RDFS.label, Literal("Rack activity sensor")))
    g.add((rack_sensor, HCM_TECH.hasSensorIdentifier, Literal("rack-sensor-1")))

    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    end = datetime(2026, 1, 11, tzinfo=timezone.utc)
    recording_start = datetime(2026, 1, 4, tzinfo=timezone.utc)
    observation_rows: list[dict[str, str | int]] = []
    subject_nodes: list[URIRef] = []
    group_nodes: dict[str, URIRef] = {}

    for group_index, (group_key, treatment, enrichment) in enumerate(GROUPS, start=1):
        group = EX[f"group-{group_key}"]
        group_nodes[group_key] = group
        add_named(g, group, HCM_BIO.ExperimentalGroup, f"{treatment} / {enrichment} group")
        g.add((group, RDF.type, STATO["0000193"]))
        g.add((group, SCHEMA.additionalProperty, level_nodes[treatment]))
        g.add((group, SCHEMA.additionalProperty, level_nodes[enrichment]))
        g.add((root, SCHEMA.mentions, group))
        g.add((study, SCHEMA.mentions, group))

        for replicate in (1, 2):
            animal_number = (group_index - 1) * 2 + replicate
            animal = EX[f"animal-{animal_number}"]
            cage = EX[f"cage-{animal_number}"]
            assignment = EX[f"assignment-{animal_number}"]
            subject_nodes.append(animal)

            add_named(g, animal, HCM_BIO.Subject, f"animal-{animal_number}")
            g.add((animal, RDF.type, BIOSCHEMAS.Sample))
            g.add((animal, SCHEMA.additionalType, Literal("Source")))
            g.add((animal, RDFS.label, Literal(f"animal-{animal_number}")))
            g.add((animal, HCM_BIO.hasSpecies, Literal("Mus musculus")))
            g.add((animal, HCM_BIO.belongsToGroup, group))
            g.add((animal, SCHEMA.additionalProperty, level_nodes[treatment]))
            g.add((animal, SCHEMA.additionalProperty, level_nodes[enrichment]))
            g.add((animal, HCM_BIO.hasHousingAssignment, assignment))
            g.add((group, HCM_BIO.hasMember, animal))
            g.add((study, SCHEMA.mentions, animal))

            add_named(g, cage, HCM.MonitoredEnclosure, f"Cage {animal_number}")
            g.add((cage, RDFS.label, Literal(f"Cage {animal_number}")))
            g.add((cage, HCM.hasEnclosureIdentifier, Literal(f"cage-{animal_number}")))
            g.add((cage, HCM.hasDimensions, dimensions))
            g.add((cage, HCM_TECH.monitoredBy, rack_sensor))

            g.add((assignment, RDF.type, HCM_BIO.HousingAssignment))
            g.add((assignment, HCM_BIO.assignedToEnclosure, cage))
            add_interval(g, assignment, str(animal_number), start, end)

            for day in range(1, 8):
                value = (
                    100
                    + (12 if treatment == "active" else 0)
                    + (5 if enrichment == "enriched" else 0)
                    + (3 if treatment == "active" and enrichment == "enriched" else 0)
                    + 2 * day
                    + ANIMAL_EFFECTS[animal_number - 1]
                    + WITHIN_ANIMAL_NOISE[animal_number - 1][day - 1]
                )
                observed_start = recording_start + timedelta(days=day - 1)
                observed_end = observed_start + timedelta(hours=12)
                observation = EX[f"observation-{animal_number}-day-{day}"]
                result = EX[f"result-{animal_number}-day-{day}"]
                phenomenon = EX[f"interval-observation-{animal_number}-day-{day}"]
                observation_cage = EX["cage-9"] if animal_number == 1 else cage
                g.add((observation, RDF.type, HCM_OBS.BehaviorObservation))
                g.add((observation, SOSA.hasFeatureOfInterest, animal))
                g.add((observation, SOSA.observedProperty, dependent_variable))
                g.add((observation, SOSA.madeBySensor, rack_sensor))
                g.add((observation, SOSA.hasResult, result))
                g.add((observation, SOSA.phenomenonTime, phenomenon))
                g.add((observation, HCM_OBS.occursIn, observation_cage))
                g.add((result, RDF.type, HCM_OBS.BehaviorResult))
                g.add((result, RDF.type, HCM_OBS.QuantityValue))
                g.add((result, QUDT.numericValue, Literal(f"{value}.0", datatype=XSD.decimal)))
                g.add((result, QUDT.hasUnit, UNIT.UNITLESS))
                add_interval_bounds(
                    g,
                    phenomenon,
                    f"observation-{animal_number}-day-{day}",
                    observed_start,
                    observed_end,
                )
                observation_rows.append(
                    {
                        "animal": f"animal-{animal_number}",
                        "group": group_key,
                        "day": day,
                        "activity_count": value,
                    }
                )

    # Re-house animal 1 without changing its identity or creating a Sample.
    animal_1 = EX["animal-1"]
    first_assignment = EX["assignment-1"]
    first_interval = EX["interval-1"]
    first_end = EX["instant-1-end"]
    g.set((first_end, TIME.inXSDDateTime, lit_datetime(recording_start)))
    cage_9 = EX["cage-9"]
    add_named(g, cage_9, HCM.MonitoredEnclosure, "Cage 9")
    g.add((cage_9, RDFS.label, Literal("Cage 9")))
    g.add((cage_9, HCM.hasEnclosureIdentifier, Literal("cage-9")))
    g.add((cage_9, HCM.hasDimensions, dimensions))
    g.add((cage_9, HCM_TECH.monitoredBy, rack_sensor))
    # Do not materialize hcm:hasMonitoredAnimals in this historical fixture.
    # Its two successive values for animal 1 would require different explicit
    # evaluation times; the time-bounded HousingAssignment records are the
    # authoritative representation.
    second_assignment = EX["assignment-1-rehousing"]
    g.add((animal_1, HCM_BIO.hasHousingAssignment, second_assignment))
    g.add((second_assignment, RDF.type, HCM_BIO.HousingAssignment))
    g.add((second_assignment, HCM_BIO.assignedToEnclosure, cage_9))
    add_interval(g, second_assignment, "1-rehousing", recording_start, end)

    allocation_protocol = EX["protocol-allocation"]
    add_named(g, allocation_protocol, BIOSCHEMAS.LabProtocol, "Animal housing allocation protocol")
    g.add((allocation_protocol, RDF.type, PROV.Plan))
    allocation = EX["process-initial-allocation"]
    add_named(g, allocation, BIOSCHEMAS.LabProcess, "Initial animal allocation")
    g.add((allocation, RDF.type, PROV.Activity))
    g.add((allocation, BIOSCHEMAS_PROP.executesLabProtocol, allocation_protocol))
    for animal_number, animal in enumerate(subject_nodes, start=1):
        assignment = EX[f"assignment-{animal_number}"]
        cage = EX[f"cage-{animal_number}"]
        g.add((allocation, SCHEMA.object, animal))
        g.add((allocation, PROV.used, animal))
        g.add((allocation, PROV.used, cage))
        g.add((allocation, PROV.generated, assignment))
        g.add((assignment, PROV.wasGeneratedBy, allocation))
    g.add((study, SCHEMA.about, allocation))

    rehousing = EX["process-rehousing-animal-1"]
    add_named(g, rehousing, BIOSCHEMAS.LabProcess, "Re-house animal 1")
    g.add((rehousing, RDF.type, PROV.Activity))
    g.add((rehousing, SCHEMA.object, animal_1))
    g.add((rehousing, BIOSCHEMAS_PROP.executesLabProtocol, allocation_protocol))
    g.add((rehousing, PROV.used, animal_1))
    g.add((rehousing, PROV.used, cage_9))
    g.add((rehousing, PROV.generated, second_assignment))
    g.add((second_assignment, PROV.wasGeneratedBy, rehousing))
    g.add((study, SCHEMA.about, rehousing))

    # Recording produces a file; it does not produce replacement animals.
    recording_protocol = EX["protocol-recording"]
    add_named(g, recording_protocol, BIOSCHEMAS.LabProtocol, "Seven-day dark-phase activity recording")
    recording = EX["process-recording"]
    raw_file = URIRef("data/dark-phase-activity.csv")
    add_named(g, recording, BIOSCHEMAS.LabProcess, "Record repeated dark-phase activity")
    g.add((recording, RDF.type, PROV.Activity))
    g.add((recording, BIOSCHEMAS_PROP.executesLabProtocol, recording_protocol))
    g.add((recording, SCHEMA.result, raw_file))
    g.add((recording, PROV.generated, raw_file))
    for animal in subject_nodes:
        g.add((recording, SCHEMA.object, animal))
        g.add((recording, PROV.used, animal))
    add_named(g, raw_file, SCHEMA.MediaObject, "dark-phase-activity.csv")
    g.add((raw_file, RDF.type, HCM_TECH.TimeSeries))
    g.add((raw_file, RDF.type, PROV.Entity))
    g.add((raw_file, SCHEMA.encodingFormat, Literal("text/csv")))
    g.add((raw_file, HCM_TECH.hasFileFormat, Literal("text/csv")))
    g.add((raw_file, HCM_TECH.hasStoragePath, Literal("./data/dark-phase-activity.csv")))
    g.add((raw_file, PROV.wasGeneratedBy, recording))
    g.add((assay, SCHEMA.about, recording))
    g.add((assay, SCHEMA.hasPart, raw_file))

    # Real specimen collection creates a distinct Sample.
    specimen_protocol = EX["protocol-specimen-collection"]
    specimen_process = EX["process-specimen-collection"]
    tissue = EX["tissue-sample-animal-8"]
    add_named(g, specimen_protocol, BIOSCHEMAS.LabProtocol, "Tissue specimen collection protocol")
    add_named(g, specimen_process, BIOSCHEMAS.LabProcess, "Collect tissue from animal 8")
    g.add((specimen_process, RDF.type, PROV.Activity))
    g.add((specimen_process, SCHEMA.object, EX["animal-8"]))
    g.add((specimen_process, SCHEMA.result, tissue))
    g.add((specimen_process, BIOSCHEMAS_PROP.executesLabProtocol, specimen_protocol))
    g.add((specimen_process, PROV.used, EX["animal-8"]))
    g.add((specimen_process, PROV.generated, tissue))
    add_named(g, tissue, BIOSCHEMAS.Sample, "Tissue sample from animal 8")
    g.add((tissue, SCHEMA.additionalType, Literal("Sample")))
    g.add((tissue, PROV.wasDerivedFrom, EX["animal-8"]))
    g.add((assay, SCHEMA.about, specimen_process))

    # Model fitting generates semantic STATO entities and a separate file.
    model_results = fit_mixed_model(observation_rows)
    analysis_protocol = EX["protocol-linear-mixed-model"]
    analysis = EX["process-linear-mixed-model"]
    results_file = URIRef("data/model-results.csv")
    model_fragment = URIRef("data/model-results.csv#row=2")
    contrast_fragment = URIRef("data/model-results.csv#row=3")
    model = EX["fitted-linear-mixed-model"]
    contrast = EX["active-versus-vehicle-contrast"]
    null_hypothesis = EX["active-versus-vehicle-null-hypothesis"]
    estimate = EX["treatment-contrast-estimate"]
    confidence_interval = EX["treatment-contrast-95ci"]
    p_value = EX["treatment-contrast-p-value"]
    add_named(g, analysis_protocol, BIOSCHEMAS.LabProtocol, "Linear mixed model analysis protocol")
    add_named(g, analysis, BIOSCHEMAS.LabProcess, "Fit repeated-measures linear mixed model")
    g.add((analysis, RDF.type, PROV.Activity))
    g.add((analysis, RDF.type, STATO["0000218"]))
    g.add((analysis, SCHEMA.object, raw_file))
    g.add((analysis, SCHEMA.result, results_file))
    g.add((analysis, BIOSCHEMAS_PROP.executesLabProtocol, analysis_protocol))
    g.add((analysis, PROV.used, raw_file))
    add_named(g, results_file, SCHEMA.MediaObject, "model-results.csv")
    g.add((results_file, RDF.type, PROV.Entity))
    g.add((results_file, SCHEMA.encodingFormat, Literal("text/csv")))
    g.add((results_file, SCHEMA.hasPart, model_fragment))
    g.add((results_file, SCHEMA.hasPart, contrast_fragment))
    add_named(g, model_fragment, SCHEMA.MediaObject, "model-results.csv model row")
    g.add((model_fragment, SCHEMA.usageInfo, Literal("RFC 7111 row selector: row=2")))
    add_named(g, contrast_fragment, SCHEMA.MediaObject, "model-results.csv treatment contrast row")
    g.add((contrast_fragment, SCHEMA.usageInfo, Literal("RFC 7111 row selector: row=3")))

    add_named(
        g,
        contrast,
        SCHEMA.PropertyValue,
        "Active treatment versus vehicle contrast at standard enrichment",
    )
    g.add((contrast, SCHEMA.propertyID, factor_nodes["treatment"]))
    g.add((contrast, SCHEMA.value, Literal("active minus vehicle at standard enrichment, adjusted for day")))
    g.add((contrast, SCHEMA.unitText, Literal("activity counts per dark phase")))
    g.add((contrast, SCHEMA.variableMeasured, dependent_variable))
    add_named(
        g,
        null_hypothesis,
        SCHEMA.PropertyValue,
        "Zero active-treatment contrast at standard enrichment null hypothesis",
    )
    g.add((null_hypothesis, SCHEMA.about, contrast))
    g.add((null_hypothesis, SCHEMA.value, Literal("0.0", datatype=XSD.decimal)))
    g.add((null_hypothesis, SCHEMA.unitText, Literal("activity counts per dark phase")))

    for result_node, result_type, name, value in (
        (model, STATO["0000464"], "Fitted linear mixed model", model_results["formula"]),
        (
            estimate,
            STATO["0000384"],
            "Active-treatment contrast estimate at standard enrichment",
            model_results["estimate"],
        ),
        (
            confidence_interval,
            STATO["0000231"],
            "Active-treatment contrast 95% confidence interval at standard enrichment",
            f"[{model_results['ci_lower']}, {model_results['ci_upper']}]",
        ),
        (
            p_value,
            STATO["0000700"],
            "Active-treatment contrast p-value at standard enrichment",
            model_results["p_value"],
        ),
    ):
        add_named(g, result_node, result_type, name)
        g.add((result_node, RDF.type, PROV.Entity))
        g.add((analysis, PROV.generated, result_node))
        g.add((result_node, PROV.wasGeneratedBy, analysis))
        g.add(((model_fragment if result_node == model else contrast_fragment), SCHEMA.about, result_node))
        if value is not None:
            datatype = XSD.decimal if result_node in {estimate, p_value} else None
            g.add((result_node, SCHEMA.value, Literal(value, datatype=datatype)))
    g.add((model, SCHEMA.description, Literal(model_results["formula"])))
    g.add((estimate, SCHEMA.about, contrast))
    g.add((estimate, SCHEMA.unitText, Literal("activity counts per dark phase")))
    g.add((confidence_interval, SCHEMA.about, estimate))
    g.add((confidence_interval, SCHEMA.unitText, Literal("activity counts per dark phase")))
    g.add((p_value, SCHEMA.about, null_hypothesis))
    g.add((analysis, PROV.generated, results_file))
    g.add((results_file, PROV.wasGeneratedBy, analysis))
    g.add((assay, SCHEMA.about, analysis))
    g.add((assay, SCHEMA.hasPart, results_file))

    g.add((descriptor, RDF.type, SCHEMA.CreativeWork))
    g.add((descriptor, DCTERMS.conformsTo, CORE_PROFILE))
    g.add((descriptor, SCHEMA.about, root))
    return g, observation_rows, model_results


def write_outputs(
    g: Graph,
    observations: list[dict[str, str | int]],
    model_results: dict[str, str],
) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "data").mkdir(parents=True, exist_ok=True)

    ttl = g.serialize(format="turtle")
    (OUT / "canonical.ttl").write_text(
        "# GENERATED by tooling/generate_isa_roundtrip_fixture.py — DO NOT EDIT\n" + ttl,
        encoding="utf-8",
        newline="\n",
    )

    custom_context = {
        "LabProcess": str(BIOSCHEMAS.LabProcess),
        "LabProtocol": str(BIOSCHEMAS.LabProtocol),
        "Sample": str(BIOSCHEMAS.Sample),
        "executesLabProtocol": str(BIOSCHEMAS_PROP.executesLabProtocol),
        "parameterValue": str(BIOSCHEMAS_PROP.parameterValue),
        "conformsTo": str(DCTERMS.conformsTo),
        "hcm": str(HCM),
        "hcm-bio": str(HCM_BIO),
        "hcm-obs": str(HCM_OBS),
        "hcm-tech": str(HCM_TECH),
        "prov": str(PROV),
        "sosa": str(SOSA),
        "time": str(TIME),
        "obi": str(OBI),
        "stato": str(STATO),
        "rdfs": str(RDFS),
    }
    # The official RO-Crate context supplies Schema.org terms. Supplying them
    # locally for compaction keeps generation deterministic and offline.
    for term in (
        "CreativeWork", "Dataset", "MediaObject", "Person", "PropertyValue",
        "about", "additionalProperty", "additionalType", "creator",
        "datePublished", "description", "encodingFormat", "familyName",
        "givenName", "hasPart", "identifier", "license", "mentions", "name", "object",
        "propertyID", "result", "unitText", "usageInfo", "value",
        "variableMeasured",
    ):
        custom_context[term] = str(SCHEMA[term])
    namespace_tokens = {
        str(HCM): "hcm",
        str(HCM_BIO): "hcm_bio",
        str(HCM_OBS): "hcm_obs",
        str(HCM_TECH): "hcm_tech",
        str(PROV): "prov",
        str(SOSA): "sosa",
        str(TIME): "time",
        str(RDFS): "rdfs",
    }
    # roc-validator's compacted-format check requires every property key to be
    # an explicit context term; namespace-prefix declarations alone are not
    # sufficient for custom HCMO/PROV/SOSA/Time properties.
    for predicate in sorted({str(predicate) for predicate in g.predicates()}):
        if predicate == str(RDF.type) or predicate in custom_context.values():
            continue
        local = predicate.rsplit("#", 1)[-1].rsplit("/", 1)[-1]
        term = local
        if term in custom_context and custom_context[term] != predicate:
            token = next(
                (name for namespace, name in namespace_tokens.items() if predicate.startswith(namespace)),
                "term",
            )
            term = f"{token}_{local}"
        custom_context[term] = predicate
    compacted = json.loads(
        g.serialize(format="json-ld", context=custom_context, auto_compact=True)
    )
    graph_nodes = compacted.get("@graph", [])
    crate = {
        "@context": ["https://w3id.org/ro/crate/1.2/context", custom_context],
        "@graph": sorted(graph_nodes, key=lambda node: node.get("@id", "")),
    }
    (OUT / "ro-crate-metadata.json").write_text(
        json.dumps(crate, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    with (OUT / "data" / "dark-phase-activity.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["animal", "group", "day", "activity_count"],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(observations)

    with (OUT / "data" / "model-results.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(
            [
                "entity",
                "term",
                "estimate",
                "ci_lower",
                "ci_upper",
                "p_value",
                "model_formula",
                "fixed_effects",
                "random_effect",
            ]
        )
        writer.writerow(
            [
                "https://example.org/hcmo/isa-roundtrip/fitted-linear-mixed-model",
                "fitted linear mixed model",
                "",
                "",
                "",
                "",
                model_results["formula"],
                model_results["fixed_effects"],
                model_results["random_effect"],
            ]
        )
        writer.writerow(
            [
                "https://example.org/hcmo/isa-roundtrip/active-versus-vehicle-contrast",
                "active treatment contrast at standard enrichment",
                model_results["estimate"],
                model_results["ci_lower"],
                model_results["ci_upper"],
                model_results["p_value"],
                "",
                "",
                "",
            ]
        )


def main() -> int:
    graph, observations, model_results = build_graph()
    write_outputs(graph, observations, model_results)
    print(f"Generated ISA round-trip fixture: {len(graph)} triples, {len(observations)} observations")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
