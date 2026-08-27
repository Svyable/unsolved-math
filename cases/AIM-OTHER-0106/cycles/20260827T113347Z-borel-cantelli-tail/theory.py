"""Construct rational interval-union certificates by sorted interval merging."""

import json
from fractions import Fraction as F
from pathlib import Path


def merge(intervals):
    result = []
    for a, b in sorted(intervals):
        if a >= b:
            continue
        if result and a <= result[-1][1]:
            result[-1][1] = max(result[-1][1], b)
        else:
            result.append([a, b])
    return result


def intervals(q, delta):
    if q <= 0 or delta < 0:
        raise ValueError("positive denominator and nonnegative radius required")
    return merge(
        [[max(F(0), (F(p) - delta) / q), min(F(1), (F(p) + delta) / q)] for p in range(-1, q + 2)]
    )


def length(parts):
    return sum((b - a for a, b in parts), F(0))


def main():
    spec = json.loads(Path("input.json").read_text())
    events = []
    for q in range(1, spec["event_q_max"] + 1):
        for radius in spec["radii"]:
            area = length(intervals(q, F(radius)))
            assert area == min(F(1), 2 * F(radius))
            events.append([q, radius, str(area)])
    rows = []
    featured = None
    for r, k in spec["cases"]:
        parts = merge([ab for q in range(r, k + 1) for ab in intervals(q, F(1, q * q))])
        area = length(parts)
        moment = sum((F(2, q * q) for q in range(r, k + 1)), F(0))
        rest = F(2, k)
        rows.append(
            {
                "R": r,
                "K": k,
                "finite_union": str(area),
                "first_moment_prefix": str(moment),
                "remainder_bound": str(rest),
                "tail_bound": str(min(F(1), area + rest)),
                "first_moment_tail": str(min(F(1), moment + rest)),
                "integral_only_bound": str(min(F(1), F(2, r - 1))),
            }
        )
        if [r, k] == spec["featured_case"]:
            featured = [[str(a), str(b)] for a, b in parts]
    assert featured is not None
    i2, i3 = intervals(2, F(1, 4)), intervals(3, F(1, 9))
    intersection = merge([[max(a, c), min(b, d)] for a, b in i2 for c, d in i3])
    joint, product = length(intersection), length(i2) * length(i3)
    assert joint != product
    print(
        json.dumps(
            {
                "method": "sorted interval merging",
                "events": events,
                "rows": rows,
                "featured_intervals": featured,
                "independence_counterexample": {
                    "q": [2, 3],
                    "joint": str(joint),
                    "product": str(product),
                },
            },
            sort_keys=True,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
