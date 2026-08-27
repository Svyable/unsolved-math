"""Separate exact cell-partition checker; no theory imports or floating point."""

import copy
import json
import sys
from fractions import Fraction as F
from itertools import pairwise
from pathlib import Path


def inside(x, q, delta):
    if q == 0 or delta < 0:
        raise ValueError("nonzero denominator and nonnegative radius required")
    value = q * x
    residue = value - (value.numerator // value.denominator)
    return min(residue, 1 - residue) < delta


def cuts(q, delta):
    q = abs(q)
    if q == 0 or delta < 0:
        raise ValueError("invalid input")
    return {F(0), F(1)} | {
        v for j in range(-2, q + 3) for v in [(j - delta) / q, (j + delta) / q] if 0 < v < 1
    }


def measure(events, intersection=False):
    points = sorted(set().union({F(0), F(1)}, *(cuts(q, d) for q, d in events)))
    total = F(0)
    for a, b in pairwise(points):
        membership = [inside((a + b) / 2, q, d) for q, d in events]
        if all(membership) if intersection else any(membership):
            total += b - a
    return total


def main():
    spec = json.loads(Path("input.json").read_text())
    # Counterexample and boundary search precedes any acceptance calculation.
    e2, e3 = (2, F(1, 4)), (3, F(1, 9))
    joint = measure([e2, e3], intersection=True)
    product = measure([e2]) * measure([e3])
    assert joint != product
    boundaries = {
        "zero_radius_empty": measure([(2, F(0))]) == 0,
        "half_radius_full_measure": measure([(2, F(1, 2))]) == 1,
        "large_radius_saturates": measure([(3, F(3, 4))]) == 1,
        "strict_endpoint_excluded": not inside(F(1, 8), 2, F(1, 4)),
        "integer_center_included": inside(F(1, 2), 2, F(1, 4)),
        "nonprimitive_q_allowed": measure([(6, F(1, 16))]) == F(1, 8),
        "negative_q_same_event": measure([(-3, F(1, 9))]) == measure([e3]),
        "powered_norm_essential": F(1, 8) ** 2 < F(1, 16) < F(1, 8),
        "epsilon_zero_integral_diverges": sum(F(1, j) for j in range(8, 16)) >= F(1, 2),
    }
    try:
        inside(F(0), 0, F(1, 2))
    except ValueError:
        boundaries["zero_q_rejected"] = True
    assert len(boundaries) == 10 and all(boundaries.values())
    events = []
    for q in range(1, spec["event_q_max"] + 1):
        for radius in spec["radii"]:
            d = F(radius)
            result = measure([(q, d)])
            assert result == min(F(1), 2 * d)
            events.append([q, radius, str(result)])
    rows = []
    for r, k in spec["cases"]:
        union = measure([(q, F(1, q * q)) for q in range(r, k + 1)])
        moment = sum(measure([(q, F(1, q * q))]) for q in range(r, k + 1))
        remainder = F(2, k)
        assert union <= moment
        rows.append(
            {
                "R": r,
                "K": k,
                "finite_union": str(union),
                "first_moment_prefix": str(moment),
                "remainder_bound": str(remainder),
                "tail_bound": str(min(F(1), union + remainder)),
                "first_moment_tail": str(min(F(1), moment + remainder)),
                "integral_only_bound": str(min(F(1), F(2, r - 1))),
            }
        )
    counterexample = {"q": [2, 3], "joint": str(joint), "product": str(product)}
    result = {
        "method": "exact rational cell partition and direct modular inequalities",
        "boundary_checks": boundaries,
        "events": events,
        "rows": rows,
        "independence_counterexample": counterexample,
    }
    if len(sys.argv) > 1:
        certificate = json.loads(Path(sys.argv[1]).read_text())

        def accepts(cert):
            if cert["rows"] != rows or cert["events"] != events:
                return False
            if cert["independence_counterexample"] != counterexample:
                return False
            intervals = [(F(a), F(b)) for a, b in cert["featured_intervals"]]
            if any(not 0 <= a < b <= 1 for a, b in intervals):
                return False
            r, k = spec["featured_case"]
            points = sorted(
                set().union(
                    {v for ab in intervals for v in ab},
                    *(cuts(q, F(1, q * q)) for q in range(r, k + 1)),
                )
            )
            for a, b in pairwise(points):
                x = (a + b) / 2
                if any(lo < x < hi for lo, hi in intervals) != any(
                    inside(x, q, F(1, q * q)) for q in range(r, k + 1)
                ):
                    return False
            feature = next(row for row in rows if [row["R"], row["K"]] == [r, k])
            return sum(b - a for a, b in intervals) == F(feature["finite_union"])

        assert accepts(certificate)
        mutations = []
        for key, value in [
            ("finite_union", "0"),
            ("remainder_bound", "0"),
            ("tail_bound", "0"),
            ("first_moment_prefix", "0"),
        ]:
            bad = copy.deepcopy(certificate)
            bad["rows"][0][key] = value
            mutations.append((key, bad))
        bad = copy.deepcopy(certificate)
        bad["featured_intervals"].pop()
        mutations.append(("deleted_interval", bad))
        bad = copy.deepcopy(certificate)
        bad["featured_intervals"][0][1] = str(F(bad["featured_intervals"][0][1]) / 2)
        mutations.append(("shortened_interval", bad))
        bad = copy.deepcopy(certificate)
        bad["independence_counterexample"]["joint"] = str(product)
        mutations.append(("independence_shortcut", bad))
        rejected = [name for name, bad in mutations if not accepts(bad)]
        assert len(rejected) == 7
        feature = next(row for row in rows if [row["R"], row["K"]] == spec["featured_case"])
        assert F(feature["tail_bound"]) < F(9, 20) < F(feature["first_moment_tail"])
        improvements = sum(F(row["tail_bound"]) < F(row["first_moment_tail"]) for row in rows)
        assert improvements == 34
        result["certificate_accepted"] = True
        result["mutations_rejected"] = rejected
        result["featured_threshold"] = "tail_bound < 9/20 < first_moment_tail"
        result["strictly_improved_cases"] = improvements
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
