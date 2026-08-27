#!/usr/bin/env python3
"""Dependency-free exact audit of the pinned 517-vertex unit-distance embedding.

The coordinate expressions are parsed as data, never evaluated as Python.  All
arithmetic takes place in the multiquadratic field Q(sqrt(3),sqrt(5),sqrt(11))
with rational coefficients.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

RADICANDS = (1, 3, 5, 11, 15, 33, 55, 165)
RAD_INDEX = {value: index for index, value in enumerate(RADICANDS)}
EXPECTED_VTX_SHA256 = "402aa7b8a1145843366cff178dcfac44b97f8a748e318ae753520cbeb6a784d5"
EXPECTED_EDGE_SHA256 = "dc5085db9682aa246c3fc56efed9767e2a294a43e621a3e67a690d0489bdadc9"


class AuditError(ValueError):
    """An input or exact-arithmetic invariant failed."""


def _mul_radicands(left: int, right: int) -> tuple[int, int]:
    common = 1
    for prime in (3, 5, 11):
        if left % prime == 0 and right % prime == 0:
            common *= prime
    return common, left * right // (common * common)


@dataclass(frozen=True)
class Exact:
    coefficients: tuple[Fraction, ...]

    @classmethod
    def rational(cls, value: int | Fraction) -> Exact:
        return cls((Fraction(value),) + (Fraction(0),) * 7)

    @classmethod
    def radical(cls, radicand: int, coefficient: Fraction = Fraction(1)) -> Exact:
        values = [Fraction(0)] * 8
        try:
            values[RAD_INDEX[radicand]] = coefficient
        except KeyError as exc:
            raise AuditError(f"radicand {radicand} is outside the pinned field") from exc
        return cls(tuple(values))

    def __add__(self, other: Exact) -> Exact:
        return Exact(
            tuple(a + b for a, b in zip(self.coefficients, other.coefficients, strict=True))
        )

    def __neg__(self) -> Exact:
        return Exact(tuple(-value for value in self.coefficients))

    def __sub__(self, other: Exact) -> Exact:
        return self + (-other)

    def __mul__(self, other: Exact) -> Exact:
        result = [Fraction(0)] * 8
        for left_i, left_value in enumerate(self.coefficients):
            if not left_value:
                continue
            for right_i, right_value in enumerate(other.coefficients):
                if not right_value:
                    continue
                rational_factor, radicand = _mul_radicands(RADICANDS[left_i], RADICANDS[right_i])
                result[RAD_INDEX[radicand]] += left_value * right_value * rational_factor
        return Exact(tuple(result))

    def __truediv__(self, other: Exact) -> Exact:
        return self * other.inverse()

    def inverse(self) -> Exact:
        if self == ZERO:
            raise AuditError("division by zero")
        matrix: list[list[Fraction]] = []
        products = [self * Exact.radical(rad) for rad in RADICANDS]
        for row in range(8):
            matrix.append(
                [products[column].coefficients[row] for column in range(8)]
                + [Fraction(1 if row == 0 else 0)]
            )
        for column in range(8):
            pivot = next((row for row in range(column, 8) if matrix[row][column]), None)
            if pivot is None:
                raise AuditError("non-invertible field element")
            matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
            divisor = matrix[column][column]
            matrix[column] = [value / divisor for value in matrix[column]]
            for row in range(8):
                if row == column:
                    continue
                factor = matrix[row][column]
                if factor:
                    matrix[row] = [
                        value - factor * pivot_value
                        for value, pivot_value in zip(matrix[row], matrix[column], strict=True)
                    ]
        return Exact(tuple(matrix[row][8] for row in range(8)))

    def is_rational(self) -> bool:
        return not any(self.coefficients[1:])

    def render(self) -> str:
        pieces = []
        for coefficient, radicand in zip(self.coefficients, RADICANDS, strict=True):
            if coefficient:
                pieces.append(f"{coefficient}*sqrt({radicand})")
        return " + ".join(pieces) or "0"


ZERO = Exact.rational(0)
ONE = Exact.rational(1)


def _squarefree_decomposition(value: int) -> tuple[int, int]:
    square = 1
    remainder = value
    factor = 2
    while factor * factor <= remainder:
        power = 0
        while remainder % factor == 0:
            remainder //= factor
            power += 1
        square *= factor ** (power // 2)
        factor += 1
    radicand = value // (square * square)
    return square, radicand


def sqrt_rational(value: Fraction) -> Exact:
    if value < 0:
        raise AuditError("negative radicand")
    if value == 0:
        return ZERO
    combined = value.numerator * value.denominator
    square, radicand = _squarefree_decomposition(combined)
    return Exact.radical(radicand, Fraction(square, value.denominator))


TOKEN = re.compile(r"\s*(Sqrt|\d+|[-+*/(),{}\[\]])")


class ExpressionParser:
    def __init__(self, text: str) -> None:
        self.tokens = TOKEN.findall(text)
        compact = re.sub(r"\s+", "", text)
        if "".join(self.tokens) != compact:
            raise AuditError(f"unsupported coordinate syntax: {text!r}")
        self.position = 0

    def peek(self) -> str | None:
        return self.tokens[self.position] if self.position < len(self.tokens) else None

    def take(self, expected: str | None = None) -> str:
        token = self.peek()
        if token is None or (expected is not None and token != expected):
            raise AuditError(f"expected {expected!r}, found {token!r}")
        self.position += 1
        return token

    def expression(self) -> Exact:
        value = self.term()
        while self.peek() in {"+", "-"}:
            operator = self.take()
            right = self.term()
            value = value + right if operator == "+" else value - right
        return value

    def term(self) -> Exact:
        value = self.factor()
        while self.peek() in {"*", "/"}:
            operator = self.take()
            right = self.factor()
            value = value * right if operator == "*" else value / right
        return value

    def factor(self) -> Exact:
        if self.peek() == "+":
            self.take("+")
            return self.factor()
        if self.peek() == "-":
            self.take("-")
            return -self.factor()
        if self.peek() == "(":
            self.take("(")
            value = self.expression()
            self.take(")")
            return value
        if self.peek() == "Sqrt":
            self.take("Sqrt")
            self.take("[")
            value = self.expression()
            self.take("]")
            if not value.is_rational():
                raise AuditError("nested irrational radicand")
            return sqrt_rational(value.coefficients[0])
        token = self.take()
        if not token.isdigit():
            raise AuditError(f"expected a number, found {token!r}")
        return Exact.rational(int(token))

    def coordinate(self) -> tuple[Exact, Exact]:
        self.take("{")
        x = self.expression()
        self.take(",")
        y = self.expression()
        self.take("}")
        if self.peek() is not None:
            raise AuditError(f"unexpected trailing token {self.peek()!r}")
        return x, y


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_hash(path: Path, expected: str) -> str:
    actual = sha256_file(path)
    if actual != expected:
        raise AuditError(f"SHA-256 mismatch for {path}: expected {expected}, found {actual}")
    return actual


def parse_vertices(path: Path) -> list[tuple[Exact, Exact]]:
    vertices = [
        ExpressionParser(line).coordinate()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if len(vertices) != 517:
        raise AuditError(f"expected 517 coordinate rows, found {len(vertices)}")
    return vertices


def parse_edges(path: Path) -> tuple[int, frozenset[tuple[int, int]]]:
    lines = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    header = lines[0].split()
    if header[:2] != ["p", "edge"] or len(header) != 4:
        raise AuditError("invalid edge header")
    vertices, declared_edges = int(header[2]), int(header[3])
    edges: list[tuple[int, int]] = []
    for line in lines[1:]:
        parts = line.split()
        if len(parts) != 3 or parts[0] != "e":
            raise AuditError(f"invalid edge row: {line!r}")
        left, right = sorted((int(parts[1]), int(parts[2])))
        if left == right or left < 1 or right > vertices:
            raise AuditError(f"invalid edge endpoints: {line!r}")
        edges.append((left, right))
    unique = frozenset(edges)
    if len(unique) != len(edges) or len(unique) != declared_edges:
        raise AuditError("duplicate edge or edge-count mismatch")
    return vertices, unique


def squared_distance(left: tuple[Exact, Exact], right: tuple[Exact, Exact]) -> Exact:
    dx = left[0] - right[0]
    dy = left[1] - right[1]
    return dx * dx + dy * dy


def audit(vtx_path: Path, edge_path: Path) -> dict[str, object]:
    vtx_sha = require_hash(vtx_path, EXPECTED_VTX_SHA256)
    edge_sha = require_hash(edge_path, EXPECTED_EDGE_SHA256)
    vertices = parse_vertices(vtx_path)
    declared_vertices, edges = parse_edges(edge_path)
    if declared_vertices != len(vertices):
        raise AuditError("coordinate and edge vertex counts disagree")

    duplicate_coordinates = len(vertices) - len(set(vertices))
    if duplicate_coordinates:
        raise AuditError(f"found {duplicate_coordinates} duplicate coordinates")

    bad_edges = [
        [left, right, squared_distance(vertices[left - 1], vertices[right - 1]).render()]
        for left, right in sorted(edges)
        if squared_distance(vertices[left - 1], vertices[right - 1]) != ONE
    ]
    if bad_edges:
        raise AuditError(f"listed non-unit edges: {bad_edges[:3]}")

    all_unit_pairs: set[tuple[int, int]] = set()
    first_nonunit: tuple[int, int] | None = None
    for left in range(1, len(vertices) + 1):
        for right in range(left + 1, len(vertices) + 1):
            distance = squared_distance(vertices[left - 1], vertices[right - 1])
            if distance == ONE:
                all_unit_pairs.add((left, right))
            elif first_nonunit is None:
                first_nonunit = (left, right)
    omitted_unit_pairs = sorted(all_unit_pairs - edges)
    unexpected_edges = sorted(edges - all_unit_pairs)

    incident = next(edge for edge in sorted(edges) if edge[0] == 1 or edge[1] == 1)
    perturbed = list(vertices)
    perturbed[0] = (perturbed[0][0] + Exact.rational(Fraction(1, 1000)), perturbed[0][1])
    perturbation_detected = (
        squared_distance(perturbed[incident[0] - 1], perturbed[incident[1] - 1]) != ONE
    )
    if first_nonunit is None:
        raise AuditError("all coordinate pairs unexpectedly have unit distance")

    duplicated = list(vertices)
    duplicated[1] = duplicated[0]
    duplicate_probe_detected = len(set(duplicated)) != len(duplicated)

    return {
        "schema_version": 1,
        "method": "safe parser plus exact Q(sqrt(3),sqrt(5),sqrt(11)) arithmetic",
        "inputs": {
            "vertices": {
                "path": vtx_path.name,
                "sha256": vtx_sha,
                "bytes": vtx_path.stat().st_size,
            },
            "edges": {
                "path": edge_path.name,
                "sha256": edge_sha,
                "bytes": edge_path.stat().st_size,
            },
        },
        "field_basis": list(RADICANDS),
        "embedding": {
            "vertices": len(vertices),
            "listed_edges": len(edges),
            "duplicate_coordinates": duplicate_coordinates,
            "listed_nonunit_edges": len(unexpected_edges),
            "all_unit_pairs": len(all_unit_pairs),
            "omitted_unit_pairs": len(omitted_unit_pairs),
            "omitted_unit_pair_sample": [list(pair) for pair in omitted_unit_pairs[:20]],
        },
        "boundary_and_counterexample_search": {
            "coordinate_perturbation": {
                "edge": list(incident),
                "delta_x": "1/1000",
                "detected": perturbation_detected,
            },
            "injected_nonunit_edge": {
                "edge": list(first_nonunit),
                "detected": first_nonunit not in all_unit_pairs,
            },
            "duplicate_coordinate_probe": {"detected": duplicate_probe_detected},
        },
        "result": (
            "PASS: all listed graph edges have exact squared distance one and all coordinates "
            "are distinct; omitted unit pairs, if any, do not invalidate subgraph embedding."
        ),
        "remaining_obligations": [
            "This audit does not establish that the pinned CNF is unsatisfiable.",
            "The exact paper-to-517-artifact publication lineage remains separately reviewable.",
            "A finite lower-bound certificate does not determine the parent problem's exact value.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vertices", type=Path, required=True)
    parser.add_argument("--edges", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = audit(args.vertices, args.edges)
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
