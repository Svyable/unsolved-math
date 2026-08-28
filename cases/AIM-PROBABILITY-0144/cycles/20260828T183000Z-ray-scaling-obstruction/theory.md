# Sharp ray scaling is not a root-system repair

## Delta from the prior packet

The prior I2(5) audit found two abstract one-relation refinements of the
equal-length cone order. Here those SAME five rays admit an explicit coordinate
realization after individual rescaling, with sharp maximum scale phi. However,
the realized target order breaks the original coordinate-swap symmetry and
the signed vectors are not closed under the original simple reflections.
This is a quantified distinction between a point configuration and a root
system, not a new root-system theorem, a broader-type search or a parent solution.

## Frozen setting and definitions

Let phi=(1+sqrt(5))/2, phi^2=phi+1, 1<phi<2. In the simple-root basis, fix

    r0=(1,0), r1=(0,1), r2=(phi,1), r3=(1,phi), r4=(phi,phi).
    v0=r0, v1=r1, v2=a*r2, v3=b*r3, v4=c*r4, a,b,c>0.

The Gram form is fixed as [[1,-phi/2],[-phi/2,1]]. The two ORIGINAL simple
reflections are s1(x,y)=(-x+phi*y,y) and s2(x,y)=(x,-y+phi*x).
Closure means both preserve the signed set S={+-v0,...,+-v4}, not only the
positive vectors or the rays. No change of Gram form, simple roots or directions
is allowed. All roots before rescaling have norm one, so in the optimization
domain 1<=a,b,c<=D, D bounds the largest norm relative to the fixed simples.

The strict cone relation i<j means i!=j and vj-vi has both coordinates
nonnegative; one coordinate may be zero. A successful repair retains the eight
old relations 0,1<2,3,4 and 2,3<4 and has
H(s,t)=sum_A s^|A intersect {0,1}| t^|A|=1+2st+3t+s^2*t^2.
The coordinate swap has fixed label permutation sigma=(0 1)(2 3), fixing 4.
Order invariance under sigma is tested separately from reflection closure.

## Approaches and falsification targets

1. Preserve the reflection system, or require the original swap symmetry of
   its labelled cone order. This cannot attain the target refinement here.
2. Allow positive independent ray scales. Solve coordinate inequalities for
   the two possible middle-chain orientations and construct exact attainers.
3. Certify the lower bound by nonnegative linear combinations of necessary
   inequalities. This provides an executable algebraic certificate, not a
   minimum inferred from a finite grid.

Targets: arbitrarily small scaling suffices; target H implies reflection
closure; equality in a coordinate must be disallowed; a symmetric choice of
the two abstract refinements exists.

## Typed claims and arguments

**REGION — DERIVED, UNVERIFIED universal argument.** For all positive a,b,c,
success is equivalent to

    a>=1, b>=1, c>=a, c>=b,
    and either b>=phi*a or a>=phi*b.

The first four inequalities are exactly retention of the old relations:
r1<=v2 requires a>=1, r0<=v3 requires b>=1, v2<=v4 requires c>=a,
and v3<=v4 requires c>=b. They imply the other old comparisons.
Only {2,3} remains undecided. The target H permits the pair {0,1} but
no other incomparable pair, so 2 and 3 must be comparable. The coordinate
test v2<=v3 reduces to b>=phi*a; the reverse to a>=phi*b.
Both cannot hold for positive a,b because phi^2>1. Falsifier: a positive
triple with a different exact relation/antichain profile.

**OPTIMUM — DERIVED, UNVERIFIED general implication with checked algebraic
certificates.** A successful triple in [1,D]^3 exists iff D>=phi. For the
orientation v2<v3, the following necessary nonnegative terms sum to D-phi:

    phi*(a-1) + (b-phi*a) + (D-b) = D-phi.

For the reverse orientation interchange a,b. The two coefficient certificates
are in experiments/lower-bound-certificate.json. A separate checker derives
the constraint rows from the frozen coordinates and verifies nonnegative
multipliers and exact polynomial reduction modulo phi^2-phi-1.
Thus either orientation requires D>=phi. The triples (1,phi,phi) and
(phi,1,phi) attain it; they remain feasible for every larger D. At equality,
nonnegative terms force the smaller middle scale to 1 and larger to phi;
c>=max(a,b) and c<=D then force c=phi. These are exactly two labelled
optimal triples. Falsifier: a bad dual identity, an omitted orientation,
a smaller feasible budget or an additional equality-case triple.

**ROOT_SHORTCUT — DERIVED, FALSIFIED.** A scaled configuration having target H
and retaining the old cone order is still a root system for the original
simple reflections. At (a,b,c)=(1,phi,phi), the positive vectors are

    (1,0), (0,1), (phi,1), (phi,1+phi), (1+phi,1+phi).

They have the target order, but s2(v0)=(1,phi) is absent even from the signed
set. The opposite optimal triple has the mirrored missing reflection.
Falsifier of this counterexample certificate: membership of the reflected
vector or an incorrect target H computation.

**CLOSURE — DERIVED, UNVERIFIED universal argument.** For any positive scales,
S is closed under both original simple reflections iff a=b=c=1. Necessity:
s1(v1)=r2 forces a=1 since S has one positive vector on that ray; s2(v0)=r3
forces b=1; then s2(v2)=r4 forces c=1. Sufficiency is the finite reflection
closure of the original ten roots, checked directly. No successful repair
therefore retains closure in this fixed setting. Falsifier: an alternative
scaled vector on a required ray or a different closed positive triple.

**SWAP — DERIVED, UNVERIFIED universal argument.** No successful retained
order is invariant under sigma: it contains exactly one of 2<3 and 3<2,
while sigma exchanges them. This obstruction holds for the two abstract
refinements themselves, not just for the optimal coordinates. It does not
forbid an isomorphism between the two different orders. Falsifier: a target
refinement whose relation set is fixed by sigma.

**CENSUS — DERIVED, EXPERIMENTALLY_SUPPORTED.** Among 1,331 frozen triples,
285 retain the old relations and 38 have the target H. All 38 fail both swap
invariance and reflection closure; the sole reflection-closed triple is the
original unscaled one. The separate algorithms agree on the full canonical
case-stream digest, 121 aggregate rows and 24 near-boundary triples. The grid
includes positive scales below 1 solely as boundary controls. Falsifier:
a mismatched exact case stream, count, vector or certificate.

## Limits and next step

The full real-parameter reduction, optimal inference from the algebraic
identities, and equality classification are ordinary same-author arguments,
not kernel-accepted proofs. The independent computation is method/process
separation, not independent human/model authorship. Source scope needs human
review. No H3/H4 extension, modified metric, canonical root labelling, all
six published properties, novelty or solution of the parent is claimed.
Retain the sharp fixed-ray certificate and closure obstruction; further grids
alone are not new progress.
