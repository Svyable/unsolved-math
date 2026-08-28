"""Exact support-envelope critical-point certificate generator."""

import hashlib
import itertools
import json
import sys
from fractions import Fraction as F
from pathlib import Path


def packed(obj):
    return (json.dumps(obj, sort_keys=True, separators=(",", ":")) + "\n").encode()


def row(par):
    d, e, v, a, eps, total = par
    c = a - eps

    def support(t):
        return v * t - c * t * t / 2 + abs(d + e * t) + abs(d - e * t)

    knot = min(total, d / e) if e else total
    pieces = [(F(0), knot, v), (knot, total, v + 2 * e)]
    candidates = {F(0), knot, total}
    for lo, hi, slope in pieces:
        if c > 0 and lo <= slope / c <= hi:
            candidates.add(slope / c)
    value, negtime = max((support(t), -t) for t in candidates)
    grid = max(support(t) for t in [F(0), total / 2, total])
    box_times = {F(0), total}
    if c > 0 and 0 <= (v + 2 * e) / c <= total:
        box_times.add((v + 2 * e) / c)
    box = max(2 * d + (v + 2 * e) * t - c * t * t / 2 for t in box_times)
    return [*[str(x) for x in par], str(value), str(-negtime), str(grid), str(box)]


def main():
    spec = json.loads(Path(sys.argv[1]).read_text())
    output = Path(sys.argv[2])
    rows = [row(par) for par in itertools.product(*[list(map(F, x)) for x in spec["parameters"]])]
    table = packed(rows)
    counts = {"concave": 0, "linear": 0, "convex": 0}
    for r in rows:
        c = F(r[3]) - F(r[4])
        counts["concave" if c > 0 else "linear" if c == 0 else "convex"] += 1
    summary = dict(
        cases=len(rows),
        table_sha256=hashlib.sha256(table).hexdigest(),
        sample_misses=sum(F(r[8]) < F(r[6]) for r in rows),
        strict_box_gaps=sum(F(r[6]) < F(r[9]) for r in rows),
        base=row(list(map(F, spec["base"]))),
        curvature_counts=counts,
    )
    # Explicit realization of the interior support maximum; no fitted numeric values.
    d, e, v, a, eps, total = map(F, spec["base"])
    time = (v + 2 * e) / (a - eps)
    value = (v + 2 * e) * time - (a - eps) * time * time / 2
    witness = dict(
        z=["1", "-1"],
        initial_x="0",
        initial_v=str(v + 2 * e),
        w=str(eps),
        time=str(time),
        value=str(value),
        grid_max=summary["base"][8],
        box_max=summary["base"][9],
        sample_threshold=spec["sample_threshold"],
        safe_threshold=spec["safe_threshold"],
    )
    assert 0 < d / e < time < total
    assert value - F(spec["sample_threshold"]) == F(1, 40)
    assert F(spec["safe_threshold"]) - value == F(1, 20)
    output.with_name("theory-table.json").write_bytes(table)
    output.write_bytes(packed(dict(summary=summary, witness=witness)))
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
