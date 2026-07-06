#!/usr/bin/env python3
"""Generate MOCK Tecniplast DVC(R) traces that mirror the REAL export schema.

This reproduces the two file shapes found in a real DVC Analytics export
(see ``../real/``), so HCMO ingestion/validation can be exercised against
synthetic-but-faithful data:

  1. ``mock_<GROUP>_animal_loc__index_smoothed.csv``
     One row per 1-minute bin. Columns:
       day, hour, minute, relativeTime,
       <GROUP>_TIMESTAMP, <GROUP>_AVG, <GROUP>_SEM, <GROUP>_QRT, <GROUP>_SAMPLES,
       <GROUP>_<cageId> ...            (one column per cage, activation index)

  2. ``mock_<GROUP>_events.csv``
     One row per cage-lifecycle event. Columns:
       group, day, hour, minute, relativeTime, timestamp,
       cage, rack, position, event

Conventions reverse-engineered from the real cohort file and reproduced here:
  * relativeTime      = day*86400 + hour*3600 + minute*60 (+seconds for events),
                        i.e. seconds since local midnight of day 0.
  * <GROUP>_AVG       = mean of the online cages' activation values in the bin.
  * <GROUP>_SEM       = sample standard deviation (ddof=1) of those values
                        (this is what the column contains in the real export).
  * <GROUP>_QRT       = [min, min+.25R, min+.5R, min+.75R, max, min, max], R=max-min
                        (i.e. linspace(min,max,5) then min,max appended).
  * <GROUP>_SAMPLES   = ~ online_cages * 240  (4 Hz * 60 s), with small jitter.
  * timestamps        = ISO 8601 with milliseconds and a numeric offset (e.g. -0400).
  * cages come online progressively at the start (INSERTED events), so the first
    minutes have empty cells for not-yet-inserted cages — exactly as in the real file.

This is SYNTHETIC data (not real animals). Deterministic: a fixed seed yields
byte-identical output. Standard library only.

Usage:
    python3 generate_dvc_traces.py                 # defaults: B6_M, 8 cages, 3 days
    python3 generate_dvc_traces.py --cages 24 --days 14
    python3 generate_dvc_traces.py --group B6_F --outdir .
"""
from __future__ import annotations

import argparse
import csv
import random
import statistics
from datetime import datetime, timedelta

# ------------------------------------------------------------------ helpers ---

def cage_ids(group: str, n: int) -> list[str]:
    """Deterministic cage identifiers in the real style, e.g. B6_M_12_3401."""
    return [f"{group}_12_{3400 + i}" for i in range(n)]


def rack_position(i: int) -> str:
    """Assign a grid slot: A6,B6,C6,D6,E6, then A5,B5,... (column fills down)."""
    row = chr(ord("A") + (i % 5))
    col = 6 - (i // 5)
    return f"{row}{col}"


def circadian_mean(hour: float, lights_on: int, lights_off: int) -> float:
    """Nocturnal drive: high in the dark phase, low in light, smooth at edges."""
    dark_mean, light_mean = 6.0, 1.6
    # distance (h) into/out of the dark phase, smoothed over a 1 h ramp
    if lights_on <= hour < lights_off:
        base = light_mean
        # small lift near lights-off anticipation
        if lights_off - hour < 1.0:
            base += (light_mean_gap := (dark_mean - light_mean)) * (1.0 - (lights_off - hour))
    else:
        base = dark_mean
        # taper in the hour after lights-off and before lights-on
        into = hour - lights_off if hour >= lights_off else hour + (24 - lights_off)
        if into < 1.0:
            base = light_mean + (dark_mean - light_mean) * into
        out = lights_on - hour if hour < lights_on else 0.0
        if 0.0 < out < 1.0:
            base = light_mean + (dark_mean - light_mean) * out
    return base


def fmt_ts(dt: datetime, offset: str, millis: int) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%S") + f".{millis:03d}" + offset


def qrt(vals: list[float]) -> str:
    lo, hi = min(vals), max(vals)
    r = hi - lo
    pts = [lo + r * f for f in (0.0, 0.25, 0.5, 0.75, 1.0)] + [lo, hi]
    return "[" + ",".join(repr(p) for p in pts) + "]"


# -------------------------------------------------------------------- main ----

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--group", default="B6_M", help="group label / column prefix (default B6_M)")
    ap.add_argument("--cages", type=int, default=8, help="number of cages (default 8; real cohort had 24)")
    ap.add_argument("--days", type=int, default=3, help="recording days (default 3; real cohort had 14)")
    ap.add_argument("--start", default="2025-10-14T10:15:00", help="local start datetime (ISO, no offset)")
    ap.add_argument("--offset", default="-0400", help="numeric UTC offset string (default -0400)")
    ap.add_argument("--lights-on", type=int, default=7, help="lights-on hour (default 7)")
    ap.add_argument("--lights-off", type=int, default=19, help="lights-off hour (default 19)")
    ap.add_argument("--seed", type=int, default=7, help="RNG seed (default 7)")
    ap.add_argument("--outdir", default=".", help="output directory (default .)")
    args = ap.parse_args()

    rng = random.Random(args.seed)
    group = args.group
    cages = cage_ids(group, args.cages)
    start = datetime.fromisoformat(args.start)
    day0_midnight = start.replace(hour=0, minute=0, second=0, microsecond=0)

    # cage i comes online at minute max(0, i-1) after start (first two ~ together)
    online_minute = {c: max(0, i - 1) for i, c in enumerate(cages)}

    # per-cage constant offset + slow personality, so cages differ but track together
    cage_bias = {c: rng.gauss(0.0, 0.7) for c in cages}
    cage_level = {c: 0.0 for c in cages}  # slow random walk

    total_minutes = args.days * 24 * 60
    loc_path = f"{args.outdir}/mock_{group}_animal_loc__index_smoothed.csv"
    ev_path = f"{args.outdir}/mock_{group}_events.csv"

    # ---- animal_loc__index_smoothed ----
    with open(loc_path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        header = ["day", "hour", "minute", "relativeTime",
                  f"{group}_TIMESTAMP", f"{group}_AVG", f"{group}_SEM",
                  f"{group}_QRT", f"{group}_SAMPLES"] + cages
        w.writerow(header)

        for b in range(total_minutes):
            t = start.replace(second=0, microsecond=0) + timedelta(minutes=b)
            day = (t.replace(hour=0, minute=0) - day0_midnight).days
            rel = day * 86400 + t.hour * 3600 + t.minute * 60
            cmean = circadian_mean(t.hour + t.minute / 60.0, args.lights_on, args.lights_off)

            row_vals = {}
            for c in cages:
                if online_minute[c] > b:
                    continue  # not inserted yet -> empty cell
                # slow drift + circadian + per-cage bias + minute noise
                cage_level[c] = 0.92 * cage_level[c] + 0.08 * rng.gauss(0.0, 1.4)
                v = cmean + cage_bias[c] + cage_level[c] + rng.gauss(0.0, 0.8)
                # occasional deep rest (mostly in light) and activity bouts (mostly dark)
                if rng.random() < (0.10 if cmean < 3 else 0.02):
                    v *= 0.15
                if rng.random() < (0.05 if cmean > 4 else 0.01):
                    v += rng.uniform(2.0, 6.0)
                row_vals[c] = max(0.0, round(v, 9))

            vals = list(row_vals.values())
            if vals:
                avg = statistics.fmean(vals)
                sem = statistics.stdev(vals) if len(vals) > 1 else 0.0
                samples = int(round(len(vals) * 240 * rng.uniform(0.96, 1.02)))
                q = qrt(vals)
            else:
                avg = sem = 0.0
                samples = 0
                q = "[]"

            cells = ["" if c not in row_vals else repr(row_vals[c]) for c in cages]
            w.writerow([day, t.hour, t.minute, rel,
                        fmt_ts(t, args.offset, 0),
                        repr(round(avg, 9)), repr(round(sem, 9)), q, samples] + cells)

    # ---- events ----
    events = []  # (rel, day, hour, minute, dt, millis, cage, rack, position, event)

    def add(dt: datetime, cage: str, event: str, rack: str = "", pos: str = ""):
        day = (dt.replace(hour=0, minute=0, second=0, microsecond=0) - day0_midnight).days
        rel = day * 86400 + dt.hour * 3600 + dt.minute * 60 + dt.second
        events.append((rel, day, dt.hour, dt.minute, dt, dt.microsecond // 1000, cage, rack, pos, event))

    # cage bring-up sequence at the start (REGISTERED -> ADDED -> CAGE_ONLINE -> INSERTED)
    for i, c in enumerate(cages):
        insert_dt = start + timedelta(minutes=online_minute[c], seconds=rng.randint(2, 55),
                                      milliseconds=rng.randint(0, 999))
        add(insert_dt - timedelta(seconds=rng.randint(30, 90)), c, "REGISTERED")
        add(insert_dt - timedelta(seconds=rng.randint(10, 25)), c, "ADDED")
        add(insert_dt - timedelta(seconds=rng.randint(3, 8)), c, "CAGE_ONLINE")
        add(insert_dt, c, "INSERTED", rack="AAAA", pos=rack_position(i))

    # periodic UPDATED metadata pings, a few per day across random cages
    for d in range(args.days):
        for _ in range(max(2, args.cages // 3)):
            c = rng.choice(cages)
            dt = start + timedelta(days=d, hours=rng.randint(0, 23),
                                   minutes=rng.randint(0, 59), seconds=rng.randint(0, 59),
                                   milliseconds=rng.randint(0, 999))
            add(dt, c, "UPDATED")

    # one cage-change on the last full day for the first cage: REMOVED then re-INSERTED
    if args.days >= 2:
        cc = start + timedelta(days=args.days - 1, hours=9, minutes=rng.randint(0, 30))
        add(cc, cages[0], "REMOVED")
        add(cc + timedelta(minutes=rng.randint(2, 6), seconds=rng.randint(0, 59),
                           milliseconds=rng.randint(0, 999)),
            cages[0], "INSERTED", rack="AAAA", pos=rack_position(0))

    events.sort(key=lambda e: e[0])
    with open(ev_path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["group", "day", "hour", "minute", "relativeTime", "timestamp",
                    "cage", "rack", "position", "event"])
        for rel, day, hh, mm, dt, ms, cage, rack, pos, event in events:
            w.writerow([group, day, hh, mm, rel, fmt_ts(dt, args.offset, ms),
                        cage, rack, pos, event])

    print(f"wrote {loc_path}  ({total_minutes} rows x {len(cages)} cages)")
    print(f"wrote {ev_path}   ({len(events)} events)")


if __name__ == "__main__":
    main()
