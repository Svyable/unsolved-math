"""Bounded fresh-process replay with no experiment network or model calls."""

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
    start = time.monotonic()
    command = [sys.executable, "-I", script, *args]
    proc = subprocess.run(
        command, cwd=ROOT, env={}, capture_output=True, timeout=200, preexec_fn=limits, check=True
    )
    value = json.loads(proc.stdout)
    (ROOT / output).write_bytes(proc.stdout)
    return value, {
        "command": command,
        "exit_code": proc.returncode,
        "seconds": round(time.monotonic() - start, 3),
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
        baseline = json.loads((ROOT / "verification-baseline.json").read_text())
        assert theory["core"] == verification["core"] == baseline["core"]
        assert all(verification[k] == v for k, v in baseline.items())
        log = {
            "runs": [tlog, vlog],
            "python": sys.version,
            "core_matches": True,
            "isolation": (
                "Fresh -I interpreters and empty environments; CPU, wall, memory and "
                "file limits. No network code; no OS network namespace. "
                "Same-assistant authorship, not independent human/model review."
            ),
        }
        (ROOT / "execution.json").write_text(json.dumps(log, indent=2) + "\n")
        print(json.dumps(log, indent=2))
