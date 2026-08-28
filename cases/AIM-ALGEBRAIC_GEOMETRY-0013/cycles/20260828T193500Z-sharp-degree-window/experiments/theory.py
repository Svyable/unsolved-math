"""Homogeneous gcd and Hilbert-series formula; no matrix-rank implementation."""

import argparse
import hashlib
import itertools
import json
from pathlib import Path


def encoded(obj):
    return (json.dumps(obj, sort_keys=True, separators=(",", ":")) + "\n").encode()


def trim(f):
    f = list(f)
    while f and not f[-1]:
        f.pop()
    return f


def common_degree(f, g, p):
    if not any(f) and not any(g):
        return None
    d = len(f) - 1
    if not any(f) or not any(g):
        return d
    u, v = trim(f), trim(g)
    infinity = min(d - len(u) + 1, d - len(v) + 1)
    while v:
        while len(u) >= len(v):
            s = len(u) - len(v)
            c = u[-1] * pow(v[-1], -1, p) % p
            for j, x in enumerate(v):
                u[s + j] = (u[s + j] - c * x) % p
            u = trim(u)
        u, v = v, u
    return len(u) - 1 + infinity


def hilbert(d, e, r):
    def piece(s):
        return max(s + 1, 0)

    if e is None:
        return [piece(r), 2 * piece(r - d), piece(r - 2 * d)]
    return [
        piece(r) - 2 * piece(r - d) + piece(r - 2 * d + e),
        piece(r - 2 * d + e) - piece(r - 2 * d),
        0,
    ]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    args = ap.parse_args()
    spec = json.loads(Path(args.input).read_text())
    stream = hashlib.sha256()
    aggregates = []
    total = pieces = 0
    for p, d in spec["field_degrees"]:
        forms = list(itertools.product(range(p), repeat=d + 1))
        histogram = [0] * (d + 1)
        zeros = admissible = early_fail = euler_false = 0
        for f in forms:
            for g in forms:
                e = common_degree(f, g, p)
                good = e == 0
                hs = [hilbert(d, e, r) for r in range(-1, 2 * d + 2)]
                if e is None:
                    zeros += 1
                else:
                    histogram[e] += 1
                admissible += good
                early_fail += good and hs[2 * d - 1][0] != 0
                euler_false += not good
                stream.update(encoded([p, d, list(f), list(g), e, hs]))
                total += 1
                pieces += len(hs)
        aggregates.append(
            dict(
                p=p,
                d=d,
                pairs=len(forms) ** 2,
                gcd_degree_histogram=histogram,
                both_zero=zeros,
                admissible=admissible,
                early_false_rejections=early_fail,
                euler_false_acceptances=euler_false,
            )
        )
    controls = [
        dict(
            d=d,
            early=hilbert(d, 0, 2 * d - 2),
            cutoff=hilbert(d, 0, 2 * d - 1),
            bad=hilbert(d, d, 2 * d - 1),
        )
        for d in spec["certificate_degrees"]
    ]
    windows = []
    for A in spec["shift_bounds"]:
        for D in spec["degree_bounds"]:
            N = A + 2 * D - 1
            rejected = [
                dict(n=n, expected_virtual=n >= A, homology=hilbert(D, D if n < A else 0, n - A))
                for n in range(N)
            ]
            windows.append(dict(A=A, D=D, N=N, smaller_degrees_rejected=rejected))
    core = dict(
        pairs=total,
        graded_pieces=pieces,
        case_stream_sha256=stream.hexdigest(),
        rows=aggregates,
        controls=controls,
        hidden_shift_homology=hilbert(2, 2, -1),
        windows=windows,
    )
    certificates = []
    for d in spec["certificate_degrees"]:
        q = [[int(i == j) for i in range(2 * d)] for j in range(d)]
        z = [
            [int(i == j) if i < d else 2 * int(i - d == j) for i in range(2 * d)] for j in range(d)
        ]
        certificates.append(
            dict(
                p=3,
                d=d,
                r=2 * d - 1,
                f=[0] * d + [1],
                g=[0] * d + [1],
                homology=[d, d, 0],
                quotient_vectors=q,
                cycle_vectors=z,
            )
        )
    Path(args.output).write_bytes(encoded(dict(summary=core, certificates=certificates)))
    print(
        json.dumps(
            dict(
                pairs=total,
                graded_pieces=pieces,
                stream=stream.hexdigest(),
                certificates=len(certificates),
            )
        )
    )


if __name__ == "__main__":
    main()
