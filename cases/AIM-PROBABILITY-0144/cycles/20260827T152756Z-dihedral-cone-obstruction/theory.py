"""Phi-ring reflection BFS and direct antichain certificate construction."""

import json
from fractions import Fraction
from itertools import combinations, permutations
from pathlib import Path


def plus(x, y):
    return (x[0] + y[0], x[1] + y[1])


def minus(x):
    return (-x[0], -x[1])


def times(x, y):
    return (x[0] * y[0] + x[1] * y[1], x[0] * y[1] + x[1] * y[0] + x[1] * y[1])


def sign(x):
    a, b = x
    if not b:
        return (a > 0) - (a < 0)
    lo, hi = Fraction(1), Fraction(2)
    while True:
        low, high = sorted([a + b * lo, a + b * hi])
        if low > 0:
            return 1
        if high < 0:
            return -1
        mid = (lo + hi) / 2
        if mid * mid - mid - 1 < 0:
            lo = mid
        else:
            hi = mid


def reflection(v, i):
    a, b = v
    if i == 0:
        return (plus(minus(a), times((0, 1), b)), b)
    return (a, plus(minus(b), times((0, 1), a)))


def profile(n, edges):
    antichains = []
    polynomial = {}
    for k in range(n + 1):
        for subset in combinations(range(n), k):
            if any((a, b) in edges or (b, a) in edges for a, b in combinations(subset, 2)):
                continue
            mask = sum(1 << a for a in subset)
            antichains.append(mask)
            key = f"{sum(a in (0, 1) for a in subset)},{k}"
            polynomial[key] = polynomial.get(key, 0) + 1
    transition = {}
    for mask in antichains:
        ideal = {
            v
            for v in range(n)
            if mask >> v & 1 or any(mask >> w & 1 and (v, w) in edges for w in range(n))
        }
        complement = set(range(n)) - ideal
        minimal = {v for v in complement if not any((w, v) in edges for w in complement)}
        transition[mask] = sum(1 << v for v in minimal)
    assert set(transition) == set(transition.values())
    cycles, visited = [], set()
    for start in sorted(antichains):
        if start in visited:
            continue
        cycle, v = [], start
        while v not in visited:
            visited.add(v)
            cycle.append(v)
            v = transition[v]
        assert v == start
        cycles.append(cycle)
    return {
        "relations": [list(e) for e in sorted(edges)],
        "H": polynomial,
        "antichains": sorted(antichains),
        "orbits": cycles,
        "orbit_lengths": sorted(map(len, cycles)),
    }


def chain_order(n, order):
    return {(a, b) for a in [0, 1] for b in order} | {
        (order[i], order[j]) for i in range(n - 2) for j in range(i + 1, n - 2)
    }


def main():
    spec = json.loads(Path("input.json").read_text())
    roots = [tuple(tuple(c) for c in r) for r in spec["positive_roots"]]
    full, todo = set(roots[:2]), list(roots[:2])
    while todo:
        v = todo.pop()
        for i in [0, 1]:
            r = reflection(v, i)
            if r not in full:
                full.add(r)
                todo.append(r)
        assert len(full) <= 10
    assert {v for v in full if all(sign(c) >= 0 for c in v)} == set(roots)
    cone = {
        (i, j)
        for i, u in enumerate(roots)
        for j, v in enumerate(roots)
        if i != j and all(sign(plus(y, minus(x))) >= 0 for x, y in zip(u, v, strict=True))
    }
    v, period = roots[0], 0
    while True:
        v = reflection(reflection(v, 1), 0)
        period += 1
        if v == roots[0]:
            break
        assert period <= 5
    matching = {
        str(n): sorted(
            [
                [list(e) for e in sorted(chain_order(n, order))]
                for order in permutations(range(2, n))
            ]
        )
        for n in spec["census_m"]
    }
    extensions = [set(map(tuple, rel)) for rel in matching["5"] if cone <= set(map(tuple, rel))]
    minimal = [e for e in extensions if not any(cone <= other < e for other in extensions)]
    core = {
        "root_count": len(full),
        "positive_root_count": len(roots),
        "rotation_order": period,
        "cone": profile(5, cone),
        "extensions": sorted([profile(5, e) for e in minimal], key=lambda p: p["relations"]),
        "family": {str(n): profile(n, chain_order(n, list(range(2, n)))) for n in spec["family_m"]},
        "matching_orders": matching,
    }
    print(json.dumps({"core": core}, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
