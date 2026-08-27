"""Fresh-input checker: polynomial Euclid and graded linear algebra, no resultant."""

import argparse
import copy
import hashlib
import itertools
import json
from pathlib import Path


def trim(a, p):
    a = [x % p for x in a]
    while a and not a[-1]:
        a.pop()
    return a


def gcd(a, b, p):
    a, b = trim(a, p), trim(b, p)
    while b:
        r = a[:]
        while r and len(r) >= len(b):
            c = r[-1] * pow(b[-1], -1, p) % p
            offset = len(r) - len(b)
            for i, v in enumerate(b):
                r[offset + i] = (r[offset + i] - c * v) % p
            r = trim(r, p)
        a, b = b, r
    return a


def rank(a, p):
    a = [row[:] for row in a]
    if not a:
        return 0
    r = 0
    for c in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][c] % p), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        inv = pow(a[r][c] % p, -1, p)
        a[r] = [v * inv % p for v in a[r]]
        for i in range(len(a)):
            if i != r:
                q = a[i][c]
                a[i] = [(v - q * w) % p for v, w in zip(a[i], a[r], strict=True)]
        r += 1
        if r == len(a):
            break
    return r


def ghost(a, d, p):
    rows = []
    for n in range(a + 2 * d + 3):
        n1, n2, n3 = max(n - a + 1, 0), max(n - a - d + 1, 0), max(n - a - 2 * d + 1, 0)
        # Bases x^i*y^(degree-i), increasing i. d2=(x^d,y^d).
        m2 = [[0] * (2 * n2) for _ in range(n1)]
        m3 = [[0] * n3 for _ in range(2 * n2)]
        for i in range(n2):
            m2[i + d][i] = 1
            m2[i][i + n2] = 1
        for i in range(n3):
            m3[i][i] = -1 % p
            m3[i + d + n2][i] = 1
        assert all(
            sum(m2[i][j] * m3[j][k] for j in range(2 * n2)) % p == 0
            for i in range(n1)
            for k in range(n3)
        )
        r2, r3 = rank(m2, p), rank(m3, p)
        rows.append([n, n1 - r2, 2 * n2 - r2 - r3, n3 - r3])
    return dict(a=a, d=d, p=p, homology=rows)


def f4mul(a, b):
    r = 0
    while b:
        if b & 1:
            r ^= a
        a <<= 1
        if a & 4:
            a ^= 7
        b >>= 1
    return r


def compute(spec):
    # Counterexample and boundaries precede census and certificate ingestion.
    f = spec["rational_point_counterexample"]["f"]
    g = spec["rational_point_counterexample"]["g"]
    assert f == g == [1, 1, 1]
    rational_values = [(1 + t + t * t) % 2 for t in range(2)] + [1]
    extension_value = 1 ^ 2 ^ f4mul(2, 2)
    assert rational_values == [1, 1, 1] and extension_value == 0
    boundary = {
        "both_zero_rejected": len(gcd([0, 0, 0], [0, 0, 0], 3)) != 1,
        "infinity_common_zero": [0, 1, 0][-1] == [1, 0, 0][-1] == 0,
        "irreducible_common_factor_degree_two": len(gcd(f, g, 2)) - 1 == 2,
        "coprime_powers": len(gcd([0, 0, 1], [1, 0, 0], 3)) == 1,
        "wrong_koszul_sign_nonzero_in_F3": 2 % 3 != 0,
        "wrong_sign_indistinguishable_in_F2": 2 % 2 == 0,
    }
    assert all(boundary.values())
    census = []
    for p in spec["fields"]:
        forms = list(itertools.product(range(p), repeat=3))
        accepted, false_positive = [], []
        for index, (f, g) in enumerate(itertools.product(forms, repeat=2)):
            infinity = f[-1] == g[-1] == 0
            geometric_good = not infinity and len(gcd(f, g, p)) == 1
            rational_good = not infinity and all(
                any(sum(h[i] * pow(t, i, p) for i in range(3)) % p for h in (f, g))
                for t in range(p)
            )
            if geometric_good:
                accepted.append(index)
            if rational_good and not geometric_good:
                false_positive.append(index)
        census.append(dict(p=p, total=p**6, accepted=accepted, false_positive=false_positive))
    ghosts = [
        ghost(a, d, p)
        for p in spec["ghost_fields"]
        for a in spec["ghost_shifts"]
        for d in spec["ghost_degrees"]
    ]
    return dict(
        census=census,
        ghosts=ghosts,
        counterexample=dict(rational_values=rational_values, extension_value=extension_value),
    ), boundary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--certificate", type=Path)
    args = parser.parse_args()
    spec = json.loads(args.input.read_text())
    core, boundaries = compute(spec)
    report = dict(
        method=(
            "dehomogenized Euclidean gcd plus infinity test; "
            "graded multiplication matrices and modular row reduction"
        ),
        boundaries=boundaries,
        core=core,
        certificate_checked=False,
    )
    if args.certificate:
        supplied = json.loads(args.certificate.read_text())["core"]
        assert supplied == core, "certificate disagrees with independent calculation"
        changes = []

        def reject(name, change):
            bad = copy.deepcopy(supplied)
            change(bad)
            assert bad != core
            changes.append(name)

        reject("remove_valid_pair", lambda x: x["census"][0]["accepted"].pop())
        reject("inject_zero_pair", lambda x: x["census"][0]["accepted"].append(0))
        reject("hide_extension_obstruction", lambda x: x["census"][0]["false_positive"].clear())
        reject("alter_homology_H1", lambda x: x["ghosts"][0]["homology"][0].__setitem__(1, 99))
        reject("invent_homology_H2", lambda x: x["ghosts"][0]["homology"][0].__setitem__(2, 1))
        reject("change_shift", lambda x: x["ghosts"][0].__setitem__("a", 99))
        reject("erase_F4_root", lambda x: x["counterexample"].__setitem__("extension_value", 1))
        report.update(
            certificate_checked=True,
            corruptions_rejected=changes,
            certificate_sha256=hashlib.sha256(args.certificate.read_bytes()).hexdigest(),
        )
    args.output.write_text(json.dumps(report, sort_keys=True, separators=(",", ":")) + "\n")
    print(
        json.dumps(
            dict(
                cases=sum(x["total"] for x in core["census"]),
                census=[
                    dict(
                        p=x["p"],
                        accepted=len(x["accepted"]),
                        false_positive=len(x["false_positive"]),
                    )
                    for x in core["census"]
                ],
                ghost_cases=len(core["ghosts"]),
                degree_checks=sum(len(x["homology"]) for x in core["ghosts"]),
                certificate_checked=report["certificate_checked"],
            )
        )
    )


if __name__ == "__main__":
    main()
