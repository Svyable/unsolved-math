"""Fresh-context verifier: union-find connectivity and literal path stepping."""

import argparse
import copy
import hashlib
import itertools
import json
from pathlib import Path


def encoded(obj):
    return (json.dumps(obj, sort_keys=True, separators=(",", ":")) + "\n").encode()


def permutation(p):
    return bool(p) and sorted(p) == list(range(len(p)))


def connected(a, b):
    parent = list(range(len(a)))

    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x

    for p in (a, b):
        for i, j in enumerate(p):
            parent[find(i)] = find(j)
    return len({find(i) for i in range(len(a))}) == 1


def walk(b, x, n):
    result = [x]
    for _ in range(n):
        result.append(b[result[-1]])
    return result


def inspect(a, b, x, n):
    assert permutation(a) and permutation(b) and len(a) == len(b)
    assert 0 <= x < len(a) and n >= 0
    d = len(a)
    first = walk(b, x, d)
    m = next(i for i in range(1, d + 1) if first[i] == x)
    path = walk(b, x, n)
    return dict(
        degree=d, period=m, endpoint=path[-1], closed=a[path[-1]] == x,
        winding=sum(v == x for v in path[1:]), remainder=n % m,
        degree_endpoint=walk(b, x, n % d)[-1], degree_winding=n // d,
        graph_simple=a[path[-1]] == x and len(set(path)) == len(path),
        path=[*path, a[path[-1]]], transitive=connected(a, b),
    )


def reconstruct(spec):
    # Adversarial cases are evaluated before any supplied certificate is opened.
    e = spec["counterexample"]
    example = inspect(e["A"], e["B"], e["x"], e["n"])
    assert example["transitive"] and example["closed"]
    assert example["period"] < example["degree"]
    assert example["endpoint"] != example["degree_endpoint"]
    assert example["winding"] != example["degree_winding"]
    assert inspect([0], [0], 0, 0)["graph_simple"]
    assert inspect([0, 1], [1, 0], 0, 0)["closed"]
    assert not connected([0, 1, 2], [1, 0, 2])
    assert not permutation([0, 0])
    rows = []
    pair_count = transitive_count = rooted_count = 0
    for d in spec["degrees"]:
        buckets = {n: dict(d=d, n=n, closed=0, short_orbit=0,
                          bad_endpoint=0, bad_winding=0, graph_simple=0)
                   for n in spec["exponents"]}
        perms = list(itertools.permutations(range(d)))
        for a in perms:
            for b in perms:
                pair_count += 1
                if not connected(a, b):
                    continue
                transitive_count += 1
                for x in range(d):
                    # Literal stepping, including each return to x.
                    returns = walk(b, x, d)
                    m = next(i for i in range(1, d + 1) if returns[i] == x)
                    for n in spec["exponents"]:
                        rooted_count += 1
                        path = walk(b, x, n)
                        assert path[-1] == walk(b, x, n % m)[-1]
                        turns = sum(v == x for v in path[1:])
                        assert turns == n // m
                        if a[path[-1]] != x:
                            continue
                        row = buckets[n]
                        row["closed"] += 1
                        row["short_orbit"] += m < d
                        row["bad_endpoint"] += path[-1] != walk(b, x, n % d)[-1]
                        row["bad_winding"] += turns != n // d
                        row["graph_simple"] += len(set(path)) == n + 1
                        if n >= d:
                            assert len(set(path)) < n + 1
        rows.extend(buckets.values())
    constructions = []
    for n in spec["construction_exponents"]:
        # Independent specification: complete the path by cyclic successor.
        d = n + 1
        a = [(j + 1) % d for j in range(d)]
        b = a[:]
        checked = inspect(a, b, 0, n)
        assert checked["graph_simple"] and checked["transitive"]
        constructions.append(dict(n=n, A=a, B=b, x=0, checked=checked))
    table = dict(rows=rows, counterexample=example, constructions=constructions)
    summary = dict(
        permutation_pairs=pair_count, transitive_pairs=transitive_count,
        rooted_exponent_cases=rooted_count, table_rows=len(rows),
        closed_walks=sum(r["closed"] for r in rows),
        short_orbit_closed_walks=sum(r["short_orbit"] for r in rows),
        degree_endpoint_failures=sum(r["bad_endpoint"] for r in rows),
        degree_winding_failures=sum(r["bad_winding"] for r in rows),
        construction_certificates=len(constructions), counterexample=example,
        corrected_period_mismatches=0, boundary_controls=4,
        table_sha256=hashlib.sha256(encoded(table)).hexdigest(),
    )
    return summary, table


def accepts(candidate, summary, table):
    # Equality to a freshly rebuilt full census checks omissions and all fields.
    return candidate == dict(summary=summary, table=table)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--certificate", type=Path)
    args = parser.parse_args()
    spec = json.loads(args.input.read_text())
    summary, table = reconstruct(spec)
    args.output.with_name("verification-table.json").write_bytes(encoded(table))
    result = summary
    if args.certificate:
        candidate = json.loads(args.certificate.read_text())
        assert accepts(candidate, summary, table)
        changes = [
            ("period_replaced_by_degree", lambda c: c["table"]["counterexample"].update(period=3)),
            ("endpoint_replaced_by_degree_remainder",
             lambda c: c["table"]["counterexample"].update(endpoint=0)),
            ("wrong_winding", lambda c: c["table"]["counterexample"].update(winding=1)),
            ("closure_reversed", lambda c: c["table"]["counterexample"].update(closed=False)),
            ("census_count", lambda c: c["table"]["rows"][0].update(closed=0)),
            ("invalid_construction",
             lambda c: c["table"]["constructions"][2]["A"].__setitem__(0, 0)),
            ("missing_exponent", lambda c: c["table"]["rows"].pop()),
        ]
        rejected = []
        for name, mutate in changes:
            bad = copy.deepcopy(candidate)
            mutate(bad)
            assert not accepts(bad, summary, table)
            rejected.append(name)
        result = dict(summary=summary, authentic_accepted=True,
                      corruptions_rejected=rejected,
                      method="union-find plus direct path traversal before certificate read")
    args.output.write_bytes(encoded(result))
    report = result if not args.certificate else dict(summary=summary, rejected=len(rejected))
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
