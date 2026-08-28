# Fresh-process verification

## Actual independence

verify.py and its baseline execution preceded theory.py. The verifier begins with the frozen input, not the theory conclusion. A new Python -I process with an empty environment reconstructs all expectations before reading the proposed certificate. There are no theory imports. Theory uses monotonicity and Horner-sign bisection; verification uses generic exact Euclidean polynomial remainders and Sturm variation counts. Its Fourier check uses the radial Laplacian instead of Laguerre coefficients. Both implementations have same-assistant authorship and share the input; no independent human/model or kernel review is claimed. The machine output has a harmless trailing word typo in its independence string; this paragraph states the intended limitation precisely.

## Counterexample and boundary checks first

Before accepting any proposal, check P(14)=211, P(15)=-30 and Q(15)=0. A three-positive-root control, 6-11u+6u^2-u^3, prevents opposite endpoint signs from being mistaken for uniqueness. The repeated-root control (u-1)^2 verifies the squarefree/distinct-root convention: it has one distinct root in (0,2), without a sign change. The actual cubic's positive-root count is one.

The generic Sturm chain is

    [225,13,13,-1], [13,26,-3],
    [-2194/9,-416/9], [8980371/43264],

with ascending coefficients. At zero its sign variations are two; at positive infinity one. It has one distinct positive root. At each dyadic bracket, variation differences independently certify exactly one root inside and none beyond the upper endpoint. Endpoint evaluations also certify strict opposite signs. The nearest cutoff 119/8 at three bits gives positive P=1793/512 and is rejected before any claim of a valid improvement.

## Computation and certificate audit

For each bit depth 1 through 32, binary search uses root counts in (0,x), not the theory's sign predicate. The separate complete tables agree, including both endpoints, exact polynomial values, nearest endpoint and its validity. All 32 downward cutoffs fail; 15 nearest cutoffs fail. At 32 bits the interval has width exactly 2^-32. Powers and division are exact fractions; verifier uses 2^24*12! whereas theory uses 4^12*12!.

The certificate checker treats P,Q,dimension,interval,root count and objective as untrusted. It checks the fixed problem binding, ordered positive interval, required width, endpoint signs, one enclosed positive root, no roots beyond U, and exact objective arithmetic. It accepts the authentic certificate and rejects seven modifications: wrong dimension, changed P, changed Q, reversed interval, collapsed interval, understated objective, false root count. These targeted mutations do not establish general parser security or formal proof acceptance.

The radial operator D[p]=-u*p''+(2u-12)*p'+(12-u)*p reproduces both Fourier directions. The factorization Q=(u-15)^2(u+1), equal positive origins, and polynomial-Gaussian admissibility are checked in the notes. The numerical root interval is not a replacement for those conditions.

## Citation and proof-step audit

Cohn--Elkies, arXiv math/0110009v3 dated 2003-09-03, Theorem 3.2 on printed page 695 was freshly read on 2026-08-28. It uses non-strict inequalities, so the limiting cutoff alpha is allowed. The theorem bounds center density; multiplying the ball volume at radius sqrt(T/pi)/2 produces the stated covered-volume objective. No current-status or best-bound claim is inferred from that historical paper. The original AIM HTTP and HTTPS endpoints failed; the heading is supported only by the pinned dataset. No human source-scope review is fabricated.

The ordinary proof's positivity on [0,13], derivative sign beyond 13, intermediate-value use, allowed endpoint equality and increasing objective were inspected. Sturm theory and the Fourier/packing theorems remain external mathematical dependencies, not kernel accepted. Matching programs strengthen the finite arithmetic evidence but do not supply independently authored analytic review.

Reproduction: run.py baseline, theory, verify, replay. Five mathematical subprocesses used; each fresh process has CPU 180s, wall 200s, memory 512MiB limits. The scripts do not access the network; no network namespace is claimed. Replay reproduces both outputs unchanged. Table paths are distinct even though contents and SHA-256 coincide.

Outcome: an independently computed algebraic cutoff certificate, a concrete invalid nearest rounding, and a certified improvement over the fixed prior bound. No parent solution or general optimal sphere-packing bound is established.
