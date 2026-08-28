"""Independent finite quotient and congruence enumeration, counterexamples first."""

import argparse
import copy
import json
from collections import Counter
from functools import cache
from pathlib import Path


@cache
def quotient(a, b, c):
    modulus = a*c
    subgroup, todo = {(0, 0)}, [(0, 0)]
    while todo:
        x, y = todo.pop()
        for dx, dy in ((a, b), (0, c)):
            z = ((x+dx) % modulus, (y+dy) % modulus)
            if z not in subgroup:
                subgroup.add(z)
                todo.append(z)
    labels, reps = {}, []
    for x in range(modulus):
        for y in range(modulus):
            if (x, y) in labels:
                continue
            label = len(reps)
            reps.append((x, y))
            for dx, dy in subgroup:
                z = ((x+dx) % modulus, (y+dy) % modulus)
                assert z not in labels
                labels[z] = label
    orders = []
    for x, y in reps:
        order = next(n for n in range(1, modulus+1)
                     if labels[(n*x % modulus, n*y % modulus)] == 0)
        orders.append(order)
    return len(reps), sorted(Counter(orders).items())


def rank(a, b, c, p):
    m = [[a % p, b % p], [0, c % p]]
    row = 0
    for col in range(2):
        pivot = next((i for i in range(row, 2) if m[i][col]), None)
        if pivot is None:
            continue
        m[row], m[pivot] = m[pivot], m[row]
        inv = next(x for x in range(1, p) if x*m[row][col] % p == 1)
        m[row] = [x*inv % p for x in m[row]]
        for i in range(2):
            if i != row:
                scale = m[i][col]
                m[i] = [(m[i][j]-scale*m[row][j]) % p for j in range(2)]
        row += 1
    return row


def row(p, a, b, c, rs):
    degree, histogram = quotient(a, b, c)
    sep, ins = 0, 0
    for order, count in histogram:
        if order % p:
            sep += count
        reduced = order
        while reduced % p == 0:
            reduced //= p
        if reduced == 1:
            ins += count
    kernels = []
    for r in rs:
        n = p**r-1
        count = sum((a*x+b*y) % n == 0 and c*y % n == 0
                    for x in range(n) for y in range(n))
        kernels.append(count)
    assert sep*ins == degree
    return dict(p=p, a=a, b=b, c=c, total_degree=degree,
                separable_degree=sep, inseparable_degree=ins,
                jacobian_rank=rank(a,b,c,p), rational_kernel_counts=kernels,
                quotient_order_histogram=[list(x) for x in histogram])


def boundary():
    first = row(2, 2, 0, 1, [1,2])
    second = row(2, 4, 0, 1, [1,2])
    assert first["jacobian_rank"] == second["jacobian_rank"] == 1
    assert first["inseparable_degree"] == 2
    assert second["inseparable_degree"] == 4
    assert second["rational_kernel_counts"] == [1,1]
    unit = row(2, 1, 0, 1, [1,2])
    assert unit["total_degree"] == 1 and unit["jacobian_rank"] == 2
    shear = row(2, 2, 1, 2, [1,2])
    assert shear["inseparable_degree"] == 4 and shear["jacobian_rank"] == 1
    prime_to_p = row(2, 3, 0, 1, [1,2])
    assert prime_to_p["separable_degree"] == 3
    assert prime_to_p["rational_kernel_counts"] == [1,3]
    return dict(same_rank_different_degree=[first,second], unit=unit,
                off_diagonal=shear, finite_field_extension=prime_to_p)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("--certificate")
    args = parser.parse_args()
    spec = json.loads(Path(args.input).read_text())
    controls = boundary()
    rows = [row(p,a,b,c,spec["field_extension_degrees"])
            for p in spec["primes"] for a in spec["a"]
            for b in spec["b"] for c in spec["c"]]
    expected = dict(rows=rows)
    result = dict(boundary=controls, expected=expected, cases=len(rows),
                  rank_shortcut_failures=sum(x["inseparable_degree"] !=
                                            x["p"]**(2-x["jacobian_rank"]) for x in rows),
                  rational_count_shortfalls=sum(k < x["total_degree"] for x in rows
                                                for k in x["rational_kernel_counts"]))
    if args.certificate:
        supplied = json.loads(Path(args.certificate).read_text())
        assert supplied == expected
        mutations = []
        for field in ("total_degree","separable_degree","inseparable_degree","jacobian_rank"):
            bad = copy.deepcopy(supplied)
            bad["rows"][7][field] += 1
            mutations.append(bad)
        for field in ("rational_kernel_counts","quotient_order_histogram"):
            bad = copy.deepcopy(supplied)
            bad["rows"][7][field].pop()
            mutations.append(bad)
        bad = copy.deepcopy(supplied)
        bad["rows"].pop()
        mutations.append(bad)
        assert all(x != expected for x in mutations)
        result["mutations_rejected"] = len(mutations)
        result["certificate_matches"] = True
    Path(args.output).write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k not in ("expected","boundary")}))


if __name__ == "__main__":
    main()
