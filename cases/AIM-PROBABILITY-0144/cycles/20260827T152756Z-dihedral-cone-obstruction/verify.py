"""Independent radical/ideal/census verifier; no theory imports."""

import copy
import json
import sys
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path


def add(x, y):
    return (x[0] + y[0], x[1] + y[1])


def neg(x):
    return (-x[0], -x[1])


def mul(x, y):
    return (x[0] * y[0] + 5 * x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def sign(x):
    a, b = x
    if not b:
        return (a > 0) - (a < 0)
    if not a or (a > 0) == (b > 0):
        return (b > 0) - (b < 0)
    comparison = (a * a > 5 * b * b) - (a * a < 5 * b * b)
    return comparison if a > 0 else -comparison


PHI = (F(1, 2), F(1, 2))


def reflect(v, i):
    a, b = v
    return (add(neg(a), mul(PHI, b)), b) if i == 0 else (a, add(neg(b), mul(PHI, a)))


def rotate(v):
    return reflect(reflect(v, 1), 0)


def predecessors(n, edges):
    pred = [0] * n
    for a, b in edges:
        if a == b:
            raise ValueError("strict order is irreflexive")
        pred[b] |= 1 << a
    if any(pred[a] & (1 << b) for a, b in edges):
        raise ValueError("cycle")
    if any(pred[a] & ~pred[b] for a, b in edges):
        raise ValueError("missing transitive relation")
    return pred


def ideals(n, pred):
    return [
        mask
        for mask in range(1 << n)
        if all(not (mask >> v & 1) or pred[v] & mask == pred[v] for v in range(n))
    ]


def profile(n, edges):
    pred = predecessors(n, edges)
    successor = [0] * n
    for a, b in edges:
        successor[a] |= 1 << b
    mapping = {}
    polynomial = {}
    for ideal in ideals(n, pred):
        maximal = sum(1 << v for v in range(n) if ideal >> v & 1 and not successor[v] & ideal)
        minimal_complement = sum(
            1 << v for v in range(n) if not ideal >> v & 1 and pred[v] & ideal == pred[v]
        )
        mapping[maximal] = minimal_complement
        key = f"{(maximal & 3).bit_count()},{maximal.bit_count()}"
        polynomial[key] = polynomial.get(key, 0) + 1
    assert len(mapping) == len(set(mapping.values())) and set(mapping) == set(mapping.values())
    cycles = []
    unseen = set(mapping)
    while unseen:
        start = min(unseen)
        cycle, v = [], start
        while v not in cycle:
            cycle.append(v)
            unseen.remove(v)
            v = mapping[v]
        assert v == start
        cycles.append(cycle)
    return {
        "relations": [list(ab) for ab in sorted(edges)],
        "H": polynomial,
        "antichains": sorted(mapping),
        "orbits": cycles,
        "orbit_lengths": sorted(map(len, cycles)),
    }


def desired(n):
    return {"0,0": 1, "0,1": n - 2, "1,1": 2, "2,2": 1}


def census(n):
    simple_pairs = [(a, b) for a in [0, 1] for b in range(2, n)]
    other_pairs = list(combinations(range(2, n), 2))
    valid, candidates, matches = 0, 0, []
    for bits in range(1 << len(simple_pairs)):
        base = [edge for k, edge in enumerate(simple_pairs) if bits >> k & 1]
        for states in product(range(3), repeat=len(other_pairs)):
            candidates += 1
            edges = base + [
                (a, b) if state == 1 else (b, a)
                for (a, b), state in zip(other_pairs, states, strict=True)
                if state
            ]
            try:
                pred = predecessors(n, edges)
            except ValueError:
                continue
            if any(not pred[v] for v in range(2, n)):
                continue
            valid += 1
            # The H target allows exactly one incomparable pair: the two marked minima.
            # Check by the full ideal-to-antichain enumeration, not that shortcut.
            poly = {}
            for ideal in ideals(n, pred):
                maximal = ideal
                for a, b in edges:
                    if ideal >> b & 1:
                        maximal &= ~(1 << a)
                key = f"{(maximal & 3).bit_count()},{maximal.bit_count()}"
                poly[key] = poly.get(key, 0) + 1
            if poly == desired(n):
                matches.append([list(ab) for ab in sorted(edges)])
    return {
        "m": n,
        "candidate_assignments": candidates,
        "valid_posets": valid,
        "matching_orders": sorted(matches),
    }


def main():
    spec = json.loads(Path("input.json").read_text())
    roots = [tuple((F(a) + F(b, 2), F(b, 2)) for a, b in root) for root in spec["positive_roots"]]
    full = set(roots) | {tuple(neg(x) for x in root) for root in roots}
    v, rotated = roots[0], []
    for _ in range(5):
        rotated.append(v)
        v = rotate(v)
    assert v == roots[0] and len(set(rotated)) == 5
    assert full == set(rotated) | {tuple(neg(x) for x in r) for r in rotated}
    for root in full:
        a, b = root
        norm = add(add(mul(a, a), mul(b, b)), neg(mul(PHI, mul(a, b))))
        assert norm == (1, 0)
        for i in [0, 1]:
            assert reflect(root, i) in full and reflect(reflect(root, i), i) == root
    cone = {
        (i, j)
        for i, u in enumerate(roots)
        for j, v in enumerate(roots)
        if i != j and all(sign(add(y, neg(x))) >= 0 for x, y in zip(u, v, strict=True))
    }
    # Falsification and boundaries BEFORE accepting any abstract model.
    cone_profile = profile(5, cone)
    assert cone_profile["H"] != desired(5)
    assert [2, 3] not in cone_profile["relations"] and [3, 2] not in cone_profile["relations"]
    boundaries = {
        "incomparable_non_simple_pair": True,
        "zero_sign": sign((0, 0)) == 0,
        "negative_radical_sign": sign((2, -1)) < 0,
        "positive_mixed_sign": sign((-2, 1)) > 0,
        "two_simple_roots_minimal": [v for v, p in enumerate(predecessors(5, cone)) if not p]
        == [0, 1],
        "empty_antichain_present": 0 in cone_profile["antichains"],
        "all_roots_not_antichain": 31 not in cone_profile["antichains"],
    }
    for name, bad in [
        ("self_relation_rejected", cone | {(0, 0)}),
        ("reverse_cycle_rejected", cone | {(4, 0)}),
        ("missing_transitivity_rejected", cone - {(0, 4)}),
    ]:
        try:
            predecessors(5, bad)
        except ValueError:
            boundaries[name] = True
    assert len(boundaries) == 10 and all(boundaries.values())
    counts = [census(n) for n in spec["census_m"]]
    matching = {str(row["m"]): row["matching_orders"] for row in counts}
    compatible = [set(map(tuple, rel)) for rel in matching["5"] if cone <= set(map(tuple, rel))]
    minimal = [
        edges for edges in compatible if not any(cone <= other < edges for other in compatible)
    ]
    extension_profiles = sorted([profile(5, e) for e in minimal], key=lambda p: p["relations"])
    family = {}
    for n in spec["family_m"]:
        edges = {(a, b) for a in range(n) for b in range(2, n) if a < b}
        family[str(n)] = profile(n, edges)
        assert family[str(n)]["H"] == desired(n)
    core = {
        "root_count": len(full),
        "positive_root_count": len(roots),
        "rotation_order": len(rotated),
        "cone": cone_profile,
        "extensions": extension_profiles,
        "family": family,
        "matching_orders": matching,
    }
    result = {
        "core": core,
        "boundary_checks": boundaries,
        "census": [{k: v for k, v in row.items() if k != "matching_orders"} for row in counts],
    }
    if len(sys.argv) > 1:
        proposal = json.loads(Path(sys.argv[1]).read_text())["core"]
        assert proposal == core
        mutations = []
        for name in [
            "H_coefficient",
            "orbit_profile",
            "missing_relation",
            "root_count",
            "missing_extension",
            "wrong_marked_count",
            "wrong_family",
        ]:
            bad = copy.deepcopy(proposal)
            if name == "H_coefficient":
                bad["cone"]["H"]["0,2"] = 0
            elif name == "orbit_profile":
                bad["cone"]["orbit_lengths"] = [2, 5]
            elif name == "missing_relation":
                bad["cone"]["relations"].pop()
            elif name == "root_count":
                bad["root_count"] = 9
            elif name == "missing_extension":
                bad["extensions"].pop()
            elif name == "wrong_marked_count":
                bad["cone"]["H"]["1,1"] = 1
            else:
                bad["family"]["3"]["H"]["0,1"] = 2
            assert bad != core
            mutations.append(name)
        result["certificate_accepted"] = True
        result["mutations_rejected"] = mutations
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
