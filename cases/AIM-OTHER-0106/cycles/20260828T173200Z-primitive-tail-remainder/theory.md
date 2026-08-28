# Primitive fractions with a tail cutoff

## Delta and scope

This follows `20260827T113347Z-borel-cantelli-tail`. It changes the remainder
mechanism at the SAME R=4,K=32, not the prefix cutoff or the ambient model.
The prior exact prefix measure U is retained. Its remainder 2/K=1/16 becomes
B(32)=17333/403920. Thus U+B(32)<17/40<U+1/16. This is an elementary scalar
calibration, not a new Diophantine approximation theorem or a matrix-manifold
result. The imported status remains unverified and unchanged.

## Definitions and quantifiers

Fix integers R>=2 and K>=R. On [0,1] with Lebesgue measure lambda, let
E_q={x:dist(qx,Z)<q^-2}, q a positive integer, and
U(R,K)=lambda(union_{R<=q<=K} E_q).
Each E_q is the union of intervals of radius q^-3 centered at p/q,
0<=p<=q, clipped to [0,1]. Negative q duplicate the event. No event
independence is assumed. Interval endpoints do not affect measure; strict
membership matters for the pointwise statements below.

A reduced center a/d has gcd(a,d)=1. For d=1 include both 0/1 and 1/1.
Write q_d=d*ceil(R/d). Let J_R(a/d) be the open interval of radius q_d^-3
about a/d, intersected with [0,1]. All unions below use these relative sets,
even though executable interval certificates store their measure-equivalent
closed spans and may join touching endpoints.

## Approaches and falsification targets

1. Discard every nonprimitive numerator-denominator pair and retain only
   reduced d>=R. This shortcut is false: it loses the d<R exceptions.
2. Group all pairs by reduced center and keep the largest interval, then use
   a two-prime upper bound for the number of remaining primitive centers.
3. Partition the same two-prime weights into six residue classes. Convex
   midpoint integrals give a second upper envelope used in verification.

The targets are loss of rational centers, missing cutoff exceptions, wrong
integral inequality direction for negative coefficients, and a false transfer
from ambient measure to a submanifold.

## Claims, origins, and proofs

**DROP (DERIVED; FALSIFIED).** The primitive-only d>=R union equals the
original q>=R union. At x=1/2,R=4, E_4 holds. For odd q, every integer is
at least 1/2 from qx, exceeding q^-2. For even q>=4, the nearest integer
q/2 is not coprime to q; all other integers are at least 1 away. Thus no
primitive pair with q>=4 covers this point. This is a pointwise counterexample,
not alone a positive-measure counterexample. For the finite R=K=4 union,
the full measure is 1/8, while the primitive-only measure is 1/16; the omitted
endpoint half-intervals and the center 1/2 account for the missing 1/16.
Falsifier of the certificate: a primitive approximant covering 1/2, or a
different exact finite union measure.

**REINDEX (DERIVED; UNVERIFIED universal argument).** For every R>=2,
union_{q>=R} E_q = union_{d>=1,0<=a<=d,gcd(a,d)=1} J_R(a/d).
Indeed, all representatives of a/d have q a multiple of d, and the radius
q^-3 decreases strictly with q. The first allowed multiple is q_d. Conversely
that representative is an original event. The finite R..K version retains
exactly those d with q_d<=K. No limit interchange or independence is used.
Falsifier: a reduced center missing its first multiple or a nonnested interval.

**EXCEPTIONS (DERIVED; UNVERIFIED universal argument).** If d<R then
q_d<=R+d-1<=2R-2. Consequently K>=2R-2 captures every low-denominator
exception. Outside the prefix only primitive centers d>K remain necessary.
They number phi(d), all strictly interior, with total interval length
2*phi(d)/d^3. Countable subadditivity therefore gives

    lambda(union_{q>=R} E_q) <= min(1, U(R,K)+2*sum_{q>K} phi(q)/q^3).

Falsifier: an uncaptured d<R center under the stated K condition, or an
incorrect primitive count. The K condition is sufficient, not claimed optimal.

**REMAINDER (DERIVED; UNVERIFIED universal argument).** For every
K>=max(6,2R-2), define

    B(K)=2*(1/K - 1/[8*(floor(K/2)+1)]
               - 1/[27*(floor(K/3)+1)] + 1/[216*floor(K/6)]).

The bound above is at most min(1,U(R,K)+B(K)). To see this, every integer
coprime to q avoids divisibility by 2 or 3 when these primes divide q. Hence
phi(q)/q <= w(q)=(1-1_{2|q}/2)*(1-1_{3|q}/3). Expanding gives

    sum_{q>K} w(q)/q^2
      = T(K) - T(floor(K/2))/8 - T(floor(K/3))/27
             + T(floor(K/6))/216,
    T(M)=sum_{m>M} 1/m^2.

For M>=1 the decreasing-integrand comparison gives
1/(M+1)<=T(M)<=1/M. Use LOWER bounds on the two negative terms and
UPPER bounds on the positive terms. All series converge absolutely, so this
finite signed decomposition is valid. Falsifier: a reversed sign, invalid
floor, or failed integral comparison. In particular K<6 is outside this formula.

**FINITE (DERIVED; EXPERIMENTALLY_SUPPORTED).** The implementations agree on
21 prefix cases, 4,799 open endpoint atoms, and 128 totient counts. The featured
certificate has 325 reduced centers and 297 measure-equivalent union spans.
These finite checks do not establish REINDEX or REMAINDER for arbitrary inputs.
Falsifier: a mismatch in exact areas, centers, spans, or canonical table hash.

## Exact featured certificate

    U = 284968313371778844546722106704309081947931 /
        752789659364709316726334427027022464000000
    U+B(32) = 317271995204241972361184264120776155547931 /
              752789659364709316726334427027022464000000
    (U+1/16)-(U+B(32)) = 989/50490 > 0.

The exact table compares to 17/40, not a rounded decimal. The residue envelope
7210711/175301280 is smaller still, but the headline comparison deliberately
uses the explicitly displayed signed-integral remainder B.

## Remaining objections

Universal arguments need independently authored proof review. Both scripts
and prose have same-assistant authorship, despite different algorithms and
fresh processes. Neither a proof assistant nor an independent human/model
checked the infinite argument. The source is a spliced fragment requiring
human scope review. No submanifold restriction, actual matrix computation,
novelty, or parent solution follows from this scalar certificate.
