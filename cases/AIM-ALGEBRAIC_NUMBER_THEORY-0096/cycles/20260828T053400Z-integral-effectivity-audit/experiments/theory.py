"""Bit-polynomial field arithmetic and explicit chart unit certificates."""

import json
import sys
from collections import Counter
from itertools import product
from pathlib import Path


def remainder(a, b):
    while a.bit_length() >= b.bit_length():
        a ^= b << (a.bit_length() - b.bit_length())
    return a


def field(n, modulus):
    for d in range(1, n // 2 + 1):
        assert all(remainder(modulus, b) for b in range(2**d, 2 ** (d + 1)))

    def mul(a, b):
        out = 0
        while b:
            if b & 1:
                out ^= a
            a <<= 1
            if a & (1 << n):
                a ^= modulus
            b >>= 1
        return out

    return mul


def quartic(mul, x, y, z):
    xx, yy, zz = mul(x, x), mul(y, y), mul(z, z)
    return (
        mul(xx, xx)
        ^ mul(yy, yy)
        ^ mul(zz, zz)
        ^ mul(xx, yy)
        ^ mul(xx, zz)
        ^ mul(yy, zz)
        ^ mul(mul(x, y), mul(z, x ^ y ^ z))
    )


def polynomial(monomials):
    out = 0
    for i, j in monomials:
        out ^= 1 << (16 * i + j)
    return out


def terms(poly):
    return [(i // 16, i % 16) for i in range(poly.bit_length()) if (poly >> i) & 1]


def multiply(a, b):
    return polynomial((i + k, j + ell) for i, j in terms(a) for k, ell in terms(b))


def main():
    spec = json.loads(Path(sys.argv[1]).read_text())
    expected = [
        [4, 0, 0],
        [0, 4, 0],
        [0, 0, 4],
        [2, 2, 0],
        [2, 0, 2],
        [0, 2, 2],
        [2, 1, 1],
        [1, 2, 1],
        [1, 1, 2],
    ]
    assert spec["monomials"] == expected
    remainders = []
    certificates = []
    p = polynomial([(2, 0), (1, 0)])
    q = polynomial([(0, 2), (0, 1)])
    for axis in range(3):
        f = polynomial(tuple(e for j, e in enumerate(m) if j != axis) for m in expected)
        # f=1+P^2+Q^2+PQ; f_u=Q, f_v=P.
        unit = f ^ multiply(p ^ q, p) ^ multiply(q, q)
        assert unit == 1
        remainders.append([list(m) for m in terms(unit)])
        certificates.append(
            dict(
                chart=axis,
                f=terms(f),
                du_multiplier=terms(q),
                dv_multiplier=terms(p ^ q),
                unit=terms(unit),
            )
        )
    rows = []
    witnesses = []
    for entry in spec["fields"]:
        n, modulus = entry["degree"], entry["modulus"]
        mul = field(n, modulus)
        size = 2**n
        points = [(1, y, z) for y in range(size) for z in range(size)]
        points += [(0, 1, z) for z in range(size)] + [(0, 0, 1)]
        roots = [p for p in points if quartic(mul, *p) == 0]
        unseen = set(roots)
        counts = Counter()
        while unseen:
            start = min(unseen)
            orbit = []
            point = start
            while point not in orbit:
                assert point in unseen
                unseen.remove(point)
                orbit.append(point)
                point = tuple(mul(x, x) for x in point)
            assert point == start
            counts[len(orbit)] += 1
        rows.append(
            dict(
                degree=n,
                modulus=modulus,
                ambient_count=len(points),
                points=[list(p) for p in roots],
                point_count=len(roots),
                closed_orbits=[[d, c] for d, c in sorted(counts.items())],
            )
        )
        if n in [2, 3]:
            point = roots[0]
            orbit = []
            for _ in range(n):
                orbit.append(list(point))
                point = tuple(mul(x, x) for x in point)
            assert point == roots[0] and len({tuple(p) for p in orbit}) == n
            witnesses.append(dict(degree=n, orbit=orbit))
    mul = field(1, 3)
    base = [quartic(mul, *p) for p in product(range(2), repeat=3) if any(p)]
    assert base == [1] * 7
    result = dict(
        base_values=base,
        chart_remainders=remainders,
        fields=rows,
        witnesses=witnesses,
        signed_degree=-2 + 3,
        controls=["drop-X4-detects-point", "reducible-modulus-rejected", "Fermat-derivatives-zero"],
    )
    assert quartic(mul, 1, 0, 0) ^ 1 == 0
    assert remainder(5, 3) == 0
    Path(sys.argv[2]).write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    Path(sys.argv[2]).with_name("theory-details.json").write_text(
        json.dumps(
            dict(
                chart_unit_certificates=certificates,
                identity="f + Q*f_u + (P+Q)*f_v = 1; P=u^2+u, Q=v^2+v",
            ),
            sort_keys=True,
            indent=2,
        )
        + "\n"
    )
    print(json.dumps({"point_counts": [r["point_count"] for r in rows], "witnesses": witnesses}))


if __name__ == "__main__":
    main()
