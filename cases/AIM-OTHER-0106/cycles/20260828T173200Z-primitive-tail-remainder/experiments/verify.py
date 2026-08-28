"""Verifier first: exact endpoint atoms and literal approximation inequalities.

No theory import. Baseline runs before the theory implementation is authored.
"""

import argparse
import copy
import hashlib
import json
from fractions import Fraction as F
from itertools import pairwise
from math import gcd
from pathlib import Path


def encode(obj):
    return (json.dumps(obj, sort_keys=True, indent=2) + "\n").encode()


def member(x, q):
    y = q * x
    n = y.numerator // y.denominator
    return min(y - n, n + 1 - y) < F(1, q * q)


def centers(R, K):
    rows = []
    for d in range(1, K + 1):
        q = next((v for v in range(R, K + 1) if v % d == 0), None)
        if q is None:
            continue
        for a in range(d + 1):
            if gcd(a, d) == 1:
                rows.append([a, d, q, str(F(1, q**3))])
    return rows


def atom_audit(R, K):
    cs = centers(R, K)
    ends = {F(0), F(1)}
    for q in range(R, K + 1):
        for a in range(q + 1):
            ends.update([max(F(0), F(a, q) - F(1, q**3)), min(F(1), F(a, q) + F(1, q**3))])
    cuts = sorted(ends)
    raw = reduced = naive = F(0)
    merged = []
    for left, right in pairwise(cuts):
        x = (left + right) / 2
        yes = any(member(x, q) for q in range(R, K + 1))
        red = any(abs(x - F(a, d)) < F(radius) for a, d, q, radius in cs)
        nai = any(d >= R and abs(x - F(a, d)) < F(radius) for a, d, q, radius in cs)
        assert yes == red
        raw += (right - left) * yes
        reduced += (right - left) * red
        naive += (right - left) * nai
        if yes:
            if merged and merged[-1][1] == left:
                merged[-1][1] = right
            else:
                merged.append([left, right])
    return raw, reduced, naive, [[str(a), str(b)] for a, b in merged], len(cuts) - 1


def remainder(K):
    # Expand the six periodic weights; signed integral bounds checked separately.
    terms = [(1, 1), (2, -1), (3, -1), (6, 1)]
    ans = F(0)
    for d, sign in terms:
        M = sum(v % d == 0 for v in range(1, K + 1))
        integral = F(1, M if sign > 0 else M + 1)
        ans += sign * integral / d**3
    return 2 * ans


def residue_bound(K):
    # Convex midpoint cells of length six, a second independent upper envelope.
    total = F(0)
    for r in range(6):
        a = next(v for v in range(K + 1, K + 7) if v % 6 == r)
        w = F(sum(gcd(j, gcd(a, 6)) == 1 for j in range(1, 7)), 6)
        total += w / (3 * (a - 3))
    return total


def baseline(spec, outdir):
    # Counterexample and strict boundary checks precede all confirmation work.
    assert member(F(1, 2), 4)
    assert not any(
        abs(F(1, 2) - F(a, q)) < F(1, q**3)
        for q in range(4, 129)
        for a in range(q + 1)
        if gcd(a, q) == 1
    )
    boundary = [
        member(F(0), 4),
        member(F(1), 4),
        not member(F(1, 2) + F(1, 64), 4),
        not member(F(1, 2) - F(1, 64), 4),
        member(F(1, 2) + F(1, 128), 4),
        not any(d == 3 for a, d, q, radius in centers(4, 5)),
        any(d == 3 and q == 6 for a, d, q, radius in centers(4, 6)),
    ]
    assert all(boundary)
    rows = []
    atoms = 0
    featured = None
    for R, K in spec["cases"]:
        raw, red, naive, intervals, count = atom_audit(R, K)
        atoms += count
        eligible = max(6, 2 * R - 2) <= K
        B = remainder(K) if eligible else None
        C = residue_bound(K) if eligible else None
        rows.append(
            dict(
                R=R,
                K=K,
                area=str(raw),
                reduced_area=str(red),
                naive_primitive_area=str(naive),
                old_bound=str(min(F(1), raw + F(2, K))),
                new_remainder=str(B) if B is not None else None,
                residue_remainder=str(C) if C is not None else None,
                new_bound=str(min(F(1), raw + B)) if B is not None else None,
            )
        )
        if spec["featured"] == [R, K]:
            featured = dict(reduced_centers=centers(R, K), merged_intervals=intervals)
            assert C <= B and raw + B < F(spec["threshold"]) < raw + F(2, K)
        if [R, K] == [4, 4]:
            assert raw == F(1, 8) and naive == F(1, 16)
    phi_rows = []
    for q in spec["totient_denominators"]:
        phi = sum(gcd(a, q) == 1 for a in range(1, q + 1))
        selected = sum(
            not (q % 2 == 0 and a % 2 == 0) and not (q % 3 == 0 and a % 3 == 0)
            for a in range(1, q + 1)
        )
        assert phi <= selected
        expanded = F(1) - F(q % 2 == 0, 2) - F(q % 3 == 0, 3) + F(q % 6 == 0, 6)
        assert F(selected, q) == expanded
        phi_rows.append([q, phi, str(expanded)])
    table = dict(cases=rows, totients=phi_rows)
    (outdir / "verification-table.json").write_bytes(encode(table))
    (outdir / "verification-certificates.json").write_bytes(encode(featured))
    summary = dict(
        cases=len(rows),
        endpoint_atoms=atoms,
        totient_cases=len(phi_rows),
        boundary_controls=len(boundary),
        counterexample=dict(
            x="1/2",
            R=4,
            K=4,
            full_area="1/8",
            naive_primitive_area="1/16",
            point_check_denominators=125,
        ),
        table_sha256=hashlib.sha256(encode(table)).hexdigest(),
        featured=next(r for r in rows if [r["R"], r["K"]] == spec["featured"]),
    )
    return summary, featured


def check(cert, summary, expected):
    assert cert["summary"] == summary
    assert cert["certificates"] == expected


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path)
    ap.add_argument("output", type=Path)
    ap.add_argument("--certificate", type=Path)
    args = ap.parse_args()
    spec = json.loads(args.input.read_text())
    summary, expected = baseline(spec, args.output.parent)
    output = summary
    if args.certificate:
        cert = json.loads(args.certificate.read_text())
        check(cert, summary, expected)
        mutations = []
        for kind in range(7):
            bad = copy.deepcopy(cert)
            if kind == 0:
                bad["summary"]["featured"]["area"] = "0"
            if kind == 1:
                bad["summary"]["featured"]["new_remainder"] = "1/100"
            if kind == 2:
                bad["summary"]["totient_cases"] = 127
            if kind == 3:
                bad["certificates"]["reduced_centers"][0][2] = 1
            if kind == 4:
                bad["certificates"]["reduced_centers"][0][3] = "1/4"
            if kind == 5:
                bad["certificates"]["merged_intervals"][0][1] = "1"
            if kind == 6:
                bad["certificates"]["reduced_centers"].pop()
            try:
                check(bad, summary, expected)
            except AssertionError:
                mutations.append(kind)
            else:
                raise AssertionError("corruption accepted")
        output = dict(
            summary=summary,
            merged_intervals_checked=len(expected["merged_intervals"]),
            reduced_centers_checked=len(expected["reduced_centers"]),
            corrupted_packets_rejected=mutations,
            independence=(
                "same assistant; fresh process; raw modular endpoint atoms and gcd counts; "
                "no theory imports; shared input and signed-tail proof obligations"
            ),
        )
    args.output.write_bytes(encode(output))
    print(
        json.dumps(
            dict(
                cases=summary["cases"],
                atoms=summary["endpoint_atoms"],
                featured=summary["featured"],
                certificate=bool(args.certificate),
            )
        )
    )


if __name__ == "__main__":
    main()
