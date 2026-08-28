"""Exact Frobenius power sums and Newton identities; no matrix arithmetic."""

import argparse
import itertools
import json
from math import prod
from pathlib import Path


def sums(q, t, n):
    s = [2, t]
    for _ in range(2, n + 1):
        s.append(t * s[-1] - q * s[-2])
    return s


def evaluate_characteristic(power_sums, x):
    coeffs = [1]
    for k in range(1, len(power_sums)):
        num = -sum(coeffs[k-i] * power_sums[i] for i in range(1, k+1))
        assert num % k == 0
        coeffs.append(num // k)
    value = 0
    for c in coeffs:
        value = value * x + c
    return value


def determinants(q, ts):
    ss = [sums(q, t, 20) for t in ts]
    triple = [prod(s[k] for s in ss) for k in range(21)]
    total = [triple[k] + 2 * q**k * sum(s[k] for s in ss) for k in range(21)]
    assert triple[0] == 8 and total[0] == 20
    r = evaluate_characteristic(triple[:9], q*q)
    d = evaluate_characteristic(total, q*q)
    b = r * prod((q+1-t)**2 for t in ts)
    assert d == q**18 * b
    return r, b, d


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    args = parser.parse_args()
    spec = json.loads(Path(args.input).read_text())
    curves, rows = [], []
    for q in spec["primes"]:
        models = []
        for a in range(q):
            for b in range(q):
                if (4*a**3 + 27*b**2) % q == 0:
                    continue
                points = q + 1
                for x in range(q):
                    value = pow((x**3+a*x+b) % q, (q-1)//2, q)
                    points += -1 if value == q-1 else value
                models.append([a, b, points, q+1-points])
        traces = sorted({m[3] for m in models})
        curves.append(dict(q=q, models=models, traces=traces))
        for ts in itertools.combinations_with_replacement(traces, 3):
            r, b, d = determinants(q, ts)
            rows.append(dict(q=q, traces=list(ts), R=r, B=b, D20=d))
    zero = []
    for q in spec["trace_zero_q"]:
        r, b, _ = determinants(q, [0, 0, 0])
        assert r == q**12 * (q+1)**4
        assert b == q**12 * (q+1)**10
        zero.append(dict(q=q, R=r, B=b))
    result = dict(curves=curves, rows=rows, trace_zero=zero)
    Path(args.output).write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps(dict(models=sum(len(c["models"]) for c in curves), triples=len(rows))))


if __name__ == "__main__":
    main()
