#!/usr/bin/env python3
"""Generate SYNTHETIC, schema-faithful Noldus PhenoTyper / EthoVision XT exports
and the corresponding HCMO instance graph.

No real PhenoTyper recordings were available for redistribution. Three mock
files under ``datasets/mock/`` reproduce the documented shapes of EthoVision XT
exports:

  * ``ethovision_track_sample_arena1.csv`` raw centre-point track (25 samples/s,
    20 s) with the EthoVision header block, unit row and ``Trial time``,
    ``Recording time``, ``X center``, ``Y center``, ``Area``, ``Distance moved``,
    ``Velocity``, ``In zone(Shelter / center-point)``, ``Movement(Moving / center-point)``
  * ``ethovision_time_bins.csv``     Statistics & Charts export, 1-min bins
  * ``ethovision_behavior_events.csv`` Behavior Recognition event log

Output: ``examples/systems/noldus-phenotyper.ttl``

Modelling decisions (see ``hcmo-mapping.tsv`` and ``README.md``):
  * PhenoTyper 3000 cage + top unit -> hcm:MonitoredEnclosure, IR camera
    hcm-tech:Sensor, white/IR LED hcm-tech:Actuator, shelter hcm:Enrichment
  * per-bin distance/velocity/shelter/moving -> sosa:Observation with
    hcm-obs:QuantityValue results (derived by EthoVision, sosa:usedProcedure)
  * recognised behaviours -> hcm-obs:BehaviorObservation + BehaviorResult
  * the raw track sample -> hcm-obs:LocationResultTable (SemTS segment with
    X/Y data dimensions) that is the result of one tracking observation
  * the run spans the light-to-dark transition of a 12:12 cycle (dark 19:00)

Deterministic (fixed seed). Standard library + rdflib only.
"""
from __future__ import annotations

import csv
import math
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
    SEMTS,
    SOSA,
    TIME,
    UNIT,
    InstanceGraph,
)

MOCK_DIR = HERE / "datasets" / "mock"
TRACK = MOCK_DIR / "ethovision_track_sample_arena1.csv"
BINS = MOCK_DIR / "ethovision_time_bins.csv"
EVENTS = MOCK_DIR / "ethovision_behavior_events.csv"
OUT = ROOT / "examples" / "systems" / "noldus-phenotyper.ttl"
BASE = "https://w3id.org/hcmo/id/eval/noldus-phenotyper/"

TZ = timezone(timedelta(hours=2))
START = datetime(2026, 6, 2, 18, 0, tzinfo=TZ)
BIN_MIN = 1
BINS_PER_ARENA = 120  # 2 hours
DARK_START_HOUR = 19
SAMPLE_RATE = 25  # samples per second
TRACK_SECONDS = 20
ARENAS = [(1, "female", "mouse-1"), (2, "female", "mouse-2")]
# PhenoTyper 3000: 30 x 30 cm floor, 35 cm high (vendor specification).
ARENA_DIMENSIONS_CM = (Decimal("30"), Decimal("30"), Decimal("35"))
BEHAVIORS = ["grooming", "rearing supported", "rearing unsupported", "eating", "sniffing"]


def synthesize() -> tuple[list[dict], list[dict], list[dict]]:
    rng = random.Random(20260602)
    bins, events, track = [], [], []
    for arena, _, subject in ARENAS:
        for index in range(BINS_PER_ARENA):
            when = START + timedelta(minutes=index * BIN_MIN)
            dark = when.hour >= DARK_START_HOUR
            distance = rng.uniform(40, 220) * (2.2 if dark else 1.0)
            shelter = rng.uniform(0, 40) if dark else rng.uniform(15, 58)
            moving = max(0.0, min(60.0 - shelter, rng.uniform(5, 45) * (1.6 if dark else 1.0)))
            bins.append({
                "Trial": "1",
                "Arena": str(arena),
                "Subject": subject,
                "Bin start": when.strftime("%Y-%m-%d %H:%M:%S"),
                "Bin duration [s]": "60",
                "Distance moved [cm]": f"{distance:.2f}",
                "Velocity mean [cm/s]": f"{distance / 60:.3f}",
                "In zone(Shelter / center-point) duration [s]": f"{shelter:.2f}",
                "Movement(Moving / center-point) duration [s]": f"{moving:.2f}",
            })
        t = 0.0
        while t < BINS_PER_ARENA * 60:
            t += rng.uniform(90, 420)
            if t >= BINS_PER_ARENA * 60:
                break
            behavior = rng.choice(BEHAVIORS)
            duration = rng.uniform(1.5, 25.0)
            events.append({
                "Trial": "1",
                "Arena": str(arena),
                "Subject": subject,
                "Behavior": behavior,
                "Start [s]": f"{t:.2f}",
                "Stop [s]": f"{t + duration:.2f}",
            })
    # raw track sample for arena 1
    x, y = 15.0, 15.0
    prev = (x, y)
    for i in range(SAMPLE_RATE * TRACK_SECONDS):
        seconds = i / SAMPLE_RATE
        angle = rng.uniform(0, 2 * math.pi)
        step = rng.uniform(0, 0.6)
        x = min(29.0, max(1.0, x + step * math.cos(angle)))
        y = min(29.0, max(1.0, y + step * math.sin(angle)))
        moved = math.dist(prev, (x, y))
        prev = (x, y)
        in_shelter = 1 if (x < 8 and y < 8) else 0
        track.append({
            "Trial time": f"{seconds:.2f}",
            "Recording time": f"{seconds:.2f}",
            "X center": f"{x:.3f}",
            "Y center": f"{y:.3f}",
            "Area": f"{rng.uniform(5.5, 7.5):.2f}",
            "Distance moved": f"{moved:.3f}",
            "Velocity": f"{moved * SAMPLE_RATE:.3f}",
            "In zone(Shelter / center-point)": str(in_shelter),
            "Movement(Moving / center-point)": "1" if moved * SAMPLE_RATE > 2.0 else "0",
        })
    return bins, events, track


def write_exports(bins, events, track) -> None:
    MOCK_DIR.mkdir(parents=True, exist_ok=True)
    with TRACK.open("w", encoding="utf-8", newline="\n") as handle:
        header = [
            ("Number of header lines:", "12"),
            ("Experiment", "SYNTHETIC PhenoTyper home-cage trial (schema-faithful mock, no real animals)"),
            ("Trial name", "Trial     1"),
            ("Trial ID", "1"),
            ("Arena name", "Arena 1"),
            ("Subject", "mouse-1"),
            ("Start time", START.strftime("%d/%m/%Y %H:%M:%S")),
            ("Sample rate", f"{SAMPLE_RATE}.00"),
            ("Video file", "Trial1_Arena1.mpg"),
            ("Tracking source", "PhenoTyper top unit IR camera"),
            ("Missing values", "-"),
        ]
        writer = csv.writer(handle, lineterminator="\n")
        for key, value in header:
            writer.writerow([key, value])
        writer.writerow(list(track[0].keys()))
        writer.writerow(["s", "s", "cm", "cm", "cm2", "cm", "cm/s", "-", "-"])
        for row in track:
            writer.writerow(list(row.values()))
    for path, rows in ((BINS, bins), (EVENTS, events)):
        with path.open("w", encoding="utf-8", newline="\n") as handle:
            handle.write("SYNTHETIC EthoVision XT export - schema-faithful mock generated by generate_hcmo_instance.py; no real animals\n")
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)


def main() -> int:
    bins, events, track = synthesize()
    write_exports(bins, events, track)

    ig = InstanceGraph(BASE, "pt")
    ig.dataset_note(
        "phenotyper-mock-export",
        label="Synthetic PhenoTyper/EthoVision XT exports (2 arenas, 2 h)",
        description="Schema-faithful synthetic EthoVision XT track, time-bin and behaviour exports; values are generated, not recorded.",
        source="docs/hcm-systems/systems/noldus-phenotyper/README.md",
        real_data=False,
    )

    vendor = ig.typed("noldus", SCHEMA.Organization, label="Noldus Information Technology")
    workstation = ig.hardware("ethovision-workstation", label="EthoVision XT acquisition workstation")
    ig.add(workstation, SCHEMA.manufacturer, vendor)
    ethovision = ig.software("ethovision-xt", label="EthoVision XT video tracking software", version="17", runs_on=workstation)
    tracking = ig.typed("centre-point-tracking", SOSA.Procedure, label="EthoVision centre-point detection and time-bin statistics",
                        comment="Centre-point detection on the top-unit IR video at 25 samples/s; distance, velocity and zone/movement durations aggregated per 1-min bin.")
    recognition = ig.typed("behavior-recognition", SOSA.Procedure, label="EthoVision Behavior Recognition module (rodent)",
                           comment="Automatic classification of grooming, rearing, eating and sniffing from the video; no confidence scores are exported.")

    series_track = ig.time_series("track-series-arena-1", label="Raw centre-point track sample, arena 1 (20 s at 25 samples/s)", file_format="text/csv",
                                  storage_path="docs/hcm-systems/systems/noldus-phenotyper/datasets/mock/ethovision_track_sample_arena1.csv", sampling_rate_hz=SAMPLE_RATE)
    series_bins = ig.time_series("time-bin-series", label="EthoVision time-bin statistics export", file_format="text/csv",
                                 storage_path="docs/hcm-systems/systems/noldus-phenotyper/datasets/mock/ethovision_time_bins.csv")
    series_events = ig.time_series("behavior-event-series", label="EthoVision behaviour event export", file_format="text/csv",
                                   storage_path="docs/hcm-systems/systems/noldus-phenotyper/datasets/mock/ethovision_behavior_events.csv")
    for series in (series_track, series_bins, series_events):
        ig.add(series, PROV.wasAttributedTo, ethovision)

    p_distance = ig.observable_property("distance-moved", "distance moved (centre-point)")
    p_velocity = ig.observable_property("mean-velocity", "mean velocity (centre-point)")
    p_shelter = ig.observable_property("time-in-shelter", "time in shelter zone")
    p_moving = ig.observable_property("time-moving", "time in movement state")
    p_position = ig.observable_property("centre-point-position", "centre-point position (X, Y)")
    p_behavior = ig.observable_property("behavior-category", "recognised behaviour category")

    light_cycle = ig.light_cycle("light-cycle-12-12", dark_start="19:00:00", dark_hours=12, light_hours=12, label="12:12 light-dark cycle, dark from 19:00 (top-unit white LED schedule)")
    profile = ig.environment_profile("phenotyper-room-profile", label="PhenoTyper room environment profile", light_cycle=light_cycle)

    subjects, arenas, cameras = {}, {}, {}
    run_end = START + timedelta(minutes=BIN_MIN * BINS_PER_ARENA)
    for arena, sex, subject_id in ARENAS:
        dims = ig.dimensions(f"arena-{arena}-dimensions", *ARENA_DIMENSIONS_CM)
        enclosure = ig.enclosure(f"arena-{arena}", label=f"PhenoTyper 3000 home cage, arena {arena}", identifier=f"Arena {arena}", dimensions=dims,
                                 manufacturer="Noldus Information Technology", comment="PhenoTyper 3000 (30 x 30 cm) with shelter, top unit with IR-sensitive camera and white/IR LED units.")
        ig.add(enclosure, HCM_ENV.hasEnvironment, profile)
        ig.add(enclosure, HCM.hasEnrichment, ig.enrichment(f"arena-{arena}-shelter", "shelter", f"Shelter (hiding box) in arena {arena}"))
        ig.actuator(f"arena-{arena}-white-led", label=f"Top-unit white light LED, arena {arena}", enclosure=enclosure)
        ig.actuator(f"arena-{arena}-ir-led", label=f"Top-unit infrared LED, arena {arena}", enclosure=enclosure)
        camera = ig.sensor(f"arena-{arena}-camera", label=f"Top-unit infrared-sensitive camera, arena {arena}", identifier=f"PT-camera-{arena}",
                           technology="infrared video", sensor_type="video camera", sampling_rate_hz=SAMPLE_RATE, installed_in=enclosure,
                           captures=[p_position, p_distance, p_velocity, p_shelter, p_moving, p_behavior])
        ig.add(camera, HCM_TECH.communicatesWith, workstation)
        subject = ig.subject(subject_id, label=f"Mouse {arena} (PhenoTyper arena {arena})", species="Mus musculus", strain="C57BL/6J", sex=sex, date_of_birth="2026-01-20")
        ig.add(subject, DCTERMS.identifier, Literal(subject_id))
        ig.housing(f"housing-{subject_id}", holder=subject, enclosure=enclosure, start=START - timedelta(days=3), end=run_end + timedelta(days=4))
        subjects[arena], arenas[arena], cameras[arena] = subject, enclosure, camera

    instants = {}

    def instant_for(when: datetime, local: str | None = None):
        if when not in instants:
            instants[when] = ig.instant(local or f"t-{when.strftime('%Y%m%dT%H%M%S')}", when)
        return instants[when]

    n_obs = 0
    for row in bins:
        arena = int(row["Arena"])
        when = datetime.strptime(row["Bin start"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=TZ)
        stamp = when.strftime("%Y%m%dT%H%M")
        interval = ig.iri(f"bin-{stamp}")
        if (interval, None, None) not in ig.g:
            interval = ig.typed(f"bin-{stamp}", TIME.Interval)
            ig.add(interval, TIME.hasBeginning, instant_for(when, f"t-{stamp}"))
            ig.add(interval, TIME.hasEnd, instant_for(when + timedelta(minutes=BIN_MIN), f"t-{(when + timedelta(minutes=BIN_MIN)).strftime('%Y%m%dT%H%M')}"))
        for key, prop, unit, column in (
            ("distance", p_distance, UNIT.CentiM, "Distance moved [cm]"),
            ("velocity", p_velocity, UNIT["CentiM-PER-SEC"], "Velocity mean [cm/s]"),
            ("shelter", p_shelter, UNIT.SEC, "In zone(Shelter / center-point) duration [s]"),
            ("moving", p_moving, UNIT.SEC, "Movement(Moving / center-point) duration [s]"),
        ):
            result = ig.result_quantity(f"res-{key}-{arena}-{stamp}", row[column], unit)
            ig.observation(f"obs-{key}-{arena}-{stamp}", cls=SOSA.Observation, feature=subjects[arena], sensor=cameras[arena], prop=prop, result=result,
                           phenomenon_time=interval, occurs_in=arenas[arena], procedure=tracking)
            n_obs += 1

    n_behavior = 0
    for index, event in enumerate(events, start=1):
        arena = int(event["Arena"])
        start = START + timedelta(seconds=float(event["Start [s]"]))
        stop = START + timedelta(seconds=float(event["Stop [s]"]))
        interval = ig.interval(f"behavior-{index}-time", start, stop, duration_unit=TIME.unitSecond)
        result = ig.behavior_result(f"res-behavior-{index}", event["Behavior"])
        ig.observation(f"obs-behavior-{index}", cls=HCM_OBS.BehaviorObservation, feature=subjects[arena], sensor=cameras[arena], prop=p_behavior, result=result,
                       phenomenon_time=interval, occurs_in=arenas[arena], procedure=recognition)
        n_behavior += 1

    # raw track sample as a SemTS location result table
    table = ig.typed("track-table-arena-1", HCM_OBS.LocationResultTable, label="Centre-point track table, arena 1, 20-s sample")
    for dim, label, unit in (("x-center", "X center", "cm"), ("y-center", "Y center", "cm")):
        dimension = ig.typed(f"dimension-{dim}", SEMTS.DataDimension, label=f"{label} [{unit}]")
        ig.add(table, SEMTS.segmentDimension, dimension)
    ig.add(table, PROV.wasDerivedFrom, series_track)
    track_interval = ig.interval("track-sample-time", START, START + timedelta(seconds=TRACK_SECONDS), duration_unit=TIME.unitSecond)
    ig.observation("obs-track-arena-1", cls=SOSA.Observation, feature=subjects[1], sensor=cameras[1], prop=p_position, result=table,
                   phenomenon_time=track_interval, occurs_in=arenas[1], procedure=tracking)
    n_obs += 1

    header = (
        "# GENERATED by docs/hcm-systems/systems/noldus-phenotyper/generate_hcmo_instance.py — DO NOT EDIT\n"
        "# HCMO instance graph derived from SYNTHETIC, schema-faithful PhenoTyper/EthoVision XT exports (no real animals).\n"
        f"# {len(ARENAS)} arenas, {BINS_PER_ARENA} one-minute bins each from {START.isoformat()}; {n_obs} quantitative and {n_behavior} behaviour observations.\n"
    )
    ig.serialize(OUT, header)
    print(f"wrote {OUT.relative_to(ROOT)}: {len(ig.g)} triples, {n_obs} + {n_behavior} observations; {len(bins)} bins, {len(events)} events, {len(track)} track samples")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
