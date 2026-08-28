"""Direct inequality search and product-rational binomials, no theory imports."""

import argparse
import copy
import json
from fractions import Fraction
from pathlib import Path


def choose(n, r):
    value = Fraction(1)
    for j in range(1, r + 1):
        value *= Fraction(n - j + 1, j)
    assert value.denominator == 1
    return value.numerator


def threshold(k, d):
    b = choose(k + d, d)
    low, high = k, k + 1
    while (k + 1) * (high - k) < b:
        high = k + 2 * (high - k)
    while low + 1 < high:
        mid = (low + high) // 2
        if (k + 1) * (mid - k) >= b:
            high = mid
        else:
            low = mid
    assert (k + 1) * (high - k) >= b > (k + 1) * (high - k - 1)
    return b, high


def row(k, d):
    b, n = threshold(k, d)
    remainder = b % (k + 1)
    return dict(
        d=d,
        k=hex(k),
        binomial=hex(b),
        n=hex(n),
        slack=hex((k + 1) * (n - k) - b),
        predecessor_deficit=hex(b - (k + 1) * (n - 1 - k)),
        remainder=hex(remainder),
        floor_wrong=remainder != 0,
    )


def calculate(spec):
    # Counterexample/boundary probes precede recurrence confirmation.
    assert threshold(1, 2) == (3, 3)
    assert threshold(0, 2) == (1, 1)
    assert threshold(4, 3) == (35, 11)
    boundary = [row(k, d) for d in spec["boundary_d"] for k in spec["boundary_k"]]
    rows, k = [], 0
    for d in spec["degrees"]:
        if d > 2:
            a = choose(k + d - 2, d - 2)
            # Adjacent-binomial identity rather than two library calls.
            b = Fraction(a * (k + d - 1), d - 1)
            assert b.denominator == 1
            k = 1 + 2 * a + b.numerator
        rows.append(row(k, d))
    assert int(rows[3]["k"], 16) == spec["seed"]
    power = 1
    for _ in range(spec["dyadic_denominator"]):
        power *= spec["seed"]
    dyadic, two = 0, 1
    while two < power:
        two *= 2
        dyadic += 1
    assert two // 2 < power <= two
    comparisons, f = [], 1
    for d in range(2, max(spec["comparison_degrees"]) + 1):
        f *= d - 1
        if d not in spec["comparison_degrees"]:
            continue
        a = (d - 1) * f // 24
        assert 24 * a == (d - 1) * f
        e = dyadic * a // spec["dyadic_denominator"]
        if e * spec["dyadic_denominator"] < dyadic * a:
            e += 1
        comparisons.append(
            dict(
                d=d,
                seed_power_exponent=a,
                dyadic_exponent=e,
                imported_exponent=20 * a,
                published_exponent=d * f,
            )
        )
        if d in spec["degrees"]:
            n = int(rows[d - 2]["n"], 16)
            assert n <= spec["seed"] ** a <= 2**e <= 2 ** (20 * a)
    return dict(
        rows=rows,
        boundary=boundary,
        comparisons=comparisons,
        dyadic=dict(
            denominator=spec["dyadic_denominator"],
            numerator=dyadic,
            seed_power=hex(power),
            lower_gap=hex(power - two // 2),
            upper_gap=hex(two - power),
        ),
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("--certificate")
    args = parser.parse_args()
    spec = json.loads(Path(args.input).read_text())
    core = calculate(spec)
    rejected = []
    if args.certificate:
        supplied = json.loads(Path(args.certificate).read_text())["core"]
        assert supplied == core
        for name in ["floor", "seed", "omit", "slack", "log_floor", "exponent", "boundary"]:
            bad = copy.deepcopy(supplied)
            if name == "floor":
                bad["rows"][3]["n"] = hex(int(bad["rows"][3]["n"], 16) - 1)
            elif name == "seed":
                bad["rows"][3]["k"] = hex(spec["seed"] - 1)
            elif name == "omit":
                bad["rows"].pop()
            elif name == "slack":
                bad["rows"][3]["slack"] = "0x0"
            elif name == "log_floor":
                bad["dyadic"]["numerator"] -= 1
            elif name == "exponent":
                bad["comparisons"][2]["dyadic_exponent"] -= 1
            else:
                bad["boundary"][1]["n"] = "0x2"
            assert bad != core
            rejected.append(name)
    result = dict(
        core=core,
        method="rational products, direct inequality binary search",
        rejected=rejected,
        cases=len(core["boundary"]),
    )
    Path(args.output).write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(
        json.dumps(
            dict(
                rows=len(core["rows"]),
                boundary=len(core["boundary"]),
                floor_failures=sum(r["floor_wrong"] for r in core["boundary"]),
                rejected=len(rejected),
            )
        )
    )


if __name__ == "__main__":
    main()
