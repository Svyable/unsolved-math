# Exact degree-three Gaussian certificate in dimension 24

Agent output is unverified research assistance, not a mathematical result.

## Frozen source and target

The canonical statement is only “Numerical LP bounds in high dimensions.” It is
preserved exactly in `snapshot.json`; neither this packet nor its title repairs
that heading into a new canonical question. The original AIM page could not be
retrieved. The imported research summary is an unverified lead, not a theorem.

One bounded target: certify all sign and Fourier conditions for one rational
degree-three polynomial-Gaussian candidate in dimension 24, and determine whether
its density bound improves the stated degree-one calibration. This produces a
reusable exact certificate, not a new best packing bound or a solution of the
source agenda. The dimension-24 optimal packing is already covered by the 2017
Cohn–Kumar–Miller–Radchenko–Viazovska paper; see `sources.json`.

## Definitions, assumptions and quantifiers

Fix n=24, m=n/2=12, u=pi*|x|^2. The Fourier convention is
hat(f)(y)=integral f(x)*exp(2*pi*i*<x,y>) dx. All functions here are real radial
polynomials times exp(-pi*|x|^2), hence Schwartz and admissible for the cited
Cohn–Elkies theorem. Polynomial signs apply to EVERY real u in the stated
half-line, not just rational grid nodes. The Gaussian is strictly positive.

Write f(x)=P(u)*exp(-u) and hat(f)(y)=Q(pi*|y|^2)*exp(-pi*|y|^2).
Required: P(0)>0, Q(0)>0, Q(u)>=0 for u>=0, P(u)<=0 for u>=T>0,
and a correct Fourier identity. By scaling Theorem 3.1, the packing density
(covered volume fraction, not center density) is at most

    B = T^m * P(0) / (4^m * m! * Q(0)).

The factor is volume of a ball of radius sqrt(T/pi)/2; pi cancels exactly in
even dimension. No floating-point objective or outward rounding is needed.
The final candidate also has P(0)=Q(0), so Theorem 3.2 applies directly.
We use the published packing theorem as a cited dependency, not a kernel-checked
or independently re-proved result. No external mathematical status is modified.

## Two approaches considered

1. A rational mesh with certified derivative and infinite-tail bounds, after
   factoring exact squares. This needs covering radii, margins and derivative
   certificates; samples alone do not imply global signs. It is unnecessary for
   the simple candidate family used here, and is not implemented in this cycle.
2. Exact nonnegative factors for Q and nonpositive shifted coefficients for P.
   This covers the whole half-lines with finitely many coefficient identities,
   handles double roots without a positive margin, and avoids discretizing signs.

Only approach 2 is used for certification. Its test is sufficient, not necessary:
a rejected triple may still have correct signs by a more powerful method.
The finite parameter grid searches for a candidate; it is not the sign proof.

## Search and Fourier certificate

Search Q(u)=(u-b)^2*(u+c) with integer 1<=b<=30, 1<=c<=20 and
T=j/4 for integers 4<=j<=120. There are 70,200 triples. Require positive
origins and nonpositive coefficients of P(T+v), v>=0. Of these, 13,135 pass.
The best exact B among passing triples, with deterministic ties by b,c,T, is
b=15, c=1, T=15. This is finite-grid optimality only, not optimality in any
continuous family or among all auxiliary functions.

The theory implementation computes the polynomial-Gaussian transform through

    Fourier[u^k exp(-u)] = k! L_k^(m-1)(u) exp(-u).

This follows by differentiating the Gaussian identity
Fourier[exp(-a*pi*|x|^2)] = a^(-m)*exp(-pi*|y|^2/a) at a=1.
The coefficient of u^j is k!*(-1)^j*binom(k+m-1,k-j)/j!.
This monomial-transform formula is NOT the Laguerre eigenbasis with argument 2u.
The separate checker derives the transform by the radial Laplacian instead.

The winning exact pair is

    P(u) = 225 + 13u + 13u^2 - u^3,
    Q(u) = 225 + 195u - 29u^2 + u^3 = (u-15)^2*(u+1).

Both origins equal 225. Q(u)>=0 for all u>=0, including its double root at 15.
For EVERY v>=0,

    P(15+v) = -30 - 272v - 32v^2 - v^3 < 0.

These identities establish the global signs, including the infinite tail.
The conditional density bound is exactly

    B3 = 15^12/(4^12*12!) = 21357421875/1322849927168.

The degree-one baseline is P1(u)=13-u, Q1(u)=1+u, T1=13, giving

    B1 = 13^13/(4^12*12!) = 302875106592253/8036313307545600.

The ratio B3/B1=129746337890625/302875106592253 is strictly below one.
This is improvement over a deliberately weak calibration only. It is not a
state-of-the-art bound, and no novelty claim is made.

## Falsification and remaining obligations

Target errors include a wrong Fourier normalization, a sign reversal, a missed
double-root neighborhood, an undersized tail threshold, division by Q(0)=0,
and confusing center density with covered volume. The verifier rejects seven
mutated certificates and constructs a between-grid negative dip. The accepted
candidate is independently regenerated, not accepted because of theory prose.

Remaining: the broad AIM heading needs human scope review; the AIM page is
unavailable; the imported general certification lemma has not been established
here. The published packing theorem, Gaussian transform and ordinary analytic
justifications remain non-kernel dependencies. Both programs have same-assistant
authorship; independence is algorithmic and fresh-process, not human/model review.
