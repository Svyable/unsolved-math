"""Two-generator lift presentation, not the bar-chain reduction."""

import argparse
import hashlib
import json
from math import gcd
from pathlib import Path


def encoded(x):
    return json.dumps(x, sort_keys=True, separators=(",", ":")).encode()


def profile(m, k, length):
    d = gcd(m, k)
    return dict(m=m, k=k, subdivision=length, h1=dict(free_rank=1, torsion=[d] if d > 1 else []))


def certificate(m, k, length):
    d = gcd(m, k)
    n, step = m * length, k * length
    covector = [m // d]
    covector += [
        ((v + g * step) // n) * (m // d) - g * (k // d) for g in range(1, m) for v in range(n)
    ]
    return dict(
        **profile(m, k, length), relation=[k, m], free_covector=covector, fiber_value=m // d
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    args = ap.parse_args()
    spec = json.loads(Path(args.input).read_text())
    rows = [
        profile(m, k, length)
        for m in spec["group_orders"]
        for k in range(m)
        for length in spec["subdivisions"]
    ]
    out = dict(
        profiles=rows,
        certificates=[certificate(*x) for x in spec["certificates"]],
        profile_count=len(rows),
        profiles_sha256=hashlib.sha256(encoded(rows)).hexdigest(),
    )
    Path(args.output).write_text(json.dumps(out, sort_keys=True, indent=2) + "\n")
    print(json.dumps({k: v for k, v in out.items() if k not in {"profiles", "certificates"}}))


if __name__ == "__main__":
    main()
