"""Verifier-first toric affine-cover Cech matrices and exact weight inequalities."""

import argparse
import copy
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path


def encoded(x):
    return (json.dumps(x, sort_keys=True, separators=(",", ":")) + "\n").encode()


def rank(mat):
    rows = [[Fraction(x) for x in r] for r in mat]
    k = 0
    for j in range(len(rows[0]) if rows else 0):
        i = next((i for i in range(k, len(rows)) if rows[i][j]), None)
        if i is None:
            continue
        rows[k], rows[i] = rows[i], rows[k]
        c = rows[k][j]
        rows[k] = [x / c for x in rows[k]]
        for i in range(k + 1, len(rows)):
            c = rows[i][j]
            rows[i] = [x - c * y for x, y in zip(rows[i], rows[k], strict=True)]
        k += 1
    return k


def complex_for(mask):
    cones = [{i, (i + 1) % 4} for i in range(4)]
    bad = {i for i in range(4) if mask >> i & 1}
    faces = []
    for q in range(4):
        faces.append(
            [
                list(s)
                for s in itertools.combinations(range(4), q + 1)
                if not set.intersection(*(cones[i] for i in s)) & bad
            ]
        )
    ds = []
    for q in range(3):
        mat = []
        for t in faces[q + 1]:
            row = [0] * len(faces[q])
            for j in range(len(t)):
                sub = t[:j] + t[j + 1 :]
                if sub in faces[q]:
                    row[faces[q].index(sub)] = (-1) ** j
            mat.append(row)
        ds.append(mat)
    for q in range(2):
        for row in ds[q + 1]:
            for col in zip(*ds[q], strict=True):
                assert sum(x * y for x, y in zip(row, col, strict=True)) == 0
    ranks = [0, *(rank(d) for d in ds), 0]
    betti = [len(faces[q]) - ranks[q] - ranks[q + 1] for q in range(4)]
    return dict(mask=mask, faces=faces, differentials=ds, ranks=ranks[1:-1], betti=betti)


def negative_mask(n, a, b, x, y):
    values = [y + a, x + b, -y, -x + n * y]
    return sum(1 << i for i, v in enumerate(values) if v < 0)


def weight_classes(n, a, b, patterns):
    result = []
    for c in patterns:
        if not any(c["betti"]):
            continue
        mask = c["mask"]
        # Nonacyclic masks must put opposite truth values on the two y rays.
        # Their inequalities then bound y on both sides, with no lattice cutoff.
        lowers, uppers = [], []
        (uppers if mask & 1 else lowers).append(-a - 1 if mask & 1 else -a)
        (lowers if mask & 4 else uppers).append(1 if mask & 4 else 0)
        assert lowers and uppers
        for y in range(max(lowers), min(uppers) + 1):
            xl, xu = [], []
            (xu if mask & 2 else xl).append(-b - 1 if mask & 2 else -b)
            (xl if mask & 8 else xu).append(n * y + 1 if mask & 8 else n * y)
            assert xl and xu
            for x in range(max(xl), min(xu) + 1):
                assert negative_mask(n, a, b, x, y) == mask
                for q, dim in enumerate(c["betti"]):
                    assert dim in [0, 1]
                    if dim:
                        result.append([q, x, y])
    return sorted(result)


def row(n, a, b, patterns):
    weights = weight_classes(n, a, b, patterns)
    dims = [sum(w[0] == q for w in weights) for q in range(3)]
    assert not any(w[0] == 3 for w in weights)
    return dict(n=n, a=a, b=b, betti=dims, chi=dims[0] - dims[1] + dims[2]), weights


def valid(certs, spec, patterns):
    if len(certs) != len(spec["certificates"]):
        return False
    for cert, params in zip(certs, spec["certificates"], strict=True):
        if [cert[k] for k in ["n", "a", "b"]] != params:
            return False
        expected, weights = row(*params, patterns)
        if cert["betti"] != expected["betti"]:
            return False
        classes = cert["classes"]
        if sorted([c["q"], *c["weight"]] for c in classes) != weights:
            return False
        for c in classes:
            q = c["q"]
            x, y = c["weight"]
            z = patterns[negative_mask(*params, x, y)]
            v = c["vector"]
            if len(v) != len(z["faces"][q]) or any(not isinstance(t, int) for t in v):
                return False
            if any(sum(t * u for t, u in zip(r, v, strict=True)) for r in z["differentials"][q]):
                return False
            boundary = z["differentials"][q - 1] if q else [[] for _ in v]
            joined = [[*r, t] for r, t in zip(boundary, v, strict=True)]
            if rank(joined) != rank(boundary) + 1:
                return False
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--certificate")
    args = ap.parse_args()
    spec = json.loads(Path(args.input).read_text())
    patterns = [complex_for(m) for m in range(16)]
    # Counterexample and boundary search before census or certificate reading.
    controls = [
        row(*v, patterns)[0]
        for v in [(2, 1, 0), (2, 1, -1), (0, 1, -1), (2, -1, 100), (2, -2, -4), (2, -2, -3)]
    ]
    assert [c["betti"] for c in controls] == [
        [1, 1, 0],
        [0, 2, 0],
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 1],
        [0, 0, 0],
    ]
    rows = []
    digest = hashlib.sha256()
    count = 0
    for n in spec["twists"]:
        for a in range(spec["a_range"][0], spec["a_range"][1] + 1):
            for b in range(spec["b_range"][0], spec["b_range"][1] + 1):
                r, weights = row(n, a, b, patterns)
                rows.append(r)
                digest.update(encoded(r))
                count += len(weights)
    summary = dict(
        cases=len(rows),
        rows_sha256=digest.hexdigest(),
        immaculate=sum(not any(r["betti"]) for r in rows),
        euler_false_acceptances=sum(r["chi"] == 0 and any(r["betti"]) for r in rows),
        base_window_false_acceptances=sum(r["b"] == -1 and any(r["betti"]) for r in rows),
        controls=controls,
    )
    output = dict(summary=summary, patterns=patterns, nonzero_weight_classes=count)
    if args.certificate:
        prop = json.loads(Path(args.certificate).read_text())
        assert prop["summary"] == summary
        assert valid(prop["certificates"], spec, patterns)
        failures = []
        for name in ["missing", "weight", "zero", "noncocycle", "dimension", "twist", "duplicate"]:
            bad = copy.deepcopy(prop["certificates"])
            if name == "missing":
                bad[0]["classes"].pop()
            if name == "weight":
                bad[0]["classes"][1]["weight"] = [0, 0]
            if name == "zero":
                bad[0]["classes"][1]["vector"] = [0] * 4
            if name == "noncocycle":
                bad[0]["classes"][1]["vector"][0] = 2
            if name == "dimension":
                bad[0]["betti"] = [0, 0, 0]
            if name == "twist":
                bad[0]["n"] = 0
            if name == "duplicate":
                bad[0]["classes"].append(bad[0]["classes"][0])
            assert not valid(bad, spec, patterns), name
            failures.append(name)
        output.update(
            certificates_checked=len(prop["certificates"]),
            class_vectors_checked=sum(len(c["classes"]) for c in prop["certificates"]),
            corruptions_rejected=failures,
        )
    Path(args.output).write_bytes(encoded(output))
    print(
        json.dumps({k: v for k, v in output.items() if k not in ["patterns", "summary"]} | summary)
    )


if __name__ == "__main__":
    main()
