"""Valuation classification and factorization-based control certificates."""

import argparse
import json
from collections import Counter
from itertools import product
from math import comb
from pathlib import Path


def valuation(f):
    return next((i for i, a in enumerate(f) if a), len(f))


def analyze(f, g):
    m = len(f)
    a, b = valuation(f), valuation(g)
    is_complex = a + b >= m
    return dict(
        complex=is_complex, ranks=[m - a, m - b], homology=a + b - m if is_complex else None
    )


def compute(spec):
    edges = dict(
        bad=analyze([0, 0, 1], [0, 0, 1]),
        zero=analyze([0, 0, 0], [0, 0, 0]),
        unit=analyze([1, 0, 0], [0, 0, 0]),
        dual=analyze([0, 1], [0, 1]),
    )
    census = []
    for p in spec["fields"]:
        for m in spec["lengths"]:
            vals = [valuation(f) for f in product(range(p), repeat=m)]
            complexes, exact, hist = [], [], Counter()
            for i, a in enumerate(vals):
                for j, b in enumerate(vals):
                    if a + b >= m:
                        idx = i * len(vals) + j
                        complexes.append(idx)
                        hist[str(a + b - m)] += 1
                        if a + b == m:
                            exact.append(idx)
            census.append(
                dict(
                    p=p,
                    m=m,
                    total=p ** (2 * m),
                    complexes=complexes,
                    exact=exact,
                    homology=dict(hist),
                )
            )
    controls = []
    for p in spec["control_primes"]:
        for sep in [False, True]:
            # Kernels are complementary principal ideals. For square-free
            # z^p-z the augmentation factor is projective by CRT.
            ext = [1] + [int(not sep)] * spec["ext_max_degree"]
            idem = [1] + [0] * (p - 2) + [p - 1] if sep else None
            frob = [comb(p, i) * (-1) ** (p - i) % p for i in range(p + 1)]
            controls.append(
                dict(p=p, separable=sep, ranks=[p - 1, 1], ext=ext, idempotent=idem, frobenius=frob)
            )
    return dict(boundaries=edges, census=census, controls=controls)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    spec = json.loads(args.input.read_text())
    core = compute(spec)
    report = dict(method="valuation of truncated polynomials and control factorization", core=core)
    args.output.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n")
    print(
        json.dumps(
            dict(
                pairs=sum(x["total"] for x in core["census"]),
                exact=sum(len(x["exact"]) for x in core["census"]),
            )
        )
    )


if __name__ == "__main__":
    main()
