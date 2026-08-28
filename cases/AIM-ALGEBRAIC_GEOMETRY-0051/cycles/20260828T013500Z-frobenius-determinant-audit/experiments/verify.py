"""Counterexample-first verifier: point enumeration and fraction-free matrices."""

import argparse
import copy
import itertools
import json
from pathlib import Path


def det(a):
    a = [row[:] for row in a]
    n, prev, sign = len(a), 1, 1
    for k in range(n - 1):
        if a[k][k] == 0:
            pivot = next((i for i in range(k + 1, n) if a[i][k]), None)
            if pivot is None:
                return 0
            a[k], a[pivot] = a[pivot], a[k]
            sign = -sign
        pivot = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                num = a[i][j] * pivot - a[i][k] * a[k][j]
                assert num % prev == 0
                a[i][j] = num // prev
        for i in range(k + 1, n):
            a[i][k] = 0
        prev = pivot
    return sign * a[-1][-1]


def tensor(a, b):
    return [[x * y for x in ar for y in br] for ar in a for br in b]


def matrix(q, ts, full=False):
    ms = [[[0, -q], [1, t]] for t in ts]
    a = tensor(tensor(ms[0], ms[1]), ms[2])
    if full:
        blocks = [a] + [[[q * x for x in row] for row in m] for m in ms for _ in range(2)]
        a = [[0] * 20 for _ in range(20)]
        pos = 0
        for block in blocks:
            for i, row in enumerate(block):
                for j, x in enumerate(row):
                    a[pos + i][pos + j] = x
            pos += len(block)
        assert pos == 20
    return a


def shifted_det(a, x):
    return det([[x * (i == j) - v for j, v in enumerate(row)] for i, row in enumerate(a)])


def valuation(n, ell):
    assert n != 0
    v = 0
    while n % ell == 0:
        n //= ell
        v += 1
    return v


def boundary():
    # Runs before point enumeration, reconstruction, or reading theory evidence.
    a = matrix(5, [0, 0, 0])
    r = shifted_det(a, 25)
    d = shifted_det(matrix(5, [0, 0, 0], True), 25)
    assert valuation(r, 2) == 4 and valuation(d, 2) == 10
    assert d % (5**18) == 0
    # Rank/rational surjectivity alone does not ensure an integral saturated image.
    unit_image = sorted({x % 49 for x in range(49)})
    seven_image = sorted({7 * x % 49 for x in range(49)})
    assert len(unit_image) == 49 and len(seven_image) == 7
    assert d % 7 != 0
    # Zero trace, repeated roots, and a pivot swap exercise determinant boundaries.
    assert det([[0, 1], [1, 0]]) == -1
    assert det([[1, 1], [1, 1]]) == 0
    repeated = shifted_det(matrix(4, [4, 4, 4]), 16)
    assert repeated == 8**8
    return dict(q=5, traces=[0, 0, 0], R=r, D20=d,
                omitted_summands_v2=4, full_v2=10,
                lattice_control=dict(modulus=49, unit_image_size=49,
                                     seven_image_size=7, cokernel_order=7),
                repeated_root_R=repeated)


def reconstruct(spec):
    curves, rows, full_checks = [], [], 0
    for q in spec["primes"]:
        models = []
        for a in range(q):
            for b in range(q):
                if (4 * a**3 + 27 * b**2) % q == 0:
                    continue
                count = 1 + sum((y*y - x*x*x - a*x - b) % q == 0
                                for x in range(q) for y in range(q))
                models.append([a, b, count, q + 1 - count])
        traces = sorted({m[3] for m in models})
        curves.append(dict(q=q, models=models, traces=traces))
        for ts in itertools.combinations_with_replacement(traces, 3):
            r = shifted_det(matrix(q, ts), q*q)
            d = r
            for t in ts:
                block = [[q*q, q*q], [-q, q*q-q*t]]
                d *= det(block) ** 2
            assert d % q**18 == 0
            b = d // q**18
            rows.append(dict(q=q, traces=list(ts), R=r, B=b, D20=d))
            if ts[0] == ts[1] == ts[2]:
                assert shifted_det(matrix(q, ts, True), q*q) == d
                full_checks += 1
    zero = []
    for q in spec["trace_zero_q"]:
        r = shifted_det(matrix(q, [0, 0, 0]), q*q)
        b = shifted_det(matrix(q, [0, 0, 0], True), q*q) // q**18
        assert r == q**12 * (q+1)**4 and b == q**12 * (q+1)**10
        zero.append(dict(q=q, R=r, B=b))
    return dict(curves=curves, rows=rows, trace_zero=zero), full_checks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("--certificate")
    args = parser.parse_args()
    spec = json.loads(Path(args.input).read_text())
    controls = boundary()
    expected, full_checks = reconstruct(spec)
    result = dict(boundary=controls, expected=expected,
                  models=sum(len(c["models"]) for c in expected["curves"]),
                  triples=len(expected["rows"]), full_matrix_checks=full_checks)
    if args.certificate:
        supplied = json.loads(Path(args.certificate).read_text())
        assert supplied == expected
        bad = []
        for field in ("R", "B", "D20"):
            altered = copy.deepcopy(supplied)
            altered["rows"][0][field] += 1
            bad.append(altered)
        altered = copy.deepcopy(supplied)
        altered["curves"][0]["models"][0][2] += 1
        bad.append(altered)
        altered = copy.deepcopy(supplied)
        altered["trace_zero"][0]["B"] += 1
        bad.append(altered)
        altered = copy.deepcopy(supplied)
        altered["rows"].pop()
        bad.append(altered)
        altered = copy.deepcopy(supplied)
        altered["rows"][0]["traces"][0] += 1
        bad.append(altered)
        assert all(x != expected for x in bad)
        result["mutations_rejected"] = len(bad)
        result["certificate_matches"] = True
    Path(args.output).write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k not in ("expected", "boundary")}))


if __name__ == "__main__":
    main()
