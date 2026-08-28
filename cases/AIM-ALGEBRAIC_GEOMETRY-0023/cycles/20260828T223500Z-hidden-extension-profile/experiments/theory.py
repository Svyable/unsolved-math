"""Block decomposition and cyclic-order formulas, separate from literal addition."""

import argparse
import hashlib
import itertools
import json
from collections import Counter
from math import gcd, lcm
from pathlib import Path


def encoded(x):
    return json.dumps(x, sort_keys=True, separators=(",", ":")).encode()


def blocks(edges):
    starts = [0] + [i + 1 for i, e in enumerate(edges) if e == 0]
    ends = [*starts[1:], len(edges) + 1]
    return list(zip(starts, ends, strict=True))


def row(p, edges):
    n = len(edges) + 1
    bs = blocks(edges)
    orders = []
    for x in itertools.product(range(p), repeat=n):
        orders.append(
            lcm(
                *(
                    p ** (b - a) // gcd(p ** (b - a), sum(x[i] * p ** (i - a) for i in range(a, b)))
                    for a, b in bs
                )
            )
        )
    hist = Counter(orders)
    # Independent analytic order histogram from killed-by-p^k cardinalities.
    counts = {"1": 1}
    previous = 1
    for k in range(1, max(b - a for a, b in bs) + 1):
        killed = p ** sum(min(k, b - a) for a, b in bs)
        counts[str(p**k)] = killed - previous
        previous = killed
    assert counts == {str(k): v for k, v in hist.items()}
    return dict(
        p=p,
        edges=list(edges),
        cardinality=p**n,
        exponent=p ** max(b - a for a, b in bs),
        order_histogram=counts,
        ordered_orders_sha256=hashlib.sha256(encoded(orders)).hexdigest(),
    )


def certificate(p, edges):
    n = len(edges) + 1
    bs = blocks(edges)
    a, b = max(bs, key=lambda ab: ab[1] - ab[0])
    return dict(
        p=p,
        edges=edges,
        moduli=[p ** (d - c) for c, d in bs],
        matrix=[[p ** (i - c) if c <= i < d else 0 for i in range(n)] for c, d in bs],
        witness=[int(i == a) for i in range(n)],
        exponent=p ** (b - a),
        nonzero_multiple=[int(i == b - 1) for i in range(n)],
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    args = ap.parse_args()
    spec = json.loads(Path(args.input).read_text())
    rows = [
        row(p, e)
        for p, top in spec["domains"]
        for n in range(1, top + 1)
        for e in itertools.product([0, 1], repeat=n - 1)
    ]
    out = dict(
        rows=rows,
        summary=dict(
            groups=len(rows),
            elements=sum(r["cardinality"] for r in rows),
            rows_sha256=hashlib.sha256(encoded(rows)).hexdigest(),
        ),
        certificates=[certificate(p, e) for p, e in spec["certificates"]],
    )
    Path(args.output).write_text(json.dumps(out, sort_keys=True, indent=2) + "\n")
    print(json.dumps(out["summary"]))


if __name__ == "__main__":
    main()
