"""Exact Sylvester determinant and standard-monomial ghost certificates."""

import argparse
import itertools
import json
from pathlib import Path

PERMS = [
    (s, (-1) ** sum(s[i] > s[j] for i in range(4) for j in range(i + 1, 4)))
    for s in itertools.permutations(range(4))
]


def resultant(f, g, p):
    # Degree-three multiplication map S_1^2 -> S_3, with columns f, xf, g, xg
    # after dehomogenizing y=1. No gcd or row-reduction calls.
    a, b, c = f
    d, e, h = g
    m = [[a, 0, d, 0], [b, a, e, d], [c, b, h, e], [0, c, 0, h]]
    return sum(sign * m[0][s[0]] * m[1][s[1]] * m[2][s[2]] * m[3][s[3]] for s, sign in PERMS) % p


def rational_common_zero(f, g, p):
    points = [(1, 0)] + [(x, 1) for x in range(p)]
    values = []
    for x, y in points:
        fv = f[0] * y * y + f[1] * x * y + f[2] * x * x
        gv = g[0] * y * y + g[1] * x * y + g[2] * x * x
        values.append(fv % p == gv % p == 0)
    return any(values)


def compute(spec):
    census = []
    for p in spec["fields"]:
        accepted, false_positive = [], []
        for index, values in enumerate(itertools.product(range(p), repeat=6)):
            f, g = values[:3], values[3:]
            good = resultant(f, g, p) != 0
            if good:
                accepted.append(index)
            if not good and not rational_common_zero(f, g, p):
                false_positive.append(index)
        census.append(dict(p=p, total=p**6, accepted=accepted, false_positive=false_positive))
    ghosts = []
    for p in spec["ghost_fields"]:
        for a in spec["ghost_shifts"]:
            for d in spec["ghost_degrees"]:
                basis = [(i, j) for i in range(d) for j in range(d)]
                rows = [
                    [n, sum(i + j == n - a for i, j in basis), 0, 0] for n in range(a + 2 * d + 3)
                ]
                assert sum(row[1] for row in rows) == d * d
                ghosts.append(dict(a=a, d=d, p=p, homology=rows))
    # In F2[t]/(t²+t+1), (1+t+t²) reduces to (1+1)+(1+1)t.
    ce = spec["rational_point_counterexample"]
    f = ce["f"]
    assert f == ce["g"] == [1, 1, 1]
    remainder = [(f[0] + f[2]) % 2, (f[1] + f[2]) % 2]
    assert remainder == [0, 0]
    rational_values = [(f[0] + f[1] * x + f[2] * x * x) % 2 for x in range(2)] + [f[2]]
    return dict(
        census=census,
        ghosts=ghosts,
        counterexample=dict(rational_values=rational_values, extension_value=0),
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    core = compute(json.loads(args.input.read_text()))
    result = dict(method="24-term exact Sylvester determinant; monomial quotient basis", core=core)
    args.output.write_text(json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n")
    print(
        json.dumps(
            dict(
                cases=sum(x["total"] for x in core["census"]),
                accepted=sum(len(x["accepted"]) for x in core["census"]),
                rational_false_positives=sum(len(x["false_positive"]) for x in core["census"]),
                ghost_cases=len(core["ghosts"]),
            )
        )
    )


if __name__ == "__main__":
    main()
