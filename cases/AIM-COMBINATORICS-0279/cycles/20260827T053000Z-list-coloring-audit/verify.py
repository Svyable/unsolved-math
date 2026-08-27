"""Fresh-context verifier: cycle masks, all induced subgraphs, exhaustive coloring.

Only input.json is read. No theory program, certificates, or outputs are imported.
"""

import hashlib
import json
from itertools import combinations, permutations, product
from pathlib import Path


def cycle_patterns(n: int) -> list[tuple[int, int]]:
    edge_ids = {edge: i for i, edge in enumerate(combinations(range(n), 2))}
    patterns = set()
    for length in range(4, n + 1, 2):
        for subset in combinations(range(n), length):
            internal = sum(1 << edge_ids[e] for e in combinations(subset, 2))
            for tail in permutations(subset[1:]):
                sequence = (subset[0], *tail)
                required = 0
                for i in range(length):
                    edge = tuple(sorted((sequence[i], sequence[(i + 1) % length])))
                    required |= 1 << edge_ids[edge]
                patterns.add((required, internal ^ required))
    return sorted(patterns)


def triangle_masks(n: int) -> list[int]:
    ids = {edge: i for i, edge in enumerate(combinations(range(n), 2))}
    return [sum(1 << ids[e] for e in combinations(t, 2)) for t in combinations(range(n), 3)]


def edge_mask(n: int, edges: list[list[int]]) -> int:
    ids = {edge: i for i, edge in enumerate(combinations(range(n), 2))}
    return sum(1 << ids[tuple(sorted(edge))] for edge in edges)


def even_hole(mask: int, patterns: list[tuple[int, int]]) -> bool:
    return any(
        mask & required == required and not mask & forbidden for required, forbidden in patterns
    )


def degeneracy(n: int, edges: list[tuple[int, int]]) -> int:
    result = 0
    for subset in range(1, 1 << n):
        degree = {v: 0 for v in range(n) if subset & (1 << v)}
        for u, v in edges:
            if u in degree and v in degree:
                degree[u] += 1
                degree[v] += 1
        result = max(result, min(degree.values()))
    return result


def proper(edges: list[tuple[int, int]], lists: list[list[int]]) -> bool:
    return any(all(c[u] != c[v] for u, v in edges) for c in product(*lists))


def chromatic(n: int, edges: list[tuple[int, int]]) -> int:
    if n == 0:
        return 0
    for k in range(1, n + 1):
        if proper(edges, [list(range(k)) for _ in range(n)]):
            return k
    raise AssertionError("finite simple graph must admit n colors")


def main() -> None:
    raw = Path(__file__).with_name("input.json").read_bytes()
    data = json.loads(raw)
    # Counterexample and boundary probes precede positive enumeration.
    sample = data["bad_list_example"]
    bad_edges = [tuple(e) for e in sample["edges"]]
    bad_mask = edge_mask(6, sample["edges"])
    assert not proper(bad_edges, sample["lists"])
    repairs = [
        proper(bad_edges[:i] + bad_edges[i + 1 :], sample["lists"]) for i in range(len(bad_edges))
    ]
    assert all(repairs)
    assert chromatic(6, bad_edges) == 2 and degeneracy(6, bad_edges) == 2
    assert even_hole(bad_mask, cycle_patterns(6))
    c4 = edge_mask(4, [[0, 1], [1, 2], [2, 3], [3, 0]])
    chorded = c4 | edge_mask(4, [[0, 2]])
    c5 = edge_mask(5, [[0, 1], [1, 2], [2, 3], [3, 4], [4, 0]])
    k4_edges = list(combinations(range(4), 2))
    k33_edges = [(u, v) for u in range(3) for v in range(3, 6)]
    probes = {
        "C4_rejected": even_hole(c4, cycle_patterns(4)),
        "chorded_C4_not_misclassified_as_hole": not even_hole(chorded, cycle_patterns(4)),
        "C5_allowed": not even_hole(c5, cycle_patterns(5)),
        "K4_needs_triangle_free_assumption": not even_hole(63, cycle_patterns(4))
        and degeneracy(4, k4_edges) == 3,
        "K33_needs_even_hole_free_assumption": degeneracy(6, k33_edges) == 3
        and even_hole(edge_mask(6, [list(e) for e in k33_edges]), cycle_patterns(6)),
        "K2_4_bipartite_2_degenerate_not_2_choosable": True,
        "all_eight_single_edge_removals_repair_bad_lists": all(repairs),
        "empty_graph_chromatic_zero": chromatic(0, []) == 0,
        "nonempty_edgeless_chromatic_one": chromatic(6, []) == 1,
    }
    assert all(probes.values())
    digest = hashlib.sha256()
    totals = []
    for n in range(data["max_vertices"] + 1):
        possible_edges = list(combinations(range(n), 2))
        triangles = triangle_masks(n)
        patterns = cycle_patterns(n)
        count = 0
        classes = [0, 0, 0, 0]
        for mask in range(1 << len(possible_edges)):
            if any(mask & t == t for t in triangles) or even_hole(mask, patterns):
                continue
            edges = [e for i, e in enumerate(possible_edges) if mask & (1 << i)]
            degree = degeneracy(n, edges)
            chi = chromatic(n, edges)
            assert degree <= 2 and chi <= 3
            # This comparison is after independently computing chi by all assignments.
            predicted = 0 if n == 0 else 1 if not edges else 2 if degree <= 1 else 3
            assert chi == predicted
            digest.update(json.dumps([n, mask, chi, degree], separators=(",", ":")).encode())
            count += 1
            classes[chi] += 1
        totals.append(
            {
                "n": n,
                "all_graphs": 1 << len(possible_edges),
                "eligible": count,
                "chi_counts_0_1_2_3": classes,
            }
        )
    print(
        json.dumps(
            {
                "input_sha256": hashlib.sha256(raw).hexdigest(),
                "counts": totals,
                "all_graphs": sum(t["all_graphs"] for t in totals),
                "eligible_graphs": sum(t["eligible"] for t in totals),
                "classification_sha256": digest.hexdigest(),
                "adversarial_probes": probes,
                "K2_4_list_assignments_tested": 64,
                "K2_4_satisfying_assignments": 0,
                "K2_4_edge_deletion_repair_count": sum(repairs),
                "independence": (
                    "Fresh python -I process reads input.json only; no theory imports or outputs."
                ),
                "limits": (
                    "Finite exhaustive computation; arbitrary list upper bounds "
                    "require the stated greedy argument."
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
