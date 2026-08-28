"""Independent corner/segment integration; no theory import or envelope formula."""

import argparse
import copy
import hashlib
import itertools
import json
from fractions import Fraction as F
from pathlib import Path


def packed(obj):
    return (json.dumps(obj, sort_keys=True, separators=(",", ":")) + "\n").encode()


def advance(x, v, acc, dt):
    return x + v * dt + acc * dt * dt / 2, v + acc * dt


def segment(x, v, acc, dt):
    times = [F(0), dt]
    if acc < 0 and 0 <= -v / acc <= dt:
        times.append(-v / acc)
    return max((advance(x, v, acc, t)[0], -t) for t in times)


def trajectory(par, z, signs):
    d, e, vbar, a, eps, total = par
    x, v = d * sum(z), vbar + e * (z[0] - z[1])
    best = (x, F(0))
    elapsed = F(0)
    dt = total / len(signs)
    for sign in signs:
        acc = -a + sign * eps
        value, negtime = segment(x, v, acc, dt)
        best = max(best, (value, negtime - elapsed))
        x, v = advance(x, v, acc, dt)
        elapsed += dt
    return best[0], -best[1]


CORNERS = list(itertools.product([-1, 1], repeat=2))


def row(par):
    d, e, vbar, a, eps, total = par
    best = max((value, -time) for value, time in (trajectory(par, z, [1]) for z in CORNERS))
    grid = max(
        advance(d * sum(z), vbar + e * (z[0] - z[1]), -a + eps, t)[0]
        for z in CORNERS
        for t in [F(0), total / 2, total]
    )
    box = max(segment(2 * d * z[0], vbar + 2 * e * z[1], -a + eps, total)[0] for z in CORNERS)
    return [*[str(v) for v in par], str(best[0]), str(-best[1]), str(grid), str(box)]


def certificate_ok(cert, spec):
    """Recompute the finite witness and its admissibility, not JSON checksum matching."""
    try:
        par = list(map(F, spec["base"]))
        d, e, vbar, a, eps, total = par
        z = list(map(F, cert["z"]))
        w, t = F(cert["w"]), F(cert["time"])
        if len(z) != 2 or any(abs(v) > 1 for v in z) or abs(w) > eps or not 0 <= t <= total:
            return False
        x0, v0 = d * sum(z), vbar + e * (z[0] - z[1])
        value = advance(x0, v0, -a + w, t)[0]
        expected = row(par)
        return (
            F(cert["initial_x"]) == x0
            and F(cert["initial_v"]) == v0
            and F(cert["value"]) == value == F(expected[6])
            and t == F(expected[7])
            and F(cert["grid_max"]) == F(expected[8])
            and F(cert["box_max"]) == F(expected[9])
            and F(cert["sample_threshold"]) == F(spec["sample_threshold"])
            and F(cert["safe_threshold"]) == F(spec["safe_threshold"])
            and F(expected[8]) <= F(spec["sample_threshold"]) < value
            and value <= F(spec["safe_threshold"]) < F(expected[9])
        )
    except (KeyError, ValueError, TypeError, ZeroDivisionError):
        return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--certificate", type=Path)
    args = parser.parse_args()
    spec = json.loads(args.input.read_text())
    # Counterexample and degenerate boundaries BEFORE census and certificate read.
    base = row(list(map(F, spec["base"])))
    assert base[6:] == ["2/5", "2/3", "3/8", "1/2"]
    assert trajectory(list(map(F, spec["base"])), [1, -1], [1]) == (F(2, 5), F(2, 3))
    assert row([F(0)] * 6)[6:] == ["0", "0", "0", "0"]
    assert row(list(map(F, ["1/20", "1/10", "-1", "2", "1/5", "0"])))[6:] == [
        "1/10",
        "0",
        "1/10",
        "1/10",
    ]
    rows, paths, misses, gaps = [], 0, 0, 0
    curvature_counts = {"concave": 0, "linear": 0, "convex": 0}
    for par in itertools.product(*[list(map(F, axis)) for axis in spec["parameters"]]):
        r = row(par)
        worst = F(r[6])
        attained = False
        for z in CORNERS:
            for signs in itertools.product([-1, 1], repeat=3):
                value, _ = trajectory(par, z, signs)
                assert value <= worst
                attained |= value == worst
                paths += 1
        assert attained
        misses += F(r[8]) < worst
        gaps += worst < F(r[9])
        c = par[3] - par[4]
        curvature_counts["concave" if c > 0 else "linear" if c == 0 else "convex"] += 1
        rows.append(r)
    table = packed(rows)
    summary = dict(
        cases=len(rows),
        table_sha256=hashlib.sha256(table).hexdigest(),
        sample_misses=misses,
        strict_box_gaps=gaps,
        base=base,
        curvature_counts=curvature_counts,
    )
    if args.certificate:
        cert = json.loads(args.certificate.read_text())
        assert cert["summary"] == summary
        assert certificate_ok(cert["witness"], spec)
        mutations = [
            ("z", ["2", "-1"]),
            ("w", "1"),
            ("time", "2"),
            ("initial_x", "1/10"),
            ("value", "3/8"),
            ("grid_max", "2/5"),
            ("box_max", "2/5"),
        ]
        rejected = []
        for field, value in mutations:
            bad = copy.deepcopy(cert["witness"])
            bad[field] = value
            assert not certificate_ok(bad, spec), field
            rejected.append(field)
        out = dict(
            summary=summary,
            exact_piecewise_trajectories=paths,
            corrupted_certificates_rejected=rejected,
            certificate_accepted=True,
            order="counterexample, boundaries, census, certificate and mutations",
            independence=(
                "Fresh process; direct integration of all initial corners and control segments; "
                "no support-envelope or theory code import. Same assistant/shared input; "
                "not independent human/model/kernel review."
            ),
        )
        args.output.with_name("verification-table.json").write_bytes(table)
    else:
        out = summary
    args.output.write_bytes(packed(out))
    print(
        json.dumps(
            dict(cases=len(rows), trajectories=paths, sample_misses=misses, strict_box_gaps=gaps)
        )
    )


if __name__ == "__main__":
    main()
