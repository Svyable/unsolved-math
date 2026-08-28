"""Sector formulas, degree peeling, and explicit minor/path-decomposition witnesses."""

import hashlib
import json
import sys
from itertools import combinations, product
from pathlib import Path


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":")) + "\n"


def model(lengths):
    rim = sum(lengths)
    anchors = [sum(lengths[:i]) for i in range(len(lengths))]
    edges = {tuple(sorted((i, (i + 1) % rim))) for i in range(rim)}
    edges |= {(a, rim) for a in anchors}
    return rim + 1, edges, anchors


def predicted_cycles(lengths):
    rim = sum(lengths)
    starts = [sum(lengths[:i]) for i in range(len(lengths))]
    cycles = [tuple(range(rim))]
    for a, length in zip(starts, lengths, strict=True):
        cycles.append(tuple(sorted([rim, *((a + j) % rim for j in range(length + 1))])))
    return sorted(cycles)


def peel(n, edges):
    active = set(range(n))
    order = []
    max_degree = 0
    while active:
        degrees = {v: sum(v in e and set(e) <= active for e in edges) for v in active}
        v = min(active, key=lambda x: (degrees[x], x))
        max_degree = max(max_degree, degrees[v])
        order.append(v)
        active.remove(v)
    return order, max_degree


def certify(lengths):
    n, edges, anchors = model(lengths)
    order, degree = peel(n, edges)
    assert degree == 2
    rim = n - 1
    branches = [
        [rim],
        list(range(anchors[1])),
        list(range(anchors[1], anchors[2])),
        list(range(anchors[2], rim)),
    ]
    bags = [[rim, 0, i, i + 1] for i in range(1, rim - 1)]
    return dict(
        lengths=list(lengths),
        n=n,
        edges=[list(e) for e in sorted(edges)],
        peeling_order=order,
        minor_branches=branches,
        bags=bags,
        bag_edges=[[i, i + 1] for i in range(len(bags) - 1)],
    )


def fill_trace(cert):
    active = set(range(cert["n"]))
    edges = {tuple(e) for e in cert["edges"]}
    steps = []
    for v in cert["peeling_order"]:
        neighbors = sorted(w for w in active if tuple(sorted((v, w))) in edges)
        fill = {tuple(e) for e in combinations(neighbors, 2)} - edges
        steps.append(
            dict(
                vertex=v,
                neighbors=neighbors,
                degree=len(neighbors),
                added_edges=[list(e) for e in sorted(fill)],
            )
        )
        edges |= fill
        active.remove(v)
    return steps


def main():
    spec = json.loads(Path(sys.argv[1]).read_text())
    assert spec["spoke_counts"] == [3, 4, 5]
    assert spec["sector_lengths"] == [2, 3, 4, 5]
    rows = []
    certs = []
    for k in spec["spoke_counts"]:
        for lengths in product(spec["sector_lengths"], repeat=k):
            n, edges, _ = model(lengths)
            _, deg = peel(n, edges)
            holes = predicted_cycles(lengths)
            tf = min(lengths) >= 2
            ehf = all(length % 2 for length in lengths) and k % 2 == 1
            assert ehf == all(len(h) % 2 for h in holes)
            rows.append([list(lengths), n, tf, ehf, sorted(map(len, holes)), deg])
            if ehf:
                certs.append(certify(lengths))
    witness = certify(spec["witness"])
    trace = fill_trace(witness)
    assert max(s["degree"] for s in trace) == 3
    controls = [
        [name, sorted(map(len, predicted_cycles(lengths)))]
        for name, lengths in [
            ("triangle-sector", [1, 3, 3]),
            ("even-sector", [2, 3, 3]),
            ("even-rim", [3, 3, 3, 3]),
        ]
    ]
    summary = dict(
        case_count=len(rows),
        eligible_count=len(certs),
        table_sha256=hashlib.sha256(canonical(rows).encode()).hexdigest(),
        witness=dict(
            n=witness["n"],
            edges=witness["edges"],
            holes=[list(h) for h in predicted_cycles(spec["witness"])],
            degeneracy=2,
            treewidth=3,
        ),
        controls=controls,
    )
    out = Path(sys.argv[2])
    out.write_text(canonical(dict(summary=summary, certificates=certs)))
    out.with_name("theory-table.json").write_text(canonical(rows))
    out.with_name("fill-trace.json").write_text(canonical(trace))
    print(
        json.dumps(
            dict(
                summary=summary,
                peeling_order=witness["peeling_order"],
                first_overflow=next(s for s in trace if s["degree"] > 2),
            )
        )
    )


if __name__ == "__main__":
    main()
