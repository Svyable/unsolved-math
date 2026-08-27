"""Closed projective-space cohomology windows and product formulas."""

import argparse
import json
from itertools import product
from math import comb, prod
from pathlib import Path


def support(n, mask):
    b = [0] * (n + 1)
    if mask == 0:
        b[0] = 1
    elif mask == (1 << (n + 1)) - 1:
        b[n] = 1
    return b


def tensor_betti(factors):
    result = [1]
    for factor in factors:
        new = [0] * (len(result) + len(factor) - 1)
        for i, x in enumerate(result):
            for j, y in enumerate(factor):
                new[i + j] += x * y
        result = new
    return result


def line(ns, ds):
    b = [0] * (sum(ns) + 1)
    if any(-n <= d <= -1 for n, d in zip(ns, ds, strict=True)):
        return b
    q = sum(n for n, d in zip(ns, ds, strict=True) if d < 0)
    b[q] = prod(comb(d + n, n) if d >= 0 else comb(-d - 1, n) for n, d in zip(ns, ds, strict=True))
    return b


def compute(spec):
    supports = [
        dict(n=n, mask=m, betti=support(n, m))
        for n in spec["dimensions"]
        for m in range(1 << (n + 1))
    ]
    patterns = []
    for ns in spec["products"]:
        for masks in product(*(range(1 << (n + 1)) for n in ns)):
            patterns.append(
                dict(
                    dimensions=ns,
                    masks=list(masks),
                    betti=tensor_betti([support(n, m) for n, m in zip(ns, masks, strict=True)]),
                )
            )
    lines = []
    degrees = range(spec["degree_min"], spec["degree_max"] + 1)
    for ns in spec["products"]:
        for ds in product(degrees, repeat=len(ns)):
            lines.append(
                dict(
                    dimensions=ns,
                    degrees=list(ds),
                    from_unit=line(ns, ds),
                    to_unit=line(ns, [-d for d in ds]),
                )
            )
    rays = [[1, 0, 0, 0], [0, 1, 0, 0], [-1, -1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [0, 0, -1, -1]]
    col = [
        [i, j]
        for i in range(6)
        for j in range(i + 1, 6)
        if all(
            rays[i][a] * rays[j][b] - rays[i][b] * rays[j][a] == 0
            for a in range(4)
            for b in range(a + 1, 4)
        )
    ]
    return dict(
        witness=dict(
            dimensions=[2, 2],
            degrees=[-1, 0],
            from_unit=line([2, 2], [-1, 0]),
            to_unit=line([2, 2], [1, 0]),
        ),
        supports=supports,
        product_patterns=patterns,
        line_bundles=lines,
        rays=rays,
        collinear_pairs=col,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    core = compute(json.loads(args.input.read_text()))
    args.output.write_text(
        json.dumps(
            dict(method="cohomology windows and binomial product", core=core),
            sort_keys=True,
            indent=2,
        )
        + "\n"
    )
    print(json.dumps(dict(lines=len(core["line_bundles"]), patterns=len(core["product_patterns"]))))


if __name__ == "__main__":
    main()
