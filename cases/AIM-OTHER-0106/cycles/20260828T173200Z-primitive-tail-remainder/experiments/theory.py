"""Theory: reduced-center construction, interval union, multiplicative totients."""

import hashlib
import json
import sys
from fractions import Fraction as F
from math import gcd
from pathlib import Path


def encode(obj):
    return (json.dumps(obj, sort_keys=True, indent=2) + "\n").encode()


def reduced(R, K):
    result = []
    for d in range(1, K + 1):
        q = d * ((R + d - 1) // d)
        if q <= K:
            for a in range(d + 1):
                if gcd(a, d) == 1:
                    result.append([a, d, q, str(F(1, q**3))])
    return result


def union(cs):
    intervals = sorted(
        (max(F(0), F(a, d) - F(rad)), min(F(1), F(a, d) + F(rad))) for a, d, q, rad in cs
    )
    ans = []
    for a, b in intervals:
        if ans and a <= ans[-1][1]:
            ans[-1][1] = max(ans[-1][1], b)
        else:
            ans.append([a, b])
    return sum((b - a for a, b in ans), F(0)), [[str(a), str(b)] for a, b in ans]


def phi(n):
    result = n
    p = 2
    remaining = n
    while p * p <= remaining:
        if remaining % p == 0:
            result = result // p * (p - 1)
            while remaining % p == 0:
                remaining //= p
        p += 1
    if remaining > 1:
        result = result // remaining * (remaining - 1)
    return result


def main():
    spec = json.loads(Path(sys.argv[1]).read_text())
    out = Path(sys.argv[2])
    rows = []
    atoms = 0
    certificate = None
    for R, K in spec["cases"]:
        cs = reduced(R, K)
        area, intervals = union(cs)
        naive, _ = union([v for v in cs if v[1] >= R])
        # Diagnostic endpoint-count metadata only; union measure uses merging above.
        endpoints = {F(0), F(1)}
        for q in range(R, K + 1):
            for a in range(q + 1):
                endpoints |= {max(F(0), F(a, q) - F(1, q**3)), min(F(1), F(a, q) + F(1, q**3))}
        atoms += len(endpoints) - 1
        B = C = None
        if max(6, 2 * R - 2) <= K:
            B = 2 * (
                F(1, K) - F(1, 8 * (K // 2 + 1)) - F(1, 27 * (K // 3 + 1)) + F(1, 216 * (K // 6))
            )
            C = F(0)
            for a in range(K + 1, K + 7):
                weight = (F(1, 2) if a % 2 == 0 else F(1)) * (F(2, 3) if a % 3 == 0 else F(1))
                C += weight / F(3 * (a - 3))
            assert B > 0 and C > 0
        rows.append(
            dict(
                R=R,
                K=K,
                area=str(area),
                reduced_area=str(area),
                naive_primitive_area=str(naive),
                old_bound=str(min(F(1), area + F(2, K))),
                new_remainder=str(B) if B is not None else None,
                residue_remainder=str(C) if C is not None else None,
                new_bound=str(min(F(1), area + B)) if B is not None else None,
            )
        )
        if spec["featured"] == [R, K]:
            certificate = dict(reduced_centers=cs, merged_intervals=intervals)
            assert area + B < F(spec["threshold"]) < area + F(2, K) and C <= B
        if (R, K) == (4, 4):
            assert area == F(1, 8) and naive == F(1, 16)
    phi_rows = []
    for q in spec["totient_denominators"]:
        w = (F(1, 2) if q % 2 == 0 else F(1)) * (F(2, 3) if q % 3 == 0 else F(1))
        assert F(phi(q), q) <= w
        phi_rows.append([q, phi(q), str(w)])
    table = dict(cases=rows, totients=phi_rows)
    (out.parent / "theory-table.json").write_bytes(encode(table))
    summary = dict(
        cases=len(rows),
        endpoint_atoms=atoms,
        totient_cases=len(phi_rows),
        boundary_controls=7,
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
    out.write_bytes(encode(dict(summary=summary, certificates=certificate)))
    print(
        json.dumps(
            dict(
                cases=len(rows),
                featured=summary["featured"],
                reduced_centers=len(certificate["reduced_centers"]),
                merged_intervals=len(certificate["merged_intervals"]),
            )
        )
    )


if __name__ == "__main__":
    main()
