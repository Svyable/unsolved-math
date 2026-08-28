"""Verifier-first normalized bar chains and explicit free-bar contraction."""

import argparse
import copy
import hashlib
import itertools
import json
from pathlib import Path


def encoded(x):
    return (json.dumps(x, sort_keys=True, separators=(",", ":")) + "\n").encode()


def add(out, key, value, p):
    out[key] = (out.get(key, 0) + value) % p
    if not out[key]:
        del out[key]


def apply(vec, fn, p):
    out = {}
    for key, c in vec.items():
        for k, v in fn(key).items():
            add(out, k, c * v, p)
    return out


def rank(columns, p):
    pivots = {}
    for col in columns:
        v = col.copy()
        while v:
            k = min(v)
            c = v[k]
            if k not in pivots:
                inv = pow(c, -1, p)
                pivots[k] = {j: x * inv % p for j, x in v.items()}
                break
            for j, x in pivots[k].items():
                add(v, j, -c * x, p)
    return len(pivots)


def algebra(ms):
    basis = list(itertools.product(*(range(m) for m in ms)))
    index = {x: i for i, x in enumerate(basis)}

    def mul(i, j):
        x = tuple(a + b for a, b in zip(basis[i], basis[j], strict=True))
        return index.get(x)

    return basis, mul


def bar(word, mul, p, free=False):
    out = {}
    if free and len(word) == 1:
        return {(): 1} if word[0] == 0 else {}
    # Reduced chains omit the leading A factor; their first merge has sign -1.
    for j in range(len(word) - 1):
        z = mul(word[j], word[j + 1])
        if z is not None:
            sign = (-1) ** (j if free else j + 1)
            add(out, (*word[:j], z, *word[j + 2 :]), sign, p)
    return out


def contraction(word):
    if not word:
        return {(0,): 1}
    return {(0, *word): 1} if word[0] != 0 else {}


def audit(p, ms, maxn, maxs):
    basis, mul = algebra(ms)
    ideal = range(1, len(basis))
    diffs = [[]]
    ranks = [0]
    checks = 0
    stream = hashlib.sha256()
    for n in range(1, maxn + 2):
        columns = []
        for w in itertools.product(ideal, repeat=n):
            col = bar(w, mul, p)
            assert not apply(col, lambda v: bar(v, mul, p), p)
            checks += 1
            stream.update(encoded([list(w), [[list(k), c] for k, c in sorted(col.items())]]))
            columns.append(col)
        diffs.append(columns)
        ranks.append(rank(columns, p))
    betti = [(len(basis) - 1) ** n - ranks[n] - ranks[n + 1] for n in range(maxn + 1)]
    homotopies = 0
    for n in range(maxs + 1):
        for a0 in range(len(basis)):
            for rest in itertools.product(ideal, repeat=n):
                w = (a0, *rest)
                out = apply(contraction(w), lambda v: bar(v, mul, p, True), p)
                other = apply(bar(w, mul, p, True), contraction, p)
                for k, v in other.items():
                    add(out, k, v, p)
                assert out == {w: 1}, (p, ms, w, out)
                homotopies += 1
    product_indices = sorted({z for i in ideal for j in ideal if (z := mul(i, j)) is not None})
    embedding = len(ideal) - len(product_indices)
    assert embedding == betti[1]
    return (
        dict(p=p, exponents=ms, dimension=len(basis), betti=betti, embedding_dimension=embedding),
        dict(
            p=p,
            exponents=ms,
            bar_differential_ranks=ranks[1:],
            bar_square_checks=checks,
            contraction_identities=homotopies,
            differential_stream_sha256=stream.hexdigest(),
        ),
        product_indices,
    )


def cert_valid(certs, rows):
    if len(certs) != len(rows):
        return False
    for c, row in zip(certs, rows, strict=True):
        if any(c[key] != row[key] for key in ["p", "exponents", "dimension"]):
            return False
        p = c["p"]
        basis, mul = algebra(c["exponents"])
        size = len(basis) - 1
        fs = c["ext1_functionals"]
        if c["ext1_dimension"] != row["betti"][1] or len(fs) != row["betti"][1]:
            return False
        if any(
            len(f) != size or any(not isinstance(x, int) or x < 0 or x >= p for x in f) for f in fs
        ):
            return False
        cols = [{i: x for i, x in enumerate(f) if x} for f in fs]
        if rank(cols, p) != len(fs):
            return False
        for i in range(1, len(basis)):
            for j in range(1, len(basis)):
                z = mul(i, j)
                if z is not None and any(f[z - 1] for f in fs):
                    return False
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--certificate")
    args = ap.parse_args()
    spec = json.loads(Path(args.input).read_text())
    # Counterexample before the main census: I/I^2 dimensions for dimension-four algebras.
    witness = []
    for ms in [[4], [2, 2]]:
        basis, mul = algebra(ms)
        squares = sorted(
            {z for i in range(1, 4) for j in range(1, 4) if (z := mul(i, j)) is not None}
        )
        witness.append(
            dict(
                exponents=ms,
                dimension=4,
                ideal_square_basis=[list(basis[z]) for z in squares],
                ext1=3 - len(squares),
            )
        )
    assert [w["ext1"] for w in witness] == [1, 2]
    # Empty bar word and square-zero products are boundary cases.
    _, mul = algebra([2])
    assert bar((), mul, 3) == {} and bar((1, 1), mul, 3) == {}
    rows = []
    details = []
    for p in spec["primes"]:
        for ms in spec["exponent_lists"]:
            row, detail, _ = audit(p, ms, spec["max_ext_degree"], spec["max_contraction_degree"])
            rows.append(row)
            details.append(detail)
    core = dict(rows=rows, equal_dimension_witness=witness)
    output = dict(summary=core, bar_audit=details)
    if args.certificate:
        prop = json.loads(Path(args.certificate).read_text())
        assert prop["summary"] == core
        certs = prop["certificates"]
        assert cert_valid(certs, rows)
        rejected = []
        for name in [
            "missing",
            "algebra",
            "prime",
            "dimension",
            "zero_functional",
            "noncocycle",
            "extra_functional",
        ]:
            bad = copy.deepcopy(certs)
            if name == "missing":
                bad.pop()
            if name == "algebra":
                bad[2]["exponents"] = [2, 2]
            if name == "prime":
                bad[0]["p"] = 3
            if name == "dimension":
                bad[2]["ext1_dimension"] = 2
            if name == "zero_functional":
                bad[0]["ext1_functionals"] = [[0]]
            if name == "noncocycle":
                bad[2]["ext1_functionals"][0][1] = 1
            if name == "extra_functional":
                bad[0]["ext1_functionals"].append([1])
            assert not cert_valid(bad, rows), name
            rejected.append(name)
        output.update(certificates_checked=len(certs), corruptions_rejected=rejected)
    Path(args.output).write_bytes(encoded(output))
    print(
        json.dumps(
            dict(
                algebras=len(rows),
                ext_entries=sum(len(r["betti"]) for r in rows),
                bar_square_checks=sum(r["bar_square_checks"] for r in details),
                contractions=sum(r["contraction_identities"] for r in details),
                certificate_mode=bool(args.certificate),
            )
        )
    )


if __name__ == "__main__":
    main()
