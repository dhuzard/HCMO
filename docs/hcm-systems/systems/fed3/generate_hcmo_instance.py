#!/usr/bin/env python3
"""Generate a SYNTHETIC, schema-faithful FED3 log and its HCMO instance graph.

FED3 (Feeding Experimentation Device 3; Matikainen-Ankney et al., eLife 2021)
is an open-source operant home-cage feeding device that logs one CSV row per
event (nose-poke or pellet) to its SD card. The mock ``FED001_060226_00.CSV``
follows the FED3 library column layout:

  MM:DD:YYYY hh:mm:ss, Library_Version, Session_type, Device_Number,
  Battery_Voltage, Motor_Turns, FR, Event, Active_Poke, Left_Poke_Count,
  Right_Poke_Count, Pellet_Count, Block_Pellet_Count, Retrieval_Time,
  InterPellet_Interval, Poke_Time

Output: ``examples/systems/fed3.ttl``

Modelling decisions (see ``hcmo-mapping.tsv`` and ``README.md``):
  * standard shoebox cage holding the FED3 -> hcm:MonitoredEnclosure
  * the device -> hcm-tech:Hardware (firmware = Library_Version); its two
    nose-poke photointerrupters and the pellet-well photointerrupter are
    hcm-tech:Sensor; the pellet dispenser stepper motor is hcm-tech:Actuator
  * each nose-poke row -> sosa:Observation about the mouse with an
    hcm-obs:CategoricalResult (left/right) and a Poke_Time-long phenomenon time
  * each pellet row -> sosa:Observation whose hcm-obs:QuantityValue result is the
    retrieval latency (Retrieval_Time, s) and whose phenomenon time spans from
    dispensing to retrieval
  * FR schedule / active poke -> a sosa:Procedure referenced by every observation
  * the 3-h session spans the light-to-dark transition (dark from 19:00)

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
    HCM_TECH,
    PROV,
    SCHEMA,
    SOSA,
    TIME,
    UNIT,
    InstanceGraph,
)

MOCK_DIR = HERE / "datasets" / "mock"
LOG = MOCK_DIR / "FED001_060226_00.CSV"
OUT = ROOT / "examples" / "systems" / "fed3.ttl"
BASE = "https://w3id.org/hcmo/id/eval/fed3/"

TZ = timezone(timedelta(hours=2))
START = datetime(2026, 6, 2, 18, 30, tzinfo=TZ)
SESSION_HOURS = 3
DARK_START_HOUR = 19
LIBRARY_VERSION = "1.16.3"
DEVICE_NUMBER = 1
# Assumed standard mouse shoebox cage inner dimensions (cm) for the synthetic profile.
CAGE_DIMENSIONS_CM = (Decimal("19.5"), Decimal("32.5"), Decimal("13.0"))
COLUMNS = [
    "MM:DD:YYYY hh:mm:ss", "Library_Version", "Session_type", "Device_Number", "Battery_Voltage",
    "Motor_Turns", "FR", "Event", "Active_Poke", "Left_Poke_Count", "Right_Poke_Count",
    "Pellet_Count", "Block_Pellet_Count", "Retrieval_Time", "InterPellet_Interval", "Poke_Time",
]


def synthesize() -> list[dict[str, str]]:
    rng = random.Random(20260602)
    rows: list[dict[str, str]] = []
    t = START
    end = START + timedelta(hours=SESSION_HOURS)
    left = right = pellets = 0
    battery = 4.12
    last_pellet: datetime | None = None
    while True:
        dark = t.hour >= DARK_START_HOUR
        t += timedelta(seconds=rng.uniform(40, 260) * (0.45 if dark else 1.0))
        if t >= end:
            break
        battery -= 0.0004
        poke_time = round(rng.uniform(0.12, 1.4), 2)
        if rng.random() < 0.15:
            right += 1
            rows.append(_row(t, battery, "Right", left, right, pellets, "", "", poke_time))
            continue
        left += 1
        rows.append(_row(t, battery, "Left", left, right, pellets, "", "", poke_time))
        # FR1: the active (left) poke dispenses a pellet, retrieved after a latency
        pellets += 1
        retrieval = round(rng.uniform(0.8, 45.0), 2)
        dispensed = t + timedelta(seconds=rng.uniform(0.3, 0.8))
        ipi = "" if last_pellet is None else f"{(dispensed - last_pellet).total_seconds():.2f}"
        rows.append(_row(dispensed, battery, "Pellet", left, right, pellets, f"{retrieval:.2f}", ipi, ""))
        last_pellet = dispensed
        t = dispensed + timedelta(seconds=retrieval)
    return rows


def _row(t, battery, event, left, right, pellets, retrieval, ipi, poke_time) -> dict[str, str]:
    return {
        "MM:DD:YYYY hh:mm:ss": t.strftime("%m/%d/%Y %H:%M:%S"),
        "Library_Version": LIBRARY_VERSION,
        "Session_type": "FR1",
        "Device_Number": str(DEVICE_NUMBER),
        "Battery_Voltage": f"{battery:.2f}",
        "Motor_Turns": str(pellets),
        "FR": "1",
        "Event": event,
        "Active_Poke": "Left",
        "Left_Poke_Count": str(left),
        "Right_Poke_Count": str(right),
        "Pellet_Count": str(pellets),
        "Block_Pellet_Count": str(pellets),
        "Retrieval_Time": retrieval,
        "InterPellet_Interval": ipi,
        "Poke_Time": "" if poke_time == "" else f"{poke_time:.2f}",
    }


def write_log(rows: list[dict[str, str]]) -> None:
    MOCK_DIR.mkdir(parents=True, exist_ok=True)
    with LOG.open("w", encoding="utf-8", newline="\n") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def parse_time(text: str) -> datetime:
    return datetime.strptime(text, "%m/%d/%Y %H:%M:%S").replace(tzinfo=TZ)


def main() -> int:
    rows = synthesize()
    write_log(rows)

    ig = InstanceGraph(BASE, "fed")
    ig.dataset_note(
        "fed3-mock-log",
        label="Synthetic FED3 event log (FR1, 3 h)",
        description="Schema-faithful synthetic FED3 SD-card log following the FED3 library column layout; events are generated, not recorded. The file name mimics FED<device>_<MMDDYY>_<session>.CSV.",
        source="docs/hcm-systems/systems/fed3/README.md",
        real_data=False,
    )

    device = ig.hardware("fed3-device-1", label="FED3 device 1 (open-source operant feeder)", model_number="FED3", firmware=LIBRARY_VERSION)
    ig.add(device, DCTERMS.identifier, Literal(str(DEVICE_NUMBER)))
    ig.add(device, RDFS.comment, Literal("Battery-powered Adafruit Feather M0 Adalogger based device; logs to SD card. Library_Version is recorded as firmware."))
    procedure = ig.typed("fr1-left-active", SOSA.Procedure, label="FED3 session type FR1, active poke Left",
                         comment="Fixed-ratio 1: every active (left) nose-poke dispenses one 20-mg pellet; right pokes are recorded but not rewarded.")
    log_series = ig.time_series("fed3-log-series", label="FED3 SD-card event log FED001_060226_00.CSV", file_format="text/csv",
                                storage_path="docs/hcm-systems/systems/fed3/datasets/mock/FED001_060226_00.CSV")
    ig.add(log_series, PROV.wasAttributedTo, device)

    p_poke = ig.observable_property("nose-poke-event", "nose-poke event (left or right port)")
    p_retrieval = ig.observable_property("pellet-retrieval-latency", "pellet retrieval latency")

    light_cycle = ig.light_cycle("light-cycle-12-12", dark_start="19:00:00", dark_hours=12, light_hours=12, label="12:12 light-dark cycle, dark from 19:00")
    profile = ig.environment_profile("holding-room-profile", label="Holding room environment profile", light_cycle=light_cycle)

    dims = ig.dimensions("cage-fed-1-dimensions", *CAGE_DIMENSIONS_CM)
    cage = ig.enclosure("cage-fed-1", label="Home cage with FED3 device 1", identifier="FED-cage-1", dimensions=dims,
                        comment="Standard mouse shoebox cage; the FED3 sits inside the cage. Dimensions are assumed for the synthetic profile.")
    ig.add(cage, HCM_ENV.hasEnvironment, profile)
    ig.add(cage, HCM.hasEnrichment, ig.enrichment("cage-fed-1-nesting", "nesting material", "Nesting material in the FED3 cage"))
    ig.add(device, HCM_TECH.supportsEnclosure, cage)
    ig.actuator("fed3-pellet-dispenser", label="FED3 pellet dispenser stepper motor", enclosure=cage)
    left_port = ig.sensor("fed3-left-poke-sensor", label="FED3 left nose-poke photointerrupter", identifier="FED3-1-left-poke", technology="infrared photointerrupter", installed_in=cage, captures=[p_poke])
    right_port = ig.sensor("fed3-right-poke-sensor", label="FED3 right nose-poke photointerrupter", identifier="FED3-1-right-poke", technology="infrared photointerrupter", installed_in=cage, captures=[p_poke])
    well = ig.sensor("fed3-pellet-well-sensor", label="FED3 pellet-well photointerrupter", identifier="FED3-1-pellet-well", technology="infrared photointerrupter", installed_in=cage, captures=[p_retrieval])
    for sensor in (left_port, right_port, well):
        ig.add(sensor, HCM_TECH.communicatesWith, device)

    mouse = ig.subject("mouse-1", label="Mouse 1 (FED3 device 1)", species="Mus musculus", strain="C57BL/6J", sex="male", date_of_birth="2026-01-05")
    ig.add(mouse, DCTERMS.identifier, Literal("FED3-1-mouse"))
    ig.housing("housing-mouse-1", holder=mouse, enclosure=cage, start=START - timedelta(days=7), end=START + timedelta(days=7))

    n_pokes = n_pellets = 0
    for index, row in enumerate(rows, start=1):
        when = parse_time(row["MM:DD:YYYY hh:mm:ss"])
        if row["Event"] in ("Left", "Right"):
            duration = float(row["Poke_Time"])
            interval = ig.interval(f"poke-{index}-time", when, when + timedelta(seconds=duration), duration_unit=TIME.unitSecond)
            sensor = left_port if row["Event"] == "Left" else right_port
            result = ig.categorical_result(f"res-poke-{index}", f"{row['Event'].lower()} nose-poke")
            ig.observation(f"obs-poke-{index}", cls=SOSA.Observation, feature=mouse, sensor=sensor, prop=p_poke, result=result,
                           phenomenon_time=interval, occurs_in=cage, procedure=procedure)
            n_pokes += 1
        else:
            latency = float(row["Retrieval_Time"])
            interval = ig.interval(f"pellet-{index}-time", when, when + timedelta(seconds=latency), duration_unit=TIME.unitSecond)
            result = ig.result_quantity(f"res-pellet-{index}", row["Retrieval_Time"], UNIT.SEC)
            ig.observation(f"obs-pellet-{index}", cls=SOSA.Observation, feature=mouse, sensor=well, prop=p_retrieval, result=result,
                           phenomenon_time=interval, occurs_in=cage, procedure=procedure)
            n_pellets += 1

    header = (
        "# GENERATED by docs/hcm-systems/systems/fed3/generate_hcmo_instance.py — DO NOT EDIT\n"
        "# HCMO instance graph derived from a SYNTHETIC, schema-faithful FED3 event log (no real animals).\n"
        f"# One single-housed mouse, FR1 session of {SESSION_HOURS} h from {START.isoformat()}; {n_pokes} nose-poke and {n_pellets} pellet observations.\n"
    )
    ig.serialize(OUT, header)
    print(f"wrote {OUT.relative_to(ROOT)}: {len(ig.g)} triples, {n_pokes} poke + {n_pellets} pellet observations; log {LOG.relative_to(ROOT)} ({len(rows)} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
