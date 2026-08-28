"""Exact three-variable LP verifier; no theory imports or interval formula."""

import argparse
import copy
import hashlib
import itertools
import json
from fractions import Fraction as F
from functools import cache
from pathlib import Path


def encode(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def det(a):
    return (a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
            - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
            + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]))


@cache
def bases(normals):
    result = []
    for ids in itertools.combinations(range(len(normals)), 3):
        a = [normals[i] for i in ids]
        denominator = det(a)
        if not denominator:
            continue
        inverse = []
        for col in range(3):
            row = []
            for rhs in range(3):
                replaced = [list(r) for r in a]
                for j in range(3):
                    replaced[j][col] = int(j == rhs)
                row.append(F(det(replaced), denominator))
            inverse.append(row)
        result.append((ids, inverse))
    return result


def optimize(inequalities, objective):
    normals = tuple(tuple(row[:3]) for row in inequalities)
    bounds = [F(row[3]) for row in inequalities]
    best = None
    witness = None
    for ids, inverse in bases(normals):
        v = tuple(sum((inverse[i][j] * bounds[ids[j]] for j in range(3)), F(0))
                  for i in range(3))
        if any(sum((row[j] * v[j] for j in range(3)), F(0)) > bound
               for row, bound in zip(normals, bounds, strict=True)):
            continue
        value = sum((objective[j] * v[j] for j in range(3)), F(0))
        if best is None or value > best:
            best, witness = value, v
    return best, witness


def slack(rect):
    a, b, c, d = map(F, rect)
    assert a < b and c < d
    box = [(-1, 0, 0, -a), (1, 0, 0, b), (0, -1, 0, -c), (0, 1, 0, d)]
    scores = []
    for e, f in itertools.product((-1, 1), repeat=2):
        constraints = [*box, (-e, -e, 1, -1), (f, -f, 1, -1)]
        value, _ = optimize(constraints, (0, 0, 1))
        assert value is not None
        scores.append(value)
    return max(scores)


def sampled(rect):
    a, b, c, d = map(F, rect)
    points = [*itertools.product((a, b), (c, d)), ((a + b) / 2, (c + d) / 2)]
    return all(abs(x + y) <= 1 or abs(y - x) <= 1 for x, y in points)


def frontier(length, bound):
    # Variables p,r,t are nonnegative absolute-coordinate extrema.
    common = [(-1, 0, 0, 0), (0, -1, 0, 0), (0, 0, -1, 0),
              (0, 1, -1, 0), (-1, 0, 1, 1),
              (1, 0, 0, bound), (0, 1, 0, bound), (0, 0, 1, bound)]
    maxima, witnesses = [], []
    for cross_x, cross_y in ((False, True), (True, True),
                             (True, False), (False, False)):
        constraints = list(common)
        if cross_x:
            constraints += [(1, 0, 0, 0), (0, -1, 0, 1 - length / 2)]
        else:
            constraints += [(1, -1, 0, 1 - length)]
        if cross_y:
            constraints += [(0, 1, 0, 0)]
        value, v = optimize(constraints, (0, 0, 2) if cross_y else (0, -1, 1))
        maxima.append(value)
        if value is not None and value > 0:
            p, r, t = v
            xs = [-length / 2, length / 2] if cross_x else [p, p + length]
            ys = [-t, t] if cross_y else [r, t]
            rect = [*xs, *ys]
            assert slack(rect) <= 0
            witnesses.append((value, rect))
    possible = [m for m in maxima if m is not None]
    height = max(possible) if possible else None
    witness = next((r for h, r in witnesses if h == height), None)
    return maxima, height, witness


def reconstruct(spec, outdir):
    # Boundary/counterexample checks precede all certificate reads.
    example = spec["counterexample"]
    assert sampled(example) and slack(example) == 1
    assert slack([-1, 1, -1, 1]) == 0
    assert slack([0, F(1, 2), 0, F(1, 2)]) < 0
    assert slack([2, 3, 0, F(1, 2)]) > 0
    physical = spec["physical"]
    c, s, delta = (F(physical[k]) for k in ("c", "s", "delta"))
    assert c > 0 and s > 0 and delta > 0 and c * c + s * s == 1
    intervals = list(itertools.combinations(map(F, spec["grid"]), 2))
    rows = []
    for xs, ys in itertools.product(intervals, repeat=2):
        rect = [*xs, *ys]
        rows.append([*[str(v) for v in rect], str(slack(rect)), sampled(rect)])
    frontier_rows, own_witnesses = [], []
    for value in spec["lengths"]:
        maxima, height, rect = frontier(F(value), F(spec["lp_gauge_bound"]))
        frontier_rows.append([value, None if height is None else str(height),
                              [None if m is None else str(m) for m in maxima]])
        own_witnesses.append([value, None if rect is None else [str(v) for v in rect]])
    table = dict(rectangles=rows, frontier=frontier_rows)
    outdir.joinpath("verification-frontier.json").write_bytes(encode(own_witnesses))
    summary = dict(
        rectangle_cases=len(rows), exterior_lp_problems=4 * len(rows),
        contained=sum(F(r[4]) <= 0 for r in rows),
        sample_false_positives=sum(r[5] and F(r[4]) > 0 for r in rows),
        frontier_lengths=len(frontier_rows), frontier_lp_problems=4 * len(frontier_rows),
        positive_frontier_certificates=sum(row[1] is not None for row in own_witnesses),
        counterexample=dict(rectangle=example, samples_pass=True,
                            missed_point=["2", "0"], violation="1"),
        physical_rectangle=[str(F(example[i]) * delta / (2 * (s if i < 2 else c)))
                            for i in range(4)],
        table_sha256=hashlib.sha256(encode(table)).hexdigest(), boundary_controls=4,
    )
    return summary, table


def accept(candidate, summary, table):
    if candidate.get("summary") != summary or candidate.get("table") != table:
        return False
    rows = candidate.get("frontier_certificates", [])
    expected = [r for r in table["frontier"] if r[1] is not None and F(r[1]) > 0]
    if len(rows) != len(expected):
        return False
    try:
        for row, target in zip(rows, expected, strict=True):
            length, rect = row
            a, b, c, d = map(F, rect)
            if length != target[0] or b - a != F(length) or d - c != F(target[1]):
                return False
            if slack(rect) > 0:
                return False
    except (ValueError, AssertionError, TypeError):
        return False
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--certificate", type=Path)
    args = parser.parse_args()
    spec = json.loads(args.input.read_text())
    summary, table = reconstruct(spec, args.output.parent)
    args.output.with_name("verification-table.json").write_bytes(encode(table))
    result = summary
    if args.certificate:
        candidate = json.loads(args.certificate.read_text())
        assert accept(candidate, summary, table)
        corruptions = [
            ("false_containment", lambda c: c["table"]["rectangles"][0].__setitem__(4, "99")),
            ("missing_rectangle", lambda c: c["table"]["rectangles"].pop()),
            ("wrong_frontier", lambda c: c["table"]["frontier"][0].__setitem__(1, "9")),
            ("missing_witness", lambda c: c["frontier_certificates"].pop()),
            ("reversed_rectangle", lambda c: c["frontier_certificates"][0][1].reverse()),
            ("false_sample_count", lambda c: c["summary"].update(sample_false_positives=-1)),
            ("translated_outside", lambda c: c["frontier_certificates"][0].__setitem__(
                1, ["10", "41/4", "0", "7/2"])),
        ]
        rejected = []
        for name, change in corruptions:
            bad = copy.deepcopy(candidate)
            change(bad)
            assert not accept(bad, summary, table)
            rejected.append(name)
        result = dict(summary=summary, corruptions_rejected=rejected, authentic_accepted=True)
    args.output.write_bytes(encode(result))
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
