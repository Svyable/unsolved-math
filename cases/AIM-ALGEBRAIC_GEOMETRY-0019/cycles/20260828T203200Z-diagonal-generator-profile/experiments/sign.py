"""Two literal paths through the mixed tensor cell; no tensor matrix import."""

import argparse
import copy
import json
from pathlib import Path


def path_sum(p, signed):
    # First decrease x, then y: +xy. First decrease y, then x: -xy
    # because the original x degree was one. All other monomials have zero coefficient.
    paths = [((1, 0), (0, 1), 1), ((0, 1), (1, 0), -1 if signed else 1)]
    terms = {}
    for a, b, c in paths:
        monomial = tuple(x + y for x, y in zip(a, b, strict=True))
        terms[monomial] = (terms.get(monomial, 0) + c) % p
    return [terms.get(m, 0) for m in [(0, 0), (0, 1), (1, 0), (1, 1)]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--certificate", required=True)
    args = ap.parse_args()
    spec = json.loads(Path(args.input).read_text())
    # Odd-characteristic failure first, before reading submitted probes.
    assert path_sum(3, False) == [0, 0, 0, 2] and path_sum(3, True) == [0, 0, 0, 0]
    expected = [
        dict(
            p=p,
            exponents=[2, 2],
            source_multidegree=[1, 1],
            unsigned_square=path_sum(p, False),
            signed_square=path_sum(p, True),
        )
        for p in spec["primes"]
    ]
    proposed = json.loads(Path(args.certificate).read_text())["sign_probes"]
    assert proposed == expected
    mutations = []
    for name in ["erase_odd_failure", "invent_char_two_failure", "break_signed", "omit_prime"]:
        bad = copy.deepcopy(proposed)
        if name == "erase_odd_failure":
            bad[1]["unsigned_square"] = [0] * 4
        if name == "invent_char_two_failure":
            bad[0]["unsigned_square"][-1] = 1
        if name == "break_signed":
            bad[2]["signed_square"][-1] = 2
        if name == "omit_prime":
            bad.pop()
        assert bad != expected
        mutations.append(name)
    result = dict(
        method="literal signed path sums, no tensor/bar matrix code",
        probes=expected,
        corruptions_rejected=mutations,
    )
    Path(args.output).write_text(json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n")
    print(json.dumps(dict(probes=len(expected), corruptions_rejected=len(mutations))))


if __name__ == "__main__":
    main()
