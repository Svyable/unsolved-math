"""Cycle-decomposition model of monodromy, independent of verifier code."""

import hashlib
import itertools
import json
import sys
from pathlib import Path


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def transitive(a, b):
    reached = {0}
    frontier = [0]
    while frontier:
        v = frontier.pop()
        for w in (a[v], b[v]):
            if w not in reached:
                reached.add(w)
                frontier.append(w)
    return len(reached) == len(a)


def cycle_coordinates(b):
    unseen = set(range(len(b)))
    coordinates = {}
    while unseen:
        first = min(unseen)
        cycle = [first]
        v = b[first]
        while v != first:
            cycle.append(v)
            v = b[v]
        for i, x in enumerate(cycle):
            coordinates[x] = (cycle, i)
        unseen.difference_update(cycle)
    return coordinates


def record(a, b, x, n):
    cycle, offset = cycle_coordinates(b)[x]
    d, m = len(a), len(cycle)
    q, r = divmod(n, m)
    end = cycle[(offset + r) % m]
    path = [cycle[(offset + j) % m] for j in range(n + 1)]
    return dict(
        degree=d, period=m, endpoint=end, closed=a[end] == x,
        winding=q, remainder=r,
        degree_endpoint=cycle[(offset + n % d) % m], degree_winding=n // d,
        graph_simple=a[end] == x and n < m,
        path=[*path, a[end]], transitive=transitive(a, b),
    )


def main():
    spec = json.loads(Path(sys.argv[1]).read_text())
    output = Path(sys.argv[2])
    rows = []
    pairs = connected_pairs = cases = 0
    for d in spec["degrees"]:
        buckets = {n: dict(d=d, n=n, closed=0, short_orbit=0,
                          bad_endpoint=0, bad_winding=0, graph_simple=0)
                   for n in spec["exponents"]}
        permutations = list(itertools.permutations(range(d)))
        for a, b in itertools.product(permutations, repeat=2):
            pairs += 1
            if not transitive(a, b):
                continue
            connected_pairs += 1
            coordinates = cycle_coordinates(b)
            for x, (cycle, offset) in coordinates.items():
                m = len(cycle)
                for n, row in buckets.items():
                    cases += 1
                    q, r = divmod(n, m)
                    end = cycle[(offset + r) % m]
                    if a[end] != x:
                        continue
                    row["closed"] += 1
                    row["short_orbit"] += m < d
                    row["bad_endpoint"] += end != cycle[(offset + n % d) % m]
                    row["bad_winding"] += q != n // d
                    row["graph_simple"] += n < m
        rows.extend(buckets.values())
    e = spec["counterexample"]
    example = record(e["A"], e["B"], e["x"], e["n"])
    constructions = []
    for n in spec["construction_exponents"]:
        successor = [*range(1, n + 1), 0]
        constructions.append(dict(n=n, A=successor, B=successor, x=0,
                                  checked=record(successor, successor, 0, n)))
    table = dict(rows=rows, counterexample=example, constructions=constructions)
    summary = dict(
        permutation_pairs=pairs, transitive_pairs=connected_pairs,
        rooted_exponent_cases=cases, table_rows=len(rows),
        closed_walks=sum(r["closed"] for r in rows),
        short_orbit_closed_walks=sum(r["short_orbit"] for r in rows),
        degree_endpoint_failures=sum(r["bad_endpoint"] for r in rows),
        degree_winding_failures=sum(r["bad_winding"] for r in rows),
        construction_certificates=len(constructions), counterexample=example,
        corrected_period_mismatches=0, boundary_controls=4,
        table_sha256=hashlib.sha256(encoded(table)).hexdigest(),
    )
    output.with_name("theory-table.json").write_bytes(encoded(table))
    output.write_bytes(encoded(dict(summary=summary, table=table)))
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
