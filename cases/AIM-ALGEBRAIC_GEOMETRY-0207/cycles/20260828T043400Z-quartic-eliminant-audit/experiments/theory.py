"""Sparse coefficient identity and anharmonic-orbit calculation."""

import json
import sys
from fractions import Fraction as F
from pathlib import Path


def add(a, b, scale=1):
    out = dict(a)
    for monomial, coefficient in b.items():
        out[monomial] = out.get(monomial, 0) + scale * coefficient
    return {m: c for m, c in out.items() if c}


def mul(a, b):
    out = {}
    for (i, j), c in a.items():
        for (k, ell), d in b.items():
            out[i + k, j + ell] = out.get((i + k, j + ell), 0) + c * d
    return {m: c for m, c in out.items() if c}


def power(a, n):
    out = {(0, 0): 1}
    for _ in range(n):
        out = mul(out, a)
    return out


def evaluate(poly, s, t):
    return sum(c * s**i * t**j for (i, j), c in poly.items())


def invariants(a, b, c, d, e):
    i = 12 * a * e - 3 * b * d + c**2
    j = 72 * a * c * e + 9 * b * c * d - 27 * a * d**2 - 27 * b**2 * e - 2 * c**3
    return [str(i), str(j), str(F(4 * i**3 - j**2, 27))]


def orbit(t):
    return {t, 1 - t, 1 / t, 1 / (1 - t), t / (t - 1), (t - 1) / t}


def main():
    spec = json.loads(Path(sys.argv[1]).read_text())
    one, s, t = {(0, 0): 1}, {(1, 0): 1}, {(0, 1): 1}
    si = add(add(power(s, 2), s, -1), one)
    ti = add(add(power(t, 2), t, -1), one)
    sj = mul(mul(add(s, one), add(add(s, s), one, -1)), add(s, one, -2))
    tj = mul(mul(add(t, one), add(add(t, t), one, -1)), add(t, one, -2))
    identity = add(mul(power(sj, 2), power(ti, 3)), mul(power(tj, 2), power(si, 3)), -1)
    factors = [
        add(s, t, -1),
        add(add(s, t), one, -1),
        add(mul(t, s), one, -1),
        add(mul(add(one, t, -1), s), one, -1),
        add(mul(add(t, one, -1), s), t, -1),
        add(add(mul(t, s), t, -1), one),
    ]
    product = {(0, 0): -27}
    for factor in factors:
        product = mul(product, factor)
    assert identity == product
    assert max(i for i, _ in identity) <= 6 and max(j for _, j in identity) <= 6
    intervals = [(-3, -2), (-1, 0), (0, 1), (2, 3)]

    def realpoly(x):
        return x**4 - 6 * x * x + 1

    for a, b in intervals:
        assert realpoly(a) * realpoly(b) < 0
    # Four disjoint sign-change intervals exhaust the degree; X^4+Y^4 is positive.
    boundary = dict(
        real_invariants=[invariants(1, 0, 0, 0, 1), invariants(1, 0, -6, 0, 1)],
        real_root_counts=[0, 4],
        repeated_invariants=[invariants(1, 0, 0, 0, 0), invariants(0, 1, 0, 0, 0)],
        multiplicities=[[4], [3, 1]],
        i_zero=invariants(1, 0, 0, 1, 0),
    )
    grid = [
        [x, y, str(evaluate(identity, x, y))]
        for x in spec["interpolation_grid"]
        for y in spec["interpolation_grid"]
    ]
    values = sorted(
        {F(p, q) for p in spec["numerators"] for q in spec["denominators"]} - {F(0), F(1)}
    )
    rows = []
    for x in values:
        for y in values:
            equivalent = x in orbit(y)
            assert equivalent == (evaluate(identity, x, y) == 0)
            rows.append([str(x), str(y), 24 // len(orbit(y)) if equivalent else 0])
    result = dict(
        boundary=boundary,
        identity_grid=grid,
        rows=rows,
        parameter_count=len(values),
        pair_count=len(rows),
        equivalent_pairs=sum(r[2] > 0 for r in rows),
        projective_maps=sum(r[2] for r in rows),
    )
    Path(sys.argv[2]).write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    details = dict(
        identity_coefficients=[[i, j, c] for (i, j), c in sorted(identity.items())],
        real_root_intervals=intervals,
        harmonic_orbit=sorted(map(str, orbit(F(2)))),
        identity="J(s)^2 I(t)^3-J(t)^2 I(s)^3 = -27 product of the six displayed factors",
    )
    Path(sys.argv[2]).with_name("theory-details.json").write_text(
        json.dumps(details, sort_keys=True, indent=2) + "\n"
    )
    print(
        json.dumps(
            {
                k: result[k]
                for k in ["parameter_count", "pair_count", "equivalent_pairs", "projective_maps"]
            }
        )
    )


if __name__ == "__main__":
    main()
