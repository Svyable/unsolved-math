"""Exact finite grid search via monomial/Laguerre Fourier coefficients."""

import hashlib
import json
from fractions import Fraction as F
from math import comb, factorial
from pathlib import Path


def transform(q, m):
    # F[u^k exp(-u)] = k! L_k^(m-1)(u) exp(-u).
    return [sum((q[k] * factorial(k) * (-1)**j * comb(k + m - 1, k - j)
                 / F(factorial(j)) for k in range(j, len(q))), F(0))
            for j in range(len(q))]


def shift(p, t):
    return [sum((p[k] * comb(k, j) * t**(k-j)
                 for k in range(j, len(p))), F(0)) for j in range(len(p))]


def main():
    data = json.loads(Path(__file__).with_name('input.json').read_text())
    n = data['dimension']
    assert n == 24
    m = n // 2
    baseline = F((m+1)**(m+1), 4**m * factorial(m))
    best = None
    tested = accepted = 0
    digest = hashlib.sha256()
    for b in range(data['b_integer_range'][0], data['b_integer_range'][1]+1):
        for c in range(data['c_integer_range'][0], data['c_integer_range'][1]+1):
            q = [F(b*b*c), F(b*b-2*b*c), F(c-2*b), F(1)]
            p = transform(q, m)
            assert transform(p, m) == q
            for tq in range(data['T_quarters_range'][0], data['T_quarters_range'][1]+1):
                tested += 1
                t = F(tq, 4)
                shifted = shift(p, t)
                if p[0] <= 0 or q[0] <= 0 or any(v > 0 for v in shifted):
                    continue
                bound = t**m * p[0] / (4**m * factorial(m) * q[0])
                accepted += 1
                row = [b, c, str(t), str(bound)]
                digest.update((json.dumps(row, separators=(',', ':'))+'\n').encode())
                key = (bound, b, c, t)
                if best is None or key < best[0]:
                    best = (key, {
                        'dimension': n, 'b': b, 'c': c, 'T': str(t),
                        'P_coefficients_ascending': list(map(str, p)),
                        'Q_coefficients_ascending': list(map(str, q)),
                        'P_shifted_at_T': list(map(str, shifted)),
                        'density_upper_bound': str(bound),
                    })
    assert best is not None
    bound = best[0][0]
    assert 0 < bound < baseline < 1
    output = {
        'method': 'exact Laguerre coefficient transform plus shifted-monomial tail certificate',
        'grid_triples_tested': tested, 'certified_triples': accepted,
        'certified_grid_sha256': digest.hexdigest(),
        'certificate': best[1], 'degree_one_baseline': str(baseline),
        'ratio_to_baseline': str(bound / baseline),
        'strict_improvement': True,
        'scope': 'Best certified triple on specified finite grid only; not optimality or novelty.',
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
