#!/usr/bin/env python3
"""
generate_dvc_mock.py — deterministic mock generator for Tecniplast DVC(R)-style
home-cage-monitoring exports, for HCMO ontology validation.

This produces a *believable* — not real — cage-level activity + environment export
in the shape the DVC Analytics platform emits: one row per cage per 1-minute bin,
carrying the Animal Locomotion Index (ALI, 0-100 %), the Bedding Status Index (BSI),
and the rack environmental channels (temperature, relative humidity).

Grounded in publicly documented DVC mechanics (see dvc-system-profile.md, section 5):
  - 12 capacitive electrodes sampled at 4 Hz (250 ms); the platform aggregates to
    1-min / 1-h bins for export.
  - ALI = proportion of the 12 electrodes active in a bin, 0 % (none) .. 100 % (all).
  - BSI decreases as bedding moisture rises; it resets upward at each cage change.
  - Mice are nocturnal: activity concentrates in the dark phase.

NOTE ON FIDELITY: the exact vendor column header strings and timestamp format are NOT
publicly documented (proprietary DVC Analytics export). The header names below are a
*reconstruction* consistent with the documented variables, chosen to be self-describing
for ontology mapping. Do not present them as verbatim vendor headers.

Stdlib only (csv, math, random, datetime) — no build step, no dependencies.
Deterministic: fixed seed => identical output every run.

Usage:
    python3 generate_dvc_mock.py            # writes dvc_activity_mock.csv here
    python3 generate_dvc_mock.py --days 3   # shorter run
"""

import argparse
import csv
import math
import random
from datetime import datetime, timedelta, timezone

SEED = 20260706
TZ = timezone(timedelta(hours=1))  # facility local time, UTC+01:00 (Europe/Rome-like)

# ---- Cage roster ------------------------------------------------------------
# Two single-housed males (centroid-trackable) + two group-housed female cages
# (cage-level aggregate only) — mirrors the two DVC housing regimes.
CAGES = [
    # cage_id,     rack_id, position, strain,        sex,      density
    ("DVC-A1-C03", "RACK-A1", "C03", "C57BL/6J",     "male",   1),
    ("DVC-A1-C07", "RACK-A1", "C07", "C57BL/6J",     "male",   1),
    ("DVC-A1-C11", "RACK-A1", "C11", "BALB/cAnNCrl", "female", 4),
    ("DVC-A1-C14", "RACK-A1", "C14", "BALB/cAnNCrl", "female", 4),
]

# ---- Light programme (Leddy-style per-cage LED, 12:12 LD) --------------------
LIGHTS_ON_HOUR = 7    # 07:00 lights on  -> light (inactive) phase
LIGHTS_OFF_HOUR = 19  # 19:00 lights off -> dark (active) phase

# ---- Husbandry --------------------------------------------------------------
CAGE_CHANGE_WEEKDAY = 0     # Monday
CAGE_CHANGE_HOUR = 9        # morning cage change / handling
BIN_MINUTES = 1


def is_dark(dt):
    return not (LIGHTS_ON_HOUR <= dt.hour < LIGHTS_OFF_HOUR)


def light_phase(dt):
    return "dark" if is_dark(dt) else "light"


def days_since_change(dt, last_change):
    return (dt - last_change).total_seconds() / 86400.0


def ali_value(rng, dt, density, dsc, post_change_bump):
    """Animal Locomotion Index, 0-100 %. Circadian base + bouts + rest, scaled by
    group size (super-additive but sub-linear)."""
    # Smooth circadian drive: peak mid-dark, trough mid-light.
    # phase angle over 24 h, dark centred ~01:00
    hours = dt.hour + dt.minute / 60.0
    # shift so dark-phase midpoint (~01:00) is the activity peak
    theta = (hours - 1.0) / 24.0 * 2 * math.pi
    circadian = 0.5 * (1 + math.cos(theta))          # 1 at ~01:00, 0 at ~13:00
    base = 3.0 + 14.0 * circadian                    # ~3 % light .. ~17 % dark (per animal)

    # crepuscular bumps just after lights-off (19:00) and before lights-on (07:00)
    if dt.hour in (19, 20):
        base += 6.0
    if dt.hour == 6:
        base += 4.0

    # group scaling: aggregate rises with density but sub-linearly (huddling/overlap)
    density_gain = 1.0 + 0.55 * (density - 1)         # 1 animal:1.0x, 4 animals:~2.65x
    val = base * density_gain

    # bout structure: occasional high-activity bouts, frequent near-rest in light phase
    r = rng.random()
    if is_dark(dt):
        if r < 0.06:
            val += rng.uniform(20, 55)               # vigorous locomotion bout
        elif r < 0.30:
            val += rng.uniform(4, 14)
        elif r > 0.92:
            val *= 0.2                                # brief rest even at night
    else:
        if r < 0.75:
            val *= rng.uniform(0.05, 0.35)           # long rest dominates light phase
        elif r > 0.98:
            val += rng.uniform(10, 30)               # rare daytime disturbance

    # acclimatisation: first ~2 days slightly elevated & noisier
    if dsc < 2.0:
        val *= 1.0 + 0.15 * (2.0 - dsc) / 2.0

    # transient handling spike in the ~2 h after a cage change
    val += post_change_bump

    # measurement noise
    val += rng.gauss(0, 1.2)
    return round(max(0.0, min(100.0, val)), 2)


def bsi_value(rng, dsc, density):
    """Bedding Status Index (arbitrary units, ~100 fresh -> declines with moisture).
    Resets at each cage change (dsc -> 0). Declines faster at higher density."""
    fresh = 100.0
    decline_rate = 3.2 * (0.6 + 0.25 * density)      # units/day; higher density wetter
    val = fresh - decline_rate * dsc
    # mild diurnal ripple (more urine deposited in active dark phase)
    val += 1.5 * math.sin(dsc * 2 * math.pi)
    val += rng.gauss(0, 0.6)
    return round(max(0.0, val), 2)


def env_values(rng, dt, dsc, density):
    """Rack Environmental Monitor: temperature (C) and relative humidity (%)."""
    hours = dt.hour + dt.minute / 60.0
    temp = 22.0 + 0.5 * math.sin((hours - 6) / 24 * 2 * math.pi) + rng.gauss(0, 0.15)
    # humidity drifts up as bedding soils and with density
    rh = 52.0 + 0.9 * dsc * (0.6 + 0.2 * density) + 3.0 * math.sin(hours / 24 * 2 * math.pi)
    rh += rng.gauss(0, 1.5)
    return round(temp, 2), round(max(30.0, min(80.0, rh)), 1)


def last_cage_change_before(dt, start):
    """Most recent Monday 09:00 at or before dt (never before the study start)."""
    d = dt
    while True:
        candidate = d.replace(hour=CAGE_CHANGE_HOUR, minute=0, second=0, microsecond=0)
        if d.weekday() == CAGE_CHANGE_WEEKDAY and candidate <= dt and candidate >= start:
            return candidate
        d -= timedelta(days=1)
        if d < start - timedelta(days=8):
            return start  # fall back to study start


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--out", default="dvc_activity_mock.csv")
    args = ap.parse_args()

    rng = random.Random(SEED)
    # Study begins at a cage change: Monday 2026-03-02, 09:00 local (day 0 = fresh cage)
    start = datetime(2026, 3, 2, CAGE_CHANGE_HOUR, 0, 0, tzinfo=TZ)
    n_bins = args.days * 24 * (60 // BIN_MINUTES)

    header = [
        "DateTime",              # ISO 8601 with UTC offset (facility local)
        "UnixTimeMillis",        # int, ms since epoch (UTC)
        "RackId",                # str
        "CagePosition",          # str, slot on the rack
        "CageId",                # str, logical cage identifier
        "Strain",                # str
        "Sex",                   # str
        "HousingDensity",        # int, animals in cage (cage-level signal)
        "LightPhase",            # str, light|dark
        "DaysSinceCageChange",   # float, days
        "ActivationDensityPct",  # float, ALI 0-100 %
        "BeddingStatusIndex",    # float, arbitrary units (higher = drier)
        "RackTemperatureC",      # float, degrees Celsius
        "RackHumidityPct",       # float, % RH
    ]

    rows = 0
    with open(args.out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        for i in range(n_bins):
            dt = start + timedelta(minutes=i * BIN_MINUTES)
            unix_ms = int(dt.astimezone(timezone.utc).timestamp() * 1000)
            lc = last_cage_change_before(dt, start)
            dsc = days_since_change(dt, lc)
            # post-change handling bump for ~2 h after the change
            minutes_since_change = (dt - lc).total_seconds() / 60.0
            post_bump = 0.0
            if 0 <= minutes_since_change <= 120:
                post_bump = 12.0 * (1 - minutes_since_change / 120.0)
            for cage_id, rack_id, pos, strain, sex, density in CAGES:
                ali = ali_value(rng, dt, density, dsc, post_bump)
                bsi = bsi_value(rng, dsc, density)
                temp, rh = env_values(rng, dt, dsc, density)
                w.writerow([
                    dt.isoformat(timespec="seconds"),
                    unix_ms,
                    rack_id, pos, cage_id, strain, sex, density,
                    light_phase(dt),
                    round(dsc, 4),
                    ali, bsi, temp, rh,
                ])
                rows += 1

    print(f"wrote {rows} rows ({len(CAGES)} cages x {n_bins} bins) to {args.out}")


if __name__ == "__main__":
    main()
