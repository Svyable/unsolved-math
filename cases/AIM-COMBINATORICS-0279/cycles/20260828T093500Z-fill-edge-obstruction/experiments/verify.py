"""Independent edge-set cycles, torso dynamic programming, and certificate checks."""

import argparse
import copy
import hashlib
import json
from itertools import combinations, product
from pathlib import Path


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":")) + "\n"


def build(lengths):
    # Build by extending individual paths, not modular rim-neighbor formulas.
    n = sum(lengths) + 1
    hub = n - 1
    edges = set()
    anchors = []
    cursor = 0
    for length in lengths:
        anchors.append(cursor)
        for _ in range(length):
            nxt = cursor + 1 if cursor + 1 < hub else 0
            edges.add(tuple(sorted((cursor, nxt))))
            cursor += 1
    edges.update((a, hub) for a in anchors)
    return n, edges


def adjacency(n, edges):
    a = [set() for _ in range(n)]
    for u, v in edges:
        a[u].add(v)
        a[v].add(u)
    return a


def cycles(n, edges):
    a = adjacency(n, edges)
    result = set()

    # Enumerate all simple cycles rooted at their least vertex; then test chords.
    def visit(path):
        for w in a[path[-1]]:
            if w == path[0] and len(path) >= 3:
                if path[1] < path[-1]:
                    m = set(path)
                    if all(len(a[v] & m) == 2 for v in m):
                        result.add(tuple(sorted(path)))
            elif w > path[0] and w not in path:
                visit([*path, w])

    for v in range(n):
        visit([v])
    return sorted(result)


def peel_width(n, edges, order):
    assert sorted(order) == list(range(n))
    a = adjacency(n, edges)
    remaining = set(range(n))
    width = 0
    for v in order:
        width = max(width, len(a[v] & remaining))
        remaining.remove(v)
    return width


def degeneracy(n, edges):
    a = adjacency(n, edges)
    active = set(range(n))
    answer = 0
    while active:
        # Batched core peeling, rather than minimum-degree vertex ordering.
        minimum = min(len(a[v] & active) for v in active)
        answer = max(answer, minimum)
        remove = {v for v in active if len(a[v] & active) == minimum}
        active -= remove
    return answer


def treewidth_dp(n, edges):
    a = adjacency(n, edges)
    dp = [n] * (1 << n)
    parent = [None] * (1 << n)
    dp[0] = 0
    transitions = 0
    for mask in range((1 << n) - 1):
        eliminated = {v for v in range(n) if mask >> v & 1}
        for v in range(n):
            if v in eliminated:
                continue
            # Filled neighbors are endpoints of paths whose interior is eliminated.
            seen = {v}
            pending = [v]
            boundary = set()
            while pending:
                u = pending.pop()
                for w in a[u]:
                    if w in seen:
                        continue
                    seen.add(w)
                    if w in eliminated:
                        pending.append(w)
                    else:
                        boundary.add(w)
            score = max(dp[mask], len(boundary))
            new = mask | (1 << v)
            transitions += 1
            if score < dp[new]:
                dp[new] = score
                parent[new] = (mask, v)
    order = []
    mask = (1 << n) - 1
    while mask:
        mask, v = parent[mask]
        order.append(v)
    return dp[-1], list(reversed(order)), transitions


def connected(vertices, edges):
    if not vertices:
        return False
    seen = {next(iter(vertices))}
    while True:
        grown = seen | {v for u, v in edges if u in seen and v in vertices}
        grown |= {u for u, v in edges if v in seen and u in vertices}
        if grown == seen:
            return seen == vertices
        seen = grown


def validate_certificate(cert):
    n, edges = build(cert["lengths"])
    assert cert["n"] == n and cert["edges"] == [list(e) for e in sorted(edges)]
    assert peel_width(n, edges, cert["peeling_order"]) == 2
    branches = [set(b) for b in cert["minor_branches"]]
    assert len(branches) == 4
    assert all(b <= set(range(n)) and connected(b, edges) for b in branches)
    assert sum(map(len, branches)) == len(set().union(*branches))
    for x, y in combinations(branches, 2):
        assert any((u in x and v in y) or (v in x and u in y) for u, v in edges)
    bags = [set(b) for b in cert["bags"]]
    links = {tuple(sorted(e)) for e in cert["bag_edges"]}
    assert bags and max(map(len, bags)) == 4
    assert all(b <= set(range(n)) for b in bags)
    assert len(links) == len(bags) - 1
    assert all(0 <= x < y < len(bags) for x, y in links)
    assert connected(set(range(len(bags))), links)
    assert set().union(*bags) == set(range(n))
    assert all(any(u in b and v in b for b in bags) for u, v in edges)
    for v in range(n):
        assert connected({i for i, b in enumerate(bags) if v in b}, links)


def reconstruct(spec):
    # Counterexample and boundary searches precede family confirmation.
    n, edges = build(spec["witness"])
    holes = cycles(n, edges)
    assert [len(h) for h in holes].count(5) == 3
    assert sorted(map(len, holes)) == [5, 5, 5, 9]
    tw, order, transitions = treewidth_dp(n, edges)
    deg = degeneracy(n, edges)
    assert (deg, tw) == (2, 3)
    controls = []
    for name, lengths in [
        ("triangle-sector", [1, 3, 3]),
        ("even-sector", [2, 3, 3]),
        ("even-rim", [3, 3, 3, 3]),
    ]:
        nn, ee = build(lengths)
        cc = cycles(nn, ee)
        controls.append([name, sorted(map(len, cc))])
    assert 3 in controls[0][1]
    assert 4 in controls[1][1]
    assert 12 in controls[2][1]
    four_cycle = {(0, 1), (1, 2), (2, 3), (0, 3)}
    assert treewidth_dp(4, four_cycle)[0] == 2
    assert treewidth_dp(4, set(combinations(range(4), 2)))[0] == 3
    rows = []
    eligible = 0
    for k in spec["spoke_counts"]:
        for lengths in product(spec["sector_lengths"], repeat=k):
            nn, ee = build(lengths)
            cc = cycles(nn, ee)
            tf = all(len(c) != 3 for c in cc)
            ehf = all(len(c) % 2 for c in cc if len(c) >= 4)
            dd = degeneracy(nn, ee)
            rows.append([list(lengths), nn, tf, ehf, sorted(map(len, cc)), dd])
            eligible += tf and ehf
    summary = dict(
        case_count=len(rows),
        eligible_count=eligible,
        table_sha256=hashlib.sha256(canonical(rows).encode()).hexdigest(),
        witness=dict(
            n=n,
            edges=[list(e) for e in sorted(edges)],
            holes=[list(h) for h in holes],
            degeneracy=deg,
            treewidth=tw,
        ),
        controls=controls,
    )
    return summary, dict(optimal_order=order, dp_states=1 << n, dp_transitions=transitions)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("--certificate")
    args = parser.parse_args()
    result, details = reconstruct(json.loads(Path(args.input).read_text()))
    output = result
    if args.certificate:
        certificate = json.loads(Path(args.certificate).read_text())
        assert certificate["summary"] == result
        certs = certificate["certificates"]
        assert len(certs) == result["eligible_count"]
        expected = [
            list(ls)
            for k in [3, 4, 5]
            for ls in product([2, 3, 4, 5], repeat=k)
            if k % 2 and all(x % 2 for x in ls)
        ]
        assert [c["lengths"] for c in certs] == expected
        for c in certs:
            validate_certificate(c)
        fixture = next(c for c in certs if c["lengths"] == [3, 3, 3])
        rejected = []
        for mode in range(7):
            bad = copy.deepcopy(fixture)
            if mode == 0:
                bad["edges"].pop()
            elif mode == 1:
                bad["peeling_order"][0] = bad["peeling_order"][1]
            elif mode == 2:
                bad["minor_branches"][0] = []
            elif mode == 3:
                bad["minor_branches"][1].append(bad["minor_branches"][0][0])
            elif mode == 4:
                bad["minor_branches"][1] = [1]
            elif mode == 5:
                bad["bags"][0].remove(0)
            else:
                bad["bag_edges"].pop()
            try:
                validate_certificate(bad)
            except AssertionError:
                rejected.append(mode)
            else:
                raise AssertionError(("bad certificate accepted", mode))
        output = dict(
            reconstructed=result,
            independent_details=details,
            checked_certificates=len(certs),
            rejected_mutations=rejected,
        )
    Path(args.output).write_text(canonical(output))
    print(
        json.dumps(
            dict(
                cases=result["case_count"],
                eligible=result["eligible_count"],
                witness=result["witness"],
                details=details,
            )
        )
    )


if __name__ == "__main__":
    main()
