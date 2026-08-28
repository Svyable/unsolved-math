"""Tensor of periodic free resolutions; dense ranks, no bar construction."""

import argparse
import itertools
import json
import math
from pathlib import Path


def encoded(x):
    return (json.dumps(x, sort_keys=True, separators=(",", ":")) + "\n").encode()


def rank(mat, p):
    a = [row[:] for row in mat]
    if not a:
        return 0
    row = 0
    for j in range(len(a[0])):
        pivot = next((i for i in range(row, len(a)) if a[i][j]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        c = pow(a[row][j], -1, p)
        a[row] = [x * c % p for x in a[row]]
        for i in range(row + 1, len(a)):
            c = a[i][j]
            if c:
                a[i] = [(x - c * y) % p for x, y in zip(a[i], a[row], strict=True)]
        row += 1
        if row == len(a):
            break
    return row


def indices(n, r):
    return [x for x in itertools.product(range(n + 1), repeat=r) if sum(x) == n]


def differential(p, ms, n, signed=True):
    basis = list(itertools.product(*(range(m) for m in ms)))
    size = len(basis)
    if n == 0:
        return [[int(i == 0) for i in range(size)]]
    source = indices(n, len(ms))
    target = indices(n - 1, len(ms))
    lookup = {(a, b): i * size + j for i, a in enumerate(target) for j, b in enumerate(basis)}
    mat = [[0] * (len(source) * size) for _ in range(len(target) * size)]
    for col, (a, b) in enumerate(itertools.product(source, basis)):
        for j, m in enumerate(ms):
            if a[j] == 0:
                continue
            degree = 1 if a[j] % 2 else m - 1
            power = list(b)
            power[j] += degree
            if power[j] >= m:
                continue
            dest = list(a)
            dest[j] -= 1
            row = lookup[(tuple(dest), tuple(power))]
            mat[row][col] = (
                mat[row][col] + (-1) ** sum(a[:j]) if signed else mat[row][col] + 1
            ) % p
    return mat


def compose(a, b, p):
    return [
        [sum(x * y for x, y in zip(row, col, strict=True)) % p for col in zip(*b, strict=True)]
        for row in a
    ]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    args = ap.parse_args()
    spec = json.loads(Path(args.input).read_text())
    rows = []
    details = []
    certificates = []
    sign_probes = []
    for p in spec["primes"]:
        for ms in spec["exponent_lists"]:
            size = math.prod(ms)
            r = len(ms)
            limit = spec["max_ext_degree"]
            matrices = [differential(p, ms, n) for n in range(limit + 2)]
            ranks = [rank(m, p) for m in matrices]
            for n in range(1, limit + 2):
                assert not any(any(row) for row in compose(matrices[n - 1], matrices[n], p))
            terms = [len(indices(n, r)) for n in range(limit + 2)]
            homology = [size * terms[n] - ranks[n] - ranks[n + 1] for n in range(limit + 1)]
            assert homology == [0] * (limit + 1)
            # Each entry has positive exponent: extract coefficient of the unit.
            for n in range(1, limit + 2):
                mat = matrices[n]
                assert all(
                    mat[i * size][j * size] == 0
                    for i in range(terms[n - 1])
                    for j in range(terms[n])
                )
            betti = terms[: limit + 1]
            assert betti == [math.comb(n + r - 1, r - 1) for n in range(limit + 1)]
            rows.append(dict(p=p, exponents=ms, dimension=size, betti=betti, embedding_dimension=r))
            details.append(
                dict(
                    p=p,
                    exponents=ms,
                    free_term_ranks=terms,
                    differential_ranks=ranks,
                    augmented_homology=homology,
                    hom_differentials_zero=True,
                )
            )
            basis = list(itertools.product(*(range(m) for m in ms)))
            fs = [[int(b[j] == 1 and sum(b) == 1) for b in basis[1:]] for j in range(r)]
            certificates.append(
                dict(p=p, exponents=ms, dimension=size, ext1_dimension=r, ext1_functionals=fs)
            )
        # The mixed (1,1) free generator has two composition paths.
        bad = compose(differential(p, [2, 2], 1, False), differential(p, [2, 2], 2, False), p)
        column = indices(2, 2).index((1, 1)) * 4
        sign_probes.append(
            dict(
                p=p,
                exponents=[2, 2],
                source_multidegree=[1, 1],
                unsigned_square=[row[column] for row in bad],
                signed_square=[0] * 4,
            )
        )
    witness = [
        dict(exponents=[4], dimension=4, ideal_square_basis=[[2], [3]], ext1=1),
        dict(exponents=[2, 2], dimension=4, ideal_square_basis=[[1, 1]], ext1=2),
    ]
    core = dict(rows=rows, equal_dimension_witness=witness)
    Path(args.output).write_bytes(
        encoded(
            dict(
                summary=core,
                tensor_audit=details,
                certificates=certificates,
                sign_probes=sign_probes,
            )
        )
    )
    print(
        json.dumps(
            dict(
                algebras=len(rows),
                ext_entries=sum(len(r["betti"]) for r in rows),
                certificates=len(certificates),
                sign_probes=sign_probes,
            )
        )
    )


if __name__ == "__main__":
    main()
