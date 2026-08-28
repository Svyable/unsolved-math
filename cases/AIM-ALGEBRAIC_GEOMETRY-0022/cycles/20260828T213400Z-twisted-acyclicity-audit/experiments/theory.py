"""Projection splitting and Serre duality; no fan Cech matrices."""

import argparse
import hashlib
import json
from pathlib import Path


def encoded(x):
    return (json.dumps(x, sort_keys=True, separators=(",", ":")) + "\n").encode()


def betti(n, a, b):
    if a == -1:
        return [0, 0, 0]
    if a <= -2:
        return list(reversed(betti(n, -a - 2, -b - n - 2)))
    degrees = [b - j * n for j in range(a + 1)]
    return [sum(max(d + 1, 0) for d in degrees), sum(max(-d - 1, 0) for d in degrees), 0]


def row(n, a, b):
    dims = betti(n, a, b)
    twice = (a + 1) * (2 * b + 2 - n * a)
    assert twice % 2 == 0
    chi = twice // 2
    assert chi == dims[0] - dims[1] + dims[2]
    immaculate = a == -1 or (b == -1 if n == 0 else (a, b) in [(0, -1), (-2, -n - 1)])
    assert immaculate == (not any(dims))
    if chi == 0 and a >= 0:
        m = a // 2
        numerator = n * (m + 1) ** 2 if a % 2 else n * m * (m + 1)
        assert numerator % 2 == 0
        assert dims == [numerator // 2, numerator // 2, 0]
    return dict(n=n, a=a, b=b, betti=dims, chi=chi)


def certificate(n, a, b):
    assert a >= 0
    classes = []
    for j in range(a + 1):
        degree = b - j * n
        for k in range(max(degree + 1, 0)):
            classes.append(dict(q=0, weight=[k - b, -j], vector=[1, 1, 1, 1]))
        for k in range(1, max(-degree, 1)):
            classes.append(dict(q=1, weight=[-j * n + k, -j], vector=[1, 1, 1, 1]))
    classes.sort(key=lambda c: [c["q"], *c["weight"]])
    return dict(n=n, a=a, b=b, betti=betti(n, a, b), classes=classes)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    args = ap.parse_args()
    spec = json.loads(Path(args.input).read_text())
    controls = [
        row(*v) for v in [(2, 1, 0), (2, 1, -1), (0, 1, -1), (2, -1, 100), (2, -2, -4), (2, -2, -3)]
    ]
    rows = []
    stream = hashlib.sha256()
    for n in spec["twists"]:
        for a in range(spec["a_range"][0], spec["a_range"][1] + 1):
            for b in range(spec["b_range"][0], spec["b_range"][1] + 1):
                r = row(n, a, b)
                rows.append(r)
                stream.update(encoded(r))
    summary = dict(
        cases=len(rows),
        rows_sha256=stream.hexdigest(),
        immaculate=sum(not any(r["betti"]) for r in rows),
        euler_false_acceptances=sum(r["chi"] == 0 and any(r["betti"]) for r in rows),
        base_window_false_acceptances=sum(r["b"] == -1 and any(r["betti"]) for r in rows),
        controls=controls,
    )
    output = dict(
        summary=summary,
        certificates=[certificate(*v) for v in spec["certificates"]],
        source_boundary=[
            dict(n=n, canonical=row(n, -2, -n - 2), canonical_plus_fibre=row(n, -2, -n - 1))
            for n in spec["twists"]
        ],
    )
    Path(args.output).write_bytes(encoded(output))
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
