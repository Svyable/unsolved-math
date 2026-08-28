"""Absolute-range containment formula and explicit frontier constructions."""

import argparse
import hashlib
import itertools
import json
from fractions import Fraction as F
from pathlib import Path


def encode(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def absolute_range(a, b):
    return (F(0) if a <= 0 <= b else min(abs(a), abs(b)), max(abs(a), abs(b)))


def violation(rect):
    a, b, c, d = rect
    p, q = absolute_range(a, b)
    r, t = absolute_range(c, d)
    return max(q - r, t - p) - 1


def samples(rect):
    a, b, c, d = rect
    points = [(a, c), (a, d), (b, c), (b, d), ((a + b) / 2, (c + d) / 2)]
    return all(min(abs(x + y), abs(y - x)) <= 1 for x, y in points)


def frontier(length):
    branches = [4 - 2 * length if length <= 1 else None,
                F(2) if length <= 2 else None,
                min(F(1), 2 - length / 2) if length <= 4 else None,
                2 - length if length <= 2 else None]
    possible = [m for m in branches if m is not None]
    height = max(possible) if possible else None
    if length <= 1:
        rect = [1 - length, F(1), length - 2, 2 - length]
    elif length <= 2:
        rect = [-length / 2, length / 2, F(-1), F(1)]
    elif length < 4:
        rect = [-length / 2, length / 2, length / 2 - 1, F(1)]
    else:
        rect = None
    if rect is not None:
        assert violation(rect) <= 0 and rect[1] - rect[0] == length
        assert rect[3] - rect[2] == height
    return branches, height, rect


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    spec = json.loads(args.input.read_text())
    intervals = list(itertools.combinations(map(F, spec["grid"]), 2))
    rows = []
    for xs, ys in itertools.product(intervals, repeat=2):
        rect = [*xs, *ys]
        rows.append([*[str(v) for v in rect], str(violation(rect)), samples(rect)])
    frontier_rows, certificates = [], []
    for value in spec["lengths"]:
        branches, height, rect = frontier(F(value))
        frontier_rows.append([value, None if height is None else str(height),
                              [None if m is None else str(m) for m in branches]])
        if rect is not None:
            certificates.append([value, [str(v) for v in rect]])
    table = dict(rectangles=rows, frontier=frontier_rows)
    example = spec["counterexample"]
    assert samples(list(map(F, example))) and violation(list(map(F, example))) == 1
    physical = spec["physical"]
    c, s, delta = (F(physical[k]) for k in ("c", "s", "delta"))
    assert c * c + s * s == 1
    summary = dict(
        rectangle_cases=len(rows), exterior_lp_problems=4 * len(rows),
        contained=sum(F(r[4]) <= 0 for r in rows),
        sample_false_positives=sum(r[5] and F(r[4]) > 0 for r in rows),
        frontier_lengths=len(frontier_rows), frontier_lp_problems=4 * len(frontier_rows),
        positive_frontier_certificates=len(certificates),
        counterexample=dict(rectangle=example, samples_pass=True,
                            missed_point=["2", "0"], violation="1"),
        physical_rectangle=[str(F(example[i]) * delta / (2 * (s if i < 2 else c)))
                            for i in range(4)],
        table_sha256=hashlib.sha256(encode(table)).hexdigest(), boundary_controls=4,
    )
    args.output.with_name("theory-table.json").write_bytes(encode(table))
    args.output.write_bytes(encode(dict(summary=summary, table=table,
                                       frontier_certificates=certificates)))
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
