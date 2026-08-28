"""Monotone-tail isolation with exact directed rounding, no Sturm code."""

import hashlib
import json
import math
import sys
from fractions import Fraction as F
from pathlib import Path


def packed(x):
    return (json.dumps(x, sort_keys=True, separators=(",", ":")) + "\n").encode()


def horner(p, x):
    y = F(0)
    for a in reversed(p):
        y = y * x + a
    return y


def transform(p, m):
    return [
        sum(
            F(a * math.factorial(k) * (-1) ** j * math.comb(k + m - 1, k - j), math.factorial(j))
            for k, a in enumerate(p)
            if k >= j
        )
        for j in range(len(p))
    ]


def main():
    spec = json.loads(Path(sys.argv[1]).read_text())
    output = Path(sys.argv[2])
    p, q = spec["P"], spec["Q"]
    assert transform(q, 12) == list(map(F, p))
    assert transform(p, 12) == list(map(F, q))
    assert p == [225, 13, 13, -1] and q == [225, 195, -29, 1]
    # For u<=13 all P terms grouped as 225+13u+u^2(13-u) are positive.
    # P'<0 on [13,infinity) since P'(13)=-156 and P''(u)=26-6u<0.
    assert horner(p, F(14)) > 0 > horner(p, F(15))
    rows = []
    for bits in spec["bit_depths"]:
        lo, hi = map(F, spec["initial_bracket"])
        for _ in range(bits):
            mid = (lo + hi) / 2
            sign = horner(p, mid)
            assert sign != 0  # A monic integral cubic has no nonintegral rational root.
            if sign > 0:
                lo = mid
            else:
                hi = mid
        nearest = hi if horner(p, (lo + hi) / 2) > 0 else lo
        rows.append(
            [
                bits,
                str(lo),
                str(hi),
                str(horner(p, lo)),
                str(horner(p, hi)),
                str(nearest),
                horner(p, nearest) < 0,
            ]
        )
    final = next(r for r in rows if r[0] == spec["final_bits"])
    lo, hi = map(F, final[1:3])
    m = spec["dimension"] // 2
    denominator = 4**m * math.factorial(m)
    lower, upper = lo**m / denominator, hi**m / denominator
    ratio = upper / (F(spec["prior_cutoff"]) ** m / denominator)
    summary = dict(
        rows=len(rows),
        table_sha256=hashlib.sha256(packed(rows)).hexdigest(),
        lower_cutoffs_rejected=len(rows),
        nearest_cutoffs_rejected=sum(not r[6] for r in rows),
        final_interval=[str(lo), str(hi)],
        objective_interval=[str(lower), str(upper)],
        ratio_to_prior=str(ratio),
    )
    cert = dict(
        dimension=spec["dimension"],
        P=p,
        Q=q,
        interval=summary["final_interval"],
        positive_root_count=1,
        objective_upper=str(upper),
    )
    assert ratio < F(183, 200)  # At least 8.5 percent below the specified old bound.
    output.with_name("theory-table.json").write_bytes(packed(rows))
    output.write_bytes(packed(dict(summary=summary, certificate=cert)))
    print(
        json.dumps(
            dict(
                interval=summary["final_interval"],
                nearest_failures=summary["nearest_cutoffs_rejected"],
                improvement_more_than_percent="8.5",
            )
        )
    )


if __name__ == "__main__":
    main()
