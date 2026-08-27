# Independent execution and adversarial review

## Independence boundary

`python -I verify.py` starts a fresh isolated process, reads only `input.json`,
and imports no theory code, theory output, or notes. It uses bitwise polynomial
arithmetic in a verified F64 presentation and explicit permutation traversal;
the theory executable instead evaluates polynomials over F2 and uses gcd formulas.
There are no random seeds, floating-point tolerances, network calls or dependencies.
Both implementations were authored by the same assistant. This is algorithmic and
execution-context independence, NOT independent human or fresh-model review.
Proof-step and citation checks below retain that limitation.

## Counterexamples and boundaries first

Before transport comparisons the verifier checks the field modulus x^6+x+1 by
trial division by every monic polynomial of degree 1..3. It similarly tests the
two input polynomials. It enumerates their roots in F64: integer encodings
58,59 and 14,23,25. Squaring permutes these roots in orbits of lengths 2 and 3;
no root is fixed. This directly rejects C1 and independently reconstructs the
closed-point degrees, index one and signed witness of degree one.

Six controls pass: reject the false implication; detect the reducible replacement
x^2+x; detect a rational root after adding x+1; obtain index two from degrees 2,4;
reject coefficients -1,-1; and detect splitting of the quadratic orbit after a
degree-two extension. These are explicit sensitivity/boundary probes, not a claim
of comprehensive mutation coverage.

## Claim and computation checks

- C1: two irreducible field factors, no Frobenius-fixed geometric point,
  gcd(2,3)=1, and -2+3=1 independently confirmed. As all closed degrees exceed one,
  no effective degree-one cycle exists. The assertion's domain is finite etale
  schemes; extending this counterexample to geometrically integral varieties is invalid.
- C2: for all 1,819 nonempty degree multisets of lengths 1..4 over 1..12, and each
  m in 1..12, traverse i -> i+m modulo d on every component. Compare the resulting
  gcd to the proposed expression and check both divisibilities: 21,828 checks,
  zero mismatches. A deterministic orbit transcript digest is recorded in
  `verification-output.json`; it is a digest of replayable intermediate data,
  not a separately stored or kernel-verified certificate.
- The finite-field model is sufficient for the bounded experiment. The
  identification of Frobenius orbits with closed points and the prime-valuation
  argument are mathematical inputs, not facts proved by Python.

## Citation check and proof-step audit

Primary-source access independently of dataset commentary confirms the passage's
placement at Question 11, remark (iv), immediately preceding Question 12 in the
AIM PDF (PDF index 48; printed page 50). `sources.json` records this mapping.
This supports C3, not an automatic status rewrite. The CT--Madore abstract
supports existence of point-free del Pezzo surfaces; it does not itself certify
the stronger index-three statement. Ax's original article was not audited.

Proof-step checklist: root-free implies irreducible ONLY in degrees 2 and 3;
finite fields supply separability; signed coefficients are allowed for zero-cycles;
positivity is indispensable for effective cycles; the p-adic minimum identity
holds for positive degrees; empty profiles and arbitrary-field generalizations
are excluded. No unreviewed proof sketch is upgraded to a formal theorem.

## Outcome and remaining objections

The exact missing implication is effectivity. The numerical and symbolic evidence
agree, with independent executable evidence in this lane. No mathematical novelty
is claimed. Source scope needs human review; the original rationally connected
setting and general-field transport remain outside this packet. No Lean kernel,
independent human reviewer, or independent model has accepted the proof steps.
