"""Exact nonnegative-linear-combination checker; derives rows from frozen rays."""

import argparse
import copy
import json
from fractions import Fraction as F
from pathlib import Path

ZERO = (F(0), F(0))
ONE = (F(1), F(0))
MINUS = (-F(1), F(0))


def read(x):
    return tuple(map(F, x))


def add(x, y):
    return x[0] + y[0], x[1] + y[1]


def neg(x):
    return -x[0], -x[1]


def multiply(x, y):
    # Multiply coefficient polynomials and reduce t^2 to t+1.
    coeff = [F(0)] * 3
    for i in range(2):
        for j in range(2):
            coeff[i + j] += x[i] * y[j]
    return coeff[0] + coeff[2], coeff[1] + coeff[2]


def check(spec, data):
    assert data["variables"] == ["a", "b", "c", "D", "constant"]
    assert [(c["bottom"], c["top"]) for c in data["certificates"]] == [(2, 3), (3, 2)]
    results = []
    for cert in data["certificates"]:
        bottom, top = cert["bottom"], cert["top"]
        roots = [[read(x) for x in r] for r in spec["roots"]]
        small = next(i for i, x in enumerate(roots[bottom]) if x == ONE)
        large = 1 - small
        simple = [ZERO] * 5
        simple[bottom - 2] = roots[bottom][small]
        simple[4] = MINUS
        middle = [ZERO] * 5
        middle[bottom - 2] = neg(roots[bottom][large])
        middle[top - 2] = roots[top][large]
        budget = [ZERO] * 5
        budget[3] = ONE
        budget[top - 2] = MINUS
        rows = [[read(v) for v in row] for row in cert["constraints"]]
        assert rows == [simple, middle, budget]
        weights = list(map(read, cert["multipliers"]))
        # Sufficient exact positivity test for the submitted 1,phi weights.
        assert len(weights) == 3 and all(a >= 0 and b >= 0 for a, b in weights)
        combination = [ZERO] * 5
        for weight, row in zip(weights, rows, strict=True):
            combination = [
                add(x, multiply(weight, y)) for x, y in zip(combination, row, strict=True)
            ]
        expected = [ZERO, ZERO, ZERO, ONE, (F(0), F(-1))]
        assert combination == expected == list(map(read, cert["combination"]))
        results.append(
            dict(
                bottom=bottom,
                top=top,
                identity="D-phi",
                nonnegative_weights=True,
                coordinate_rows_verified=True,
            )
        )
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path)
    ap.add_argument("output", type=Path)
    ap.add_argument("--certificate", required=True, type=Path)
    args = ap.parse_args()
    spec = json.loads(args.input.read_text())
    data = json.loads(args.certificate.read_text())
    checked = check(spec, data)
    rejected = []
    for i in range(4):
        bad = copy.deepcopy(data)
        if i == 0:
            bad["certificates"][0]["multipliers"][0] = ["1", "0"]
        if i == 1:
            bad["certificates"][0]["multipliers"][1] = ["-1", "0"]
        if i == 2:
            bad["certificates"][0]["constraints"][1][0] = ["0", "1"]
        if i == 3:
            bad["certificates"].pop()
        try:
            check(spec, bad)
        except AssertionError:
            rejected.append(i)
        else:
            raise AssertionError("false dual certificate accepted")
    result = dict(
        certificates_checked=checked,
        corruptions_rejected=rejected,
        scope=(
            "Exact algebraic identities and nonnegative weights; the target-to-two-orientations "
            "reduction and original metric assumptions require the stated ordinary proof audit."
        ),
    )
    args.output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
