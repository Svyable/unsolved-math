"""Post-search certificate audit against the fresh verifier's coverage digest."""

import hashlib
import json
from itertools import combinations
from pathlib import Path


def valid(row: dict) -> bool:
    n, mask = row["n"], row["mask"]
    if sorted(row["peel"]) != list(range(n)):
        return False
    remaining = set(range(n))
    edges = [e for i, e in enumerate(combinations(range(n), 2)) if mask & (1 << i)]
    width = 0
    for vertex in row["peel"]:
        degree = sum(1 for u, v in edges if u in remaining and v in remaining and vertex in (u, v))
        width = max(width, degree)
        remaining.remove(vertex)
    return width == row["width"] and width <= 2


def main() -> None:
    folder = Path(__file__).parent
    raw = (folder / "peeling-certificates.jsonl").read_bytes()
    rows = [json.loads(line) for line in raw.splitlines()]
    # Wrong permutation and a center-first star ordering must fail before checking positives.
    duplicate = {"n": 2, "mask": 1, "peel": [0, 0], "width": 1}
    center_first = {"n": 4, "mask": 7, "peel": [0, 1, 2, 3], "width": 2}
    assert not valid(duplicate) and not valid(center_first)
    assert len({(r["n"], r["mask"]) for r in rows}) == len(rows)
    assert all(valid(row) for row in rows)
    digest = hashlib.sha256()
    for row in rows:
        digest.update(
            json.dumps(
                [row["n"], row["mask"], row["chi"], row["width"]], separators=(",", ":")
            ).encode()
        )
    independent = json.loads((folder / "verification-output.json").read_bytes())
    assert len(rows) == independent["eligible_graphs"]
    assert digest.hexdigest() == independent["classification_sha256"]
    print(
        json.dumps(
            {
                "orders_validated": len(rows),
                "certificate_sha256": hashlib.sha256(raw).hexdigest(),
                "coverage_digest_matches_fresh_enumeration": True,
                "duplicate_order_detected": True,
                "bad_star_order_detected": True,
                "scope": (
                    "This post-search phase reads theory certificates "
                    "only after independent enumeration."
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
