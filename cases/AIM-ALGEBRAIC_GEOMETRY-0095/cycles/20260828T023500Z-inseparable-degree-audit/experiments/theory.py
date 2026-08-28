"""Invariant factors for monomial maps; no quotient graph or congruence search."""

import argparse
import json
from collections import Counter
from math import gcd, lcm
from pathlib import Path


def row(p,a,b,c,rs):
    d = a*c
    d1 = gcd(a,b,c)
    d2 = d//d1
    assert d2 % d1 == 0
    ins, sep = 1, d
    while sep % p == 0:
        ins *= p
        sep //= p
    rank = 2 if d % p else (1 if any(x % p for x in (a,b,c)) else 0)
    orders = Counter(lcm(d1//gcd(i,d1),d2//gcd(j,d2))
                     for i in range(d1) for j in range(d2))
    kernels = [gcd(d1,p**r-1)*gcd(d2,p**r-1) for r in rs]
    return dict(p=p,a=a,b=b,c=c,total_degree=d,separable_degree=sep,
                inseparable_degree=ins,jacobian_rank=rank,
                rational_kernel_counts=kernels,
                quotient_order_histogram=[list(x) for x in sorted(orders.items())])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    args = parser.parse_args()
    spec = json.loads(Path(args.input).read_text())
    rows = [row(p,a,b,c,spec["field_extension_degrees"])
            for p in spec["primes"] for a in spec["a"]
            for b in spec["b"] for c in spec["c"]]
    Path(args.output).write_text(json.dumps(dict(rows=rows),sort_keys=True,indent=2)+"\n")
    print(json.dumps(dict(cases=len(rows))))


if __name__ == "__main__":
    main()
