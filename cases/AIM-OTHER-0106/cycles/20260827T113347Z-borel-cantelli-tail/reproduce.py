"""Bounded replay; generated evidence, empty environment, no model/network calls."""

import hashlib
import json
import resource
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def limits():
    resource.setrlimit(resource.RLIMIT_CPU, (180, 180))
    resource.setrlimit(resource.RLIMIT_AS, (512 * 1024 * 1024, 512 * 1024 * 1024))
    resource.setrlimit(resource.RLIMIT_FSIZE, (16 * 1024 * 1024, 16 * 1024 * 1024))


def run(script, output, *args):
    before = time.monotonic()
    command = [sys.executable, "-I", script, *args]
    proc = subprocess.run(
        command, cwd=ROOT, env={}, capture_output=True, timeout=200, check=True, preexec_fn=limits
    )
    value = json.loads(proc.stdout)
    (ROOT / output).write_bytes(proc.stdout)
    return value, {
        "command": command,
        "exit_code": proc.returncode,
        "seconds": round(time.monotonic() - before, 3),
        "stdout_sha256": hashlib.sha256(proc.stdout).hexdigest(),
        "stderr": proc.stderr.decode(),
    }


if __name__ == "__main__":
    if "--baseline" in sys.argv:
        _, log = run("verify.py", "verification-baseline.json")
        (ROOT / "baseline-execution.json").write_text(json.dumps(log, indent=2) + "\n")
        print(json.dumps(log))
    else:
        theory, tlog = run("theory.py", "theory-output.json")
        verification, vlog = run("verify.py", "verification-output.json", "theory-output.json")
        for key in ["events", "rows", "independence_counterexample"]:
            assert theory[key] == verification[key]
        baseline = json.loads((ROOT / "verification-baseline.json").read_text())
        assert all(verification[key] == value for key, value in baseline.items())
        log = {
            "python": sys.version,
            "runs": [tlog, vlog],
            "matched_rows": len(theory["rows"]),
            "matched_events": len(theory["events"]),
            "mismatches": 0,
            "isolation": (
                "Fresh -I interpreters; empty environment; CPU/memory/file "
                "and wall-clock limits. No network code; OS network namespace "
                "not isolated. Same-assistant code authorship."
            ),
        }
        (ROOT / "execution.json").write_text(json.dumps(log, indent=2) + "\n")
        print(json.dumps(log, indent=2))
