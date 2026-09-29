# Live Mouse Tracker (LMT) — HCMO reference example

**Second worked example** for HCMO validation and the first open-source one: a
depth-camera and RFID tracker for group-housed rodents, with a **source-cited
system profile** and a **documented schema** read from the public sample
experiment database.

| | |
|---|---|
| **System** | Live Mouse Tracker (LMT) |
| **Authors** | de Chaumont et al. 2019, <https://doi.org/10.1038/s41551-019-0396-1> |
| **Modality** | Depth video (Kinect, 30 frames/s) + RFID (134.2 kHz FDX-B) |
| **Key outputs** | Per-frame positions and postures; individual, dyadic and group behavioural events |
| **Housing** | Group (up to four animals in the sample and the paper) |
| **Data** | One SQLite database per experiment, plus MP4 video in 10-minute segments |
| **Home page** | <https://micecraft.org/lmt/> |

## Contents

```
live-mouse-tracker/
  README.md                 ← this file
  lmt-system-profile.md     ← source-cited profile: sensors, schema, events, HCMO notes
```

The public sample database (141 MB) is **not** committed; its URL, size and
SHA-256 are in [`lmt-system-profile.md`](lmt-system-profile.md) §7.

HCMO vocabulary concepts: system `sys:live-mouse-tracker` (short name `LMT`);
file formats `ff:live-mouse-tracker-sqlite` and `ff:live-mouse-tracker-video` in
[`../../../../vocabularies/file-formats.ttl`](../../../../vocabularies/file-formats.ttl).
