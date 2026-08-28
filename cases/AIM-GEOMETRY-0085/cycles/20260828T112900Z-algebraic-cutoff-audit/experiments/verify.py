"""Independent rational Sturm and radial-Laplacian checker."""

import argparse
import copy
import hashlib
import itertools
import json
import math
from fractions import Fraction as F
from pathlib import Path


def packed(x):
    return (json.dumps(x, sort_keys=True, separators=(",", ":")) + "\n").encode()


def trim(p):
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def value(p, x):
    return sum(a * x**i for i, a in enumerate(p))


def derivative(p):
    return [i * p[i] for i in range(1, len(p))] or [F(0)]


def remainder(a, b):
    a = list(a)
    while len(a) >= len(b) and a != [0]:
        k, factor = len(a) - len(b), a[-1] / b[-1]
        for j in range(len(b)):
            a[j + k] -= factor * b[j]
        trim(a)
    return a


def sturm(p):
    seq = [p, derivative(p)]
    while seq[-1] != [0]:
        r = [-x for x in remainder(seq[-2], seq[-1])]
        if r == [0]:
            break
        seq.append(r)
    return seq


def variation(seq, x):
    vals = [p[-1] if x is None else value(p, x) for p in seq]
    signs = [1 if v > 0 else -1 for v in vals if v]
    return sum(a != b for a, b in itertools.pairwise(signs))


def roots(seq, a, b):
    return variation(seq, a) - variation(seq, b)


def radial(p, m):
    q = [F(0)] * (len(p) + 1)
    for k, a in enumerate(p):
        if k:
            q[k - 1] -= a * k * (k - 1 + m)
        q[k] += a * (2 * k + m)
        q[k + 1] -= a
    return trim(q)


def transform(p, m):
    out, basis = [F(0)] * len(p), [F(1)]
    for a in p:
        for j, b in enumerate(basis):
            out[j] += a * b
        basis = radial(basis, m)
    return trim(out)


def compute(spec):
    p = list(map(F, spec["P"]))
    q = list(map(F, spec["Q"]))
    chain = sturm(p)
    # Adversarial and boundary checks precede the census and certificate read.
    assert value(p, F(14)) == 211 and value(p, F(15)) == -30
    assert value(q, F(15)) == 0
    assert roots(sturm(list(map(F, [6, -11, 6, -1]))), F(0), F(4)) == 3
    assert roots(sturm(list(map(F, [1, -2, 1]))), F(0), F(2)) == 1
    assert roots(chain, F(0), None) == 1
    assert transform(p, 12) == q and transform(q, 12) == p
    rows = []
    for bits in spec["bit_depths"]:
        scale = 2**bits
        left, right = 14 * scale, 15 * scale
        while right - left > 1:
            mid = (left + right) // 2
            if roots(chain, F(0), F(mid, scale)) == 0:
                left = mid
            else:
                right = mid
        lo, hi = F(left, scale), F(right, scale)
        nearest = lo if roots(chain, F(0), (lo + hi) / 2) else hi
        assert roots(chain, lo, hi) == 1 and roots(chain, hi, None) == 0
        assert value(p, lo) > 0 > value(p, hi)
        rows.append(
            [
                bits,
                str(lo),
                str(hi),
                str(value(p, lo)),
                str(value(p, hi)),
                str(nearest),
                value(p, nearest) < 0,
            ]
        )
    final = next(r for r in rows if r[0] == spec["final_bits"])
    lo, hi = F(final[1]), F(final[2])
    denom = 2 ** spec["dimension"] * math.factorial(spec["dimension"] // 2)
    upper, lower = hi**12 / denom, lo**12 / denom
    summary = dict(
        rows=len(rows),
        table_sha256=hashlib.sha256(packed(rows)).hexdigest(),
        lower_cutoffs_rejected=len(rows),
        nearest_cutoffs_rejected=sum(not r[6] for r in rows),
        final_interval=[str(lo), str(hi)],
        objective_interval=[str(lower), str(upper)],
        ratio_to_prior=str(upper / (F(spec["prior_cutoff"]) ** 12 / denom)),
    )
    return summary, rows, chain


def accepts(cert, spec):
    try:
        if (
            cert["dimension"] != spec["dimension"]
            or cert["P"] != spec["P"]
            or cert["Q"] != spec["Q"]
        ):
            return False
        p = list(map(F, cert["P"]))
        chain = sturm(p)
        lo, hi = map(F, cert["interval"])
        if not 0 < lo < hi or hi - lo != F(1, 2 ** spec["final_bits"]):
            return False
        if value(p, lo) <= 0 or value(p, hi) >= 0:
            return False
        if (
            cert["positive_root_count"] != roots(chain, F(0), None)
            or cert["positive_root_count"] != 1
        ):
            return False
        if roots(chain, lo, hi) != 1 or roots(chain, hi, None):
            return False
        denom = 2 ** cert["dimension"] * math.factorial(cert["dimension"] // 2)
        return F(cert["objective_upper"]) == hi**12 / denom
    except (KeyError, TypeError, ValueError, ZeroDivisionError):
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path)
    ap.add_argument("output", type=Path)
    ap.add_argument("--certificate", type=Path)
    args = ap.parse_args()
    spec = json.loads(args.input.read_text())
    summary, rows, chain = compute(spec)
    out = summary
    if args.certificate:
        proposed = json.loads(args.certificate.read_text())
        assert proposed["summary"] == summary
        cert = proposed["certificate"]
        assert accepts(cert, spec)
        changes = [
            ("dimension", 22),
            ("P", [224, 13, 13, -1]),
            ("Q", [224, 195, -29, 1]),
            ("interval", list(reversed(cert["interval"]))),
            ("interval", [cert["interval"][0], cert["interval"][0]]),
            ("objective_upper", str(F(cert["objective_upper"]) - F(1, 10**12))),
            ("positive_root_count", 0),
        ]
        rejected = []
        for i, (field, val) in enumerate(changes):
            bad = copy.deepcopy(cert)
            bad[field] = val
            assert not accepts(bad, spec)
            rejected.append([i, field])
        out = dict(
            summary=summary,
            sturm_sequence=[[str(c) for c in p] for p in chain],
            positive_roots=roots(chain, F(0), None),
            corrupted_certificates_rejected=rejected,
            certificate_accepted=True,
            independence=(
                "Baseline authored/run before theory; generic Sturm counts and radial Laplacian "
                "differ from monotone Horner bisection and Laguerre coefficients. "
                "Same-assistant authorship; no independent human/model/kernel review.exclusive."
            ),
        )
        args.output.with_name("verification-table.json").write_bytes(packed(rows))
    args.output.write_bytes(packed(out))
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
