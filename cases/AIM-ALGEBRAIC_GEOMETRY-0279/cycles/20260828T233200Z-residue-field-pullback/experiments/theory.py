"""Monomial normal forms and coefficient-field transport, no rank implementation."""

import argparse
import hashlib
import itertools
import json
from pathlib import Path


def product(a, b, f):
    # Independent polynomial convolution followed by long division over F2.
    terms = [i for i in range(a.bit_length()) if (a >> i) & 1]
    other = [j for j in range(b.bit_length()) if (b >> j) & 1]
    out = 0
    for i in terms:
        for j in other:
            out ^= 1 << (i + j)
    while out.bit_length() >= f.bit_length():
        out ^= f << (out.bit_length() - f.bit_length())
    return out


def frobenius(a, q, f):
    assert q > 0 and q & (q - 1) == 0
    while q > 1:
        a = product(a, a, f)
        q //= 2
    return a


def profile(r, d, q):
    return dict(r=r, d=d, q=q, length=1 + r * ((2 * q - 1) * q ** (d - 1) - 1))


def certificate(r, d, q, f):
    zero = [0] * (d + 1)
    basis = [[zero, 1]]
    for tail in itertools.product(range(q), repeat=d - 1):
        for x, y in [(0, y) for y in range(q)] + [(x, 0) for x in range(1, q)]:
            a = [x, y, *tail]
            if a != zero:
                basis += [[a, 1 << b] for b in range(r)]
    roots = [None] * (1 << r)
    for b in range(1 << r):
        roots[frobenius(b, q, f)] = b
    assert None not in roots
    return dict(**profile(r, d, q), quotient_basis=basis, frobenius_roots=roots)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    args = ap.parse_args()
    spec = json.loads(Path(args.input).read_text())
    fields = {f["degree"]: f["modulus"] for f in spec["fields"]}
    profiles = [
        profile(r, d, q)
        for r in fields
        for d in spec["dimensions"]
        for q in spec["frobenius_powers"]
    ]
    out = dict(
        profiles=profiles,
        profiles_sha256=hashlib.sha256(
            json.dumps(profiles, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest(),
        certificates=[certificate(r, d, q, fields[r]) for r, d, q in spec["certificates"]],
        preserved_length_failures=sum(
            row["length"] != (2 * row["q"] - 1) * row["q"] ** (row["d"] - 1) for row in profiles
        ),
        omitted_constant_correction_failures=sum(
            row["length"] != row["r"] * (2 * row["q"] - 1) * row["q"] ** (row["d"] - 1)
            for row in profiles
        ),
    )
    Path(args.output).write_text(json.dumps(out, sort_keys=True, indent=2) + "\n")
    print(json.dumps({k: v for k, v in out.items() if k not in {"profiles", "certificates"}}))


if __name__ == "__main__":
    main()
