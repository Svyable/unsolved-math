"""Closed cyclic-group formulas, distinct from the direct group verifier."""
import json
import sys
from pathlib import Path


def valuation(d, p):
    k = 0
    while d % p == 0:
        k += 1
        d //= p
    return k


def calculate(s):
    rows = []
    for p in s['primes']:
        for cap in [0, 2]:
            for n in range(1, s['max_level'] + 1):
                e = min(n, cap) if cap else n
                old = min(n - 1, cap) if cap else n - 1
                counts = {'1': 1}
                counts.update({str(p ** k): (p - 1) * p ** (k - 1)
                               for k in range(1, e + 1)})
                rows.append(dict(p=p, cap=cap, n=n, cardinality=p ** e,
                                 exponent=p ** e, order_counts=counts,
                                 fiber_size=p ** (e - old), unit_path=[1] * n))
    witnesses = [[p, d, valuation(d, p) + 1, d % (p ** (valuation(d, p) + 1))]
                 for p in s['primes'] for d in range(1, s['max_denominator'] + 1)]
    escapes = [[p, k, k + 1, p ** k, p ** k]
               for p in s['primes'] for k in range(s['max_power'] + 1)]
    return dict(rows=rows, denominator_witnesses=witnesses, exponent_escapes=escapes,
                finite_elements_checked=sum(r['cardinality'] for r in rows))


if __name__ == '__main__':
    spec = json.loads(Path(sys.argv[1]).read_text())
    core = calculate(spec)
    Path(sys.argv[2]).write_text(json.dumps(dict(core=core), sort_keys=True, indent=2) + '\n')
    print(json.dumps(dict(rows=len(core['rows']), witnesses=len(core['denominator_witnesses']))))
