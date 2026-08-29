"""Verifier-first integral bar/cellular H1; no two-generator formula imported."""

import argparse
import copy
import hashlib
import json
from math import gcd
from pathlib import Path


def encoded(x):
    return json.dumps(x, sort_keys=True, separators=(",", ":")).encode()


def complex_data(m, k, length):
    n, step = m * length, k * length
    ends = [(v, (v + 1) % n) for v in range(n)]
    ends += [(v, (v + g * step) % n) for g in range(1, m) for v in range(n)]

    def bar(g, v):
        return n + (g - 1) * n + v % n

    columns = []

    def emit(terms):
        col = {}
        for i, a in terms:
            col[i] = col.get(i, 0) + a
        col = {i: a for i, a in col.items() if a}
        boundary = [0] * n
        for i, a in col.items():
            start, end = ends[i]
            boundary[start] -= a
            boundary[end] += a
        assert not any(boundary), "d1*d2 != 0"
        columns.append(col)

    for g in range(1, m):
        for v in range(n):
            emit([((v + g * step) % n, 1), (v, -1), (bar(g, v + 1), -1), (bar(g, v), 1)])
    for g in range(1, m):
        for h in range(1, m):
            for v in range(n):
                terms = [(bar(h, v + g * step), 1), (bar(g, v), 1)]
                if (g + h) % m:
                    terms.append((bar((g + h) % m, v), -1))
                emit(terms)
    # Delete the N-1 tree-edge coordinates. On integral cycles the remaining
    # chord coordinates are a Z-basis: the tree incidence matrix is unimodular.
    chords = list(range(n - 1, m * n))
    a = [[c.get(i, 0) for c in columns] for i in chords]
    return a, len(columns), n


def smith_profile(a):
    a = [r[:] for r in a]
    rows = len(a)
    units = 0
    while a and a[0]:
        pivot = next(
            ((i, j) for i, r in enumerate(a) for j, x in enumerate(r) if abs(x) == 1), None
        )
        if pivot is None:
            break
        i, j = pivot
        pr = a[i]
        sign = pr[j]
        # Integral elementary elimination. Column clearing of the pivot row
        # leaves this lower-right matrix unchanged after the column is cleared.
        a = [
            [x - r[j] * sign * pr[c] for c, x in enumerate(r) if c != j]
            for z, r in enumerate(a)
            if z != i
        ]
        units += 1
    nz = [(i, j, x) for i, r in enumerate(a) for j, x in enumerate(r) if x]
    if not nz:
        return dict(free_rank=rows - units, torsion=[]), units
    i, j, pivot = nz[0]
    assert all(x * pivot == a[z][j] * a[i][c] for z, r in enumerate(a) for c, x in enumerate(r)), (
        "residual rank exceeds one"
    )
    divisor = gcd(*(x for _, _, x in nz))
    return dict(free_rank=rows - units - 1, torsion=[divisor] if divisor > 1 else []), units


def compute(m, k, length):
    a, columns, n = complex_data(m, k, length)
    profile, units = smith_profile(a)
    return dict(
        m=m,
        k=k,
        subdivision=length,
        vertices=n,
        chain_ranks=[n, m * n, columns],
        cycle_rank=len(a),
        smith_unit_pivots=units,
        h1=profile,
    )


def check_certificate(c, rows):
    key = (c["m"], c["k"], c["subdivision"])
    target = next(r for r in rows if (r["m"], r["k"], r["subdivision"]) == key)
    assert c["h1"] == target["h1"]
    a, _, _ = complex_data(*key)
    covector = c["free_covector"]
    assert len(covector) == len(a)
    assert gcd(*covector) == 1, "free covector must be primitive"
    assert all(sum(covector[i] * a[i][j] for i in range(len(a))) == 0 for j in range(len(a[0]))), (
        "covector does not kill relations"
    )
    assert c["fiber_value"] == covector[0] and c["fiber_value"] > 0
    return len(a[0])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--certificate")
    args = ap.parse_args()
    spec = json.loads(Path(args.input).read_text())
    # Compute failure and fixed-point controls before opening any proposal.
    boundary = [compute(*x) for x in [[2, 1, 2], [2, 0, 2], [4, 2, 1]]]
    rows = [
        compute(m, k, length)
        for m in spec["group_orders"]
        for k in range(m)
        for length in spec["subdivisions"]
    ]
    profiles = [{k: r[k] for k in ["m", "k", "subdivision", "h1"]} for r in rows]
    summary = dict(
        cases=len(rows),
        profiles_sha256=hashlib.sha256(encoded(profiles)).hexdigest(),
        chain_identity_columns=sum(r["chain_ranks"][2] for r in rows),
        split_formula_failures=sum(r["h1"] != dict(free_rank=1, torsion=[r["m"]]) for r in rows),
    )
    out = dict(boundary=boundary, rows=rows, profiles=profiles, summary=summary)
    if args.certificate:
        proposal = json.loads(Path(args.certificate).read_text())

        def validate(q):
            assert q["profiles"] == profiles
            assert [(c["m"], c["k"], c["subdivision"]) for c in q["certificates"]] == [
                tuple(x) for x in spec["certificates"]
            ]
            return sum(check_certificate(c, rows) for c in q["certificates"])

        out["covector_relation_checks"] = validate(proposal)
        out["certificates_checked"] = len(proposal["certificates"])
        rejected = []
        for label in [
            "zero_covector",
            "changed_covector",
            "wrong_torsion",
            "wrong_fiber_degree",
            "missing_profile",
            "missing_certificate",
        ]:
            bad = copy.deepcopy(proposal)
            c = bad["certificates"][0]
            if label == "zero_covector":
                c["free_covector"] = [0] * len(c["free_covector"])
            elif label == "changed_covector":
                c["free_covector"][1] += 1
            elif label == "wrong_torsion":
                c["h1"]["torsion"] = [2]
            elif label == "wrong_fiber_degree":
                c["fiber_value"] += 1
            elif label == "missing_profile":
                bad["profiles"].pop()
            else:
                bad["certificates"].pop()
            try:
                validate(bad)
            except AssertionError:
                rejected.append(label)
            else:
                raise AssertionError("accepted corruption: " + label)
        out["corruptions_rejected"] = rejected
    Path(args.output).write_text(json.dumps(out, sort_keys=True, indent=2) + "\n")
    print(json.dumps({k: v for k, v in out.items() if k not in {"rows", "profiles", "boundary"}}))


if __name__ == "__main__":
    main()
