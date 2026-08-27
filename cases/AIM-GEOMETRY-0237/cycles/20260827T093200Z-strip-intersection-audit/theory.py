"""Exact constructive union certificates; never use finite tests as proof."""

import json
from fractions import Fraction as F
from itertools import product
from pathlib import Path


def certificate(u, delta, epsilon):
    assert 0 < u < 1 and delta > 0 and 0 < epsilon < 1
    c, s = (1 - u * u) / (1 + u * u), 2 * u / (1 + u * u)
    assert c * c + s * s == 1
    b = delta / (2 * s)
    a = (1 - epsilon) * b
    h = delta * (2 - epsilon) / (2 * c)
    # For a <= x <= b, vertical strip sections overlap and their union
    # reaches at least +/-h. These exact inequalities cover all x, not samples.
    assert s * b == delta / 2
    assert c * h - s * a == delta / 2
    assert c * h + s * a > delta / 2
    length, height = b - a, 2 * h
    return {
        k: str(v)
        for k, v in {
            "u": u,
            "delta": delta,
            "epsilon": epsilon,
            "c": c,
            "s": s,
            "a": a,
            "b": b,
            "h": h,
            "length": length,
            "height": height,
            "area": length * height,
            "shorter_side": min(length, height),
            "outside_intersection_margin": c * h + s * a - delta / 2,
        }.items()
    }


def main():
    raw = json.loads(Path(__file__).with_name("input.json").read_text())
    rows = [
        certificate(F(u), F(d), F(e))
        for u, d, e in product(raw["half_angle_parameters"], raw["widths"], raw["epsilons"])
    ]
    example = certificate(*(F(raw["example"][k]) for k in ["u", "delta", "epsilon"]))
    print(
        json.dumps(
            {
                "method": (
                    "Exact vertical-section union construction "
                    "and normal-projection obstruction"
                ),
                "rows": rows,
                "example": example,
                "long_wide_certificates": sum(F(r["shorter_side"]) > F(r["delta"]) for r in rows),
                "claim_boundary": (
                    "The intersection cannot contain any rectangle with shorter side > delta. "
                    "The separately certified union rectangles do not "
                    "establish a surface flat-strip theorem."
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
