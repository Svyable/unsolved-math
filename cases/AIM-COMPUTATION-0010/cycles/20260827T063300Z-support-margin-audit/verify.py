"""Independent direct segment integration. Reads raw fixture only, no theory files."""

import hashlib
import json
from fractions import Fraction
from itertools import pairwise, product
from pathlib import Path

F = Fraction


def step(state: tuple[F, F, F], w: F, dt: F) -> tuple[F, F, F]:
    # Integrate x3'=w, then x2'=3*x3, then x1'=2*x2 from the segment start.
    x1, x2, x3 = state
    return (
        x1 + 2 * x2 * dt + 3 * x3 * dt**2 + w * dt**3,
        x2 + 3 * x3 * dt + F(3, 2) * w * dt**2,
        x3 + w * dt,
    )


def run(epsilon: F, cuts: list[F], signs: tuple[int, ...]) -> tuple[F, F, F]:
    if epsilon < 0 or any(b < a for a, b in pairwise(cuts)):
        raise ValueError("nonnegative amplitude and ordered times required")
    if len(signs) != len(cuts) - 1 or any(s not in (-1, 1) for s in signs):
        raise ValueError("input certificate violates the amplitude/sign contract")
    state = (F(0), F(0), F(0))
    for i, sign in enumerate(signs):
        state = step(state, epsilon * sign, cuts[i + 1] - cuts[i])
    return state


def dot(a: list[F], state: tuple[F, F, F]) -> F:
    return sum((x * y for x, y in zip(a, state, strict=True)), F(0))


def main() -> None:
    raw = Path(__file__).with_name("input.json").read_bytes()
    data = json.loads(raw)
    assert data["A"] == [[0, 2, 0], [0, 0, 3], [0, 0, 0]]
    assert data["B"] == [0, 0, 1] and data["initial_state"] == [0, 0, 0]
    e = F(data["base"]["epsilon"])
    t = F(data["base"]["T"])
    a = list(map(F, data["base"]["a"]))
    witness = run(e, [F(0), t / 3, 2 * t / 3, t], (1, -1, 1))
    reachable = dot(a, witness)
    positive = run(e, [F(0), t], (1,))
    negative = run(e, [F(0), t], (-1,))
    signed = dot(a, positive)
    box = sum((abs(c) * r for c, r in zip(a, positive, strict=True)), F(0))
    # Counterexample and boundaries first: a realizable trajectory, not a box vertex.
    assert signed < F(data["base"]["false_safe_threshold"]) < reachable
    assert reachable < F(data["base"]["tight_safe_threshold"]) < box
    assert tuple(-x for x in positive) == negative
    asymmetric = [F(0), F(1), F(-1)]
    correct = dot(asymmetric, run(e, [F(0), F(2, 3), F(1)], (1, -1)))
    wrong = dot(asymmetric, run(e, [F(0), F(1, 3), F(1)], (1, -1)))
    assert correct == F(5, 6) * e and wrong == e / 2 < correct
    for bad_e, bad_cuts, bad_signs in [
        (F(-1), [F(0), F(1)], (1,)),
        (e, [F(1), F(0)], (1,)),
        (e, [F(0), F(1)], (2,)),
    ]:
        try:
            run(bad_e, bad_cuts, bad_signs)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid input was accepted")
    rows = []
    coefficient_certificates = []
    trajectories = 0
    for eps_text in data["epsilon_values"]:
        for time_text in data["horizons"]:
            eps, horizon = F(eps_text), F(time_text)
            direction = [F(1), -horizon, F(2, 3) * horizon**2]
            # Exact coefficient identity, not point sampling: A^3 B=0 truncates exp(A*t)B.
            vector = tuple(map(F, data["B"]))
            coefficients = []
            for factorial in (1, 1, 2):
                coefficients.append(dot(direction, vector) / factorial)
                vector = tuple(
                    sum((F(c) * x for c, x in zip(row, vector, strict=True)), F(0))
                    for row in data["A"]
                )
            assert vector == (0, 0, 0)
            assert coefficients == [F(2, 3) * horizon**2, -3 * horizon, F(3)]
            assert 0 <= horizon / 3 <= 2 * horizon / 3 <= horizon
            coefficient_certificates.append(
                {
                    "T": str(horizon),
                    "epsilon": str(eps),
                    "coefficients": list(map(str, coefficients)),
                    "roots": [str(horizon / 3), str(2 * horizon / 3)],
                }
            )
            values = []
            for signs in product((-1, 1), repeat=3):
                endpoint = run(eps, [F(0), horizon / 3, 2 * horizon / 3, horizon], signs)
                values.append(dot(direction, endpoint))
                bound = run(eps, [F(0), horizon], (1,))
                assert all(abs(x) <= r for x, r in zip(endpoint, bound, strict=True))
                trajectories += 1
            observed = max(values)
            assert observed == F(11, 54) * eps * horizon**3
            # Check the scalar impulse kernel by direct homogeneous state propagation.
            for tau in [
                F(0),
                horizon / 6,
                horizon / 3,
                horizon / 2,
                2 * horizon / 3,
                5 * horizon / 6,
                horizon,
            ]:
                impulse = step((F(0), F(0), F(1)), F(0), tau)
                assert dot(direction, impulse) == 3 * (tau - horizon / 3) * (tau - 2 * horizon / 3)
            rows.append(
                {
                    "epsilon": str(eps),
                    "T": str(horizon),
                    "maximum_over_eight_controls": str(observed),
                    "attaining_state": list(
                        map(
                            str, run(eps, [F(0), horizon / 3, 2 * horizon / 3, horizon], (1, -1, 1))
                        )
                    ),
                }
            )
    print(
        json.dumps(
            {
                "input_sha256": hashlib.sha256(raw).hexdigest(),
                "case_count": len(rows),
                "exact_trajectories_checked": trajectories,
                "cases": rows,
                "exact_coefficient_certificates": coefficient_certificates,
                "base_terminal_state": list(map(str, witness)),
                "base_reachable_support": str(reachable),
                "base_signed_margin": str(signed),
                "base_box_margin": str(box),
                "base_violation": str(reachable - F(data["base"]["false_safe_threshold"])),
                "asymmetric_correct_support": str(correct),
                "asymmetric_wrong_switch_value": str(wrong),
                "adversarial_checks": {
                    "signed_margin_false_safe_detected": True,
                    "lost_correlation_box_is_conservative": True,
                    "time_reversal_switch_error_detected": True,
                    "negative_amplitude_rejected": True,
                    "reversed_time_rejected": True,
                    "out_of_bound_input_rejected": True,
                    "zero_amplitude_and_zero_horizon_checked": True,
                },
                "independence": (
                    "Fresh python -I process; direct triangular ODE integration, "
                    "no theory outputs/code."
                ),
                "limits": (
                    "240 exact trajectories do not alone cover all measurable inputs; "
                    "global support needs the separately stated kernel sign bound."
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
