"""Direct quotient arithmetic and row reduction, independent of valuation formulas."""

import argparse
import copy
import json
from collections import Counter
from itertools import product
from pathlib import Path


def mul(a, b, p, separable=False):
    n = len(a)
    c = [0] * (2 * n - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] = (c[i + j] + x * y) % p
    for i in range(len(c) - 1, n - 1, -1):
        if separable:
            c[i - n + 1] = (c[i - n + 1] + c[i]) % p
        c[i] = 0
    return c[:n]


def rank(a, p):
    a = [row[:] for row in a]
    r = 0
    for col in range(len(a[0])):
        pivot = next((j for j in range(r, len(a)) if a[j][col] % p), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        inv = pow(a[r][col], -1, p)
        a[r] = [(v * inv) % p for v in a[r]]
        for j in range(len(a)):
            if j != r:
                q = a[j][col]
                a[j] = [(x - q * y) % p for x, y in zip(a[j], a[r], strict=True)]
        r += 1
        if r == len(a):
            break
    return r


def matrix(f, p, sep=False):
    n = len(f)
    columns = [mul(f, [int(i == j) for i in range(n)], p, sep) for j in range(n)]
    return [list(row) for row in zip(*columns, strict=True)]


def pair(f, g, p):
    n = len(f)
    z = not any(mul(f, g, p))
    ranks = [rank(matrix(f, p), p), rank(matrix(g, p), p)]
    return dict(complex=z, ranks=ranks, homology=n - sum(ranks) if z else None)


def boundary():
    return dict(
        bad=pair([0, 0, 1], [0, 0, 1], 2),
        zero=pair([0, 0, 0], [0, 0, 0], 2),
        unit=pair([1, 0, 0], [0, 0, 0], 2),
        dual=pair([0, 1], [0, 1], 2),
    )


def control(p, sep, top):
    a = [int(i == 1) for i in range(p)]
    b = [int(i == p - 1) for i in range(p)]
    if sep:
        b[0] = p - 1
    assert not any(mul(a, b, p, sep))
    ranks = [rank(matrix(a, p, sep), p), rank(matrix(b, p, sep), p)]
    assert sum(ranks) == p
    assert all(v[0] == 0 for v in [a])
    # Hom differential is evaluation at augmentation: alternating a(0), b(0).
    cochain = [int((a if i % 2 == 0 else b)[0] != 0) for i in range(top + 1)]
    ext = [1 - cochain[0]] + [1 - cochain[i - 1] - cochain[i] for i in range(1, top + 1)]
    idem = None
    if sep:
        idem = [1] + [0] * (p - 2) + [p - 1]
        assert mul(idem, idem, p, True) == idem
        assert not any(mul(a, idem, p, True)) and idem[0] == 1
    # Repeated two-variable multiplication of (z-u), not binomial coefficients.
    poly = {(0, 0): 1}
    for _ in range(p):
        nxt = Counter()
        for (i, j), v in poly.items():
            nxt[i + 1, j] += v
            nxt[i, j + 1] -= v
        poly = {key: v % p for key, v in nxt.items() if v % p}
    frob = [poly.get((i, p - i), 0) for i in range(p + 1)]
    return dict(p=p, separable=sep, ranks=ranks, ext=ext, idempotent=idem, frobenius=frob)


def compute(spec):
    # Counterexample/boundary checks happen before exhaustive or certificate reads.
    edges = boundary()
    assert edges["bad"] == dict(complex=True, ranks=[1, 1], homology=1)
    assert edges["zero"]["homology"] == 3
    assert edges["unit"]["homology"] == edges["dual"]["homology"] == 0
    census = []
    for p in spec["fields"]:
        for n in spec["lengths"]:
            elements = list(product(range(p), repeat=n))
            ranks = [rank(matrix(f, p), p) for f in elements]
            complexes, exact, hist = [], [], Counter()
            for i, f in enumerate(elements):
                for j, g in enumerate(elements):
                    if any(mul(f, g, p)):
                        continue
                    idx = i * len(elements) + j
                    h = n - ranks[i] - ranks[j]
                    assert h >= 0
                    complexes.append(idx)
                    hist[str(h)] += 1
                    if h == 0:
                        exact.append(idx)
            census.append(
                dict(
                    p=p,
                    m=n,
                    total=len(elements) ** 2,
                    complexes=complexes,
                    exact=exact,
                    homology=dict(hist),
                )
            )
    controls = [
        control(p, sep, spec["ext_max_degree"])
        for p in spec["control_primes"]
        for sep in [False, True]
    ]
    return dict(boundaries=edges, census=census, controls=controls)


def mutations(core):
    out = []
    for i in range(7):
        bad = copy.deepcopy(core)
        if i == 0:
            bad["boundaries"]["bad"]["homology"] = 0
        elif i == 1:
            bad["census"][0]["exact"].pop()
        elif i == 2:
            bad["census"][0]["exact"].append(0)
        elif i == 3:
            bad["controls"][0]["ext"][2] = 0
        elif i == 4:
            bad["controls"][1]["ext"][2] = 1
        elif i == 5:
            bad["controls"][1]["idempotent"][0] = 0
        else:
            bad["controls"][2]["frobenius"][1] = 1
        assert bad != core
        out.append(dict(mutation=i, rejected=(bad != core)))
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--certificate", type=Path)
    args = parser.parse_args()
    spec = json.loads(args.input.read_text())
    core = compute(spec)
    report = dict(method="quotient multiplication and modular row reduction", core=core)
    if args.certificate:
        certificate = json.loads(args.certificate.read_text())
        assert certificate["core"] == core, "certificate mismatch"
        report.update(certificate_matches=True, mutations=mutations(core))
    args.output.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n")
    print(
        json.dumps(
            dict(
                pairs=sum(x["total"] for x in core["census"]),
                complexes=sum(len(x["complexes"]) for x in core["census"]),
                exact=sum(len(x["exact"]) for x in core["census"]),
            )
        )
    )


if __name__ == "__main__":
    main()
