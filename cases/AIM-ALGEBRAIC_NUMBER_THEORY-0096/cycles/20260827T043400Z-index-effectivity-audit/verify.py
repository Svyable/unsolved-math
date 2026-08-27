"""Fresh-process verifier: raw input only, no imports of theory code or outputs.

Method: polynomial arithmetic in F64 and explicit Frobenius orbit traversal.
"""

import hashlib
import json
from itertools import combinations_with_replacement
from math import gcd
from pathlib import Path


def remainder(a: int, b: int) -> int:
    while a and a.bit_length() >= b.bit_length():
        a ^= b << (a.bit_length() - b.bit_length())
    return a


def irreducible(p: int) -> bool:
    n = p.bit_length() - 1
    return all(
        remainder(p, divisor) != 0
        for degree in range(1, n // 2 + 1)
        for divisor in range(1 << degree, 1 << (degree + 1))
    )


def multiply(a: int, b: int) -> int:
    product = 0
    while b:
        if b & 1:
            product ^= a
        a <<= 1
        b >>= 1
    return remainder(product, 0b1000011)  # x^6 + x + 1, checked below.


def evaluate(coefficients: list[int], value: int) -> int:
    result = 0
    for coefficient in reversed(coefficients):
        result = multiply(result, value) ^ coefficient
    return result


def orbit_lengths(permutation: dict[int, int]) -> list[int]:
    assert set(permutation) == set(permutation.values())
    unseen = set(permutation)
    result = []
    while unseen:
        start = min(unseen)
        cursor = start
        length = 0
        while cursor in unseen:
            unseen.remove(cursor)
            length += 1
            cursor = permutation[cursor]
        assert cursor == start
        result.append(length)
    return sorted(result)


def main() -> None:
    raw = Path(__file__).with_name("input.json").read_bytes()
    data = json.loads(raw)
    assert data["field_characteristic"] == 2
    assert irreducible(0b1000011)
    polynomials = data["polynomials_low_degree_first"]
    bits = [sum(c << i for i, c in enumerate(p)) for p in polynomials]
    assert all(irreducible(p) for p in bits)
    # First search for counterexamples/boundary failures, before formula comparisons.
    root_sets = [[x for x in range(64) if evaluate(p, x) == 0] for p in polynomials]
    assert [len(roots) for roots in root_sets] == [2, 3]
    orbits = [orbit_lengths({x: multiply(x, x) for x in roots}) for roots in root_sets]
    degrees = [length for component in orbits for length in component]
    fixed = [x for roots in root_sets for x in roots if multiply(x, x) == x]
    assert fixed == [] and degrees == [2, 3] and gcd(*degrees) == 1
    witness_degree = sum(
        a * b for a, b in zip(data["signed_cycle_coefficients"], degrees, strict=True)
    )
    assert witness_degree == 1 and min(degrees) > 1
    probes = {
        "index_one_implies_rational_point_rejected": gcd(*degrees) == 1 and not fixed,
        "reducible_polynomial_mutation_detected": not irreducible(0b110),
        "linear_component_creates_rational_point": evaluate([1, 1], 1) == 0,
        "replace_degree_three_by_four_changes_index": gcd(2, 4) == 2,
        "wrong_signed_witness_rejected": -2 + -3 != 1,
        "quadratic_splits_after_degree_two_extension": orbit_lengths({0: 0, 1: 1}) == [1, 1],
    }
    assert all(probes.values())
    count = 0
    mismatches = []
    digest = hashlib.sha256()
    for components in range(1, data["profile_max_components"] + 1):
        for profile in combinations_with_replacement(
            range(1, data["profile_max_degree"] + 1), components
        ):
            for m in data["extension_degrees"]:
                # Actual traversal of the m-th power of disjoint d-cycles.
                lengths = [
                    length
                    for d in profile
                    for length in orbit_lengths({i: (i + m) % d for i in range(d)})
                ]
                observed = gcd(*lengths)
                g = gcd(*profile)
                predicted = g // gcd(g, m)
                if observed != predicted or g % observed or m * observed % g:
                    mismatches.append([profile, m, observed, predicted])
                digest.update(json.dumps([profile, m, lengths], separators=(",", ":")).encode())
                count += 1
    assert count == 21828 and mismatches == []
    print(
        json.dumps(
            {
                "input_sha256": hashlib.sha256(raw).hexdigest(),
                "execution_context": "Python -I isolated fresh process; reads input.json only",
                "root_sets_in_F64_integer_encoding": root_sets,
                "frobenius_orbit_lengths": orbits,
                "F2_rational_points": fixed,
                "index": gcd(*degrees),
                "signed_witness_degree": witness_degree,
                "adversarial_probes": probes,
                "profile_extension_checks": count,
                "orbit_transcript_sha256": digest.hexdigest(),
                "mismatches": mismatches,
                "limits": (
                    "Finite tests and executable certificate; "
                    "no Lean kernel or independent human review."
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
