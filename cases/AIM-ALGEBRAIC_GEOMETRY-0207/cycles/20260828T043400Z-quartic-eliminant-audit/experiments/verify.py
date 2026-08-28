"""Independent direct projective-map enumeration; no theory imports."""

import argparse
import copy
import json
from fractions import Fraction as Q
from itertools import pairwise, permutations
from pathlib import Path


def trim(p):
    while p and p[-1] == 0:
        p.pop()
    return p


def derivative(p):
    return trim([i * p[i] for i in range(1, len(p))])


def remainder(a, b):
    a = list(a)
    while len(a) >= len(b) and a:
        r, c = len(a) - len(b), a[-1] / b[-1]
        for j, x in enumerate(b):
            a[j + r] -= c * x
        trim(a)
    return a


def sturm(coeff):
    p = trim(list(map(Q, reversed(coeff))))
    seq = [p, derivative(p)]
    while seq[-1]:
        r = [-x for x in remainder(seq[-2], seq[-1])]
        if not r:
            break
        seq.append(r)
    assert len(seq[-1]) == 1, "not squarefree"

    def variation(negative):
        signs = [
            (1 if p[-1] > 0 else -1) * (-1 if negative and (len(p) - 1) % 2 else 1) for p in seq
        ]
        return sum(a != b for a, b in pairwise(signs))

    return variation(True) - variation(False)


def inv(coeff):
    a, b, c, d, e = map(Q, coeff)
    i = c * c - 3 * b * d + 12 * a * e
    j = -2 * c * c * c + 9 * b * c * d + 72 * a * c * e - 27 * (a * d * d + b * b * e)
    return [str(i), str(j), str((4 * i**3 - j * j) / 27)]


def det(a, b):
    return a[0] * b[1] - a[1] * b[0]


def maps(s, t):
    points = [(Q(1), Q(0)), (Q(0), Q(1)), (Q(1), Q(1)), (t, Q(1))]
    total = 0
    for a, b, c, d in permutations(points):
        u, v = det(c, b), det(a, c)
        assert u * v * det(a, b) != 0
        image = (u * s * a[0] + v * b[0], u * s * a[1] + v * b[1])
        total += det(image, d) == 0
    return total


def census(spec):
    # Counterexamples and degeneracies are checked BEFORE the confirmation census.
    real = [[1, 0, 0, 0, 1], [1, 0, -6, 0, 1]]
    boundary = dict(
        real_invariants=[inv(q) for q in real], real_root_counts=[sturm(q) for q in real]
    )
    assert boundary["real_root_counts"] == [0, 4]
    repeated = [[1, 0, 0, 0, 0], [0, 1, 0, 0, 0]]
    parts = []
    for coeff in repeated:
        p = trim(list(map(Q, reversed(coeff))))
        zero = next(i for i, x in enumerate(p) if x)
        parts.append(sorted([x for x in [zero, 5 - len(p)] if x], reverse=True))
    boundary.update(
        repeated_invariants=[inv(q) for q in repeated],
        multiplicities=parts,
        i_zero=inv([1, 0, 0, 1, 0]),
    )
    assert parts == [[4], [3, 1]]
    grid = []
    for s in spec["interpolation_grid"]:
        for t in spec["interpolation_grid"]:
            si, sj, _ = map(Q, inv([0, 1, -s - 1, s, 0]))
            ti, tj, _ = map(Q, inv([0, 1, -t - 1, t, 0]))
            value = sj * sj * ti**3 - tj * tj * si**3
            product = (
                -27
                * (s - t)
                * (s + t - 1)
                * (t * s - 1)
                * ((1 - t) * s - 1)
                * ((t - 1) * s - t)
                * (t * s - t + 1)
            )
            assert value == product
            grid.append([s, t, str(value)])
    values = sorted(
        {Q(p, q) for p in spec["numerators"] for q in spec["denominators"]} - {Q(0), Q(1)}
    )
    rows = []
    for s in values:
        for t in values:
            count = maps(s, t)
            si, sj, _ = map(Q, inv([0, 1, -s - 1, s, 0]))
            ti, tj, _ = map(Q, inv([0, 1, -t - 1, t, 0]))
            equal = sj * sj * ti**3 == tj * tj * si**3
            assert bool(count) == equal
            rows.append([str(s), str(t), count])
    return dict(
        boundary=boundary,
        identity_grid=grid,
        rows=rows,
        parameter_count=len(values),
        pair_count=len(rows),
        equivalent_pairs=sum(r[2] > 0 for r in rows),
        projective_maps=sum(r[2] for r in rows),
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("--certificate")
    args = parser.parse_args()
    expected = census(json.loads(Path(args.input).read_text()))
    result = expected
    if args.certificate:
        # Certificate read happens only after fresh counterexample search and reconstruction.
        certificate = json.loads(Path(args.certificate).read_text())
        assert certificate == expected
        paths = [
            ("boundary", "real_invariants", 0, 0),
            ("boundary", "real_root_counts", 0),
            ("boundary", "multiplicities", 0, 0),
            ("identity_grid", 0, 2),
            ("rows", 0, 2),
            ("boundary", "i_zero", 1),
            ("pair_count",),
        ]
        rejected = []
        for path in paths:
            bad = copy.deepcopy(certificate)
            obj = bad
            for key in path[:-1]:
                obj = obj[key]
            old = obj[path[-1]]
            obj[path[-1]] = str(Q(old) + 1) if isinstance(old, str) else old + 1
            assert bad != expected
            rejected.append(list(path))
        result = dict(
            reconstructed=expected,
            certificate_equal=True,
            rejected_mutations=rejected,
            method=(
                "Sturm Euclidean remainders; 24 ordered target triples per pair; "
                "degree-bounded 7x7 identity evaluation"
            ),
        )
    Path(args.output).write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(
        json.dumps(
            {
                k: expected[k]
                for k in ["parameter_count", "pair_count", "equivalent_pairs", "projective_maps"]
            }
        )
    )


if __name__ == "__main__":
    main()
