"""Theory: Q(phi), symbolic comparison conditions, direct antichains."""

import hashlib
import json
import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path


def enc(x):
    return (json.dumps(x, sort_keys=True, separators=(",", ":")) + "\n").encode()


def parse(x):
    return tuple(map(F, x))


def show(x):
    return list(map(str, x))


def add(x, y):
    return x[0] + y[0], x[1] + y[1]


def sub(x, y):
    return x[0] - y[0], x[1] - y[1]


def mul(x, y):
    return x[0] * y[0] + x[1] * y[1], x[0] * y[1] + x[1] * y[0] + x[1] * y[1]


ONE = (F(1), F(0))
PHI = (F(0), F(1))


def sign(x):
    a, b = x
    if b == 0:
        return (a > 0) - (a < 0)
    lo, hi = F(1), F(2)
    while True:
        v, w = a + b * lo, a + b * hi
        if v > 0 and w > 0:
            return 1
        if v < 0 and w < 0:
            return -1
        mid = (lo + hi) / 2
        if mid * mid - mid - 1 < 0:
            lo = mid
        else:
            hi = mid


def ge(x, y):
    return sign(sub(x, y)) >= 0


def inspect(spec, scales):
    a, b, c = scales
    pa, pb, pc = [mul(PHI, v) for v in scales]
    tests = [
        (0, 2, ge(pa, ONE)),
        (1, 2, ge(a, ONE)),
        (0, 3, ge(b, ONE)),
        (1, 3, ge(pb, ONE)),
        (0, 4, ge(pc, ONE)),
        (1, 4, ge(pc, ONE)),
        (2, 3, ge(b, pa)),
        (3, 2, ge(a, pb)),
        (2, 4, ge(c, a)),
        (4, 2, ge(a, pc)),
        (3, 4, ge(c, b)),
        (4, 3, ge(b, pc)),
    ]
    rel = {(i, j) for i, j, yes in tests if yes}
    counts = {}
    for mask in range(32):
        if any(mask >> i & 1 and mask >> j & 1 for i, j in rel):
            continue
        key = ((mask & 3).bit_count(), mask.bit_count())
        counts[key] = counts.get(key, 0) + 1
    H = [[*k, v] for k, v in sorted(counts.items())]
    retains = ge(a, ONE) and ge(b, ONE) and ge(c, a) and ge(c, b)
    target = retains and (ge(b, pa) or ge(a, pb))
    assert target == (retains and sorted(spec["target_H"]) == H)
    swap = spec["swap"]
    return dict(
        scales=[show(t) for t in scales],
        relation_mask=sum(1 << (5 * i + j) for i, j in rel),
        H=H,
        retains=retains,
        target=target,
        swap_invariant={(swap[i], swap[j]) for i, j in rel} == rel,
        reflection_closed=all(t == ONE for t in scales),
    )


def certificate(spec, scales):
    original = [tuple(parse(x) for x in v) for v in spec["roots"]]
    roots = [[mul(t, x) for x in v] for t, v in zip([ONE, ONE, *scales], original, strict=True)]
    a, b, c = scales
    if a != ONE:
        g, r, image = 0, 1, original[2]
    elif b != ONE:
        g, r, image = 1, 0, original[3]
    else:
        assert c != ONE
        g, r, image = 1, 2, original[4]
    return dict(
        core=inspect(spec, scales),
        positive_vectors=[[show(x) for x in v] for v in roots],
        missing_reflection=dict(generator=g, positive_root_index=r, image=[show(x) for x in image]),
    )


def main():
    spec = json.loads(Path(sys.argv[1]).read_text())
    out = Path(sys.argv[2])
    grid = list(map(parse, spec["scale_grid"]))
    stream = hashlib.sha256()
    groups = []
    totals = [0, 0, 0, 0]
    symmetric_targets = closed_targets = 0
    for i, j in product(range(len(grid)), repeat=2):
        sums = [0, 0, 0, 0]
        for k in range(len(grid)):
            core = inspect(spec, [grid[i], grid[j], grid[k]])
            stream.update(enc(dict(grid=[i, j, k], core=core)))
            vals = [core[n] for n in ["retains", "target", "swap_invariant", "reflection_closed"]]
            sums = [a + int(b) for a, b in zip(sums, vals, strict=True)]
            symmetric_targets += core["target"] and core["swap_invariant"]
            closed_targets += core["target"] and core["reflection_closed"]
        totals = [a + b for a, b in zip(totals, sums, strict=True)]
        groups.append([i, j, len(grid), *sums])
    boundaries = []
    for n in spec["epsilon_denominators"]:
        delta = (F(1, n), F(0))
        for name, scales, expect in [
            ("below", [ONE, sub(PHI, delta), PHI], False),
            ("above", [ONE, add(PHI, delta), add(PHI, delta)], True),
            ("top_too_low", [ONE, PHI, sub(PHI, delta)], False),
        ]:
            core = inspect(spec, scales)
            assert core["target"] == expect
            boundaries.append(dict(name=name, denominator=n, core=core))
    certs = [certificate(spec, ss) for ss in [[ONE, PHI, PHI], [PHI, ONE, PHI]]]
    featured = [c["core"] for c in certs]
    assert symmetric_targets == closed_targets == 0
    table = dict(
        group_columns=[
            "a_index",
            "b_index",
            "cases",
            "retains",
            "target",
            "swap_invariant",
            "reflection_closed",
        ],
        groups=groups,
        boundaries=boundaries,
        featured=featured,
        case_stream_sha256=stream.hexdigest(),
    )
    (out.parent / "theory-table.json").write_bytes(enc(table))
    summary = dict(
        cases=len(grid) ** 3,
        retaining_cases=totals[0],
        target_cases=totals[1],
        swap_invariant_cases=totals[2],
        reflection_closed_cases=totals[3],
        symmetric_targets=symmetric_targets,
        reflection_closed_targets=closed_targets,
        boundaries=len(boundaries),
        arithmetic_controls=5,
        table_sha256=hashlib.sha256(enc(table)).hexdigest(),
        case_stream_sha256=stream.hexdigest(),
        sharp_budget=["0", "1"],
        featured=featured,
    )
    out.write_bytes(enc(dict(summary=summary, certificates=certs)))
    print(json.dumps({k: v for k, v in summary.items() if k != "featured"}))


if __name__ == "__main__":
    main()
