"""Subset-degree hole recognition and minimum-degree peeling; standard library only."""

import argparse
import hashlib
import json
from itertools import combinations, product
from pathlib import Path


def adjacency(n: int, mask: int) -> list[int]:
    result = [0] * n
    for i, (u, v) in enumerate(combinations(range(n), 2)):
        if mask & (1 << i):
            result[u] |= 1 << v
            result[v] |= 1 << u
    return result


def has_triangle(adj: list[int]) -> bool:
    return any(
        adj[u] & adj[v]
        for u in range(len(adj))
        for v in range(u + 1, len(adj))
        if adj[u] & (1 << v)
    )


def has_even_hole(adj: list[int]) -> bool:
    for vertices in range(1 << len(adj)):
        count = vertices.bit_count()
        if count < 4 or count % 2:
            continue
        members = [v for v in range(len(adj)) if vertices & (1 << v)]
        if any((adj[v] & vertices).bit_count() != 2 for v in members):
            continue
        seen = 0
        frontier = 1 << members[0]
        while frontier:
            seen |= frontier
            neighbours = 0
            for v in members:
                if frontier & (1 << v):
                    neighbours |= adj[v]
            frontier = neighbours & vertices & ~seen
        if seen == vertices:
            return True
    return False


def peel(adj: list[int]) -> tuple[list[int], int]:
    remaining = (1 << len(adj)) - 1
    ordering = []
    width = 0
    while remaining:
        v = min(
            (v for v in range(len(adj)) if remaining & (1 << v)),
            key=lambda v: ((adj[v] & remaining).bit_count(), v),
        )
        width = max(width, (adj[v] & remaining).bit_count())
        ordering.append(v)
        remaining ^= 1 << v
    return ordering, width


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificates", type=Path, required=True)
    args = parser.parse_args()
    raw = Path(__file__).with_name("input.json").read_bytes()
    data = json.loads(raw)
    totals = []
    digest = hashlib.sha256()
    certificate_lines = []
    for n in range(data["max_vertices"] + 1):
        eligible = 0
        classes = [0, 0, 0, 0]
        graphs = 1 << (n * (n - 1) // 2)
        for mask in range(graphs):
            adj = adjacency(n, mask)
            if has_triangle(adj) or has_even_hole(adj):
                continue
            order, width = peel(adj)
            assert width <= 2
            # A graph is a forest iff its degeneracy is <= 1.
            chi = 0 if n == 0 else 1 if mask == 0 else 2 if width <= 1 else 3
            colors = [-1] * n
            for v in reversed(order):
                forbidden = {colors[u] for u in range(n) if adj[v] & (1 << u)}
                colors[v] = min(set(range(3)) - forbidden)
            assert all(
                colors[u] != colors[v]
                for u in range(n)
                for v in range(u + 1, n)
                if adj[u] & (1 << v)
            )
            eligible += 1
            classes[chi] += 1
            digest.update(json.dumps([n, mask, chi, width], separators=(",", ":")).encode())
            certificate_lines.append(
                json.dumps(
                    {"n": n, "mask": mask, "peel": order, "width": width, "chi": chi},
                    separators=(",", ":"),
                )
            )
        totals.append(
            {"n": n, "all_graphs": graphs, "eligible": eligible, "chi_counts_0_1_2_3": classes}
        )
    sample = data["bad_list_example"]
    satisfying = [
        list(c) for c in product(*sample["lists"]) if all(c[u] != c[v] for u, v in sample["edges"])
    ]
    assert not satisfying
    blocked_pairs = []
    for a in sample["lists"][0]:
        for b in sample["lists"][1]:
            witness = next(v for v in range(2, 6) if set(sample["lists"][v]) == {a, b})
            blocked_pairs.append({"left_colors": [a, b], "blocked_vertex": witness})
    args.certificates.write_text("\n".join(certificate_lines) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "input_sha256": hashlib.sha256(raw).hexdigest(),
                "counts": totals,
                "all_graphs": sum(row["all_graphs"] for row in totals),
                "eligible_graphs": sum(row["eligible"] for row in totals),
                "classification_sha256": digest.hexdigest(),
                "peeling_certificate_sha256": hashlib.sha256(
                    args.certificates.read_bytes()
                ).hexdigest(),
                "K2_4_list_assignments_tested": 64,
                "K2_4_satisfying_assignments": satisfying,
                "K2_4_obstruction_certificate": blocked_pairs,
                "scope": (
                    "All labelled simple graphs on 0..6 vertices only; "
                    "no universal theorem proved by enumeration."
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
