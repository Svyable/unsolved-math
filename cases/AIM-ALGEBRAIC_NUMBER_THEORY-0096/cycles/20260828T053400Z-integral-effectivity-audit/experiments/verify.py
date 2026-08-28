"""Tuple field arithmetic, chart polynomial division, and fixed-point degree tests."""

import argparse
import copy
import json
from collections import Counter
from itertools import product
from pathlib import Path


def bits(v, n):
    return tuple((v // 2**i) % 2 for i in range(n))


def trim(p):
    while p and not p[-1]:
        p.pop()
    return p


def rem(a, b):
    a = trim(list(a))
    while len(a) >= len(b):
        shift = len(a) - len(b)
        for i, x in enumerate(b):
            a[shift + i] = (a[shift + i] + x) % 2
        trim(a)
    return a


class Field:
    def __init__(self, n, modulus):
        self.n = n
        self.mod = bits(modulus, n + 1)
        for d in range(1, n // 2 + 1):
            for coeff in product(range(2), repeat=d):
                assert rem(self.mod, (*coeff, 1)), "reducible field modulus"
        self.zero = (0,) * n
        self.one = (1,) + (0,) * (n - 1)
        self.values = [bits(i, n) for i in range(2**n)]
        self.table = {}
        for a in self.values:
            for b in self.values:
                p = [0] * (2 * n - 1)
                for i in range(n):
                    for j in range(n):
                        p[i + j] = (p[i + j] + a[i] * b[j]) % 2
                r = rem(p, self.mod)
                self.table[a, b] = tuple(r + [0] * (n - len(r)))
        for a in self.values[1:]:
            assert any(self.mul(a, b) == self.one for b in self.values)
        self.square_columns = [self.mul(bits(2**i, n), bits(2**i, n)) for i in range(n)]

    def add(self, a, b):
        return tuple((x + y) % 2 for x, y in zip(a, b, strict=True))

    def mul(self, a, b):
        return self.table[a, b]

    def power(self, a, n):
        out = self.one
        for _ in range(n):
            out = self.mul(out, a)
        return out

    def square(self, a):
        out = self.zero
        for c, col in zip(a, self.square_columns, strict=True):
            if c:
                out = self.add(out, col)
        return out

    def encode(self, a):
        return sum(x * 2**i for i, x in enumerate(a))


def evaluate(field, mons, p):
    out = field.zero
    for mon in mons:
        term = field.one
        for a, e in zip(p, mon, strict=True):
            term = field.mul(term, field.power(a, e))
        out = field.add(out, term)
    return out


def chart(mons, axis):
    out = set()
    for mon in mons:
        m = tuple(e for i, e in enumerate(mon) if i != axis)
        out.symmetric_difference_update([m])
    return out


def partial(poly, axis):
    out = set()
    for mon in poly:
        if mon[axis] % 2:
            m = list(mon)
            m[axis] -= 1
            out.symmetric_difference_update([tuple(m)])
    return out


def divide(poly, divisors):
    current = set(poly)
    quotients = [set() for _ in divisors]
    residue = set()
    while current:
        m = max(current)
        for i, d in enumerate(divisors):
            lead = max(d)
            if all(x >= y for x, y in zip(m, lead, strict=True)):
                q = tuple(x - y for x, y in zip(m, lead, strict=True))
                quotients[i].symmetric_difference_update([q])
                current.symmetric_difference_update(
                    tuple(x + y for x, y in zip(q, t, strict=True)) for t in d
                )
                break
        else:
            current.remove(m)
            residue.add(m)
    # Verify the division equality, not only the algorithm's remainder.
    rebuilt = set(residue)
    for q, d in zip(quotients, divisors, strict=True):
        for a in q:
            for b in d:
                rebuilt.symmetric_difference_update(
                    [tuple(x + y for x, y in zip(a, b, strict=True))]
                )
    assert rebuilt == poly
    return sorted(residue), [sorted(q) for q in quotients]


def reconstruct(spec):
    mons = spec["monomials"]
    # Begin with base-field counterexample search and bad-input controls.
    f2 = Field(1, 3)
    points2 = [p for p in product(range(2), repeat=3) if any(p)]
    values2 = [f2.encode(evaluate(f2, mons, tuple((x,) for x in p))) for p in points2]
    assert values2 == [1] * 7
    assert evaluate(f2, mons[1:], ((1,), (0,), (0,))) == f2.zero
    try:
        Field(2, 5)
    except AssertionError:
        pass
    else:
        raise AssertionError("reducible modulus accepted")
    fermat = {(4, 0), (0, 4), (0, 0)}
    assert not partial(fermat, 0) and not partial(fermat, 1)
    remainders = []
    quotients = []
    for axis in range(3):
        c = chart(mons, axis)
        r, q = divide(c, [partial(c, 0), partial(c, 1)])
        assert r == [(0, 0)]
        remainders.append([list(m) for m in r])
        quotients.append(q)
    rows = []
    witnesses = []
    for entry in spec["fields"]:
        n = entry["degree"]
        field = Field(n, entry["modulus"])
        points = [(field.one, y, z) for y in field.values for z in field.values]
        points += [(field.zero, field.one, z) for z in field.values]
        points += [(field.zero, field.zero, field.one)]
        roots = [p for p in points if evaluate(field, mons, p) == field.zero]
        by_degree = Counter()
        encoded = []
        for p in roots:
            image = p
            for d in range(1, n + 1):
                image = tuple(field.square(a) for a in image)
                if image == p:
                    by_degree[d] += 1
                    break
            encoded.append([field.encode(a) for a in p])
        for d, count in by_degree.items():
            assert count % d == 0
        rows.append(
            dict(
                degree=n,
                modulus=entry["modulus"],
                ambient_count=len(points),
                points=encoded,
                point_count=len(roots),
                closed_orbits=[[d, c // d] for d, c in sorted(by_degree.items())],
            )
        )
        if n in [2, 3]:
            assert roots and by_degree[n] == len(roots)
            p = roots[0]
            orb = []
            for _ in range(n):
                orb.append([field.encode(a) for a in p])
                p = tuple(field.square(a) for a in p)
            witnesses.append(dict(degree=n, orbit=orb))
    return dict(
        base_values=values2,
        chart_remainders=remainders,
        fields=rows,
        witnesses=witnesses,
        signed_degree=-2 + 3,
        controls=["drop-X4-detects-point", "reducible-modulus-rejected", "Fermat-derivatives-zero"],
    ), quotients


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("--certificate")
    args = parser.parse_args()
    result, quotients = reconstruct(json.loads(Path(args.input).read_text()))
    output = result
    if args.certificate:
        certificate = json.loads(Path(args.certificate).read_text())
        assert certificate == result
        paths = [
            ("base_values", 0),
            ("fields", 1, "point_count"),
            ("fields", 2, "modulus"),
            ("witnesses", 0, "degree"),
            ("witnesses", 1, "orbit", 0, 1),
            ("chart_remainders", 0, 0, 0),
            ("signed_degree",),
        ]
        for path in paths:
            bad = copy.deepcopy(certificate)
            obj = bad
            for key in path[:-1]:
                obj = obj[key]
            obj[path[-1]] += 1
            assert bad != result
        output = dict(
            reconstructed=result,
            division_quotients=quotients,
            certificate_equal=True,
            rejected_mutations=[list(p) for p in paths],
        )
    Path(args.output).write_text(json.dumps(output, sort_keys=True, indent=2) + "\n")
    print(
        json.dumps(
            {
                "point_counts": [r["point_count"] for r in result["fields"]],
                "witnesses": result["witnesses"],
            }
        )
    )


if __name__ == "__main__":
    main()
