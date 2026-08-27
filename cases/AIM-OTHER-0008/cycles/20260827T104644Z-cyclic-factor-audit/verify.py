"""Independent modular-constraint check; does not import/read theory artifacts."""

import hashlib
import itertools
import json
from collections import deque
from fractions import Fraction
from pathlib import Path


def solve(permutation, modulus):
    """Propagate difference constraints on an undirected labelled graph."""
    if modulus < 1 or sorted(permutation) != list(range(len(permutation))):
        raise ValueError("positive modulus and permutation required")
    adjacency = [[] for _ in permutation]
    for source, target in enumerate(permutation):
        adjacency[source].append((target, 1))
        adjacency[target].append((source, -1))
    colors = {}
    components = []
    for root in range(len(permutation)):
        if root in colors:
            continue
        colors[root] = 0
        pending = deque([root])
        vertices = []
        consistent = True
        while pending:
            source = pending.popleft()
            vertices.append(source)
            for target, difference in adjacency[source]:
                wanted = (colors[source] + difference) % modulus
                if target in colors:
                    if colors[target] != wanted:
                        consistent = False
                else:
                    colors[target] = wanted
                    pending.append(target)
        components.append((len(vertices), consistent))
    count = 1
    for _, consistent in components:
        count *= modulus if consistent else 0
    return count, components


def valid_map(permutation, modulus, values):
    return (
        len(values) == len(permutation)
        and all(type(value) is int and 0 <= value < modulus for value in values)
        and all(
            values[target] == (values[source] + 1) % modulus
            for source, target in enumerate(permutation)
        )
    )


def brute_count(permutation, modulus):
    count = 0
    onto = 0
    tested = 0
    for values in itertools.product(range(modulus), repeat=len(permutation)):
        tested += 1
        if valid_map(permutation, modulus, values):
            count += 1
            onto += len(set(values)) == modulus
    return count, onto, tested


def main():
    root = Path(__file__).resolve().parent
    config = json.loads((root / "input.json").read_text())
    # Counterexample and boundaries precede the exhaustive confirmation sweep.
    counterexample = (1, 0, 2)
    assert brute_count(counterexample, 2) == (0, 0, 8)
    assert all(counterexample[counterexample[x]] == x for x in range(3))
    boundaries = [
        ((), 1, 1),
        ((), 2, 1),
        ((0,), 1, 1),
        ((0,), 2, 0),
        ((1, 0), 2, 2),
        ((1, 2, 0), 2, 0),
        ((1, 0, 3, 2), 2, 4),
        ((1, 2, 3, 4, 5, 0), 3, 3),
        ((1, 2, 3, 4, 5, 0), 4, 0),
    ]
    for permutation, modulus, expected in boundaries:
        assert solve(permutation, modulus)[0] == expected
    assert brute_count((), 2) == (1, 0, 1)  # Empty map is not a surjection.
    controls = []
    for name, permutation, modulus, values in [
        ("changed_color", (1, 2, 3, 0), 2, (0, 0, 0, 1)),
        ("constant_color", (1, 2, 3, 0), 2, (0, 0, 0, 0)),
        ("out_of_range", (1, 0), 2, (0, 3)),
        ("missing_value", (1, 0), 2, (0,)),
    ]:
        assert not valid_map(permutation, modulus, values)
        controls.append(name)
    for name, permutation, modulus in [
        ("not_bijective", (0, 0), 2),
        ("bad_vertex", (2, 0), 2),
        ("zero_modulus", (0,), 0),
    ]:
        try:
            solve(permutation, modulus)
        except ValueError:
            controls.append(name)
        else:
            raise AssertionError(name)
    assert valid_map((1, 2, 3, 0), 2, (0, 1, 0, 1))
    assert valid_map((1, 2, 3, 4, 5, 0), 3, (0, 1, 2, 0, 1, 2))
    digest = hashlib.sha256()
    systems = positive = brute_systems = assignments = false_positive_orders = 0
    for n in range(config["permutations_max_n"] + 1):
        for permutation in itertools.permutations(range(n)):
            # Compute global order by repeated composition, not cycle lengths/lcm.
            power = tuple(permutation)
            order = 1
            while power != tuple(range(n)):
                power = tuple(permutation[x] for x in power)
                order += 1
            for modulus in config["moduli"]:
                count, _ = solve(permutation, modulus)
                onto = count if n else 0
                row = [n, list(permutation), modulus, count, onto]
                digest.update((json.dumps(row, separators=(",", ":")) + "\n").encode())
                systems += 1
                positive += bool(onto)
                false_positive_orders += bool(n and order % modulus == 0 and not count)
                if n <= config["brute_force_max_n"] and modulus in config["brute_force_moduli"]:
                    actual, actual_onto, checked = brute_count(permutation, modulus)
                    assert (count, onto) == (actual, actual_onto)
                    brute_systems += 1
                    assignments += checked
    weighting = []
    for k in config["weighting_parameters"]:
        length = 2 * k * k
        permutation = (*range(1, length), 0, *range(length, length + k))
        count, components = solve(permutation, 2)
        states = sum(size for size, good in components if good)
        good_orbits = sum(good for _, good in components)
        weighting.append(
            {
                "k": k,
                "states": len(permutation),
                "orbits": len(components),
                "state_fraction": str(Fraction(states, len(permutation))),
                "orbit_fraction": str(Fraction(good_orbits, len(components))),
                "regular_factor_maps": count,
            }
        )
    result = {
        "method": "modular graph constraints plus direct exhaustive label assignments",
        "systems": systems,
        "positive_surjective_systems": positive,
        "table_sha256": digest.hexdigest(),
        "brute_systems": brute_systems,
        "label_assignments": assignments,
        "mismatches": 0,
        "order_shortcut_false_positives": false_positive_orders,
        "boundaries_checked": len(boundaries),
        "adversarial_controls_rejected": controls,
        "counterexample": {
            "permutation": list(counterexample),
            "N": 2,
            "source_order": 2,
            "equivariant_maps": 0,
            "label_assignments_exhausted": 8,
        },
        "weighting": weighting,
        "independence": (
            "Fresh isolated interpreter; raw constraints only, no theory imports or outputs. "
            "Same-assistant code authorship; no independent human/model or kernel review."
        ),
    }
    (root / "verification-output.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
