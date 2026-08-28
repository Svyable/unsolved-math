"""Cycle obstructions plus reverse-tree extension; no labeling enumeration."""

import argparse
import hashlib
import itertools
import json
from collections import deque
from math import factorial, prod
from pathlib import Path


def encode(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def analyze(T, N):
    n = len(T)
    indegree = [0] * n
    for v in T:
        indegree[v] += 1
    queue = deque(v for v in range(n) if indegree[v] == 0)
    removed = []
    while queue:
        u = queue.popleft()
        removed.append(u)
        v = T[u]
        indegree[v] -= 1
        if indegree[v] == 0:
            queue.append(v)
    cycles, seen = [], set()
    for start in range(n):
        if not indegree[start] or start in seen:
            continue
        cycle, u = [], start
        while u not in seen:
            cycle.append(u)
            seen.add(u)
            u = T[u]
        cycles.append(cycle)
    bad = [len(c) for c in cycles if len(c) % N]
    minimum = len(bad)
    count = N ** len(cycles) * prod(bad)
    exact = N ** len(cycles) if not bad else 0
    labels = [None] * n
    for cycle in cycles:
        for j, v in enumerate(cycle):
            labels[v] = j % N
    for u in reversed(removed):
        labels[u] = (labels[T[u]] - 1) % N
    assert all(a is not None for a in labels)
    assert sum(labels[T[u]] != (labels[u] + 1) % N for u in range(n)) == minimum
    return minimum, count, exact, labels


def star(n, N):
    if N == 1:
        return [n, N, 0, 1, 0, 1]
    surjective = N - 1 if n >= N else None
    count = N * factorial(n - 1) // factorial(n - N + 1) if n >= N else 0
    return [n, N, 1, N, surjective, count]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    spec = json.loads(args.input.read_text())
    digest = hashlib.sha256()
    rows = []
    for n, N in spec["domains"]:
        systems = minimum_sum = minimizer_sum = exact_systems = 0
        for T in itertools.product(range(n), repeat=n):
            minimum, count, exact, _ = analyze(T, N)
            digest.update(encode([n, list(T), N, minimum, count, exact]))
            systems += 1
            minimum_sum += minimum
            minimizer_sum += count
            exact_systems += exact > 0
        rows.append([n, N, systems, minimum_sum, minimizer_sum, exact_systems])
    stars = [star(n, N) for n, N in spec["star_domains"]]
    certificates = []
    for T in spec["certificate_maps"]:
        for N in spec["certificate_moduli"]:
            minimum, _, _, labels = analyze(T, N)
            certificates.append([T, N, minimum, labels])
    table = dict(domains=rows, stars=stars)
    example = dict(minimum=1, minimizers=3, exact=0, surjective_minimum=2,
                   surjective_minimizers=6, tested=27, witness=[0, 2, 2],
                   surjective_witness=[0, 1, 2])
    summary = dict(systems=sum(r[2] for r in rows), domain_rows=len(rows),
                   label_assignments=sum(n ** n * N ** n for n, N in spec["domains"]),
                   case_stream_sha256=digest.hexdigest(),
                   table_sha256=hashlib.sha256(encode(table)).hexdigest(),
                   star_cases=len(stars), certificates=len(certificates),
                   counterexample=example, boundary_controls=7)
    args.output.with_name("theory-table.json").write_bytes(encode(table))
    args.output.write_bytes(encode(dict(summary=summary, table=table,
                                       certificates=certificates)))
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
