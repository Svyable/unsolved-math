"""Exact library-binomial recurrence and quotient/remainder certificates."""

import json
import sys
from math import comb, factorial
from pathlib import Path


def row(k, d):
    b = comb(k + d, d)
    quotient, remainder = divmod(b, k + 1)
    n = k + quotient + bool(remainder)
    slack = (k + 1) * (n - k) - b
    deficit = b - (k + 1) * (n - 1 - k)
    assert 0 <= slack < k + 1 and 0 < deficit <= k + 1
    return dict(
        d=d,
        k=hex(k),
        binomial=hex(b),
        n=hex(n),
        slack=hex(slack),
        predecessor_deficit=hex(deficit),
        remainder=hex(remainder),
        floor_wrong=remainder != 0,
    )


def main():
    spec = json.loads(Path(sys.argv[1]).read_text())
    k, rows = 0, []
    for d in spec["degrees"]:
        if d > 2:
            k = 1 + 2 * comb(k + d - 2, d - 2) + comb(k + d - 1, d - 1)
        rows.append(row(k, d))
    assert int(rows[3]["k"], 16) == spec["seed"]
    boundary = [row(k, d) for d in spec["boundary_d"] for k in spec["boundary_k"]]
    power = spec["seed"] ** spec["dyadic_denominator"]
    numerator = (power - 1).bit_length()
    two = 1 << numerator
    assert two // 2 < power <= two
    comparisons = []
    for d in spec["comparison_degrees"]:
        a = (d - 1) * factorial(d - 1) // 24
        e = (numerator * a + spec["dyadic_denominator"] - 1) // spec["dyadic_denominator"]
        comparisons.append(
            dict(
                d=d,
                seed_power_exponent=a,
                dyadic_exponent=e,
                imported_exponent=20 * a,
                published_exponent=factorial(d),
            )
        )
        assert e <= 20 * a < factorial(d)
        if d in spec["degrees"]:
            n = int(rows[d - 2]["n"], 16)
            assert n <= spec["seed"] ** a <= 2**e
    core = dict(
        rows=rows,
        boundary=boundary,
        comparisons=comparisons,
        dyadic=dict(
            denominator=spec["dyadic_denominator"],
            numerator=numerator,
            seed_power=hex(power),
            lower_gap=hex(power - two // 2),
            upper_gap=hex(two - power),
        ),
    )
    result = dict(core=core, method="math.comb, divmod, factorial and integer bit length")
    Path(sys.argv[2]).write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(
        json.dumps(
            dict(
                rows=len(rows),
                boundary=len(boundary),
                seed_dyadic=[numerator, spec["dyadic_denominator"]],
                degree7_exponents=comparisons[2],
            )
        )
    )


if __name__ == "__main__":
    main()
