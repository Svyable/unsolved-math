# Exact algebraic cutoff for the existing cubic

## Scope and changed evidentiary state

The canonical statement is only a heading, preserved verbatim in snapshot.json. Its AIM page remains unavailable and human scope review is still required. We do not increase degree, change dimension or claim to answer a reconstructed question. We audit only the exact cubic from the earlier sealed packet. Previously T=15 was a sufficient quarter-grid cutoff. Here the admissible set of ALL real positive cutoffs is characterized exactly, and an algebraic optimum for this one fixed function is enclosed by rational certificates. This is not optimization over all polynomials or a new packing record.

Fix n=24, u=pi*|x|^2,

    P(u)=225+13u+13u^2-u^3,
    Q(u)=225+195u-29u^2+u^3=(u-15)^2(u+1).

The polynomial-Gaussian pair uses the Fourier convention exp(2*pi*i*<x,y>). The prior transform is reproduced, not assumed from prose: the theory uses k! L_k^(11)(u) coefficients, while the verifier iterates the radial Laplacian. Both origins equal 225. The nonnegative factorization of Q is unchanged. This packet's sole new target is the tail cutoff and its objective, not Fourier theory.

For T>0, admissibility of the tail means P(u)<=0 for EVERY real u>=T. By the cited Cohn--Elkies theorem, the covered-volume density bound for this fixed pair is B(T)=T^12/(4^12*12!). The theorem itself is an external dependency, not re-proved here. Lower bounds on B for this function are NOT lower bounds on optimal packing density.

## Two approaches

1. Keep a sufficient rational grid cutoff and round its numerical root estimate to nearest. The old certificate remains valid at 15, but the new rounded-root substitution must be tested: proximity alone does not establish a one-sided inequality.
2. Characterize the last sign change algebraically, use monotone rational bisection with directed outward rounding, and propagate its rational interval through the increasing objective. A distinct Sturm implementation checks root count, location and signs.

Falsifiers: an extra positive root, a nonnegative point beyond a claimed cutoff, an interval not enclosing the unique root, an understated objective, or confusion between squared radial units and radius.

## Ordinary all-real proof (not independent-author/kernel accepted)

On [0,13], write P(u)=225+13u+u^2(13-u)>0. At u=13, P'=-156; and P''(u)=26-6u<0 for u>=13. Consequently P is strictly decreasing on [13,infinity). Since P(14)=211 and P(15)=-30, continuity gives a unique positive root alpha in (14,15), positive values before alpha and negative values after it. Thus

    {T>0 : for all u>=T, P(u)<=0} = [alpha,infinity).

Equality T=alpha is admissible: the zero at the endpoint is permitted. B is strictly increasing for positive T, so the fixed-function optimum is B(alpha). This characterization, rather than a larger grid search, is the theoretical delta. Multiplying P by -1 makes it monic integral; any rational root would be an integer. No integer lies in (14,15), so all dyadic endpoints and midpoints avoid alpha, with no tie ambiguity in nearest rounding.

Exact sign bisection produces the 32-bit enclosure

    L = 63944510808/4294967296 = 7993063851/536870912,
    U = 63944510809/4294967296,
    L < alpha < U, U-L=1/4294967296.

The exact positive value P(L) and negative value P(U) are stored in the final table row. Therefore L is invalid and U is valid. The new certified density upper bound is exactly

    B(U) = (63944510809/4294967296)^12 / (4^12*12!).

The full numerator and denominator are in theory-output.json. Its ratio to the old bound B(15) is (U/15)^12 < 183/200: more than 8.5% improvement over that calibration only. The interval [B(L),B(U)] encloses the fixed-function optimum; B(L) is not itself a certified packing upper bound.

## Concrete rounding counterexample

At three fractional bits, rounding alpha to nearest gives T=119/8. But

    P(119/8)=1793/512 > 0.

The proposed cutoff fails its own endpoint condition despite being the nearest dyadic value. For all 32 tested bit depths, downward rounding fails; nearest rounding fails at 15 depths. Upward rounding passes at every depth. Counts are regression evidence for directed rounding, not the proof for arbitrary precision. Seven targeted corruptions challenge the finite certificate format.

## Typed claims and limits

- CUTOFF, DERIVED, UNVERIFIED: the ordinary proof establishes the asserted all-real admissible set and fixed-function optimum, subject to independent analytic review. Falsifier: a gap in monotonicity, positivity or endpoint reasoning.
- ROUNDING, DERIVED, FALSIFIED: the proposed shortcut that nearest-root rounding preserves the tail sign; the value 1793/512 is its counterexample.
- CERTIFICATE, DERIVED, EXPERIMENTALLY_SUPPORTED: the rational root bracket, exact objective interval and 32-row arithmetic. Falsifier: differing Sturm count, endpoint sign, transform or objective computation.
- SOURCE, PRIMARY_SOURCE, PRIMARY_SOURCE_SUPPORTED: Theorem 3.2 permits equal positive origins and non-strict tail/Fourier signs; conversion from center density requires the unit-ball volume. Source version and locator are in sources.json.

Remaining: human scope review of the heading; independent author/kernel review of the ordinary proof and external analytic dependencies; no higher-degree, broader-dimensional or globally optimal auxiliary function claim. This is known-method calibration. More bits for this same root are not another material advance; retain this certificate and rotate.
