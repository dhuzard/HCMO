#!/usr/bin/env python3
"""Generate a SYNTHETIC, schema-faithful TSE PhenoMaster export and its HCMO graph.

No real PhenoMaster data were available for redistribution. The export written
to ``datasets/mock/phenomaster_mock_export.csv`` reproduces the documented shape
of a PhenoMaster/LabMaster CaloSys table export (one row per animal per
sampling interval; ``Animal No.``, ``Box``, calorimetry, feeding, drinking,
activity and body-weight channels with bracketed units). Column names follow
the CalR TSE import specification and published supplementary tables; vendor
header strings vary between software versions.

Output: ``examples/systems/tse-phenomaster.ttl``

Modelling decisions (see ``hcmo-mapping.tsv`` and ``README.md``):
  * one calorimetry box  -> hcm:MonitoredEnclosure with per-box sensors
  * one animal per box   -> hcm-bio:Subject with a time-bounded housing assignment
  * VO2/VCO2/RER/H, feed, drink, beam breaks -> sosa:Observation about the
    subject with hcm-obs:QuantityValue results (no HCMO metabolic subtype yet)
  * body weight          -> hcm-obs:WeightObservation
  * box temperature      -> hcm-obs:EnvironmentObservation
  * box O2 / CO2         -> hcm-obs:GasConcentrationObservation
  * the run spans the light-to-dark transition of a 12:12 cycle (dark 19:00)

Deterministic (fixed seed). Standard library + rdflib only.
"""
from __future__ import annotations

import csv
import random
import sys
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "tooling"))

from rdflib import RDFS, Literal  # noqa: E402

from hcmo_instance import (  # noqa: E402
    DCTERMS,
    HCM,
    HCM_ENV,
    HCM_OBS,
    HCM_TECH,
    PROV,
    SCHEMA,
    SOSA,
    TIME,
    UNIT,
    InstanceGraph,
)

MOCK_DIR = HERE / "datasets" / "mock"
EXPORT = MOCK_DIR / "phenomaster_mock_export.csv"
OUT = ROOT / "examples" / "systems" / "tse-phenomaster.ttl"
BASE = "https://w3id.org/hcmo/id/eval/tse-phenomaster/"

TZ = timezone(timedelta(hours=2))
START = datetime(2026, 6, 2, 17, 0, tzinfo=TZ)
INTERVAL_MIN = 15
ROWS_PER_ANIMAL = 12  # 3 hours
DARK_START_HOUR = 19

ANIMALS = [
    # animal no, box, sex, weight g, enrichment
    (1, 1, "male", Decimal("24.3"), True),
    (2, 2, "male", Decimal("25.1"), True),
    (3, 3, "female", Decimal("20.4"), False),
    (4, 4, "female", Decimal("19.8"), False),
]
# Assumed calorimetry-cage inner dimensions for this synthetic profile (cm).
BOX_DIMENSIONS_CM = (Decimal("20.7"), Decimal("26.7"), Decimal("14.0"))

COLUMNS = [
    "Date", "Time", "Animal No.", "Box", "Weight [g]", "Drink1 [ml]", "Feed1 [g]",
    "O2 [%]", "CO2 [%]", "Temp [°C]", "VO2(1) [ml/h]", "VCO2(1) [ml/h]", "RER",
    "H(1) [kcal/h]", "XT+YT [Cnt]", "Z [Cnt]",
]


def synthesize_rows() -> list[dict[str, str]]:
    rng = random.Random(20260602)
    rows: list[dict[str, str]] = []
    cumulative = {a[0]: {"feed": Decimal("0"), "drink": Decimal("0")} for a in ANIMALS}
    for index in range(ROWS_PER_ANIMAL):
        when = START + timedelta(minutes=index * INTERVAL_MIN)
        dark = when.hour >= DARK_START_HOUR
        for animal_no, box, sex, weight, _ in ANIMALS:
            scale = float(weight) / 25.0
            vo2 = rng.uniform(52, 66) * scale * (1.25 if dark else 1.0)
            rer = rng.uniform(0.78, 0.86) if not dark else rng.uniform(0.86, 0.96)
            vco2 = vo2 * rer
            heat = (3.941 * vo2 + 1.106 * vco2) / 1000  # Weir, kcal/h
            feed_inc = Decimal(str(round(rng.uniform(0.00, 0.06) * (4 if dark else 1), 2)))
            drink_inc = Decimal(str(round(rng.uniform(0.00, 0.05) * (3 if dark else 1), 2)))
            cumulative[animal_no]["feed"] += feed_inc
            cumulative[animal_no]["drink"] += drink_inc
            beams = int(rng.uniform(40, 160) * (3.5 if dark else 1.0))
            rearing = int(rng.uniform(2, 12) * (3 if dark else 1))
            rows.append({
                "Date": when.strftime("%d.%m.%Y"),
                "Time": when.strftime("%H:%M:%S"),
                "Animal No.": str(animal_no),
                "Box": str(box),
                "Weight [g]": f"{weight + Decimal(str(round(rng.uniform(-0.1, 0.1), 1))):.1f}",
                "Drink1 [ml]": f"{cumulative[animal_no]['drink']:.2f}",
                "Feed1 [g]": f"{cumulative[animal_no]['feed']:.2f}",
                "O2 [%]": f"{rng.uniform(20.50, 20.75):.2f}",
                "CO2 [%]": f"{rng.uniform(0.30, 0.55):.2f}",
                "Temp [°C]": f"{rng.uniform(22.0, 23.0):.1f}",
                "VO2(1) [ml/h]": f"{vo2:.1f}",
                "VCO2(1) [ml/h]": f"{vco2:.1f}",
                "RER": f"{rer:.2f}",
                "H(1) [kcal/h]": f"{heat:.3f}",
                "XT+YT [Cnt]": str(beams),
                "Z [Cnt]": str(rearing),
            })
    return rows


def write_export(rows: list[dict[str, str]]) -> None:
    MOCK_DIR.mkdir(parents=True, exist_ok=True)
    with EXPORT.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write("SYNTHETIC TSE PhenoMaster/LabMaster table export - schema-faithful mock generated by generate_hcmo_instance.py; no real animals\n")
        handle.write(f"Interval: {INTERVAL_MIN} min; Boxes: {len(ANIMALS)}; Start: {START.strftime('%d.%m.%Y %H:%M:%S')} (UTC+02:00)\n")
        writer = csv.DictWriter(handle, fieldnames=COLUMNS, delimiter=";", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def parse_row_time(row: dict[str, str]) -> datetime:
    return datetime.strptime(f"{row['Date']} {row['Time']}", "%d.%m.%Y %H:%M:%S").replace(tzinfo=TZ)


def main() -> int:
    rows = synthesize_rows()
    write_export(rows)

    ig = InstanceGraph(BASE, "tse")
    ig.dataset_note(
        "phenomaster-mock-export",
        label="Synthetic TSE PhenoMaster export (4 boxes, 3 h, 15-min intervals)",
        description=(
            "Schema-faithful synthetic PhenoMaster table export; values are generated, not measured. "
            "Column set reconstructed from the CalR TSE import specification and published supplementary tables."
        ),
        source="docs/hcm-systems/systems/tse-phenomaster/README.md",
        real_data=False,
    )

    vendor = ig.typed("tse-systems", SCHEMA.Organization, label="TSE Systems GmbH")
    control_unit = ig.hardware("phenomaster-control-unit", label="PhenoMaster control unit")
    ig.add(control_unit, SCHEMA.manufacturer, vendor)
    software = ig.software("phenomaster-software", label="PhenoMaster software (CaloSys, ActiMot, Drink/Feed modules)", runs_on=control_unit)
    calorimetry = ig.typed(
        "indirect-calorimetry-procedure", SOSA.Procedure,
        label="PhenoMaster open-circuit indirect calorimetry",
        comment="VO2 and VCO2 from the O2/CO2 differential between reference and box air at the configured flow; RER = VCO2/VO2; heat by the Weir equation.",
    )
    export_series = ig.time_series(
        "phenomaster-export-series",
        label="PhenoMaster table export, 4 animals, 15-min intervals",
        file_format="text/csv",
        storage_path="docs/hcm-systems/systems/tse-phenomaster/datasets/mock/phenomaster_mock_export.csv",
    )
    ig.add(export_series, PROV.wasAttributedTo, software)

    # observable properties
    p_vo2 = ig.observable_property("oxygen-consumption-rate", "oxygen consumption rate VO2")
    p_vco2 = ig.observable_property("carbon-dioxide-production-rate", "carbon dioxide production rate VCO2")
    p_rer = ig.observable_property("respiratory-exchange-ratio", "respiratory exchange ratio RER")
    p_heat = ig.observable_property("heat-production", "heat production (energy expenditure)")
    p_feed = ig.observable_property("cumulative-food-intake", "cumulative food intake")
    p_drink = ig.observable_property("cumulative-water-intake", "cumulative water intake")
    p_beams = ig.observable_property("horizontal-beam-breaks", "horizontal light-beam interruptions XT+YT")
    p_rear = ig.observable_property("rearing-beam-breaks", "vertical light-beam interruptions Z (rearing)")
    p_weight = ig.observable_property("body-weight", "body weight")
    p_temp = ig.environmental_property("box-air-temperature", "box air temperature")
    p_o2 = ig.environmental_property("box-oxygen-concentration", "box air oxygen concentration")
    p_co2 = ig.environmental_property("box-carbon-dioxide-concentration", "box air carbon dioxide concentration")

    gas_analyzer = ig.sensor(
        "gas-analyzer",
        label="PhenoMaster O2/CO2 gas analyzer (shared, sequential box sampling)",
        identifier="TSE-gas-analyzer-1",
        technology="paramagnetic O2 and infrared CO2 analysis",
        captures=[p_o2, p_co2, p_vo2, p_vco2, p_rer, p_heat],
    )
    ig.add(gas_analyzer, HCM_TECH.communicatesWith, control_unit)

    light_cycle = ig.light_cycle("light-cycle-12-12", dark_start="19:00:00", dark_hours=12, light_hours=12, label="12:12 light-dark cycle, dark from 19:00")
    temp_spec = ig.measurement_spec("temperature-target", p_temp, Decimal("22.5"), UNIT.DEG_C, "Box temperature target 22.5 degC")
    profile = ig.environment_profile("calorimetry-room-profile", label="Calorimetry room environment profile", light_cycle=light_cycle, specs=[temp_spec])

    subjects, boxes, sensors = {}, {}, {}
    run_start = START
    run_end = START + timedelta(minutes=INTERVAL_MIN * ROWS_PER_ANIMAL)
    for animal_no, box, sex, weight, enriched in ANIMALS:
        dims = ig.dimensions(f"box-{box}-dimensions", *BOX_DIMENSIONS_CM)
        enclosure = ig.enclosure(
            f"box-{box}",
            label=f"PhenoMaster calorimetry box {box}",
            identifier=f"Box {box}",
            dimensions=dims,
            manufacturer="TSE Systems GmbH",
            comment="Sealed home-cage calorimetry box; dimensions are assumed for the synthetic profile.",
        )
        ig.add(enclosure, HCM_ENV.hasEnvironment, profile)
        ig.add(enclosure, HCM_TECH.monitoredBy, gas_analyzer)
        if enriched:
            ig.add(enclosure, HCM.hasEnrichment, ig.enrichment(f"box-{box}-nesting", "nesting material", f"Nesting material in box {box}"))
        boxes[box] = enclosure
        sensors[box] = {
            "frame": ig.sensor(f"actimot-frame-{box}", label=f"ActiMot infrared light-beam frame, box {box}", identifier=f"TSE-actimot-{box}", technology="infrared light-beam interruption", installed_in=enclosure, captures=[p_beams, p_rear]),
            "feed": ig.sensor(f"feed-sensor-{box}", label=f"Feeding load cell, box {box}", identifier=f"TSE-feed-{box}", technology="load cell", installed_in=enclosure, captures=[p_feed]),
            "drink": ig.sensor(f"drink-sensor-{box}", label=f"Drinking load cell, box {box}", identifier=f"TSE-drink-{box}", technology="load cell", installed_in=enclosure, captures=[p_drink]),
            "weight": ig.sensor(f"weight-sensor-{box}", label=f"Body-weight platform, box {box}", identifier=f"TSE-weight-{box}", technology="load cell", installed_in=enclosure, captures=[p_weight]),
            "temp": ig.sensor(f"temp-sensor-{box}", label=f"Box temperature sensor, box {box}", identifier=f"TSE-temp-{box}", technology="thermistor", installed_in=enclosure, captures=[p_temp]),
        }
        subject = ig.subject(
            f"mouse-{animal_no}",
            label=f"Mouse {animal_no} (PhenoMaster animal no. {animal_no})",
            species="Mus musculus",
            strain="C57BL/6J",
            sex=sex,
            date_of_birth="2026-02-10",
        )
        ig.add(subject, DCTERMS.identifier, Literal(str(animal_no)))
        ig.housing(f"housing-mouse-{animal_no}", holder=subject, enclosure=enclosure, start=run_start - timedelta(days=1), end=run_end + timedelta(days=1))
        subjects[animal_no] = subject

    instants = {}

    def instant_for(when: datetime):
        if when not in instants:
            instants[when] = ig.instant(f"t-{when.strftime('%Y%m%dT%H%M')}", when)
        return instants[when]

    n_obs = 0
    for row in rows:
        when = parse_row_time(row)
        stamp = when.strftime("%Y%m%dT%H%M")
        bin_local = f"bin-{stamp}"
        interval = ig.iri(bin_local)
        if (interval, None, None) not in ig.g:
            interval = ig.typed(bin_local, TIME.Interval)
            ig.add(interval, TIME.hasBeginning, instant_for(when))
            ig.add(interval, TIME.hasEnd, instant_for(when + timedelta(minutes=INTERVAL_MIN)))
        animal_no = int(row["Animal No."])
        box = int(row["Box"])
        subject, enclosure, s = subjects[animal_no], boxes[box], sensors[box]

        def obs(local, cls, feature, sensor, prop, result, procedure=None):
            nonlocal n_obs
            ig.observation(f"{local}-{animal_no}-{stamp}", cls=cls, feature=feature, sensor=sensor, prop=prop, result=result, phenomenon_time=interval, occurs_in=enclosure, procedure=procedure)
            n_obs += 1

        obs("obs-vo2", SOSA.Observation, subject, gas_analyzer, p_vo2, ig.result_quantity(f"res-vo2-{animal_no}-{stamp}", row["VO2(1) [ml/h]"], UNIT["MilliL-PER-HR"]), calorimetry)
        obs("obs-vco2", SOSA.Observation, subject, gas_analyzer, p_vco2, ig.result_quantity(f"res-vco2-{animal_no}-{stamp}", row["VCO2(1) [ml/h]"], UNIT["MilliL-PER-HR"]), calorimetry)
        obs("obs-rer", SOSA.Observation, subject, gas_analyzer, p_rer, ig.result_quantity(f"res-rer-{animal_no}-{stamp}", row["RER"], UNIT.UNITLESS), calorimetry)
        obs("obs-heat", SOSA.Observation, subject, gas_analyzer, p_heat, ig.result_quantity(f"res-heat-{animal_no}-{stamp}", row["H(1) [kcal/h]"], UNIT["KiloCAL_TH-PER-HR"]), calorimetry)
        obs("obs-feed", SOSA.Observation, subject, s["feed"], p_feed, ig.result_quantity(f"res-feed-{animal_no}-{stamp}", row["Feed1 [g]"], UNIT.GM))
        obs("obs-drink", SOSA.Observation, subject, s["drink"], p_drink, ig.result_quantity(f"res-drink-{animal_no}-{stamp}", row["Drink1 [ml]"], UNIT.MilliL))
        obs("obs-beams", SOSA.Observation, subject, s["frame"], p_beams, ig.result_quantity(f"res-beams-{animal_no}-{stamp}", row["XT+YT [Cnt]"], UNIT.NUM))
        obs("obs-rearing", SOSA.Observation, subject, s["frame"], p_rear, ig.result_quantity(f"res-rearing-{animal_no}-{stamp}", row["Z [Cnt]"], UNIT.NUM))
        obs("obs-weight", HCM_OBS.WeightObservation, subject, s["weight"], p_weight, ig.result_quantity(f"res-weight-{animal_no}-{stamp}", row["Weight [g]"], UNIT.GM))
        obs("obs-temp", HCM_OBS.EnvironmentObservation, enclosure, s["temp"], p_temp, ig.result_quantity(f"res-temp-{animal_no}-{stamp}", row["Temp [°C]"], UNIT.DEG_C))
        obs("obs-o2", HCM_OBS.GasConcentrationObservation, enclosure, gas_analyzer, p_o2, ig.result_quantity(f"res-o2-{animal_no}-{stamp}", row["O2 [%]"], UNIT.PERCENT))
        obs("obs-co2", HCM_OBS.GasConcentrationObservation, enclosure, gas_analyzer, p_co2, ig.result_quantity(f"res-co2-{animal_no}-{stamp}", row["CO2 [%]"], UNIT.PERCENT))

    header = (
        "# GENERATED by docs/hcm-systems/systems/tse-phenomaster/generate_hcmo_instance.py — DO NOT EDIT\n"
        "# HCMO instance graph derived from a SYNTHETIC, schema-faithful TSE PhenoMaster export (no real animals).\n"
        f"# {len(ANIMALS)} single-housed animals, {ROWS_PER_ANIMAL} x {INTERVAL_MIN}-min intervals from {START.isoformat()}; {n_obs} observations.\n"
    )
    ig.serialize(OUT, header)
    print(f"wrote {OUT.relative_to(ROOT)}: {len(ig.g)} triples, {n_obs} observations; export {EXPORT.relative_to(ROOT)} ({len(rows)} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
