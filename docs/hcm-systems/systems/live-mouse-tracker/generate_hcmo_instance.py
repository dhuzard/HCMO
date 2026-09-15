#!/usr/bin/env python3
"""Generate a SYNTHETIC, schema-faithful Live Mouse Tracker (LMT) database and
the corresponding HCMO instance graph.

LMT (de Chaumont et al. 2019, https://micecraft.org/lmt) tracks groups of RFID-
tagged mice with a Kinect v2 depth camera and stores everything in one SQLite
file. The mock reproduces the table layout used by the ``lmt-analysis`` package
(``fdechaumont/lmt-analysis``, files ``Animal.py``, ``Event.py``,
``Detection.py``, ``BuildDataBaseIndex.py``):

  ANIMAL   (ID, RFID, NAME, GENOTYPE, AGE, SEX, STRAIN, SETUP)
  FRAME    (FRAMENUMBER, TIMESTAMP [ms epoch], PAUSED, NUMPARTICLE, TEMPERATURE,
            HUMIDITY, SOUND, LIGHTVISIBLE, LIGHTVISIBLEANDIR)
  DETECTION(ID, FRAMENUMBER, ANIMALID, MASS_X, MASS_Y, MASS_Z, FRONT_X, FRONT_Y,
            FRONT_Z, BACK_X, BACK_Y, BACK_Z, REARING, LOOK_UP, LOOK_DOWN, DATA)
  EVENT    (ID, NAME, DESCRIPTION, STARTFRAME, ENDFRAME, IDANIMALA, IDANIMALB,
            IDANIMALC, IDANIMALD, METADATA)

Event names are the exact strings written by the lmt-analysis event builders.
Coordinates are depth-image pixels as in LMT; the SETUP field records the
pixel-to-cm scale used here.

The committed artefacts are deterministic CSV dumps of the four tables under
``datasets/mock/`` (``DETECTION.csv.gz`` is gzip-compressed with a fixed
mtime). ``--sqlite PATH`` additionally writes a real SQLite file (not
committed: its bytes depend on the SQLite version).

Scenario (requested): one 50 x 50 cm arena, 4 male Shank3 mice (2 WT, 2 KO),
Kinect v2 at 30 frames/s, 16 RFID antennas under the floor, 12:12 light cycle
with dark from 19:00, cage change every 10 days. Ten minutes of full-rate
frames, detections and events are materialised (18:55-19:05, spanning the
light-to-dark transition); the housing history covers the 30-day experiment.

Output: ``examples/systems/live-mouse-tracker.ttl``
"""
from __future__ import annotations

import argparse
import csv
import gzip
import io
import math
import random
import sqlite3
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
    SEMTS,
    SOSA,
    TIME,
    UNIT,
    InstanceGraph,
)

MOCK_DIR = HERE / "datasets" / "mock"
OUT = ROOT / "examples" / "systems" / "live-mouse-tracker.ttl"
BASE = "https://w3id.org/hcmo/id/eval/live-mouse-tracker/"

TZ = timezone(timedelta(hours=2))
EXPERIMENT_START = datetime(2026, 5, 12, 10, 0, tzinfo=TZ)   # day 0: animals placed in the arena
EXPERIMENT_DAYS = 30
CAGE_CHANGE_EVERY_DAYS = 10
RECORDING_START = datetime(2026, 6, 2, 18, 55, tzinfo=TZ)
RECORDING_MINUTES = 10
FPS = 30
DARK_START_HOUR = 19
ARENA_CM = 50
ARENA_PX = 400            # depth-image pixels spanned by the arena floor
SCALE_CM_PER_PX = ARENA_CM / ARENA_PX
ARENA_DIMENSIONS_CM = (Decimal("50"), Decimal("50"), Decimal("30"))  # height assumed
RFID_ANTENNAS = 16

ANIMALS = [
    # ID, RFID, NAME, GENOTYPE, AGE (weeks), SEX, STRAIN
    (1, "000000000001", "Mouse A", "WT", "12", "male", "B6.129-Shank3tm2Gfng/J"),
    (2, "000000000002", "Mouse B", "WT", "12", "male", "B6.129-Shank3tm2Gfng/J"),
    (3, "000000000003", "Mouse C", "KO", "12", "male", "B6.129-Shank3tm2Gfng/J"),
    (4, "000000000004", "Mouse D", "KO", "12", "male", "B6.129-Shank3tm2Gfng/J"),
]
SETUP = f"LMT arena 50x50 cm, Kinect v2 30 fps, 16 RFID antennas, scale {SCALE_CM_PER_PX:.4f} cm/px"

# exact event names from the lmt-analysis BuildEvent* modules
SINGLE_EVENTS = ["Move isolated", "Stop isolated", "Rear isolated", "Center Zone", "Periphery Zone",
                 "Rear at periphery", "Rear in centerWindow", "Water Zone", "Move high speed"]
DYADIC_EVENTS = ["Contact", "Oral-oral Contact", "Oral-genital Contact", "Side by side Contact",
                 "Side by side Contact, opposite way", "Social approach", "Approach contact", "Get away",
                 "Social escape", "Approach rear", "Train2", "Move in contact", "Stop in contact",
                 "Rear in contact", "FollowZone Isolated", "Group2"]
TRIADIC_EVENTS = ["Group3", "Train3", "Nest3"]
QUAD_EVENTS = ["Group4", "Train4", "Nest4"]


def synthesize() -> tuple[list[tuple], list[tuple], list[tuple], list[tuple]]:
    rng = random.Random(20260602)
    n_frames = RECORDING_MINUTES * 60 * FPS
    t0_ms = int(RECORDING_START.timestamp() * 1000)
    frames, detections, events = [], [], []
    # per-animal random walk in pixels (arena 0..ARENA_PX)
    pos = {a[0]: [rng.uniform(60, 340), rng.uniform(60, 340)] for a in ANIMALS}
    heading = {a[0]: rng.uniform(0, 2 * math.pi) for a in ANIMALS}
    det_id = 0
    for f in range(1, n_frames + 1):
        ts = t0_ms + int(round((f - 1) * 1000 / FPS))
        dark = datetime.fromtimestamp(ts / 1000, TZ).hour >= DARK_START_HOUR
        frames.append((
            f, ts, 0, len(ANIMALS),
            round(rng.uniform(22.2, 22.8), 1), round(rng.uniform(48, 54), 1), round(rng.uniform(20, 60), 1),
            round(rng.uniform(1, 4), 1) if dark else round(rng.uniform(180, 220), 1),
            round(rng.uniform(140, 160), 1) if dark else round(rng.uniform(300, 340), 1),
        ))
        for animal_id in pos:
            if rng.random() < 0.05:
                heading[animal_id] += rng.uniform(-1.2, 1.2)
            step = rng.uniform(0, 1.6) if rng.random() < 0.55 else 0.0
            x = min(ARENA_PX - 10, max(10, pos[animal_id][0] + step * math.cos(heading[animal_id])))
            y = min(ARENA_PX - 10, max(10, pos[animal_id][1] + step * math.sin(heading[animal_id])))
            pos[animal_id] = [x, y]
            rearing = 1 if rng.random() < 0.03 else 0
            z = rng.uniform(55, 70) if rearing else rng.uniform(25, 35)
            fx, fy = x + 12 * math.cos(heading[animal_id]), y + 12 * math.sin(heading[animal_id])
            bx, by = x - 12 * math.cos(heading[animal_id]), y - 12 * math.sin(heading[animal_id])
            det_id += 1
            detections.append((det_id, f, animal_id, round(x, 1), round(y, 1), round(z, 1),
                               round(fx, 1), round(fy, 1), round(z, 1), round(bx, 1), round(by, 1), round(z * 0.9, 1),
                               rearing, 1 if rearing and rng.random() < 0.5 else 0, 0, None))
    # events: bouts drawn over the recording (frame-based), more social activity in the dark
    event_id = 0
    ids = [a[0] for a in ANIMALS]

    def add(name, start_f, dur_f, a, b=None, c=None, d=None):
        nonlocal event_id
        event_id += 1
        events.append((event_id, name, None, start_f, min(n_frames, start_f + dur_f), a, b, c, d, None))

    for animal_id in ids:
        f = 1
        while f < n_frames:
            name = rng.choice(SINGLE_EVENTS)
            dur = int(rng.uniform(0.5, 20) * FPS)
            add(name, f, dur, animal_id)
            f += dur + int(rng.uniform(0.2, 6) * FPS)
    f = 1
    while f < n_frames:
        a, b = rng.sample(ids, 2)
        name = rng.choice(DYADIC_EVENTS)
        dur = int(rng.uniform(0.3, 8) * FPS)
        add(name, f, dur, a, b)
        f += dur + int(rng.uniform(0.5, 4) * FPS)
    for name in TRIADIC_EVENTS:
        for _ in range(3):
            a, b, c = rng.sample(ids, 3)
            add(name, rng.randint(1, n_frames - 300), int(rng.uniform(2, 30) * FPS), a, b, c)
    for name in QUAD_EVENTS:
        for _ in range(2):
            a, b, c, d = rng.sample(ids, 4)
            add(name, rng.randint(1, n_frames - 300), int(rng.uniform(5, 60) * FPS), a, b, c, d)
    events.sort(key=lambda e: (e[3], e[0]))
    animals = [(*a, SETUP) for a in ANIMALS]
    return animals, frames, detections, events


TABLES = {
    "ANIMAL": ["ID", "RFID", "NAME", "GENOTYPE", "AGE", "SEX", "STRAIN", "SETUP"],
    "FRAME": ["FRAMENUMBER", "TIMESTAMP", "PAUSED", "NUMPARTICLE", "TEMPERATURE", "HUMIDITY", "SOUND", "LIGHTVISIBLE", "LIGHTVISIBLEANDIR"],
    "DETECTION": ["ID", "FRAMENUMBER", "ANIMALID", "MASS_X", "MASS_Y", "MASS_Z", "FRONT_X", "FRONT_Y", "FRONT_Z", "BACK_X", "BACK_Y", "BACK_Z", "REARING", "LOOK_UP", "LOOK_DOWN", "DATA"],
    "EVENT": ["ID", "NAME", "DESCRIPTION", "STARTFRAME", "ENDFRAME", "IDANIMALA", "IDANIMALB", "IDANIMALC", "IDANIMALD", "METADATA"],
}


def write_csv_tables(animals, frames, detections, events) -> None:
    MOCK_DIR.mkdir(parents=True, exist_ok=True)
    for name, rows in (("ANIMAL", animals), ("FRAME", frames), ("EVENT", events)):
        with (MOCK_DIR / f"{name}.csv").open("w", encoding="utf-8", newline="\n") as handle:
            writer = csv.writer(handle, lineterminator="\n")
            writer.writerow(TABLES[name])
            writer.writerows(["" if v is None else v for v in row] for row in rows)
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(TABLES["DETECTION"])
    writer.writerows(["" if v is None else v for v in row] for row in detections)
    with gzip.GzipFile(MOCK_DIR / "DETECTION.csv.gz", "wb", mtime=0) as handle:
        handle.write(buffer.getvalue().encode("utf-8"))


def write_sqlite(path: Path, animals, frames, detections, events) -> None:
    if path.exists():
        path.unlink()
    conn = sqlite3.connect(path)
    conn.execute("CREATE TABLE ANIMAL (ID INTEGER PRIMARY KEY, RFID TEXT, NAME TEXT, GENOTYPE TEXT, AGE TEXT, SEX TEXT, STRAIN TEXT, SETUP TEXT)")
    conn.execute("CREATE TABLE FRAME (FRAMENUMBER INTEGER PRIMARY KEY, TIMESTAMP INTEGER, PAUSED INTEGER, NUMPARTICLE INTEGER, TEMPERATURE REAL, HUMIDITY REAL, SOUND REAL, LIGHTVISIBLE REAL, LIGHTVISIBLEANDIR REAL)")
    conn.execute("CREATE TABLE DETECTION (ID INTEGER PRIMARY KEY, FRAMENUMBER INTEGER, ANIMALID INTEGER, MASS_X REAL, MASS_Y REAL, MASS_Z REAL, FRONT_X REAL, FRONT_Y REAL, FRONT_Z REAL, BACK_X REAL, BACK_Y REAL, BACK_Z REAL, REARING INTEGER, LOOK_UP INTEGER, LOOK_DOWN INTEGER, DATA BLOB)")
    conn.execute("CREATE TABLE EVENT (ID INTEGER PRIMARY KEY, NAME TEXT, DESCRIPTION TEXT, STARTFRAME INTEGER, ENDFRAME INTEGER, IDANIMALA INTEGER, IDANIMALB INTEGER, IDANIMALC INTEGER, IDANIMALD INTEGER, METADATA TEXT)")
    conn.executemany("INSERT INTO ANIMAL VALUES (?,?,?,?,?,?,?,?)", animals)
    conn.executemany("INSERT INTO FRAME VALUES (?,?,?,?,?,?,?,?,?)", frames)
    conn.executemany("INSERT INTO DETECTION VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", detections)
    conn.executemany("INSERT INTO EVENT VALUES (?,?,?,?,?,?,?,?,?,?)", events)
    conn.commit()
    conn.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sqlite", type=Path, help="also write a real LMT-style SQLite file here (not committed)")
    args = parser.parse_args()

    animals, frames, detections, events = synthesize()
    write_csv_tables(animals, frames, detections, events)
    if args.sqlite:
        write_sqlite(args.sqlite, animals, frames, detections, events)

    ig = InstanceGraph(BASE, "lmt")
    ig.dataset_note(
        "lmt-mock-database",
        label="Synthetic LMT SQLite database (Shank3 scenario, 10 min at 30 fps)",
        description="Schema-faithful synthetic ANIMAL/FRAME/DETECTION/EVENT tables following the lmt-analysis layout; positions, sensor values and events are generated, not recorded.",
        source="docs/hcm-systems/systems/live-mouse-tracker/README.md",
        real_data=False,
    )

    lmt_software = ig.software("lmt-software", label="Live Mouse Tracker acquisition and tracking software (MiceCraft)")
    analysis = ig.software("lmt-analysis", label="lmt-analysis event builders (Python)")
    workstation = ig.hardware("lmt-workstation", label="LMT acquisition computer")
    ig.add(lmt_software, HCM_TECH.runsOn, workstation)
    ig.add(analysis, HCM_TECH.runsOn, workstation)
    tracking = ig.typed("depth-tracking-procedure", SOSA.Procedure, label="LMT real-time depth segmentation, identity assignment by RFID and machine learning",
                        comment="Per-frame mass, front and back points and rearing/look-up/look-down flags from the Kinect v2 depth image; identities fused from the RFID antenna grid.")
    event_building = ig.typed("event-building-procedure", SOSA.Procedure, label="lmt-analysis event detection (Rebuild_All_Events)",
                              comment="Frame-based behavioural events built from detections: individual, dyadic, triadic and group events with the exact lmt-analysis names.")

    for table in TABLES:
        path = MOCK_DIR / (f"{table}.csv.gz" if table == "DETECTION" else f"{table}.csv")
        series = ig.time_series(f"lmt-table-{table.lower()}", label=f"LMT {table} table (SQLite dump)", file_format="text/csv" if table != "DETECTION" else "application/gzip",
                                storage_path=path.relative_to(ROOT).as_posix(), sampling_rate_hz=FPS if table in ("FRAME", "DETECTION") else None)
        ig.add(series, PROV.wasAttributedTo, lmt_software if table != "EVENT" else analysis)

    p_position = ig.observable_property("body-position-3d", "mass, front and back points (depth-image pixels, height)")
    p_behavior = ig.observable_property("lmt-event", "LMT behavioural event")
    p_temp = ig.environmental_property("arena-temperature", "arena temperature (LMT sensor board)")
    p_rh = ig.environmental_property("arena-humidity", "arena relative humidity (LMT sensor board)")
    p_sound = ig.environmental_property("arena-sound-level", "arena sound level index (LMT sensor board)")
    p_light = ig.environmental_property("arena-visible-light", "arena visible light index (LMT sensor board)")
    p_light_ir = ig.environmental_property("arena-visible-and-infrared-light", "arena visible+infrared light index (LMT sensor board)")

    light_cycle = ig.light_cycle("light-cycle-12-12", dark_start="19:00:00", dark_hours=12, light_hours=12, label="12:12 light-dark cycle, dark from 19:00")
    profile = ig.environment_profile("lmt-room-profile", label="LMT room environment profile", light_cycle=light_cycle,
                                     specs=[ig.measurement_spec("arena-temperature-target", p_temp, Decimal("22.5"), UNIT.DEG_C, "Arena temperature target 22.5 degC")])

    dims = ig.dimensions("arena-dimensions", *ARENA_DIMENSIONS_CM)
    arena = ig.enclosure("arena-1", label="LMT arena 1 (50 x 50 cm home cage)", identifier="LMT-arena-1", dimensions=dims,
                         comment="Open-top 50 x 50 cm cage with bedding; Kinect v2 above, 16 RFID antennas under the floor; height assumed.")
    ig.add(arena, HCM_ENV.hasEnvironment, profile)
    ig.add(arena, HCM.hasEnrichment, ig.enrichment("arena-1-house", "house", "Plastic house in the arena"))
    ig.add(arena, HCM.hasEnrichment, ig.enrichment("arena-1-nesting", "nesting material", "Nesting material in the arena"))
    kinect = ig.sensor("kinect-v2", label="Kinect v2 depth camera above arena 1", identifier="LMT-kinect-1", technology="time-of-flight infrared depth imaging",
                       sensor_type="depth camera", model_number="Kinect v2", sampling_rate_hz=FPS, installed_in=arena, captures=[p_position, p_behavior])
    ig.add(kinect, HCM_TECH.communicatesWith, workstation)
    env_board = ig.sensor("sensor-board", label="LMT environmental sensor board (temperature, humidity, sound, light)", identifier="LMT-sensors-1",
                          technology="temperature, humidity, sound and light sensors", installed_in=arena, captures=[p_temp, p_rh, p_sound, p_light, p_light_ir])
    ig.add(env_board, HCM_TECH.communicatesWith, workstation)
    p_identity = ig.observable_property("animal-identity", "animal identity from RFID transponder reads")
    for n in range(1, RFID_ANTENNAS + 1):
        antenna = ig.sensor(f"rfid-antenna-{n:02d}", label=f"RFID antenna {n} (4 x 4 grid under the floor)", identifier=f"LMT-rfid-{n:02d}",
                            technology="low-frequency RFID reader", installed_in=arena, captures=[p_identity])
        ig.add(antenna, HCM_TECH.communicatesWith, workstation)

    experiment_end = EXPERIMENT_START + timedelta(days=EXPERIMENT_DAYS)
    groups = {g: ig.group(f"shank3-{g.lower()}", label=f"Shank3 {g} group", comment=f"Genotype {g}; genotype is recorded as group membership because HCMO 0.3.0 has no genotype property.") for g in ("WT", "KO")}
    subjects = {}
    for animal_id, rfid, name, genotype, age, sex, strain, _ in animals:
        subject = ig.subject(f"mouse-{animal_id}", label=f"{name} (LMT ANIMAL.ID {animal_id})", species="Mus musculus", strain=strain, sex=sex,
                             date_of_birth=(EXPERIMENT_START - timedelta(weeks=int(age))).date().isoformat(), group=groups[genotype])
        ig.add(subject, DCTERMS.identifier, Literal(rfid))
        ig.housing(f"housing-mouse-{animal_id}", holder=subject, enclosure=arena, start=EXPERIMENT_START, end=experiment_end)
        subjects[animal_id] = subject
    n_changes = 0
    for day in range(CAGE_CHANGE_EVERY_DAYS, EXPERIMENT_DAYS, CAGE_CHANGE_EVERY_DAYS):
        start = EXPERIMENT_START + timedelta(days=day)
        change = ig.typed(f"cage-change-day-{day}", PROV.Activity, label=f"Bedding change of arena 1 on experiment day {day} (every {CAGE_CHANGE_EVERY_DAYS} days)")
        ig.add(change, PROV.used, arena)
        ig.add(change, TIME.hasTime, ig.interval(f"cage-change-day-{day}-time", start, start + timedelta(minutes=30)))
        n_changes += 1

    frame_time = {f[0]: datetime.fromtimestamp(f[1] / 1000, TZ) for f in frames}

    # per-animal detection tables (SemTS segments)
    for animal_id, subject in subjects.items():
        table = ig.typed(f"detection-table-{animal_id}", HCM_OBS.LocationResultTable, label=f"DETECTION rows for ANIMALID {animal_id} ({RECORDING_MINUTES} min at {FPS} fps)")
        for column in ("MASS_X", "MASS_Y", "MASS_Z", "FRONT_X", "FRONT_Y", "FRONT_Z", "BACK_X", "BACK_Y", "BACK_Z", "REARING"):
            dim = ig.iri(f"dimension-{column.lower().replace('_', '-')}")
            if (dim, None, None) not in ig.g:
                ig.typed(f"dimension-{column.lower().replace('_', '-')}", SEMTS.DataDimension, label=f"{column} [{'px' if column.endswith(('X', 'Y')) else 'mm' if column.endswith('Z') else 'flag'}]")
            ig.add(table, SEMTS.segmentDimension, dim)
        ig.add(table, PROV.wasDerivedFrom, ig.iri("lmt-table-detection"))
        interval = ig.interval(f"recording-window-{animal_id}", RECORDING_START, RECORDING_START + timedelta(minutes=RECORDING_MINUTES), duration_unit=TIME.unitMinute)
        ig.observation(f"obs-track-{animal_id}", cls=SOSA.Observation, feature=subject, sensor=kinect, prop=p_position, result=table,
                       phenomenon_time=interval, occurs_in=arena, procedure=tracking)

    # events -> one behaviour observation per participating animal, sharing the result
    n_behavior = 0
    for event_id, name, _, start_f, end_f, a, b, c, d in [(e[0], e[1], e[2], e[3], e[4], e[5], e[6], e[7], e[8]) for e in events]:
        participants = [p for p in (a, b, c, d) if p is not None]
        start, end = frame_time[start_f], frame_time[min(end_f, len(frames))]
        if end <= start:
            end = start + timedelta(milliseconds=int(1000 / FPS))
        interval = ig.interval(f"event-{event_id}-time", start, end, duration_unit=TIME.unitSecond)
        result = ig.behavior_result(f"res-event-{event_id}", name)
        if len(participants) > 1:
            ig.add(result, DCTERMS.description, Literal("participants IDANIMALA..D: " + ", ".join(str(p) for p in participants)))
        for p in participants:
            ig.observation(f"obs-event-{event_id}-animal-{p}", cls=HCM_OBS.BehaviorObservation, feature=subjects[p], sensor=kinect, prop=p_behavior,
                           result=result, phenomenon_time=interval, occurs_in=arena, procedure=event_building)
            n_behavior += 1

    # FRAME sensor columns -> one environment observation per minute (mean of the frames)
    n_env = 0
    per_minute: dict[int, list] = {}
    for f in frames:
        per_minute.setdefault((f[0] - 1) // (60 * FPS), []).append(f)
    for minute, rows in sorted(per_minute.items()):
        when = RECORDING_START + timedelta(minutes=minute)
        interval = ig.interval(f"frame-minute-{minute}", when, when + timedelta(minutes=1))
        for idx, key, prop, unit in ((4, "temp", p_temp, UNIT.DEG_C), (5, "rh", p_rh, UNIT.PERCENT), (6, "sound", p_sound, UNIT.UNITLESS),
                                     (7, "light", p_light, UNIT.UNITLESS), (8, "light-ir", p_light_ir, UNIT.UNITLESS)):
            mean = Decimal(str(round(sum(r[idx] for r in rows) / len(rows), 2)))
            result = ig.result_quantity(f"res-{key}-minute-{minute}", mean, unit)
            ig.observation(f"obs-{key}-minute-{minute}", cls=HCM_OBS.EnvironmentObservation, feature=arena, sensor=env_board, prop=prop, result=result,
                           phenomenon_time=interval, occurs_in=arena)
            n_env += 1

    header = (
        "# GENERATED by docs/hcm-systems/systems/live-mouse-tracker/generate_hcmo_instance.py — DO NOT EDIT\n"
        "# HCMO instance graph derived from a SYNTHETIC, schema-faithful Live Mouse Tracker database (no real animals).\n"
        f"# 4 male Shank3 mice (2 WT, 2 KO) in one 50 x 50 cm arena; {RECORDING_MINUTES} min at {FPS} fps from {RECORDING_START.isoformat()};\n"
        f"# {len(events)} events -> {n_behavior} behaviour observations, {n_env} environment observations, {len(frames)} frames, {len(detections)} detections.\n"
    )
    ig.serialize(OUT, header)
    print(f"wrote {OUT.relative_to(ROOT)}: {len(ig.g)} triples; {len(events)} events -> {n_behavior} behaviour obs, {n_env} env obs, {len(frames)} frames, {len(detections)} detections, {n_changes} cage changes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
