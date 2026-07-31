#!/usr/bin/env python3
"""Run the independently pinned RO-Crate and ISA evidence validator."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CRATE = ROOT / "examples" / "isa-roundtrip"
EXPECTED_VALIDATOR = "0.11.3"
KNOWN_BASE_MESSAGE = (
    "The RO-Crate metadata file descriptor MUST have a `conformsTo` property "
    "with the RO-Crate specification version"
)


def run_validation(profile: str, inherit: bool) -> tuple[int, dict]:
    with tempfile.TemporaryDirectory(prefix="hcmo-rocrate-") as tmp:
        report = Path(tmp) / "report.json"
        command = [
            "rocrate-validator",
            "validate",
            str(CRATE),
            "--profile-identifier",
            profile,
            "--requirement-severity",
            "required",
            "--output-format",
            "json",
            "--output-file",
            str(report),
        ]
        if not inherit:
            command.append("--disable-profile-inheritance")
        completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
        if not report.exists():
            raise RuntimeError(
                f"validator did not produce a report for {profile}: "
                f"stdout={completed.stdout!r} stderr={completed.stderr!r}"
            )
        return completed.returncode, json.loads(report.read_text(encoding="utf-8"))


def main() -> int:
    if shutil.which("rocrate-validator") is None:
        print("[FAIL] rocrate-validator is not installed; install tooling/interoperability-requirements.txt")
        return 1
    try:
        installed = version("roc-validator")
    except PackageNotFoundError:
        print("[FAIL] roc-validator package metadata not found")
        return 1
    if installed != EXPECTED_VALIDATOR:
        print(f"[FAIL] roc-validator {installed} installed; expected {EXPECTED_VALIDATOR}")
        return 1

    core_code, core = run_validation("ro-crate-1.2", inherit=True)
    if core_code != 0 or not core.get("passed"):
        print(f"[FAIL] RO-Crate 1.2 required validation: {core.get('issues', [])}")
        return 1
    print("[OK]   RO-Crate 1.2 required validation")

    isa_code, isa = run_validation("isa-ro-crate", inherit=False)
    if isa_code != 0 or not isa.get("passed"):
        print(f"[FAIL] ISA-specific required validation: {isa.get('issues', [])}")
        return 1
    print("[OK]   ISA-specific required validation")

    inherited_code, inherited = run_validation("isa-ro-crate", inherit=True)
    if inherited_code == 0 and inherited.get("passed"):
        print("[OK]   full inherited ISA validation (upstream base-version mismatch appears resolved)")
        return 0
    messages = [issue.get("message") for issue in inherited.get("issues", [])]
    if messages == [KNOWN_BASE_MESSAGE]:
        print("[OK]   known upstream ISA/RO-Crate base-version mismatch isolated; no other required issue")
        return 0
    print(f"[FAIL] full inherited ISA validation has unexpected issues: {inherited.get('issues', [])}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
