"""Verifier first: actual graded maps; finite-factor tables, no gcd formula."""

import argparse
import copy
import hashlib
import itertools
import json
from pathlib import Path


def encoded(obj):
    return (json.dumps(obj, sort_keys=True, separators=(",", ":")) + "\n").encode()


def rank(columns, rows, p):
    pivots = {}
    for column in columns:
        v = list(column)
        for i in range(rows):
            if not v[i]:
                continue
            if i in pivots:
                c = v[i]
                v = [(x - c * y) % p for x, y in zip(v, pivots[i], strict=True)]
            else:
                c = pow(v[i], -1, p)
                pivots[i] = [c * x % p for x in v]
                break
    return len(pivots)


def mul(f, g, p):
    out = [0] * (len(f) + len(g) - 1)
    for i, x in enumerate(f):
        for j, y in enumerate(g):
            out[i + j] = (out[i + j] + x * y) % p
    return tuple(out)


def factor_table(p, d, forms):
    table = {f: set() for f in forms}
    for e in range(1, d + 1):
        for h in itertools.product(range(p), repeat=e + 1):
            if not any(h) or next(x for x in h if x) != 1:
                continue
            for q in itertools.product(range(p), repeat=d - e + 1):
                table[mul(h, q, p)].add((e, h))
    return table


def maps(f, g, p, r):
    d = len(f) - 1
    c1, c2, c3 = max(r + 1, 0), max(r - d + 1, 0), max(r - 2 * d + 1, 0)
    b = []
    for h in [f, g]:
        for i in range(c2):
            b.append([0] * i + list(h) + [0] * (c1 - i - len(h)))
    c = []
    for i in range(c3):
        c.append(
            [0] * i
            + [(-x) % p for x in g]
            + [0] * (c2 - i - len(g))
            + [0] * i
            + list(f)
            + [0] * (c2 - i - len(f))
        )
    for col in c:
        assert all(sum(b[j][i] * col[j] for j in range(2 * c2)) % p == 0 for i in range(c1))
    rb, rc = rank(b, c1, p), rank(c, 2 * c2, p)
    return [c1 - rb, 2 * c2 - rb - rc, c3 - rc]


def witnesses(spec):
    rows = []
    for d in spec["certificate_degrees"]:
        f = [0] * d + [1]
        g = [1] + [0] * d
        rows.append(
            dict(
                d=d,
                early=maps(f, g, 3, 2 * d - 2),
                cutoff=maps(f, g, 3, 2 * d - 1),
                bad=maps(f, f, 3, 2 * d - 1),
            )
        )
    return rows


def certificates_valid(certs, spec):
    if len(certs) != len(spec["certificate_degrees"]):
        return False
    for row, d in zip(certs, spec["certificate_degrees"], strict=True):
        if row["d"] != d or row["p"] != 3 or row["r"] != 2 * d - 1:
            return False
        f = [0] * d + [1]
        if row["f"] != f or row["g"] != f:
            return False
        # At this degree d3 has zero domain. These vectors must give d
        # independent cycles and d independent quotient classes.
        q, z = row["quotient_vectors"], row["cycle_vectors"]
        if len(q) != d or len(z) != d or any(len(v) != 2 * d for v in q + z):
            return False
        image = [[0] * i + f + [0] * (d - 1 - i) for i in range(d)]
        if rank(image + q, 2 * d, 3) != 2 * d or rank(z, 2 * d, 3) != d:
            return False
        if any((v[i] + v[d + i]) % 3 for v in z for i in range(d)):
            return False
        if row["homology"] != maps(f, f, 3, 2 * d - 1):
            return False
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--certificate")
    args = ap.parse_args()
    spec = json.loads(Path(args.input).read_text())
    # Counterexamples and negative-degree boundaries BEFORE the main census.
    controls = witnesses(spec)
    assert all(
        r["early"] == [1, 0, 0] and r["cutoff"] == [0, 0, 0] and r["bad"] == [r["d"], r["d"], 0]
        for r in controls
    )
    hidden = maps([0, 0, 1], [0, 0, 1], 3, -1)
    assert hidden == [0, 0, 0]
    stream = hashlib.sha256()
    aggregates = []
    pieces = total = 0
    for p, d in spec["field_degrees"]:
        forms = list(itertools.product(range(p), repeat=d + 1))
        factors = factor_table(p, d, forms)
        histogram = [0] * (d + 1)
        zeros = admissible = early_fail = euler_false = 0
        for f in forms:
            for g in forms:
                nonzero = any(f) or any(g)
                e = max((x[0] for x in factors[f] & factors[g]), default=0)
                good = nonzero and e == 0
                hs = [maps(f, g, p, r) for r in range(-1, 2 * d + 2)]
                hcut = hs[2 * d]  # r=2d-1
                assert (hcut[0] == 0) == good
                assert (hcut == [0, 0, 0]) == good
                assert hcut[0] - hcut[1] + hcut[2] == 0
                if nonzero:
                    histogram[e] += 1
                else:
                    zeros += 1
                admissible += good
                early_fail += good and hs[2 * d - 1][0] != 0
                euler_false += not good
                stream.update(encoded([p, d, list(f), list(g), e if nonzero else None, hs]))
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
    # Bounded uniform cutoff: actual maps for all shifts/degrees and power controls.
    windows = []
    for A in spec["shift_bounds"]:
        for D in spec["degree_bounds"]:
            N = A + 2 * D - 1
            for a in range(A + 1):
                for d in range(1, D + 1):
                    f = [0] * d + [1]
                    g = [1] + [0] * d
                    assert maps(f, g, 3, N - a) == [0, 0, 0]
                    assert maps(f, f, 3, N - a)[0] > 0
            rejected = []
            for n in range(N):
                f = [0] * D + [1]
                g = [1] + [0] * D
                h = maps(f, f if n < A else g, 3, n - A)
                assert h == [0, 0, 0] if n < A else h[0] > 0
                rejected.append(dict(n=n, expected_virtual=n >= A, homology=h))
            windows.append(dict(A=A, D=D, N=N, smaller_degrees_rejected=rejected))
    core = dict(
        pairs=total,
        graded_pieces=pieces,
        case_stream_sha256=stream.hexdigest(),
        rows=aggregates,
        controls=controls,
        hidden_shift_homology=hidden,
        windows=windows,
    )
    output = core
    if args.certificate:
        proposal = json.loads(Path(args.certificate).read_text())
        assert proposal["summary"] == core
        certs = proposal["certificates"]
        assert certificates_valid(certs, spec)
        corruptions = []
        for name in ["missing", "degree", "field", "form", "quotient", "cycle", "homology"]:
            bad = copy.deepcopy(certs)
            if name == "missing":
                bad.pop()
            if name == "degree":
                bad[0]["r"] += 1
            if name == "field":
                bad[0]["p"] = 2
            if name == "form":
                bad[0]["f"][0] = 1
            if name == "quotient":
                bad[0]["quotient_vectors"][0] = [0, 0]
            if name == "cycle":
                bad[0]["cycle_vectors"][0][0] = 0
            if name == "homology":
                bad[0]["homology"][0] = 0
            assert not certificates_valid(bad, spec), name
            corruptions.append(name)
        output = dict(
            summary=core, certificates_checked=len(certs), corruptions_rejected=corruptions
        )
    Path(args.output).write_bytes(encoded(output))
    print(
        json.dumps(
            dict(
                pairs=total,
                graded_pieces=pieces,
                stream=stream.hexdigest(),
                certificate_mode=bool(args.certificate),
            )
        )
    )


if __name__ == "__main__":
    main()
