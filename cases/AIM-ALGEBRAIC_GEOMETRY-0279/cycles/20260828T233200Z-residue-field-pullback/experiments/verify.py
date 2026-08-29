"""Verifier-first F2 linear algebra of explicit truncated pullback rings."""

import argparse
import copy
import hashlib
import itertools
import json
from pathlib import Path


def enc(x):
    return json.dumps(x, sort_keys=True, separators=(",", ":")).encode()


def multiply(a, b, modulus, r):
    out = 0
    while b:
        if b & 1:
            out ^= a
        b >>= 1
        a <<= 1
        if a & (1 << r):
            a ^= modulus
    return out


def power(a, q, modulus, r):
    out = 1
    for _ in range(q):
        out = multiply(out, a, modulus, r)
    return out


def insert(pivots, v):
    while v:
        j = v.bit_length() - 1
        if j not in pivots:
            pivots[j] = v
            return True
        v ^= pivots[j]
    return False


def algebra(field, d, q):
    r, modulus = field["degree"], field["modulus"]
    # Explicit field checks; multiplication is polynomial shift/reduction.
    size = 1 << r
    assert all(power(a, size, modulus, r) == a for a in range(size))
    assert all(any(multiply(a, b, modulus, r) == 1 for b in range(1, size)) for a in range(1, size))
    monomials = [a for a in itertools.product(range(q + 1), repeat=d + 1) if not (a[0] and a[1])]
    zero = (0,) * (d + 1)
    assert monomials[0] == zero
    positions = {a: i for i, a in enumerate(monomials)}
    basis = [(zero, 1)] + [(a, 1 << b) for a in monomials[1:] for b in range(r)]

    def vector(a, c):
        if not c or max(a) > q or (a[0] and a[1]):
            return 0
        i = positions[a]
        if i == 0:
            assert c <= 1, "constant not in pullback"
            return c
        return c << (1 + (i - 1) * r)

    pivots = {}
    column_count = 0
    column_hash = hashlib.sha256()
    for axis in range(d + 1):
        for b in range(r):
            # Powers of k-algebra generators beta_b*x_axis.
            c = power(1 << b, q, modulus, r)
            for a, coefficient in basis:
                exponent = list(a)
                exponent[axis] += q
                col = vector(tuple(exponent), multiply(c, coefficient, modulus, r))
                column_hash.update((str(col) + "\n").encode())
                column_count += 1
                insert(pivots, col)
    row = dict(
        r=r,
        d=d,
        q=q,
        ambient=len(basis),
        ideal_rank=len(pivots),
        length=len(basis) - len(pivots),
        columns=column_count,
        columns_sha256=column_hash.hexdigest(),
    )
    return row, basis, pivots


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--certificate")
    args = ap.parse_args()
    spec = json.loads(Path(args.input).read_text())
    fields = {f["degree"]: f for f in spec["fields"]}
    # Counterexample and q=1, no-extension, suspension boundaries first.
    boundary = [
        algebra(fields[r], d, q)[0] for r, d, q in [(2, 1, 2), (2, 1, 1), (1, 1, 2), (2, 2, 2)]
    ]
    rows = [
        algebra(f, d, q)[0]
        for f in spec["fields"]
        for d in spec["dimensions"]
        for q in spec["frobenius_powers"]
    ]
    profiles = [{k: row[k] for k in ["r", "d", "q", "length"]} for row in rows]
    out = dict(
        boundary=boundary,
        rows=rows,
        profiles=profiles,
        summary=dict(
            cases=len(rows),
            columns=sum(x["columns"] for x in rows),
            profiles_sha256=hashlib.sha256(enc(profiles)).hexdigest(),
        ),
    )
    if args.certificate:
        proposal = json.loads(Path(args.certificate).read_text())
        cache = {tuple(key): algebra(fields[key[0]], *key[1:]) for key in spec["certificates"]}

        def validate(packet):
            assert packet["profiles"] == profiles
            assert [[c[k] for k in ["r", "d", "q"]] for c in packet["certificates"]] == spec[
                "certificates"
            ]
            checks = 0
            for c in packet["certificates"]:
                key = tuple(c[k] for k in ["r", "d", "q"])
                row, basis, ideal = cache[key]
                assert c["length"] == row["length"]
                assert len(c["quotient_basis"]) == row["length"]
                index = {(a, b): i for i, (a, b) in enumerate(basis)}
                extended = ideal.copy()
                for a, b in c["quotient_basis"]:
                    assert insert(extended, 1 << index[(tuple(a), b)]), "dependent quotient vector"
                    checks += 1
                assert len(extended) == len(basis), "quotient basis incomplete"
                field = fields[c["r"]]
                roots = c["frobenius_roots"]
                assert len(roots) == 1 << c["r"]
                for a, root in enumerate(roots):
                    assert 0 <= root < len(roots)
                    assert power(root, c["q"], field["modulus"], c["r"]) == a
                    checks += 1
            return checks

        out["certificate_checks"] = validate(proposal)
        out["certificates_checked"] = len(proposal["certificates"])
        out["corruptions_rejected"] = []
        for label in [
            "wrong_length",
            "missing_basis",
            "duplicate_basis",
            "ideal_vector",
            "wrong_root",
            "missing_profile",
        ]:
            bad = copy.deepcopy(proposal)
            c = bad["certificates"][0]
            if label == "wrong_length":
                c["length"] += 1
            elif label == "missing_basis":
                c["quotient_basis"].pop()
            elif label == "duplicate_basis":
                c["quotient_basis"][-1] = c["quotient_basis"][0]
            elif label == "ideal_vector":
                c["quotient_basis"][-1] = [[2, 0], 1]
            elif label == "wrong_root":
                c["frobenius_roots"][1] = 0
            else:
                bad["profiles"].pop()
            try:
                validate(bad)
            except AssertionError:
                out["corruptions_rejected"].append(label)
            else:
                raise AssertionError("accepted corruption " + label)
    Path(args.output).write_text(json.dumps(out, sort_keys=True, indent=2) + "\n")
    print(json.dumps({k: v for k, v in out.items() if k not in {"rows", "profiles", "boundary"}}))


if __name__ == "__main__":
    main()
