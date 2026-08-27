# Separate exact verification

## Context and counterexample search first

`python -I verify.py` starts in a fresh isolated process and reads only
`input.json` and the untrusted proposed `certificate.json`. It neither imports
theory code nor reads theory outputs. Both implementations were authored by the
same assistant: independence is mathematical-method and execution-context based,
not a fresh model, human referee, or formal kernel.

Before accepting the candidate, the checker rejects seven mutations: dimension,
tail start, zero Fourier origin, understated objective, transform coefficient,
Q coefficient and tail coefficient. The smaller tail start T=14 genuinely fails:
P(14)=211>0. A zero c makes Q(0)=0 and cannot give this finite bound.

For a sampling-only negative control, use

    Q_bad(u)=(u-121/8)^2*(u+1)-1/1000.

All 121 quarter-grid samples on [0,30] are positive (minimum 249/1000), but
Q_bad(121/8)=-1/1000. Indeed every nonnegative quarter-grid point is at least
1/8 away from 121/8, so even the infinite quarter-grid misses this negative dip.
This is a sign-test counterexample, not an admissible packing candidate. It
shows why a global proof cannot be replaced by a large sample count.

The valid Q has an exact zero at u=15, so strict sampled margins near it are
not an appropriate certificate. The factorization handles that zero directly.

## Independent transform method

For u=pi*|y|^2 and m=n/2, the radial Laplacian identity gives

    Fourier[u*f] = -Delta(hat(f))/(4*pi),
    D[p] = -u*p''+(2u-m)*p'+(m-u)*p.

Starting from the self-transforming Gaussian, repeat D on the constant 1 to
transform monomials. This uses differentiation and coefficient accumulation;
there is no Laguerre polynomial or binomial-transform code in this checker.
For n=24 the first four transformed monomials are

    1,
    12-u,
    156-26u+u^2,
    2184-546u+42u^2-u^3.

Combining them with the factor-expanded Q regenerates P=(225,13,13,-1).
Applying the transform again regenerates Q. Separately, 36 basis-involution
checks cover degrees 0 through 8 in dimensions 2,8,24,48. These are regression
checks, not a universal proof of the Fourier transform theorem.

## Global signs, finite search and objective

The checker multiplies the three Q factors, regenerates P by D, and evaluates
successive exact derivatives at T. Taylor coefficients P^(j)(T)/j! are
(-30,-272,-32,-1). The polynomial identity and signs prove the entire tail;
Q's nonnegative factors prove the entire nonnegative half-line. No finite
sampling is used to conclude these global signs.

The checker independently reclassifies all 70,200 configured triples. It agrees
on 13,135 accepted triples, their ordered SHA-256 digest, and the same winning
bound. It checks the objective with 2^n rather than the theory's 4^(n/2), and
requires strictly positive origins before dividing. Comparison with theory
results occurs only after the separate execution finishes.

## Citation and proof-step audit

The primary Cohn–Elkies PDF (arXiv math/0110009v3, September 3, 2003) supplies
Theorems 3.1 and 3.2 on printed pages 694–695. The latter requires equal positive
origins; our candidate has both equal to 225. Its center-density bound (r/2)^n
must be multiplied by the unit-ball volume. With r=sqrt(15/pi), n=24 this
becomes 15^12/(4^12*12!), with no numerical pi rounding.

Schwartz regularity of polynomial-Gaussians, differentiation of their transforms,
all-real sign domains, positive denominators, and the packing/center-density
distinction were checked explicitly. The packing theorem itself is cited, not
re-proved or kernel accepted here. The 2017 primary paper already establishes
optimality of the Leech lattice; this calibration is not a new packing record.

Both AIM HTTP and HTTPS endpoints failed to return the source heading. Its
provenance is therefore only the hash-pinned dataset, not a newly verified AIM
quotation. The original URL and the HTTPS normalization are retained explicitly.
The imported general mesh/derivative/tail lemma remains unaudited.

## Outcome

The degree-three candidate has an exact finite certificate and improves the
degree-one baseline. General optimization, higher degrees, the source agenda,
independent human/model proof review and kernel formalization remain outside
this packet. No imported status or parent-problem claim is promoted.
