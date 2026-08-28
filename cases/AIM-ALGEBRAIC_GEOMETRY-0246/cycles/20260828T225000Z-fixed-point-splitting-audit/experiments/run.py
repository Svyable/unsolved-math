"""Bounded fresh-process runner; isolation is process/resource, not a network namespace."""

import argparse
import hashlib
import json
import resource
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path


def limits():
    resource.setrlimit(resource.RLIMIT_CPU, (180, 180))
    resource.setrlimit(resource.RLIMIT_AS, (512 * 1024**2, 512 * 1024**2))
    resource.setrlimit(resource.RLIMIT_FSIZE, (16 * 1024**2, 16 * 1024**2))
    resource.setrlimit(resource.RLIMIT_NOFILE, (64, 64))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["baseline", "theory", "verify", "replay"])
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    modes = (
        ["theory", "verify"]
        if args.mode == "replay"
        else ["source"]
        if args.mode == "sourcereplay"
        else [args.mode]
    )
    logs = []
    for mode in modes:
        script = (
            "source.py" if mode == "source" else "theory.py" if mode == "theory" else "verify.py"
        )
        out = "baseline.json" if mode == "baseline" else mode + "-output.json"
        path = root / "experiments" / out
        before = digest(path) if args.mode in {"replay", "sourcereplay"} else None
        cmd = [
            sys.executable,
            "-I",
            str(root / "experiments" / script),
            str(root / "input.json"),
            str(path),
        ]
        if mode in {"verify", "source"}:
            cmd += ["--certificate", str(root / "experiments/theory-output.json")]
        start = datetime.now(UTC).isoformat()
        proc = subprocess.run(
            cmd,
            cwd=root,
            env={},
            capture_output=True,
            text=True,
            timeout=200,
            preexec_fn=limits,
            check=False,
        )
        if proc.returncode:
            failed = dict(
                command=cmd,
                started_at=start,
                finished_at=datetime.now(UTC).isoformat(),
                exit_code=proc.returncode,
                stdout=proc.stdout,
                stderr=proc.stderr,
                source_sha256=digest(root / "experiments" / script),
                input_sha256=digest(root / "input.json"),
            )
            (root / "experiments" / "failed-execution.json").write_text(
                json.dumps(failed, sort_keys=True, indent=2) + "\n"
            )
            print(proc.stderr)
            raise RuntimeError("mathematical child failed; see failed-execution.json")
        after = digest(path)
        if before is not None:
            assert before == after, "replay changed output"
        logs.append(
            dict(
                mode=mode,
                started_at=start,
                finished_at=datetime.now(UTC).isoformat(),
                python=sys.version,
                command=cmd,
                environment_keys=[],
                exit_code=proc.returncode,
                stdout=proc.stdout,
                stderr=proc.stderr,
                output_sha256=after,
                source_sha256=digest(root / "experiments" / script),
                input_sha256=digest(root / "input.json"),
                cpu_seconds=180,
                wall_timeout_seconds=200,
                memory_bytes=512 * 1024**2,
                isolation=(
                    "python -I, empty environment, fresh process, resource limits; "
                    "no network namespace"
                ),
                replay_unchanged=before == after if before else None,
            )
        )
        print(proc.stdout.strip())
    log_path = root / "experiments" / f"{args.mode}-execution.json"
    if args.mode not in {"replay", "sourcereplay"} or not log_path.exists():
        log_path.write_text(json.dumps(logs, sort_keys=True, indent=2) + "\n")


if __name__ == "__main__":
    main()
