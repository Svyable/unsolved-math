#!/usr/bin/env python3
"""Strict, dependency-free audit of a pinned graph-coloring DIMACS encoding.

This checker establishes only structural equivalence between the supplied graph
and CNF, plus the precondition for three color-symmetry locks. It does not check
geometric coordinates or CNF unsatisfiability.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections.abc import Iterable
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path

COLORS = 4
LOCKS = {1: 1, 2: 2, 6: 3}
EXPECTED_EDGE_SHA256 = "dc5085db9682aa246c3fc56efed9767e2a294a43e621a3e67a690d0489bdadc9"
EXPECTED_CNF_SHA256 = "c9757e78853383462ca20b4702fc6b1cc46d88c5de71d305726396856f4765b8"


class AuditError(ValueError):
    """The supplied artifact violates a strict input invariant."""


@dataclass(frozen=True)
class Graph:
    vertices: int
    declared_edges: int
    edges: frozenset[tuple[int, int]]


@dataclass(frozen=True)
class Cnf:
    variables: int
    declared_clauses: int
    clauses: tuple[frozenset[int], ...]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_sha256(path: Path, expected: str) -> str:
    actual = sha256_file(path)
    if actual != expected:
        raise AuditError(f"SHA-256 mismatch for {path}: expected {expected}, found {actual}")
    return actual


def parse_graph(path: Path) -> Graph:
    header: tuple[int, int] | None = None
    edge_rows: list[tuple[int, int]] = []
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("c "):
            continue
        parts = line.split()
        if parts[:2] == ["p", "edge"] and len(parts) == 4:
            if header is not None:
                raise AuditError(f"duplicate graph header at line {line_number}")
            header = (int(parts[2]), int(parts[3]))
            continue
        if parts[:1] == ["e"] and len(parts) == 3:
            left, right = int(parts[1]), int(parts[2])
            edge_rows.append((min(left, right), max(left, right)))
            continue
        raise AuditError(f"unsupported graph row at line {line_number}: {raw!r}")
    if header is None:
        raise AuditError("graph header is missing")
    vertices, declared_edges = header
    if any(left == right for left, right in edge_rows):
        raise AuditError("graph contains a self-loop")
    if any(left < 1 or right > vertices for left, right in edge_rows):
        raise AuditError("graph contains an out-of-range vertex")
    edges = frozenset(edge_rows)
    if len(edges) != len(edge_rows):
        raise AuditError("graph contains duplicate undirected edges")
    if len(edges) != declared_edges:
        raise AuditError(
            f"graph edge count mismatch: header {declared_edges}, parsed {len(edges)}"
        )
    return Graph(vertices=vertices, declared_edges=declared_edges, edges=edges)


def parse_cnf(path: Path) -> Cnf:
    header: tuple[int, int] | None = None
    clauses: list[frozenset[int]] = []
    pending: list[int] = []
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("c "):
            continue
        parts = line.split()
        if parts[:2] == ["p", "cnf"] and len(parts) == 4:
            if header is not None or pending or clauses:
                raise AuditError(f"misplaced or duplicate CNF header at line {line_number}")
            header = (int(parts[2]), int(parts[3]))
            continue
        if header is None:
            raise AuditError(f"clause before CNF header at line {line_number}")
        for token in parts:
            literal = int(token)
            if literal == 0:
                clause = frozenset(pending)
                if not clause:
                    raise AuditError(f"empty clause ending at line {line_number}")
                if any(-item in clause for item in clause):
                    raise AuditError(f"tautological clause ending at line {line_number}")
                if len(clause) != len(pending):
                    raise AuditError(f"duplicate literal ending at line {line_number}")
                clauses.append(clause)
                pending = []
            else:
                pending.append(literal)
    if header is None:
        raise AuditError("CNF header is missing")
    if pending:
        raise AuditError("unterminated final CNF clause")
    variables, declared_clauses = header
    if any(abs(literal) > variables for clause in clauses for literal in clause):
        raise AuditError("CNF contains an out-of-range literal")
    if len(clauses) != declared_clauses:
        raise AuditError(
            f"CNF clause count mismatch: header {declared_clauses}, parsed {len(clauses)}"
        )
    if len(set(clauses)) != len(clauses):
        raise AuditError("CNF contains duplicate clauses")
    return Cnf(
        variables=variables,
        declared_clauses=declared_clauses,
        clauses=tuple(clauses),
    )


def variable(vertex: int, color: int) -> int:
    return COLORS * (vertex - 1) + color


def expected_clauses(graph: Graph) -> frozenset[frozenset[int]]:
    clauses: set[frozenset[int]] = set()
    for vertex in range(1, graph.vertices + 1):
        lock = LOCKS.get(vertex)
        if lock is None:
            clauses.add(frozenset(variable(vertex, color) for color in range(1, COLORS + 1)))
        else:
            clauses.add(frozenset({variable(vertex, lock)}))
        for first, second in combinations(range(1, COLORS + 1), 2):
            clauses.add(
                frozenset({-variable(vertex, first), -variable(vertex, second)})
            )
    for left, right in graph.edges:
        for color in range(1, COLORS + 1):
            clauses.add(
                frozenset({-variable(left, color), -variable(right, color)})
            )
    return frozenset(clauses)


def diff_counts(
    actual: Iterable[frozenset[int]], expected: Iterable[frozenset[int]]
) -> tuple[int, int]:
    actual_set, expected_set = set(actual), set(expected)
    return len(expected_set - actual_set), len(actual_set - expected_set)


def audit(edge_path: Path, cnf_path: Path) -> dict[str, object]:
    edge_sha = require_sha256(edge_path, EXPECTED_EDGE_SHA256)
    cnf_sha = require_sha256(cnf_path, EXPECTED_CNF_SHA256)
    graph = parse_graph(edge_path)
    cnf = parse_cnf(cnf_path)
    expected = expected_clauses(graph)
    actual = frozenset(cnf.clauses)
    missing = expected - actual
    unexpected = actual - expected
    if cnf.variables != graph.vertices * COLORS:
        raise AuditError("variable count is not vertices times four colors")
    if missing or unexpected:
        raise AuditError(
            f"clause-set mismatch: {len(missing)} missing, {len(unexpected)} unexpected"
        )

    triangle = {(1, 2), (1, 6), (2, 6)}
    triangle_present = triangle.issubset(graph.edges)
    if not triangle_present:
        raise AuditError("symmetry-locked vertices 1, 2, and 6 do not form a triangle")

    first_expected = min(expected, key=lambda clause: tuple(sorted(clause)))
    missing_probe = set(actual)
    missing_probe.remove(first_expected)
    missing_probe_counts = diff_counts(missing_probe, expected)
    extra_probe = set(actual)
    extra_probe.add(frozenset({1, -1}))
    extra_probe_counts = diff_counts(extra_probe, expected)
    edge_removal_probes: list[dict[str, object]] = []
    for removed in sorted(triangle):
        reduced_graph = Graph(
            vertices=graph.vertices,
            declared_edges=graph.declared_edges - 1,
            edges=frozenset(graph.edges - {removed}),
        )
        reduced_expected = expected_clauses(reduced_graph)
        probe_missing, probe_unexpected = diff_counts(actual, reduced_expected)
        edge_removal_probes.append(
            {
                "removed_edge": list(removed),
                "triangle_precondition": triangle.issubset(reduced_graph.edges),
                "missing_clauses": probe_missing,
                "unexpected_clauses": probe_unexpected,
            }
        )

    at_least_one_or_lock = graph.vertices - len(LOCKS) + len(LOCKS)
    at_most_one = graph.vertices * (COLORS * (COLORS - 1) // 2)
    edge_exclusion = graph.declared_edges * COLORS
    return {
        "schema_version": 1,
        "method": "independent Python standard-library parser and exact clause-set equality",
        "inputs": {
            "edge": {
                "path": edge_path.name,
                "sha256": edge_sha,
                "bytes": edge_path.stat().st_size,
            },
            "cnf": {
                "path": cnf_path.name,
                "sha256": cnf_sha,
                "bytes": cnf_path.stat().st_size,
            },
        },
        "graph": {
            "vertices": graph.vertices,
            "edges": graph.declared_edges,
            "self_loops": 0,
            "duplicate_edges": 0,
            "vertex_range": [1, graph.vertices],
        },
        "cnf": {
            "variables": cnf.variables,
            "clauses": cnf.declared_clauses,
            "duplicate_clauses": 0,
            "tautological_clauses": 0,
        },
        "exact_clause_accounting": {
            "at_least_one_or_unit_lock": at_least_one_or_lock,
            "at_most_one": at_most_one,
            "edge_same_color_exclusion": edge_exclusion,
            "expected_total": at_least_one_or_lock + at_most_one + edge_exclusion,
            "missing": 0,
            "unexpected": 0,
        },
        "symmetry_breaking": {
            "locks": [
                {"vertex": vertex, "color": color} for vertex, color in sorted(LOCKS.items())
            ],
            "triangle_edges": [list(edge) for edge in sorted(triangle)],
            "triangle_present": triangle_present,
            "equisatisfiability_argument": (
                "Every proper coloring gives the triangle three distinct colors; a global "
                "color permutation maps them to 1, 2, and 3 without changing propriety."
            ),
        },
        "boundary_and_counterexample_search": {
            "missing_clause_mutation": {
                "missing": missing_probe_counts[0],
                "unexpected": missing_probe_counts[1],
                "detected": missing_probe_counts == (1, 0),
            },
            "extra_tautology_mutation": {
                "missing": extra_probe_counts[0],
                "unexpected": extra_probe_counts[1],
                "detected": extra_probe_counts == (0, 1),
            },
            "triangle_edge_removal_mutations": edge_removal_probes,
        },
        "result": (
            "PASS: the pinned CNF exactly matches the symmetry-fixed exact-one "
            "4-coloring encoding of the pinned graph."
        ),
        "remaining_obligations": [
            (
                "No coordinate file was checked, so the graph's unit-distance "
                "embedding remains unverified."
            ),
            "No SAT/DRAT proof was checked, so CNF unsatisfiability remains unverified.",
            "The finite certificate audit does not determine the plane's chromatic number.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--edge", type=Path, required=True)
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = audit(args.edge, args.cnf)
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(rendered, end="")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
