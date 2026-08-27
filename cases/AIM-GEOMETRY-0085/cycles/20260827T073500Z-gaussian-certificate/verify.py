"""Fresh exact checker: differential Fourier recurrence, not Laguerre code."""

import copy
import hashlib
import json
from fractions import Fraction as R
from math import factorial
from pathlib import Path


def derivative(p):
    return [i*p[i] for i in range(1, len(p))] or [R(0)]


def value(p, u):
    total = R(0)
    for a in reversed(p):
        total = total*u + a
    return total


def differential_step(p, m):
    # -u*p'' + (2u-m)*p' + (m-u)*p.
    out = [R(0)] * (len(p)+1)
    for i, a in enumerate(p):
        out[i] += (2*i+m)*a
        out[i+1] -= a
        if i:
            out[i-1] -= i*(i-1+m)*a
    return out


def fourier(p, m):
    out = [R(0)]*len(p)
    monomial = [R(1)]
    for a in p:
        for j, q in enumerate(monomial):
            out[j] += a*q
        monomial = differential_step(monomial, m)
    return out


def taylor(p, t):
    result = []
    d = p
    for j in range(len(p)):
        result.append(value(d, t)/factorial(j))
        d = derivative(d)
    return result


def expand_q(b, c):
    # Multiply factor arrays, without using a pre-expanded cubic formula.
    result = [R(1)]
    for factor in ([-b, 1], [-b, 1], [c, 1]):
        nxt = [R(0)]*(len(result)+1)
        for i, a in enumerate(result):
            for j, z in enumerate(factor):
                nxt[i+j] += a*z
        result = nxt
    return result


def validate(cert, n):
    if cert['dimension'] != n or n != 24:
        return False
    b, c, t = R(cert['b']), R(cert['c']), R(cert['T'])
    if c <= 0 or t <= 0:
        return False
    q = expand_q(b, c)
    p = fourier(q, n//2)
    shifted = taylor(p, t)
    if p[0] <= 0 or q[0] <= 0 or any(a > 0 for a in shifted):
        return False
    bound = t**(n//2)*p[0]/(2**n*factorial(n//2)*q[0])
    return (list(map(R, cert['P_coefficients_ascending'])) == p
            and list(map(R, cert['Q_coefficients_ascending'])) == q
            and list(map(R, cert['P_shifted_at_T'])) == shifted
            and R(cert['density_upper_bound']) == bound)


def main():
    root = Path(__file__).parent
    config = json.loads((root/'input.json').read_text())
    cert = json.loads((root/'certificate.json').read_text())
    n = config['dimension']

    # Start with falsification, boundary and mutation checks, not confirmation.
    controls = {}
    for name, field, replacement in [
        ('wrong_dimension', 'dimension', 22),
        ('too_small_tail_start', 'T', '14'),
        ('zero_fourier_origin', 'c', 0),
        ('understated_objective', 'density_upper_bound', '1/1000'),
        ('mutated_transform', 'P_coefficients_ascending', ['226', '13', '13', '-1']),
        ('mutated_Q', 'Q_coefficients_ascending', ['224', '195', '-29', '1']),
        ('mutated_tail', 'P_shifted_at_T', ['0', '-272', '-32', '-1']),
    ]:
        bad = copy.deepcopy(cert)
        bad[field] = replacement
        controls[name] = not validate(bad, n)
    assert all(controls.values())
    # Coarse nonnegative samples do not certify between-node signs.
    hidden_root = R(121, 8)
    bad_q = expand_q(hidden_root, R(1))
    bad_q[0] -= R(1, 1000)
    samples = [value(bad_q, R(j, 4)) for j in range(121)]
    assert min(samples) > 0 and value(bad_q, hidden_root) == -R(1, 1000)
    assert validate(cert, n)
    q = expand_q(R(cert['b']), R(cert['c']))
    p = fourier(q, n//2)
    assert value(q, R(cert['b'])) == 0
    assert value(q, 0) > 0 and value(p, R(cert['T'])) < 0
    assert fourier(p, n//2) == q

    # Independently replay finite-grid classification and best-bound selection.
    tested = accepted = 0
    best = None
    digest = hashlib.sha256()
    for b in range(config['b_integer_range'][0], config['b_integer_range'][1]+1):
        for c in range(config['c_integer_range'][0], config['c_integer_range'][1]+1):
            q1 = expand_q(R(b), R(c))
            p1 = fourier(q1, n//2)
            for tq in range(config['T_quarters_range'][0], config['T_quarters_range'][1]+1):
                tested += 1
                t = R(tq, 4)
                if p1[0] <= 0 or q1[0] <= 0 or any(z > 0 for z in taylor(p1, t)):
                    continue
                bound = t**(n//2)*p1[0]/(2**n*factorial(n//2)*q1[0])
                accepted += 1
                digest.update((json.dumps([b, c, str(t), str(bound)],
                                          separators=(',', ':'))+'\n').encode())
                key = (bound, b, c, t)
                if best is None or key < best:
                    best = key
    assert best == (R(cert['density_upper_bound']), cert['b'], cert['c'], R(cert['T']))
    involutions = 0
    for dim in [2, 8, 24, 48]:
        for degree in range(9):
            basis = [R(0)]*degree+[R(1)]
            assert fourier(fourier(basis, dim//2), dim//2) == basis
            involutions += 1
    output = {
        'method': 'radial Laplacian recurrence plus Taylor derivative tail coefficients',
        'counterexample_first': True, 'adversarial_controls': controls,
        'between_grid_counterexample': {
            'root': str(hidden_root), 'value_at_root': str(value(bad_q, hidden_root)),
            'positive_samples': len(samples), 'minimum_sample': str(min(samples)),
            'polynomial_coefficients': list(map(str, bad_q)),
        },
        'certificate_valid': True,
        'P': list(map(str, p)), 'Q': list(map(str, q)),
        'tail_taylor_coefficients': list(map(str, taylor(p, R(cert['T'])))),
        'grid_triples_tested': tested, 'certified_triples': accepted,
        'certified_grid_sha256': digest.hexdigest(),
        'winning_bound': str(best[0]), 'fourier_involution_basis_checks': involutions,
        'scope': 'Exact algebraic certificates plus cited analytic theorem; no formal kernel.',
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
