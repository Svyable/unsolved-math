"""Verifier first: Q(sqrt(5)), coordinate order, ideal maxima and literal reflections."""

import argparse
import copy
import hashlib
import json
from fractions import Fraction as F
from itertools import product
from pathlib import Path


def enc(x):
    return (json.dumps(x, sort_keys=True, separators=(",", ":")) + "\n").encode()


def add(x, y):
    return (x[0] + y[0], x[1] + y[1])


def neg(x):
    return (-x[0], -x[1])


def mul(x, y):
    return (x[0] * y[0] + 5 * x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def sub(x, y):
    return add(x, neg(y))


def sg(x):
    a, b = x
    if b == 0:
        return (a > 0) - (a < 0)
    if a == 0:
        return (b > 0) - (b < 0)
    if a > 0 and b > 0:
        return 1
    if a < 0 and b < 0:
        return -1
    v = a * a - 5 * b * b
    return ((v > 0) - (v < 0)) * (1 if a > 0 else -1)


def parse(x):
    a, b = map(F, x)
    return a + b / 2, b / 2


def show(x):
    return [str(x[0] - x[1]), str(2 * x[1])]


def vector(v):
    return [show(x) for x in v]


PHI = (F(1, 2), F(1, 2))
ONE = (F(1), F(0))
ZERO = (F(0), F(0))


def reflect(v, g):
    x, y = v
    return (sub(mul(PHI, y), x), y) if g == 0 else (x, sub(mul(PHI, x), y))


def inspect(spec, scales):
    roots = [tuple(parse(x) for x in v) for v in spec["roots"]]
    roots = [tuple(mul(t, x) for x in v) for t, v in zip([ONE, ONE, *scales], roots, strict=True)]
    rel = {
        (i, j)
        for i in range(5)
        for j in range(5)
        if i != j and all(sg(sub(roots[j][z], roots[i][z])) >= 0 for z in range(2))
    }
    counts = {}
    for ideal in range(32):
        if any(ideal >> j & 1 and not ideal >> i & 1 for i, j in rel):
            continue
        A = [
            i
            for i in range(5)
            if ideal >> i & 1 and not any(ideal >> j & 1 and (i, j) in rel for j in range(5))
        ]
        key = (sum(i in spec["simple_indices"] for i in A), len(A))
        counts[key] = counts.get(key, 0) + 1
    H = [[*k, v] for k, v in sorted(counts.items())]
    retains = set(map(tuple, spec["original_relations"])) <= rel
    swap = spec["swap"]
    symmetric = {(swap[i], swap[j]) for i, j in rel} == rel
    signed = roots + [tuple(neg(x) for x in v) for v in roots]
    closed = all(reflect(v, g) in signed for g in range(2) for v in signed)
    core = dict(
        scales=[show(t) for t in scales],
        relation_mask=sum(1 << (5 * i + j) for i, j in rel),
        H=H,
        retains=retains,
        target=retains and sorted(spec["target_H"]) == H,
        swap_invariant=symmetric,
        reflection_closed=closed,
    )
    return core, roots, signed


def baseline(spec, outdir):
    # Counterexample and exact arithmetic boundary checks before the census.
    counter, roots, signed = inspect(spec, [ONE, PHI, PHI])
    assert counter["target"] and not counter["reflection_closed"] and not counter["swap_invariant"]
    assert reflect(roots[0], 1) not in signed
    assert [sg(x) for x in [ZERO, ONE, neg(ONE), (F(-2), F(1)), (F(-9, 4), F(1))]] == [
        0,
        1,
        -1,
        1,
        -1,
    ]
    base, _, _ = inspect(spec, [ONE, ONE, ONE])
    assert base["reflection_closed"] and base["swap_invariant"] and not base["target"]
    grid = list(map(parse, spec["scale_grid"]))
    stream = hashlib.sha256()
    groups = []
    totals = [0, 0, 0, 0]
    symmetric_targets = closed_targets = 0
    for i, j in product(range(len(grid)), repeat=2):
        sums = [0, 0, 0, 0]
        for k in range(len(grid)):
            core, _, _ = inspect(spec, [grid[i], grid[j], grid[k]])
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
            core, _, _ = inspect(spec, scales)
            assert core["target"] == expect
            boundaries.append(dict(name=name, denominator=n, core=core))
    featured = [inspect(spec, ss)[0] for ss in [[ONE, PHI, PHI], [PHI, ONE, PHI]]]
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
    (outdir / "verification-table.json").write_bytes(enc(table))
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
    return summary


def check(spec, cert, summary):
    assert cert["summary"] == summary
    assert len(cert["certificates"]) == 2
    for index, item in enumerate(cert["certificates"]):
        core, roots, signed = inspect(spec, list(map(parse, item["core"]["scales"])))
        assert core == summary["featured"][index] == item["core"]
        assert item["positive_vectors"] == list(map(vector, roots))
        witness = item["missing_reflection"]
        g = witness["generator"]
        r = witness["positive_root_index"]
        assert g in [0, 1] and r in range(5)
        actual = reflect(roots[r], g)
        assert vector(actual) == witness["image"] and actual not in signed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path)
    ap.add_argument("output", type=Path)
    ap.add_argument("--certificate", type=Path)
    args = ap.parse_args()
    spec = json.loads(args.input.read_text())
    summary = baseline(spec, args.output.parent)
    result = summary
    if args.certificate:
        cert = json.loads(args.certificate.read_text())
        check(spec, cert, summary)
        rejected = []
        for j in range(7):
            bad = copy.deepcopy(cert)
            if j == 0:
                bad["summary"]["sharp_budget"] = ["3/2", "0"]
            if j == 1:
                bad["summary"]["target_cases"] += 1
            if j == 2:
                bad["certificates"][0]["core"]["reflection_closed"] = True
            if j == 3:
                bad["certificates"][0]["positive_vectors"][2][0] = ["0", "0"]
            if j == 4:
                bad["certificates"][0]["missing_reflection"]["image"][0] = ["0", "0"]
            if j == 5:
                bad["certificates"].pop()
            if j == 6:
                bad["certificates"][0]["core"]["swap_invariant"] = True
            try:
                check(spec, bad, summary)
            except AssertionError:
                rejected.append(j)
            else:
                raise AssertionError("corruption accepted")
        (args.output.parent / "verification-certificates.json").write_bytes(
            enc(
                dict(
                    checked=cert["certificates"],
                    independence=(
                        "Checked using radical coordinates, ideal maxima and literal "
                        "reflected-vector membership; no theory import."
                    ),
                )
            )
        )
        result = dict(summary=summary, certificates_checked=2, corruptions_rejected=rejected)
    args.output.write_bytes(enc(result))
    print(json.dumps({k: v for k, v in summary.items() if k != "featured"}))


if __name__ == "__main__":
    main()
