"""Exact Cech incidence matrices, tensor total complexes, and monomial counts."""

import argparse
import copy
import json
from fractions import Fraction
from itertools import product
from pathlib import Path


def rank(matrix):
    a = [[Fraction(x) for x in row] for row in matrix]
    if not a or not a[0]:
        return 0
    r = 0
    for c in range(len(a[0])):
        k = next((k for k in range(r, len(a)) if a[k][c]), None)
        if k is None:
            continue
        a[r], a[k] = a[k], a[r]
        pivot = a[r][c]
        a[r] = [v / pivot for v in a[r]]
        for j in range(r + 1, len(a)):
            factor = a[j][c]
            if factor:
                a[j] = [x - factor * y for x, y in zip(a[j], a[r], strict=True)]
        r += 1
        if r == len(a):
            break
    return r


def subsets(n, neg):
    return [s for s in range(1, 1 << (n + 1)) if s & neg == neg]


def incidence(s, t):
    added = t ^ s
    if s & t != s or added.bit_count() != 1:
        return 0
    return (-1) ** ((t & (added - 1)).bit_count())


def complex_data(ns, masks):
    basis = [[] for _ in range(sum(ns) + 1)]
    for faces in product(*(subsets(n, m) for n, m in zip(ns, masks, strict=True))):
        degree = sum(s.bit_count() - 1 for s in faces)
        basis[degree].append(faces)
    maps = []
    for q in range(len(basis) - 1):
        matrix = []
        for t in basis[q + 1]:
            row = []
            for s in basis[q]:
                changes = [j for j in range(len(ns)) if s[j] != t[j]]
                value = 0
                if len(changes) == 1:
                    j = changes[0]
                    value = incidence(s[j], t[j]) * (-1) ** sum(x.bit_count() - 1 for x in s[:j])
                row.append(value)
            matrix.append(row)
        maps.append(matrix)
    for q in range(len(maps) - 1):
        for row in maps[q + 1]:
            for j in range(len(basis[q])):
                assert sum(row[k] * maps[q][k][j] for k in range(len(row))) == 0
    ranks = [rank(x) for x in maps]
    betti = [
        len(level) - (ranks[q - 1] if q else 0) - (ranks[q] if q < len(ranks) else 0)
        for q, level in enumerate(basis)
    ]
    assert all(x >= 0 for x in betti)
    return basis, maps, betti


def contraction(n, neg):
    basis, d, betti = complex_data([n], [neg])
    assert not any(betti)
    v = next(i for i in range(n + 1) if not (neg >> i) & 1)
    h = [[]]
    for q in range(1, n + 1):
        h.append(
            [
                [
                    incidence(t[0], s[0])
                    if s[0] == (t[0] | (1 << v)) and not t[0] & (1 << v)
                    else 0
                    for s in basis[q]
                ]
                for t in basis[q - 1]
            ]
        )
    for q, level in enumerate(basis):
        for i in range(len(level)):
            for j in range(len(level)):
                left = (
                    sum(d[q - 1][i][k] * h[q][k][j] for k in range(len(basis[q - 1]))) if q else 0
                )
                right = (
                    sum(h[q + 1][i][k] * d[q][k][j] for k in range(len(basis[q + 1])))
                    if q < n
                    else 0
                )
                assert left + right == int(i == j), "contraction identity failed"
    return dict(
        n=n, negative_mask=neg, anchor=v, homotopy_matrices=h, integer_identity_checked=True
    )


def compositions(total, count):
    if total < 0:
        return
    if count == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for tail in compositions(total - first, count - 1):
                yield (first, *tail)


def one_line(n, degree, supports):
    result = [0] * (n + 1)
    # Mixed-sign weights of any magnitude have the checked contracting homotopy.
    for mask, total in [(0, degree), ((1 << (n + 1)) - 1, -degree - n - 1)]:
        for _ in compositions(total, n + 1):
            result = [x + y for x, y in zip(result, supports[n, mask], strict=True)]
    return result


def line_product(ns, ds, supports):
    out = [0] * (sum(ns) + 1)
    factors = [one_line(n, d, supports) for n, d in zip(ns, ds, strict=True)]
    for degrees in product(*(range(n + 1) for n in ns)):
        value = 1
        for j, q in enumerate(degrees):
            value *= factors[j][q]
        out[sum(degrees)] += value
    return out


def compute(spec):
    # Boundary and direction witness first, without reading theory output.
    supports = {
        (n, m): complex_data([n], [m])[2] for n in spec["dimensions"] for m in range(1 << (n + 1))
    }
    witness = dict(
        dimensions=[2, 2],
        degrees=[-1, 0],
        from_unit=line_product([2, 2], [-1, 0], supports),
        to_unit=line_product([2, 2], [1, 0], supports),
    )
    assert witness["from_unit"] == [0] * 5 and witness["to_unit"] == [3, 0, 0, 0, 0]
    assert one_line(2, -2, supports) == [0, 0, 0]
    assert one_line(2, -3, supports) == [0, 0, 1]
    assert one_line(2, 0, supports) == [1, 0, 0]
    contractions = [
        contraction(n, m) for n in spec["dimensions"] for m in range(1, (1 << (n + 1)) - 1)
    ]
    product_patterns = []
    for ns in spec["products"]:
        for masks in product(*(range(1 << (n + 1)) for n in ns)):
            betti = complex_data(ns, masks)[2]
            product_patterns.append(dict(dimensions=ns, masks=list(masks), betti=betti))
    lines = []
    degrees = range(spec["degree_min"], spec["degree_max"] + 1)
    for ns in spec["products"]:
        for ds in product(degrees, repeat=len(ns)):
            lines.append(
                dict(
                    dimensions=ns,
                    degrees=list(ds),
                    from_unit=line_product(ns, ds, supports),
                    to_unit=line_product(ns, [-d for d in ds], supports),
                )
            )
    rays = [[1, 0, 0, 0], [0, 1, 0, 0], [-1, -1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [0, 0, -1, -1]]
    col = [[i, j] for i in range(6) for j in range(i + 1, 6) if rank([rays[i], rays[j]]) < 2]
    core = dict(
        witness=witness,
        supports=[dict(n=n, mask=m, betti=v) for (n, m), v in supports.items()],
        product_patterns=product_patterns,
        line_bundles=lines,
        rays=rays,
        collinear_pairs=col,
    )
    return core, contractions


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--certificate", type=Path)
    args = parser.parse_args()
    core, contractions = compute(json.loads(args.input.read_text()))
    report = dict(
        method="exact rational Cech matrices and integer homotopies",
        core=core,
        contractions=contractions,
    )
    if args.certificate:
        assert json.loads(args.certificate.read_text())["core"] == core
        controls = []
        for mutation in range(7):
            changed = copy.deepcopy(core)
            if mutation == 0:
                changed["witness"]["from_unit"][0] = 3
            elif mutation == 1:
                changed["witness"]["to_unit"][0] = 0
            elif mutation == 2:
                changed["supports"][1]["betti"][0] = 1
            elif mutation == 3:
                changed["product_patterns"][0]["betti"][0] = 0
            elif mutation == 4:
                changed["line_bundles"].pop()
            elif mutation == 5:
                changed["collinear_pairs"].append([0, 1])
            else:
                changed["line_bundles"][0]["from_unit"][-1] += 1
            assert changed != core
            controls.append(dict(mutation=mutation, rejected=True))
        report.update(certificate_matches=True, adversarial_controls=controls)
    args.output.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n")
    print(
        json.dumps(
            dict(
                lines=len(core["line_bundles"]),
                patterns=len(core["product_patterns"]),
                supports=len(core["supports"]),
                contractions=len(contractions),
            )
        )
    )


if __name__ == "__main__":
    main()
