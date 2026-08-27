"""Exact arithmetic lane. Run from any cwd; stdout is deterministic JSON."""

import hashlib
import json
from itertools import combinations_with_replacement
from math import gcd
from pathlib import Path


def main() -> None:
    source = Path(__file__).with_name("input.json").read_bytes()
    data = json.loads(source)
    polynomials = data["polynomials_low_degree_first"]
    degrees = [len(p) - 1 for p in polynomials]
    roots = [
        [a for a in (0, 1) if sum(c * a**i for i, c in enumerate(p)) % 2 == 0] for p in polynomials
    ]
    assert degrees == [2, 3] and roots == [[], []]
    # A degree-2 or degree-3 polynomial over a field is irreducible iff root-free.
    index = gcd(*degrees)
    signed_degree = sum(
        c * d for c, d in zip(data["signed_cycle_coefficients"], degrees, strict=True)
    )
    assert index == signed_degree == 1
    # For positive d_i, any nonnegative solution of sum n_i d_i = 1 has n_i <= 1.
    effective_degree_one = [[a, b] for a in range(2) for b in range(2) if 2 * a + 3 * b == 1]
    assert effective_degree_one == []
    count = 0
    for n in range(1, data["profile_max_components"] + 1):
        for profile in combinations_with_replacement(range(1, data["profile_max_degree"] + 1), n):
            g = gcd(*profile)
            for m in data["extension_degrees"]:
                base_index = gcd(*(d // gcd(d, m) for d in profile))
                assert base_index == g // gcd(g, m)
                assert g % base_index == 0 and (m * base_index) % g == 0
                count += 1
    print(
        json.dumps(
            {
                "input_sha256": hashlib.sha256(source).hexdigest(),
                "closed_point_degrees": degrees,
                "roots_in_F2": roots,
                "index": index,
                "signed_degree": signed_degree,
                "effective_degree_one_coefficients": effective_degree_one,
                "profile_extension_checks": count,
                "rational_point_extension_degrees_through_12": [
                    m for m in data["extension_degrees"] if any(m % d == 0 for d in degrees)
                ],
                "scope": data["scope"],
                "universal_formula_status": (
                    "mathematical derivation in theory.md; not kernel-checked"
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
