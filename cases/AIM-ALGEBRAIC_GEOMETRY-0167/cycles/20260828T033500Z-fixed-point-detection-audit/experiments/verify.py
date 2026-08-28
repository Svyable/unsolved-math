"""Independent finite-action checker: reconstruct before reading any certificate."""

import argparse
import copy
import hashlib
import itertools
import json
from pathlib import Path


def encoded(data):
    return (json.dumps(data, sort_keys=True, indent=2) + "\n").encode()


def action(name):
    if name.startswith("C"):
        n = int(name[1:])
        perms = [tuple((x + a) % n for x in range(n)) for a in range(n)]
    elif name == "S3":
        perms = list(itertools.permutations(range(3)))
    else:
        perms = [
            tuple((a + (-1) ** b * x) % 4 for x in range(4)) for a in range(4) for b in range(2)
        ]
    table = [[perms.index(tuple(p[q[x]] for x in range(len(p)))) for q in perms] for p in perms]
    return table


def mask(s):
    return sum(1 << x for x in s)


def subgroups(t, cyclic):
    n = len(t)
    if cyclic:
        groups = set()
        for g in range(n):
            s, x = {0}, g
            while x not in s:
                s.add(x)
                x = t[x][g]
            groups.add(frozenset(s))
    else:
        groups = set()
        for bits in range(1, 1 << n, 2):
            s = {i for i in range(n) if bits >> i & 1}
            if all(t[a][b] in s for a in s for b in s):
                groups.add(frozenset(s))
    return sorted(groups, key=mask)


def cosets(t, s):
    return sorted({frozenset(t[g][x] for x in s) for g in range(len(t))}, key=min)


def normal(t, s):
    return all({t[g][x] for x in s} == {t[x][g] for x in s} for g in range(len(t)))


def closure(t, s):
    s = set(s)
    while True:
        more = {t[a][b] for a in s for b in s}
        if more <= s:
            return s
        s |= more


def reconstruct(spec):
    # Counterexample and boundary search FIRST, before the broad census.
    c2 = action("C2")
    free, point = cosets(c2, {0}), cosets(c2, {0, 1})
    degrees = []
    for h in [{0}, {0, 1}]:

        def fixed(orbit, subgroup=h):
            return sum(all({c2[g][x] for x in c} == set(c) for g in subgroup) for c in orbit)

        degrees.append(3 * fixed(point) - fixed(free))
    assert degrees == [1, 3]
    s3 = action("S3")
    k, ell = closure(s3, {0, 1}), closure(s3, {0, 2})
    product = {s3[a][b] for a in ell for b in k}
    assert len(product) == 4 and len(closure(s3, product)) == 6
    controls = dict(
        counterexample_marks=degrees,
        identity_marks=[1, 1],
        zero_marks=[0, 0],
        negative_unit_marks=[-1, -1],
        top_test_only_marks=[0, 2],
        finite_free_orbit_marks=[2, 0],
        nonnormal_product_size=len(product),
        nonnormal_generated_size=len(closure(s3, product)),
    )
    transport, inventories = [], []
    names = [f"C{n}" for n in spec["cyclic_group_orders"]] + spec["nonabelian_groups"]
    for name in names:
        t = action(name)
        sg = subgroups(t, name.startswith("C"))
        normals = [s for s in sg if normal(t, s)]
        inventories.append(
            dict(group=name, subgroups=[mask(s) for s in sg], normals=[mask(s) for s in normals])
        )
        for nn, u, ll in itertools.product(normals, normals, sg):
            kk = nn & u
            hh = closure(t, set(ll) | kk)
            partition = cosets(t, u)
            image_l = [min(c) for c in partition if c & ll]
            image_h = [min(c) for c in partition if c & hh]
            assert image_h == image_l and kk <= hh & nn
            if len(kk) > 1:
                assert len(hh & nn) > 1
            transport.append(
                dict(
                    group=name,
                    N=mask(nn),
                    U=mask(u),
                    L=mask(ll),
                    K=mask(kk),
                    H=mask(hh),
                    image=image_l,
                    H_intersect_N=mask(hh & nn),
                    omitted_thickening_fails=len(kk) > 1 and len(ll & nn) == 1,
                )
            )
    matrices, marks = [], []
    for n in spec["mark_group_orders"]:
        t = action(f"C{n}")
        sg = sorted(subgroups(t, True), key=len)
        matrix = []
        for h in sg:
            matrix.append(
                [
                    sum(all({t[g][x] for x in c} == set(c) for g in h) for c in cosets(t, s))
                    for s in sg
                ]
            )
        matrices.append(dict(order=n, subgroup_orders=[len(s) for s in sg], matrix=matrix))
        for coeff in itertools.product(spec["mark_coefficients"], repeat=len(sg)):
            values = [sum(a * b for a, b in zip(row, coeff, strict=True)) for row in matrix]
            marks.append(
                dict(
                    order=n,
                    coeff=list(coeff),
                    marks=values,
                    underlying_unit=abs(values[0]) == 1,
                    all_units=all(abs(v) == 1 for v in values),
                )
            )
    summary = dict(
        groups=len(names),
        transport_cases=len(transport),
        nontrivial_kernel_cases=sum(r["K"] != 1 for r in transport),
        omitted_thickening_failures=sum(r["omitted_thickening_fails"] for r in transport),
        mark_cases=len(marks),
        underlying_false_positives=sum(r["underlying_unit"] and not r["all_units"] for r in marks),
    )
    return dict(
        controls=controls,
        inventories=inventories,
        transport=transport,
        mark_matrices=matrices,
        mark_cases=marks,
        summary=summary,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--certificate", type=Path)
    args = parser.parse_args()
    expected = reconstruct(json.loads(args.input.read_text()))
    result = expected
    if args.certificate:
        supplied = json.loads(args.certificate.read_text())
        assert supplied == expected, (
            "certificate differs from independently reconstructed action data"
        )
        mutations = []
        for index in range(7):
            bad = copy.deepcopy(supplied)
            if index == 0:
                bad["controls"]["counterexample_marks"][1] = 1
            elif index == 1:
                bad["transport"][0]["image"] = [999]
            elif index == 2:
                row = next(r for r in bad["transport"] if r["omitted_thickening_fails"])
                row["H"] = row["L"]
            elif index == 3:
                bad["mark_matrices"][0]["matrix"][0][0] = 1
            elif index == 4:
                bad["mark_cases"][0]["marks"][0] += 1
            elif index == 5:
                bad["transport"].pop()
            else:
                bad["inventories"][0]["normals"] = []
            assert bad != expected
            mutations.append(dict(control=index + 1, rejected=True))
        result = dict(
            summary=expected["summary"],
            controls=expected["controls"],
            reconstructed_sha256=hashlib.sha256(encoded(expected)).hexdigest(),
            certificate_matches=True,
            corruptions=mutations,
        )
    args.output.write_bytes(encoded(result))
    print(json.dumps(expected["summary"], sort_keys=True))


if __name__ == "__main__":
    main()
