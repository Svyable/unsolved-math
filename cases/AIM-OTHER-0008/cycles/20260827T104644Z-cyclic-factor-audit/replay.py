"""Replay both isolated lanes twice, compare evidence, and record execution."""

import hashlib
import json
import resource
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path


def limits():
    resource.setrlimit(resource.RLIMIT_CPU, (30, 30))
    resource.setrlimit(resource.RLIMIT_AS, (256 * 1024**2, 256 * 1024**2))
    resource.setrlimit(resource.RLIMIT_FSIZE, (32 * 1024**2, 32 * 1024**2))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    root = Path(__file__).resolve().parent
    outputs = [root / "verification-output.json", root / "theory-output.json"]
    runs = []
    first = None
    for _ in range(2):
        for script in ["verify.py", "theory.py"]:
            result = subprocess.run(
                [sys.executable, "-I", script],
                cwd=root,
                env={},
                check=True,
                capture_output=True,
                text=True,
                timeout=60,
                preexec_fn=limits,
            )
            runs.append(
                {
                    "command": f"python -I {script}",
                    "returncode": result.returncode,
                    "stdout_sha256": hashlib.sha256(result.stdout.encode()).hexdigest(),
                    "stderr": result.stderr,
                }
            )
        current = [path.read_bytes() for path in outputs]
        if first is None:
            first = current
        else:
            assert current == first, "nondeterministic output"
    theory = json.loads(outputs[1].read_text())
    verification = json.loads(outputs[0].read_text())
    common = [
        "systems",
        "positive_surjective_systems",
        "table_sha256",
        "weighting",
        "order_shortcut_false_positives",
    ]
    assert all(theory[key] == verification[key] for key in common)
    assert verification["mismatches"] == 0
    evidence = {
        "replayed_at": datetime.now(UTC).isoformat(),
        "python_version": sys.version,
        "runs": runs,
        "byte_identical_outputs": True,
        "common_fields_agree": common,
        "output_sha256": {path.name: digest(path) for path in outputs},
        "input_sha256": digest(root / "input.json"),
        "scripts_sha256": {name: digest(root / name) for name in ["verify.py", "theory.py"]},
        "uv_lock_sha256": digest(root.parents[3] / "uv.lock"),
        "wall_timeout_seconds": 60,
        "cpu_seconds": 30,
        "memory_megabytes": 256,
        "file_size_limit_megabytes": 32,
        "child_environment": "empty",
        "network_calls_in_experiments": 0,
        "os_network_namespace_isolation": False,
        "external_paid_model_calls": 0,
        "randomness": "none",
        "replay_subprocesses": 4,
        "exploratory_experiment_subprocesses_before_replay": 3,
        "independence": (
            "Different algorithms, fresh isolated child interpreters, no cross-lane imports "
            "or output consumption. Same assistant, shared spec/enumerator/runtime; "
            "not independent human/model proof review or kernel acceptance."
        ),
    }
    (root / "execution.json").write_text(json.dumps(evidence, indent=2) + "\n")
    print(json.dumps({"byte_identical_outputs": True, "common_fields_agree": common}))


if __name__ == "__main__":
    main()
