"""Independent finite actions and formal-logarithm checks; no theory imports."""

import hashlib
import json
from collections import Counter
from fractions import Fraction
from itertools import permutations, product
from math import factorial
from pathlib import Path


def valid(perms, d):
    if d < 1 or any(sorted(p) != list(range(d)) for p in perms):
        raise ValueError('positive degree and bijective generators required')


def connected(perms, d):
    valid(perms, d)
    parent = list(range(d))

    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x

    for p in perms:
        for i, j in enumerate(p):
            parent[find(i)] = find(j)
    return len({find(i) for i in range(d)}) == 1


def rooted_key(perms, d, root=0):
    valid(perms, d)
    if root not in range(d):
        raise ValueError('root outside fiber')
    order = [root]
    label = {root: 0}
    for point in order:
        for p in perms:
            if p[point] not in label:
                label[p[point]] = len(order)
                order.append(p[point])
    if len(order) != d:
        raise ValueError('action is not transitive')
    return tuple(tuple(label[p[x]] for x in order) for p in perms)


def commute(p, q):
    return all(p[q[i]] == q[p[i]] for i in range(len(p)))


def multiply(a, b, degree):
    out = [Fraction(0)]*(degree+1)
    for i, x in enumerate(a):
        for j, y in enumerate(b[:degree+1-i]):
            out[i+j] += x*y
    return out


def logarithm_counts(rank, degree):
    # All-action exponential generating series A(z); compute log(A) by powers.
    x = [Fraction(0)]+[Fraction(factorial(d)**rank, factorial(d))
                      for d in range(1, degree+1)]
    power = [Fraction(1)]+[Fraction(0)]*degree
    log = [Fraction(0)]*(degree+1)
    for k in range(1, degree+1):
        power = multiply(power, x, degree)
        for d in range(1, degree+1):
            log[d] += Fraction((-1)**(k+1), k)*power[d]
    ans = [d*log[d] for d in range(1, degree+1)]
    assert all(a.denominator == 1 and a >= 0 for a in ans)
    return [int(a) for a in ans]


def main():
    config = json.loads(Path(__file__).with_name('input.json').read_text())
    controls = {}
    controls['disconnected_action_rejected'] = not connected(((1, 0, 3, 2),), 4)
    for name, args in [
        ('nonbijective_generator_rejected', (((0, 0),), 2, 0)),
        ('zero_degree_rejected', ((), 0, 0)),
        ('bad_root_rejected', (((1, 0),), 2, 2)),
        ('nontransitive_root_encoding_rejected', (((0, 1),), 2, 0)),
    ]:
        try:
            rooted_key(*args)
        except ValueError:
            controls[name] = True
        else:
            controls[name] = False
    assert all(controls.values())

    rows = []
    total_tested = 0
    for case in config['enumeration_cases']:
        rank = case['rank']
        for d in range(1, case['max_degree']+1):
            choices = list(permutations(range(d)))
            inventory = Counter()
            commuting = Counter()
            tested = transitive = 0
            for action in product(choices, repeat=rank):
                tested += 1
                if not connected(action, d):
                    continue
                transitive += 1
                key = rooted_key(action, d)
                inventory[key] += 1
                if rank == 2 and commute(*action):
                    commuting[key] += 1
            assert tested == factorial(d)**rank
            assert all(v == factorial(d-1) for v in inventory.values())
            assert transitive == len(inventory)*factorial(d-1)
            total_tested += tested
            digest = hashlib.sha256()
            for key in sorted(inventory):
                digest.update((json.dumps(key, separators=(',', ':'))+'\n').encode())
            unbased = {min(rooted_key(key, d, root) for root in range(d))
                       for key in inventory}
            row = {'rank': rank, 'degree': d, 'tuples_tested': tested,
                   'transitive_tuples': transitive, 'based_subgroups': len(inventory),
                   'unbased_cover_classes': len(unbased),
                   'rooted_inventory_sha256': digest.hexdigest(),
                   'all_rooted_class_sizes_equal_factorial_d_minus_1': True}
            if rank == 2:
                assert len(commuting) == sum(k for k in range(1, d+1) if d % k == 0)
                row['commuting_based_subgroups'] = len(commuting)
            rows.append(row)

    log_rows = []
    for rank in config['theory_ranks']:
        for d, a in enumerate(logarithm_counts(rank, config['theory_max_degree']), 1):
            log_rows.append({'rank': rank, 'degree': d, 'based_subgroups': a})
    lookup = {(r['rank'], r['degree']): r['based_subgroups'] for r in log_rows}
    assert all(lookup[r['rank'], r['degree']] == r['based_subgroups'] for r in rows)
    two = next(r for r in rows if r['rank'] == 2 and r['degree'] == 2)
    wrong = Fraction(two['transitive_tuples'], factorial(2))
    assert wrong != two['unbased_cover_classes']
    three = next(r for r in rows if r['rank'] == 2 and r['degree'] == 3)
    assert three['commuting_based_subgroups'] < three['based_subgroups']
    # Ceil vs floor: exact boundary checks, not simulated geodesic data.
    ceil_checks = 0
    for bins in range(1, 11):
        for objects in range(101):
            floor, rem = divmod(objects, bins)
            occupancy = [floor+(j < rem) for j in range(bins)]
            assert max(occupancy) == (objects+bins-1)//bins
            ceil_checks += 1
    case = config['example']
    denominator = sum(lookup[case['rank'], d] for d in range(1, case['max_degree']+1))
    result = {
        'method': ('explicit permutation actions, rooted BFS canonicalization, '
                   'formal series logarithm'),
        'counterexample_first': True, 'adversarial_controls': controls,
        'rows': rows, 'formal_log_rows': log_rows,
        'total_tuples_tested': total_tested,
        'wrong_full_factorial_quotient': {'rank': 2, 'degree': 2,
            'labelled_transitive_actions': two['transitive_tuples'],
            'wrong_division_by_d_factorial': str(wrong),
            'actual_unbased_classes': two['unbased_cover_classes']},
        'relations_matter_control': {'rank': 2, 'degree': 3,
            'free_group_based_subgroups': three['based_subgroups'],
            'abelian_group_based_subgroups': three['commuting_based_subgroups']},
        'pigeonhole_boundary_checks': ceil_checks,
        'example_refined_denominator': denominator,
        'example_guaranteed_lifts': (case['N']+denominator-1)//denominator,
        'scope': ('Finite group-action enumeration and algebra; '
                  'no simple geodesics simulated or constructed.'),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
