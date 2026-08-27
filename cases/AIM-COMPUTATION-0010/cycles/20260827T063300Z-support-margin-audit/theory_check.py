"""Exact convolution-polynomial support certificates; all arithmetic rational."""

import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path


def integral(coefficients: list[Q], lo: Q, hi: Q) -> Q:
    return sum(
        (c * (hi ** (i + 1) - lo ** (i + 1)) / (i + 1) for i, c in enumerate(coefficients)), Q(0)
    )


def certificate(epsilon: Q, horizon: Q) -> dict:
    assert epsilon >= 0 and horizon >= 0
    # exp(A*tau) B = (3*tau^2, 3*tau, 1); A^3=0.
    kernels = [[Q(0), Q(0), Q(3)], [Q(0), Q(3)], [Q(1)]]
    direction = [Q(1), -horizon, Q(2, 3) * horizon**2]
    cuts = [Q(0), horizon / 3, 2 * horizon / 3, horizon]
    signs = [1, -1, 1]
    radii = [epsilon * integral(k, Q(0), horizon) for k in kernels]
    state = [
        epsilon
        * sum(
            (s * integral(k, lo, hi) for s, lo, hi in zip(signs, cuts[:-1], cuts[1:], strict=True)),
            Q(0),
        )
        for k in kernels
    ]
    support = sum((a * x for a, x in zip(direction, state, strict=True)), Q(0))
    signed = sum((a * r for a, r in zip(direction, radii, strict=True)), Q(0))
    box = sum((abs(a) * r for a, r in zip(direction, radii, strict=True)), Q(0))
    scale = epsilon * horizon**3
    assert support == Q(11, 54) * scale
    assert signed == scale / 6 and box == Q(19, 6) * scale
    assert all(abs(x) <= r for x, r in zip(state, radii, strict=True))
    if scale:
        assert signed < scale / 5 < support < scale / 4 < box
    return {
        "epsilon": str(epsilon),
        "T": str(horizon),
        "direction": list(map(str, direction)),
        "radii": list(map(str, radii)),
        "attaining_terminal_state": list(map(str, state)),
        "input_signs_on_forward_thirds": signs,
        "signed_radius_margin": str(signed),
        "exact_support": str(support),
        "box_support": str(box),
        "counterexample_gap": str(support - scale / 5),
        "tight_safe_gap": str(scale / 4 - support),
    }


def main() -> None:
    raw = Path(__file__).with_name("input.json").read_bytes()
    data = json.loads(raw)
    assert data["A"] == [[0, 2, 0], [0, 0, 3], [0, 0, 0]]
    assert data["B"] == [0, 0, 1] and data["initial_state"] == [0, 0, 0]
    rows = [certificate(Q(e), Q(t)) for e in data["epsilon_values"] for t in data["horizons"]]
    base = certificate(Q(data["base"]["epsilon"]), Q(data["base"]["T"]))
    assert Q(base["signed_radius_margin"]) < Q(data["base"]["false_safe_threshold"])
    assert Q(base["exact_support"]) > Q(data["base"]["false_safe_threshold"])
    assert Q(base["exact_support"]) < Q(data["base"]["tight_safe_threshold"])
    print(
        json.dumps(
            {
                "input_sha256": hashlib.sha256(raw).hexdigest(),
                "cases": rows,
                "base": base,
                "case_count": len(rows),
                "positive_scale_cases": sum(Q(r["epsilon"]) * Q(r["T"]) > 0 for r in rows),
                "kernel_factorization": "3*(tau-T/3)*(tau-2*T/3)",
                "theory_boundary": (
                    "Exact finite model; global measurable-input upper bound "
                    "uses the sign-factorization proof in theory.md."
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
