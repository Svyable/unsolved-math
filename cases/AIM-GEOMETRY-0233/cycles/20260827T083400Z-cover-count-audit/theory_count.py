"""Exact orbit-of-the-root recurrence; no permutation enumeration."""

import json
from math import comb, factorial
from pathlib import Path


def counts(rank, degree):
    if rank < 0 or degree < 1:
        raise ValueError('rank must be nonnegative and degree positive')
    transitive = [0]
    subgroups = [0]
    for d in range(1, degree+1):
        total = factorial(d)**rank
        disconnected = sum(comb(d-1, k-1)*transitive[k]*factorial(d-k)**rank
                           for k in range(1, d))
        t = total-disconnected
        assert t >= 0 and t % factorial(d-1) == 0
        transitive.append(t)
        subgroups.append(t//factorial(d-1))
    return transitive, subgroups


def main():
    config = json.loads(Path(__file__).with_name('input.json').read_text())
    rows = []
    for rank in config['theory_ranks']:
        t, a = counts(rank, config['theory_max_degree'])
        for d in range(1, len(a)):
            old = sum(factorial(k)**rank for k in range(1, d+1))
            new = sum(a[1:d+1])
            assert 0 < new <= old
            rows.append({'rank': rank, 'degree': d, 'transitive_tuples': t[d],
                         'based_subgroups': a[d], 'old_cumulative_bound': old,
                         'refined_cumulative_bound': new})
    case = config['example']
    _, a = counts(case['rank'], case['max_degree'])
    old = sum(factorial(k)**case['rank'] for k in range(1, case['max_degree']+1))
    new = sum(a[1:])
    result = {
        'method': 'partition by the orbit containing the distinguished sheet',
        'rows': rows,
        'example': {**case, 'individual_based_counts': a[1:],
                    'old_denominator': old, 'refined_denominator': new,
                    'old_guaranteed_lifts': (case['N']+old-1)//old,
                    'refined_guaranteed_lifts': (case['N']+new-1)//new},
        'scope': ('Cover-count upper bound and conditional pigeonhole conclusion; '
                  'no geodesic family constructed.'),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
