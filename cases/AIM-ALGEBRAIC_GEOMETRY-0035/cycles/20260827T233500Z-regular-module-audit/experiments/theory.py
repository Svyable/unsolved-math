"""Nilpotent matrix powers and binomial change of basis."""
import json
import sys
from math import comb
from pathlib import Path


def multiply(a, b, p):
    d = len(a)
    return [[sum(a[i][k] * b[k][j] for k in range(d)) % p
             for j in range(d)] for i in range(d)]


def classify(nmat, p, q):
    d = len(nmat)
    powers = [[[int(i == j) for j in range(d)] for i in range(d)]]
    for _ in range(q):
        powers.append(multiply(powers[-1], nmat, p))
    if any(any(row) for row in powers[q]):
        return None
    top = any(any(row) for row in powers[q - 1])
    weak = any(any(row) for row in powers[q - 2])
    generator = next((j for j in range(d)
                      if d == q and any(powers[q - 1][i][j] for i in range(d))), None)
    basis = []
    if generator is not None:
        for k in range(q):
            basis.append([sum(comb(k, t) * powers[t][i][generator]
                              for t in range(k + 1)) % p for i in range(d)])
    return dict(top=top, weak=weak, regular=d == q and top,
                generator=generator, orbit_basis_columns=basis)


def calculate(s):
    groups = []
    for c in s['exhaustive']:
        p, q, d = c['p'], c['q'], c['d']
        rows = []
        for code in range(p ** (d * d)):
            digits = [(code // p ** k) % p for k in reversed(range(d * d))]
            mat = [digits[j * d:(j + 1) * d] for j in range(d)]
            value = classify(mat, p, q)
            if value is not None:
                rows.append(dict(code=code, **value))
        groups.append(dict(p=p, q=q, d=d, matrices_tested=p ** (d * d), rows=rows))
    families = []
    for c in s['families']:
        d = sum(c['blocks'])
        endpoints, total = set(), 0
        for size in c['blocks']:
            total += size
            endpoints.add(total - 1)
        mat = [[int(j == i + 1 and i not in endpoints) for j in range(d)]
               for i in range(d)]
        families.append(dict(**c, **classify(mat, c['p'], c['q'])))
    return dict(exhaustive=groups, families=families)


if __name__ == '__main__':
    core = calculate(json.loads(Path(sys.argv[1]).read_text()))
    Path(sys.argv[2]).write_text(json.dumps(dict(core=core), sort_keys=True, indent=2) + '\n')
    print(json.dumps(dict(matrices=sum(g['matrices_tested'] for g in core['exhaustive']),
                          actions=sum(len(g['rows']) for g in core['exhaustive']))))
