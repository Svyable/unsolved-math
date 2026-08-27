"""Independent exact half-plane checker. No theory imports or formula reuse.

Starts with counterexample/edge controls, then reads the proposed certificates.
Closed-union coverage is certified by zero-area complement polygons, not samples.
"""

import hashlib
import json
from fractions import Fraction as F
from itertools import product
from pathlib import Path


def clip(poly, nx, ny, bound):
    """Sutherland-Hodgman clipping against nx*x+ny*y <= bound."""
    result = []
    for p, q in zip(poly, poly[1:] + poly[:1], strict=True):
        vp, vq = nx * p[0] + ny * p[1] - bound, nx * q[0] + ny * q[1] - bound
        if vp <= 0:
            result.append(p)
        if (vp < 0 < vq) or (vq < 0 < vp):
            t = vp / (vp - vq)
            result.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    return result


def area(poly):
    return (
        abs(
            sum(
                (p[0] * q[1] - q[0] * p[1] for p, q in zip(poly, poly[1:] + poly[:1], strict=True)),
                F(0),
            )
        )
        / 2
    )


def rotate_rectangle(length, height, t):
    co, si = (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)
    return [
        (co * x - si * y, si * x + co * y)
        for x, y in [
            (-length / 2, -height / 2),
            (length / 2, -height / 2),
            (length / 2, height / 2),
            (-length / 2, height / 2),
        ]
    ]


def outside_union(poly, c, s, delta):
    # Outside both absolute-value bands is a union of four convex regions.
    return [
        area(
            clip(clip(poly, -sign1 * s, -sign1 * c, -delta / 2), sign2 * s, -sign2 * c, -delta / 2)
        )
        for sign1, sign2 in product([-1, 1], repeat=2)
    ]


def check(row):
    r = {k: F(v) for k, v in row.items()}
    u, d, e, c, s = (r[k] for k in ["u", "delta", "epsilon", "c", "s"])
    if not (0 < u < 1 and d > 0 and 0 < e < 1 and c > 0 and s > 0):
        return False
    if c * c + s * s != 1 or s != u * (1 + c):
        return False
    a, b, h = (r[k] for k in ["a", "b", "h"])
    if not (0 <= a < b and h > 0):
        return False
    poly = [(a, -h), (b, -h), (b, h), (a, h)]
    if any(outside_union(poly, c, s, d)):
        return False
    if r["length"] != b - a or r["height"] != 2 * h or r["area"] != area(poly):
        return False
    if r["shorter_side"] != min(b - a, 2 * h):
        return False
    margin = s * a + c * h - d / 2
    if margin <= 0 or r["outside_intersection_margin"] != margin:
        return False
    # This named witness must lie in the other strip, but outside S+.
    return abs(-s * a + c * h) <= d / 2


def main():
    root = Path(__file__).parent
    raw = json.loads((root / "input.json").read_text())
    # Counterexample-first: validate polygon kernel on boundary and exterior cases.
    square = [(F(0), F(0)), (F(1), F(0)), (F(1), F(1)), (F(0), F(1))]
    kernel_controls = [
        area(clip(square, 1, 0, F(1, 2))) == F(1, 2),
        area(clip(square, 1, 0, F(-1))) == 0,
        area(clip(square, 1, 0, F(0))) == 0,
        area(clip(square, 1, 1, F(1))) == F(1, 2),
        area(square[::-1]) == 1,
    ]
    assert all(kernel_controls)
    rejected = 0
    digest = hashlib.sha256()
    for d, excess, aspect, t in product(
        raw["widths"], raw["excess_widths"], raw["aspect_ratios"], raw["orientation_parameters"]
    ):
        d, excess, aspect, t = map(F, (d, excess, aspect, t))
        poly = rotate_rectangle(d * excess * aspect, d * excess, t)
        vertical_span = max(y for _, y in poly) - min(y for _, y in poly)
        assert vertical_span > d
        rejected += 1
        digest.update((str(vertical_span) + "\n").encode())
    # At width exactly delta, a horizontal rectangle does fit a horizontal band.
    boundary = rotate_rectangle(F(10), F(1), F(0))
    assert area(clip(clip(boundary, 0, 1, F(1, 2)), 0, -1, F(1, 2))) == 10
    # Only after the adversarial search, read proposed certificates as untrusted data.
    proposed = json.loads((root / "theory-output.json").read_text())
    rows = proposed["rows"]
    expected_keys = {
        (F(u), F(d), F(e))
        for u, d, e in product(raw["half_angle_parameters"], raw["widths"], raw["epsilons"])
    }
    assert len(rows) == len(expected_keys)
    assert {(F(r["u"]), F(r["delta"]), F(r["epsilon"])) for r in rows} == expected_keys
    assert all(check(r) for r in rows)
    ex = proposed["example"]
    assert all(F(ex[k]) == F(raw["example"][k]) for k in ["u", "delta", "epsilon"])
    assert check(ex)
    # Deliberate corruptions; changes are local and never alter input artifacts.
    edits = [
        ("width_normalization", "c", F(ex["c"]) / 2),
        ("right_endpoint_gap", "b", 2 * F(ex["b"])),
        ("widened_rectangle", "h", F(ex["h"]) + F(1, 10)),
        ("false_area", "area", F(ex["area"]) + 1),
        ("reversed_interval", "a", F(ex["b"]) + 1),
        ("zero_width", "delta", F(0)),
        ("false_witness_margin", "outside_intersection_margin", F(0)),
    ]
    controls = []
    for label, key, value in edits:
        bad = dict(ex)
        bad[key] = str(value)
        assert not check(bad)
        controls.append(label)
    # Extend x beyond b: y=0 is outside BOTH bands, the exact union gap.
    gap_x = F(ex["b"]) + 1
    gap_margin = F(ex["s"]) * gap_x - F(ex["delta"]) / 2
    assert gap_margin > 0
    print(
        json.dumps(
            {
                "method": (
                    "Exact generic polygon clipping and shoelace area; "
                    "certificate-input only, no theory import"
                ),
                "polygon_controls_passed": len(kernel_controls),
                "oversized_rectangles_rejected": rejected,
                "projection_test_sha256": digest.hexdigest(),
                "boundary_equal_width_passed": True,
                "certificates_accepted": len(rows),
                "complement_regions_checked": 4 * len(rows),
                "long_wide_certificates": sum(F(r["shorter_side"]) > F(r["delta"]) for r in rows),
                "mutations_rejected": controls,
                "example": ex,
                "right_extension_gap_margin": str(gap_margin),
                "independence": (
                    "Fresh isolated process; counterexamples first, "
                    "then untrusted certificate coordinates. "
                    "Generic clipping instead of vertical-section identities. "
                    "Same-assistant authorship; "
                    "no independent model/human referee or kernel."
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
