"""Literal canonical-weight obstruction; cocycle and separating functional."""

import argparse
import copy
import json
from pathlib import Path


def dot(a, b):
    return sum(x * y for x, y in zip(a, b, strict=True))


def valid(c):
    n = c["n"]
    x, y = c["weight"]
    # Canonical D=-2S-(n+2)F; all four local ray inequalities fail.
    if not all(t < 0 for t in [y - 2, x - n - 2, -y, -x + n * y]):
        return False
    boundaries = [[-1, 0, 1, 0], [0, 1, 0, -1]]
    d = [-1, 1, -1, 1]
    v = c["cocycle"]
    functional = c["functional"]
    if len(v) != 4 or len(functional) != 4 or dot(d, v):
        return False
    return all(dot(functional, b) == 0 for b in boundaries) and dot(functional, v) != 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--certificate", required=True)
    args = ap.parse_args()
    spec = json.loads(Path(args.input).read_text())
    # Start with a non-boundary top cocycle before reading the proposal.
    certs = [
        dict(n=n, weight=[n + 1, 1], cocycle=[1, 1, 0, 0], functional=[1, 0, 1, 0])
        for n in spec["twists"]
    ]
    assert all(valid(c) for c in certs)
    prop = json.loads(Path(args.certificate).read_text())["source_boundary"]
    assert len(prop) == len(certs)
    for c, r in zip(certs, prop, strict=True):
        assert r["n"] == c["n"] and r["canonical"]["betti"][2] >= 1
    rejected = []
    for name in ["weight", "zero", "not_closed", "not_separator"]:
        c = copy.deepcopy(certs[2])
        if name == "weight":
            c["weight"] = [0, 0]
        if name == "zero":
            c["cocycle"] = [0] * 4
        if name == "not_closed":
            c["cocycle"] = [1, 0, 0, 0]
        if name == "not_separator":
            c["functional"] = [0] * 4
        assert not valid(c), name
        rejected.append(name)
    result = dict(canonical_nonzero_certificates=certs, corruptions_rejected=rejected)
    Path(args.output).write_text(json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n")
    print(json.dumps(dict(certificates=len(certs), corruptions_rejected=len(rejected))))


if __name__ == "__main__":
    main()
