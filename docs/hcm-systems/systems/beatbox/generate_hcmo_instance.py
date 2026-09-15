#!/usr/bin/env python3
"""Generate SYNTHETIC BEATBox outputs and the corresponding HCMO instance graph.

BEATBox (BEhavioural and AuTonomous operant Box, https://open-beatbox.github.io)
is an open-source, modular home-cage operant platform: a Raspberry Pi main
controller drives feeder, nose-poke, left/right touch-screen, lighting and
IR-barrier modules over a CAN bus. Its public manual (Sphinx sources in
``open-beatbox/open-beatbox.github.io``, September 2026) documents the
inter-module CAN protocol but lists the *data output format* as planned
content. Two mock files are therefore generated:

  * ``beatbox_can_event_log.csv`` -- an event log whose rows are the documented
    CAN messages (module IDs, message names, payloads and the 11-bit identifier
    computed with the documented formula ``(PRIO<<8)|(MODULE<<4)|(TYPE<<2)|CMD``)
  * ``beatbox_trials.csv`` -- a trial table DESIGNED for this evaluation (the
    GUI's trial/performance export is not yet published) for a two-choice
    touch-screen visual discrimination task with reversal.

Scenario (requested): four single-housed mice of different strains, one per
box, 6 h from 17:00 to 23:00 spanning the light-to-dark transition (dark from
19:00, set through the lighting module), autonomous trials initiated by nose
poke, S+ pattern on one screen, reward on correct touch, daily session summary.

Output: ``examples/systems/beatbox.ttl``
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
    SOSA,
    TIME,
    UNIT,
    InstanceGraph,
)

MOCK_DIR = HERE / "datasets" / "mock"
CAN_LOG = MOCK_DIR / "beatbox_can_event_log.csv"
TRIALS = MOCK_DIR / "beatbox_trials.csv"
OUT = ROOT / "examples" / "systems" / "beatbox.ttl"
BASE = "https://w3id.org/hcmo/id/eval/beatbox/"

TZ = timezone(timedelta(hours=2))
START = datetime(2026, 6, 2, 17, 0, tzinfo=TZ)
HOURS = 6
DARK_START_HOUR = 19
SESSION_DAY = 5  # day of the autonomous protocol
BOXES = [
    # box, animal id, strain, sex, S+ side on this day
    (1, "BB-001", "C57BL/6J", "male", "left"),
    (2, "BB-002", "BALB/cJ", "female", "right"),
    (3, "BB-003", "DBA/2J", "male", "left"),
    (4, "BB-004", "129S1/SvImJ", "female", "right"),
]
# assumed dimensions of the BEATBox home-cage compartment (cm) for this synthetic profile
BOX_DIMENSIONS_CM = (Decimal("30"), Decimal("40"), Decimal("25"))
S_PLUS_PATTERN, S_MINUS_PATTERN = 3, 7

# documented CAN dictionaries (docs/source/software/firmware/can-intermodule-protocol.md)
MODULES = {"MAIN": 0x1, "FEEDER": 0x2, "NOSEPOKE": 0x3, "SCREEN_LEFT": 0x4, "SCREEN_RIGHT": 0x5, "LIGHTING": 0x6, "IR_BARRIER": 0x7}
MESSAGES = {
    # name: (prio, type, cmd)
    "BEAM_EVENT": (2, 3, 1), "TOUCH_EVENT": (2, 3, 1), "BARRIER_EVENT": (2, 3, 1),
    "DISPLAY_PATTERN": (1, 2, 0), "DISPLAY_PATTERN_ACK": (3, 3, 0),
    "REQUEST_REWARD": (1, 2, 1), "REWARD_DELIVERED": (3, 3, 1),
    "SET_DUTY": (1, 2, 0), "SET_DUTY_ACK": (3, 3, 0),
}


def can_id(module: str, message: str) -> str:
    prio, msg_type, cmd = MESSAGES[message]
    return f"0x{(prio << 8) | (MODULES[module] << 4) | (msg_type << 2) | cmd:03X}"


def synthesize() -> tuple[list[dict], list[dict]]:
    rng = random.Random(20260602)
    log: list[dict] = []
    trials: list[dict] = []

    def emit(t: datetime, box: int, module: str, message: str, payload: str) -> None:
        prio, _, _ = MESSAGES[message]
        log.append({"timestamp": t.isoformat(timespec="milliseconds"), "box": box, "module": module, "message": message,
                    "payload": payload, "can_id": can_id(module, message), "prio": f"P{prio}"})

    end = START + timedelta(hours=HOURS)
    lights_off = START.replace(hour=DARK_START_HOUR, minute=0)
    for box, *_ in BOXES:
        emit(START, box, "LIGHTING", "SET_DUTY", "white=80,red=0,ir=100")
        emit(START + timedelta(milliseconds=12), box, "LIGHTING", "SET_DUTY_ACK", "white=80,red=0,ir=100")
        emit(lights_off, box, "LIGHTING", "SET_DUTY", "white=0,red=15,ir=100")
        emit(lights_off + timedelta(milliseconds=12), box, "LIGHTING", "SET_DUTY_ACK", "white=0,red=15,ir=100")
    for box, animal, strain, sex, s_plus in BOXES:
        accuracy = {"C57BL/6J": 0.82, "BALB/cJ": 0.68, "DBA/2J": 0.60, "129S1/SvImJ": 0.72}[strain]
        t = START + timedelta(minutes=rng.uniform(2, 30))
        trial = 0
        while t < end:
            dark = t.hour >= DARK_START_HOUR
            trial += 1
            emit(t, box, "NOSEPOKE", "BEAM_EVENT", "beam=1")
            t_display = t + timedelta(milliseconds=rng.randint(40, 90))
            left_pattern = S_PLUS_PATTERN if s_plus == "left" else S_MINUS_PATTERN
            right_pattern = S_MINUS_PATTERN if s_plus == "left" else S_PLUS_PATTERN
            emit(t_display, box, "SCREEN_LEFT", "DISPLAY_PATTERN", f"pattern_id={left_pattern}")
            emit(t_display + timedelta(milliseconds=5), box, "SCREEN_RIGHT", "DISPLAY_PATTERN", f"pattern_id={right_pattern}")
            latency = round(rng.uniform(0.6, 9.5) * (0.7 if dark else 1.0), 2)
            correct = rng.random() < (accuracy + (0.05 if dark else 0.0))
            side = s_plus if correct else ("right" if s_plus == "left" else "left")
            t_touch = t_display + timedelta(seconds=latency)
            emit(t_touch, box, "SCREEN_LEFT" if side == "left" else "SCREEN_RIGHT", "TOUCH_EVENT", "touch=1")
            collect = ""
            if correct:
                emit(t_touch + timedelta(milliseconds=30), box, "FEEDER", "REQUEST_REWARD", "")
                emit(t_touch + timedelta(milliseconds=rng.randint(300, 700)), box, "FEEDER", "REWARD_DELIVERED", "")
                collect_latency = round(rng.uniform(0.8, 6.0), 2)
                emit(t_touch + timedelta(seconds=collect_latency), box, "IR_BARRIER", "BARRIER_EVENT", "barrier=1")
                collect = f"{collect_latency:.2f}"
            trials.append({
                "box": box, "animal_id": animal, "strain": strain, "sex": sex, "session_day": SESSION_DAY,
                "trial": trial, "task": "two-choice visual discrimination (touch screens)", "trial_start": t.isoformat(timespec="seconds"),
                "s_plus_side": s_plus, "pattern_left": left_pattern, "pattern_right": right_pattern, "response_side": side,
                "correct": int(correct), "response_latency_s": f"{latency:.2f}", "reward_delivered": int(correct), "collection_latency_s": collect,
                "light_phase": "dark" if dark else "light",
            })
            t = t_touch + timedelta(seconds=rng.uniform(60, 900) * (0.5 if dark else 1.0))
    log.sort(key=lambda r: (r["timestamp"], r["box"]))
    return log, trials


def write_exports(log: list[dict], trials: list[dict]) -> None:
    MOCK_DIR.mkdir(parents=True, exist_ok=True)
    with CAN_LOG.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write("# SYNTHETIC BEATBox CAN event log - rows are the documented inter-module CAN messages; generated by generate_hcmo_instance.py, no real animals\n")
        writer = csv.DictWriter(handle, fieldnames=list(log[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(log)
    with TRIALS.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write("# SYNTHETIC BEATBox trial table - DESIGNED for this evaluation (the GUI export format is not yet published); no real animals\n")
        writer = csv.DictWriter(handle, fieldnames=list(trials[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(trials)


def main() -> int:
    log, trials = synthesize()
    write_exports(log, trials)

    ig = InstanceGraph(BASE, "bb")
    ig.dataset_note(
        "beatbox-mock-outputs",
        label="Synthetic BEATBox CAN event log and designed trial table (4 boxes, 6 h)",
        description="The CAN log follows the published inter-module protocol (module IDs, message names, payloads, 11-bit identifiers); the trial table is a designed export because BEATBox's data-output format is still listed as planned content in its manual.",
        source="docs/hcm-systems/systems/beatbox/README.md",
        real_data=False,
    )
    gui = ig.software("beatbox-gui", label="BEATBox Python control and monitoring GUI (Raspberry Pi)")
    task = ig.typed("visual-discrimination-task", SOSA.Procedure, label="Two-choice touch-screen visual discrimination, nose-poke initiated, FR1 reward on S+ touch",
                    comment=f"S+ pattern {S_PLUS_PATTERN} on the rewarded screen, S- pattern {S_MINUS_PATTERN} on the other; the rewarded side is fixed per animal and reversed after criterion (day {SESSION_DAY} shown).")
    log_series = ig.time_series("can-event-log", label="BEATBox CAN event log (all boxes, merged by the GUI)", file_format="text/csv",
                                storage_path=CAN_LOG.relative_to(ROOT).as_posix(),
                                comment="One row per inter-module CAN message; the box column identifies the originating controller.")
    ig.add(log_series, PROV.wasAttributedTo, gui)
    trial_series = ig.time_series("trial-table", label="BEATBox trial table (designed export)", file_format="text/csv", storage_path=TRIALS.relative_to(ROOT).as_posix())
    ig.add(trial_series, PROV.wasAttributedTo, gui)

    p_choice = ig.observable_property("discrimination-choice", "touch-screen discrimination choice (correct / incorrect)")
    p_latency = ig.observable_property("response-latency", "response latency from stimulus display to touch")
    p_collect = ig.observable_property("reward-collection-latency", "reward collection latency (touch to feeder barrier)")
    p_accuracy = ig.observable_property("session-accuracy", "session accuracy (share of correct trials)")
    p_trials = ig.observable_property("session-trial-count", "number of self-initiated trials in the session")

    light_cycle = ig.light_cycle("light-cycle-12-12", dark_start="19:00:00", dark_hours=12, light_hours=12,
                                 label="12:12 light-dark cycle, dark from 19:00 (lighting module SET_DUTY white=0)")
    profile = ig.environment_profile("beatbox-room-profile", label="BEATBox room environment profile", light_cycle=light_cycle)

    n_obs = 0
    for box, animal_id, strain, sex, s_plus in BOXES:
        dims = ig.dimensions(f"box-{box}-dimensions", *BOX_DIMENSIONS_CM)
        cage = ig.enclosure(f"box-{box}", label=f"BEATBox {box} home-cage compartment", identifier=f"BEATBox-{box}", dimensions=dims,
                            comment="Home-cage compartment with door wall, tunnel, feeder, two touch screens, nose poke, lighting and IR barriers; dimensions assumed for the synthetic profile.")
        ig.add(cage, HCM_ENV.hasEnvironment, profile)
        ig.add(cage, HCM.hasEnrichment, ig.enrichment(f"box-{box}-nesting", "nesting material", f"Nesting material in BEATBox {box}"))
        controller = ig.hardware(f"box-{box}-main-controller", label=f"Raspberry Pi main controller of BEATBox {box} (BB_RPi_shield_V1.1)", model_number="BB_RPi_shield_V1.1")
        ig.add(controller, HCM_TECH.hasProtocol, Literal("CAN 2.0A 11-bit inter-module protocol"))
        ig.add(controller, HCM_TECH.supportsEnclosure, cage)
        ig.add(gui, HCM_TECH.runsOn, controller)
        ig.add(gui, HCM_TECH.communicatesWith, controller)
        nosepoke = ig.sensor(f"box-{box}-nosepoke", label=f"Nose-poke IR beam sensor, BEATBox {box}", identifier=f"BB-{box}-NOSEPOKE", technology="infrared beam-break",
                             installed_in=cage, captures=[p_choice])
        barrier = ig.sensor(f"box-{box}-feeder-barrier", label=f"Feeder IR barrier (BB_Feeder_IRBarrier_V1.1), BEATBox {box}", identifier=f"BB-{box}-IR_BARRIER",
                            technology="infrared light curtain", model_number="BB_Feeder_IRBarrier_V1.1", installed_in=cage, captures=[p_collect])
        screens = {}
        for side in ("left", "right"):
            touch = ig.sensor(f"box-{box}-screen-{side}-touch", label=f"{side.capitalize()} touch screen (touch sensing), BEATBox {box}", identifier=f"BB-{box}-SCREEN_{side.upper()}",
                              technology="capacitive touch screen", installed_in=cage, captures=[p_choice, p_latency])
            display = ig.actuator(f"box-{box}-screen-{side}-display", label=f"{side.capitalize()} touch screen (stimulus display), BEATBox {box}", enclosure=cage)
            ig.add(touch, HCM_TECH.communicatesWith, controller)
            screens[side] = touch
        feeder = ig.actuator(f"box-{box}-feeder", label=f"Pellet feeder (BB_Feeder_main_V1.1), BEATBox {box}", enclosure=cage, model_number="BB_Feeder_main_V1.1")
        lighting = ig.actuator(f"box-{box}-lighting", label=f"Ceiling lighting module white/red/IR (BP_Lighting_V1.1), BEATBox {box}", enclosure=cage, model_number="BP_Lighting_V1.1")
        for node in (nosepoke, barrier):
            ig.add(node, HCM_TECH.communicatesWith, controller)

        mouse = ig.subject(f"mouse-{box}", label=f"Mouse {animal_id} ({strain}, BEATBox {box})", species="Mus musculus", strain=strain, sex=sex, date_of_birth="2026-02-01")
        ig.add(mouse, DCTERMS.identifier, Literal(animal_id))
        ig.housing(f"housing-mouse-{box}", holder=mouse, enclosure=cage, start=START - timedelta(days=SESSION_DAY), end=START + timedelta(days=10))

        box_trials = [t for t in trials if t["box"] == box]
        for t in box_trials:
            n = t["trial"]
            start = datetime.fromisoformat(t["trial_start"])
            latency = float(t["response_latency_s"])
            interval = ig.interval(f"trial-{box}-{n}-time", start, start + timedelta(seconds=latency + 0.1), duration_unit=TIME.unitSecond)
            choice = ig.categorical_result(f"res-choice-{box}-{n}", "correct" if t["correct"] == 1 else "incorrect")
            ig.observation(f"obs-choice-{box}-{n}", cls=SOSA.Observation, feature=mouse, sensor=screens[t["response_side"]], prop=p_choice, result=choice,
                           phenomenon_time=interval, occurs_in=cage, procedure=task)
            lat = ig.result_quantity(f"res-latency-{box}-{n}", t["response_latency_s"], UNIT.SEC)
            ig.observation(f"obs-latency-{box}-{n}", cls=SOSA.Observation, feature=mouse, sensor=screens[t["response_side"]], prop=p_latency, result=lat,
                           phenomenon_time=interval, occurs_in=cage, procedure=task)
            n_obs += 2
            if t["collection_latency_s"]:
                collect_interval = ig.interval(f"collect-{box}-{n}-time", start + timedelta(seconds=latency), start + timedelta(seconds=latency + float(t["collection_latency_s"])), duration_unit=TIME.unitSecond)
                res = ig.result_quantity(f"res-collect-{box}-{n}", t["collection_latency_s"], UNIT.SEC)
                ig.observation(f"obs-collect-{box}-{n}", cls=SOSA.Observation, feature=mouse, sensor=barrier, prop=p_collect, result=res,
                               phenomenon_time=collect_interval, occurs_in=cage, procedure=task)
                n_obs += 1
        # session summary derived by the GUI
        session = ig.interval(f"session-{box}-time", START, START + timedelta(hours=HOURS), duration_unit=TIME.unitHour)
        accuracy = Decimal(str(round(100.0 * sum(t["correct"] for t in box_trials) / len(box_trials), 1)))
        for key, prop, value, unit in (("accuracy", p_accuracy, accuracy, UNIT.PERCENT), ("trials", p_trials, len(box_trials), UNIT.NUM)):
            res = ig.result_quantity(f"res-session-{key}-{box}", value, unit)
            obs = ig.observation(f"obs-session-{key}-{box}", cls=SOSA.Observation, feature=mouse, sensor=nosepoke, prop=prop, result=res,
                                 phenomenon_time=session, occurs_in=cage, procedure=task)
            ig.add(obs, PROV.wasAttributedTo, gui)
            n_obs += 1

    header = (
        "# GENERATED by docs/hcm-systems/systems/beatbox/generate_hcmo_instance.py — DO NOT EDIT\n"
        "# HCMO instance graph derived from SYNTHETIC BEATBox outputs (CAN event log per the published protocol; designed trial table).\n"
        f"# {len(BOXES)} single-housed mice of different strains, {HOURS} h from {START.isoformat()}; {len(trials)} trials, {len(log)} CAN messages, {n_obs} observations.\n"
    )
    ig.serialize(OUT, header)
    print(f"wrote {OUT.relative_to(ROOT)}: {len(ig.g)} triples; {len(trials)} trials, {len(log)} CAN messages, {n_obs} observations")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
