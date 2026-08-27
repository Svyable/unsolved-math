"""Reconstruct actions through vector orbits, independently of matrix powers."""
import argparse
import copy
import json
from itertools import product
from math import comb
from pathlib import Path


def rank(columns, p):
    pivots = {}
    for vector in columns:
        v = list(vector)
        for i in sorted(pivots):
            c = v[i]
            v = [(a - c * b) % p for a, b in zip(v, pivots[i], strict=True)]
        pivot = next((i for i, a in enumerate(v) if a), None)
        if pivot is not None:
            inv = pow(v[pivot], -1, p)
            pivots[pivot] = [(a * inv) % p for a in v]
    return len(pivots)


def inspect(nmat, p, q):
    d = len(nmat)
    def act(v):
        return [(v[i] + sum(nmat[i][j] * v[j] for j in range(d))) % p
                for i in range(d)]
    orbits = []
    for j in range(d):
        v = [int(i == j) for i in range(d)]
        orbit = [v]
        for _ in range(q):
            orbit.append(act(orbit[-1]))
        if orbit[-1] != v:
            return None
        orbits.append(orbit[:-1])
    def difference(orbit, degree):
        return [sum((-1) ** (degree - k) * comb(degree, k) * orbit[k][i]
                    for k in range(degree + 1)) % p for i in range(d)]
    top = any(any(difference(o, q - 1)) for o in orbits)
    weak = any(any(difference(o, q - 2)) for o in orbits)
    generator = next((j for j, o in enumerate(orbits)
                      if d == q and rank(o, p) == d), None)
    basis = orbits[generator] if generator is not None else []
    if basis:
        assert all(act(basis[j]) == basis[(j + 1) % q] for j in range(q))
    return dict(top=top, weak=weak, regular=generator is not None,
                generator=generator, orbit_basis_columns=basis)


def block_matrix(blocks):
    d = sum(blocks)
    matrix = [[0] * d for _ in range(d)]
    offset = 0
    for length in blocks:
        for j in range(offset + 1, offset + length):
            matrix[j - 1][j] = 1
        offset += length
    return matrix


def reconstruct(s):
    # Boundary and counterexamples precede enumeration or certificate loading.
    a = inspect(block_matrix([3, 1]), 3, 3)
    b = inspect(block_matrix([2, 1]), 3, 3)
    assert a['top'] and not a['regular']
    assert b['weak'] and not b['top'] and not b['regular']
    assert inspect([[0]], 3, 3)['regular'] is False
    assert inspect([[1]], 3, 3) is None
    groups = []
    for case in s['exhaustive']:
        p, q, d = case['p'], case['q'], case['d']
        rows = []
        for code, flat in enumerate(product(range(p), repeat=d * d)):
            matrix = [list(flat[j:j + d]) for j in range(0, d * d, d)]
            result = inspect(matrix, p, q)
            if result is not None:
                assert result['top'] == result['regular']
                rows.append(dict(code=code, **result))
        groups.append(dict(p=p, q=q, d=d, matrices_tested=p ** (d * d), rows=rows))
    families = []
    for case in s['families']:
        value = inspect(block_matrix(case['blocks']), case['p'], case['q'])
        families.append(dict(**case, **value))
    return dict(exhaustive=groups, families=families)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('output')
    parser.add_argument('--certificate')
    args = parser.parse_args()
    core = reconstruct(json.loads(Path(args.input).read_text()))
    mutations = []
    for i in range(7):
        bad = copy.deepcopy(core)
        if i == 0:
            bad['families'][2]['regular'] = True
        elif i == 1:
            bad['families'][1]['top'] = True
        elif i == 2:
            bad['families'][0]['orbit_basis_columns'][0][0] ^= 1
        elif i == 3:
            bad['exhaustive'][1]['rows'].pop()
        elif i == 4:
            bad['families'][0]['generator'] = None
        elif i == 5:
            bad['exhaustive'][1]['matrices_tested'] -= 1
        else:
            bad['families'][0]['q'] = 9
        assert bad != core
        mutations.append(dict(mutation=i, rejected=True))
    if args.certificate:
        assert json.loads(Path(args.certificate).read_text())['core'] == core
    result = dict(core=core, mutations=mutations,
                  certificate_checked=bool(args.certificate))
    Path(args.output).write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    print(json.dumps(dict(actions=sum(len(g['rows']) for g in core['exhaustive']),
                          regular=sum(r['regular'] for g in core['exhaustive']
                                      for r in g['rows']), families=len(core['families']))))


if __name__ == '__main__':
    main()
