"""Cycle-decomposition count and constructive regular cyclic-factor audit."""

import hashlib
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path


def cycles_of(permutation):
    unseen = set(range(len(permutation)))
    cycles = []
    while unseen:
        start = min(unseen)
        orbit = []
        point = start
        while point in unseen:
            unseen.remove(point)
            orbit.append(point)
            point = permutation[point]
        assert point == start
        cycles.append(orbit)
    return cycles


def count_and_map(permutation, modulus):
    cycles = cycles_of(permutation)
    if any(len(orbit) % modulus for orbit in cycles):
        return 0, None
    values = [0] * len(permutation)
    for orbit in cycles:
        for index, point in enumerate(orbit):
            values[point] = index % modulus
    return modulus ** len(cycles), values


def main():
    root = Path(__file__).resolve().parent
    config = json.loads((root / "input.json").read_text())
    digest = hashlib.sha256()
    systems = positive = false_positive_orders = constructed = 0
    for n in range(config["permutations_max_n"] + 1):
        for permutation in itertools.permutations(range(n)):
            cycles = cycles_of(permutation)
            order = math.lcm(*(len(orbit) for orbit in cycles))
            for modulus in config["moduli"]:
                count, values = count_and_map(permutation, modulus)
                onto = count if n else 0
                systems += 1
                positive += bool(onto)
                false_positive_orders += bool(n and order % modulus == 0 and not count)
                if values is not None:
                    assert all(
                        values[target] == (values[source] + 1) % modulus
                        for source, target in enumerate(permutation)
                    )
                    assert not n or set(values) == set(range(modulus))
                    constructed += 1
                row = [n, list(permutation), modulus, count, onto]
                digest.update((json.dumps(row, separators=(",", ":")) + "\n").encode())
    weighting = []
    for k in config["weighting_parameters"]:
        length = 2 * k * k
        permutation = (*range(1, length), 0, *range(length, length + k))
        cycles = cycles_of(permutation)
        good_lengths = [len(orbit) for orbit in cycles if len(orbit) % 2 == 0]
        weighting.append(
            {
                "k": k,
                "states": len(permutation),
                "orbits": len(cycles),
                "state_fraction": str(Fraction(sum(good_lengths), len(permutation))),
                "orbit_fraction": str(Fraction(len(good_lengths), len(cycles))),
                "regular_factor_maps": count_and_map(permutation, 2)[0],
            }
        )
    result = {
        "method": "cycle decomposition, exact period divisibility, and phase construction",
        "systems": systems,
        "positive_surjective_systems": positive,
        "representative_equivariant_maps_constructed": constructed,
        "table_sha256": digest.hexdigest(),
        "order_shortcut_false_positives": false_positive_orders,
        "counterexample": {
            "permutation": [1, 0, 2],
            "N": 2,
            "cycle_lengths": [2, 1],
            "source_order": 2,
            "equivariant_maps": 0,
            "contradiction": "f(2)=f(2)+1 mod 2",
        },
        "weighting": weighting,
        "claim_boundary": (
            "Elementary finite-permutation audit, not a new ASM/PL/birational result "
            "or kernel-accepted theorem."
        ),
    }
    (root / "theory-output.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
