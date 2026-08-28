"""Exhaust all label assignments; no functional-graph formula or theory imports."""

import argparse
import copy
import hashlib
import itertools
import json
from pathlib import Path


def encode(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def valid_map(T, N):
    return (type(N) is int and N > 0 and
            all(type(v) is int and 0 <= v < len(T) for v in T))


def cost(T, N, labels):
    assert valid_map(T, N) and len(labels) == len(T)
    assert all(type(a) is int and 0 <= a < N for a in labels)
    return sum(labels[v] != (labels[u] + 1) % N for u, v in enumerate(T))


def exhaust(T, N):
    assert valid_map(T, N)
    best, count, exact = len(T) + 1, 0, 0
    sbest, scount, tested = None, 0, 0
    witness, switness = None, None
    for labels in itertools.product(range(N), repeat=len(T)):
        errors = cost(T, N, labels)
        tested += 1
        exact += errors == 0
        if errors < best:
            best, count, witness = errors, 1, list(labels)
        elif errors == best:
            count += 1
        if len(set(labels)) == N:
            if sbest is None or errors < sbest:
                sbest, scount, switness = errors, 1, list(labels)
            elif errors == sbest:
                scount += 1
    return dict(minimum=best, minimizers=count, exact=exact, surjective_minimum=sbest,
                surjective_minimizers=scount, tested=tested, witness=witness,
                surjective_witness=switness)


def reconstruct(spec, outdir):
    # Counterexample and boundaries before reading any theory certificate.
    e = spec["counterexample"]
    example = exhaust(e["T"], e["N"])
    assert example["minimum"] == 1 and example["surjective_minimum"] == 2
    assert example["minimizers"] == 3 and example["surjective_minimizers"] == 6
    assert exhaust([], 3)["exact"] == 1
    assert exhaust([], 3)["surjective_minimum"] is None
    assert exhaust([0], 1)["minimum"] == 0
    assert exhaust([0], 2)["minimum"] == 1
    assert exhaust([1, 0, 1], 2)["exact"] == 2
    assert not valid_map([1], 2) and not valid_map([0], 0)
    digest = hashlib.sha256()
    rows, gaps = [], []
    total_tested = 0
    for n, N in spec["domains"]:
        systems = minimum_sum = minimizer_sum = exact_systems = gap = tested = 0
        for T in itertools.product(range(n), repeat=n):
            r = exhaust(T, N)
            digest.update(encode([n, list(T), N, r["minimum"], r["minimizers"], r["exact"]]))
            systems += 1
            minimum_sum += r["minimum"]
            minimizer_sum += r["minimizers"]
            exact_systems += r["exact"] > 0
            gap += r["surjective_minimum"] is not None and r["surjective_minimum"] > r["minimum"]
            tested += r["tested"]
        rows.append([n, N, systems, minimum_sum, minimizer_sum, exact_systems])
        gaps.append([n, N, gap, tested])
        total_tested += tested
    stars = []
    for n, N in spec["star_domains"]:
        r = exhaust([0] * n, N)
        stars.append([n, N, r["minimum"], r["minimizers"],
                      r["surjective_minimum"], r["surjective_minimizers"]])
    certificates = []
    for T in spec["certificate_maps"]:
        for N in spec["certificate_moduli"]:
            r = exhaust(T, N)
            certificates.append([T, N, r["minimum"], r["witness"]])
    table = dict(domains=rows, stars=stars)
    summary = dict(systems=sum(r[2] for r in rows), domain_rows=len(rows),
                   label_assignments=total_tested, case_stream_sha256=digest.hexdigest(),
                   table_sha256=hashlib.sha256(encode(table)).hexdigest(),
                   star_cases=len(stars), certificates=len(certificates),
                   counterexample=example, boundary_controls=7)
    outdir.joinpath("verification-surjectivity.json").write_bytes(encode(gaps))
    outdir.joinpath("verification-certificates.json").write_bytes(encode(certificates))
    return summary, table, certificates


def accept(candidate, summary, table, reference):
    if candidate.get("summary") != summary or candidate.get("table") != table:
        return False
    certs = candidate.get("certificates", [])
    if len(certs) != len(reference):
        return False
    try:
        for (T, N, target, labels), ref in zip(certs, reference, strict=True):
            if [T, N, target] != ref[:3] or cost(T, N, labels) != target:
                return False
    except (AssertionError, TypeError, ValueError, IndexError):
        return False
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--certificate", type=Path)
    args = parser.parse_args()
    spec = json.loads(args.input.read_text())
    summary, table, reference = reconstruct(spec, args.output.parent)
    args.output.with_name("verification-table.json").write_bytes(encode(table))
    result = summary
    if args.certificate:
        candidate = json.loads(args.certificate.read_text())
        assert accept(candidate, summary, table, reference)
        changes = [
            ("wrong_minimum", lambda c: c["table"]["domains"][0].__setitem__(3, 99)),
            ("wrong_star_surjectivity", lambda c: c["table"]["stars"][10].__setitem__(4, 1)),
            ("missing_domain", lambda c: c["table"]["domains"].pop()),
            ("missing_certificate", lambda c: c["certificates"].pop()),
            ("bad_label", lambda c: c["certificates"][8][3].__setitem__(0, -1)),
            ("false_count", lambda c: c["summary"].update(systems=-1)),
            ("bad_map", lambda c: c["certificates"][8][0].__setitem__(0, 9)),
        ]
        rejected = []
        for name, change in changes:
            bad = copy.deepcopy(candidate)
            change(bad)
            assert not accept(bad, summary, table, reference)
            rejected.append(name)
        result = dict(summary=summary, authentic_accepted=True, corruptions_rejected=rejected)
    args.output.write_bytes(encode(result))
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
