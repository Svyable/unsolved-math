# Minimum cyclic-equivariance defects without a bijectivity assumption

## Bounded target and delta from the previous packet

The preceding packet, 20260827T104644Z-cyclic-factor-audit, required T to be a
permutation and audited exact regular cyclic factors. This follow-up keeps its
abstract cyclic-label model but allows an arbitrary finite self-map and measures
the least number of failed equivariance equations. It is not an application to
ASM, rowmotion, PL, birational or other actual combinatorial dynamics.

Two concrete changes result: the exact criterion loses the bijectivity
assumption, and a three-state certificate shows that minimizing equation failures
does not automatically give a surjective approximate labeling. Thus a quantitative
defect statistic must keep surjectivity as a separate requirement. These are
elementary calibration results; no novelty or parent-solution claim is made.

## Definitions, quantifiers and assumptions

For every finite X={0,...,n-1}, n>=0, total function T:X->X, and integer N>=1,
a labeling f takes values in C_N=Z/NZ. Count labeled functions, not phase classes.
Define

    D(f) = #{x in X : f(T(x)) != f(x)+1 mod N}.

Every edge has unit weight. Let d(T,N)=min_f D(f) and M(T,N) be the number of
minimizers. Let E(T,N) count zero-defect labelings. Separately let d_sur and M_sur
be the minimum and number of minimizers subject to f(X)=C_N. If no surjection
exists, d_sur is undefined (JSON null) and M_sur=0. In particular the empty
labeling has D=0, M=E=1 but is not surjective for N>=1.

A nonempty functional-graph component contains exactly one directed cycle;
all other vertices eventually enter that cycle. Let its cycles have lengths
L_1,...,L_c and call a cycle bad when N does not divide its length. Put b equal
to the number of bad cycles. Trees are directed toward cycles, not away from
them. For n=0 use c=b=0 and an empty product of 1.

## Approach 1: cycle obstructions and tree extension

DEFECT, derived ordinary universal claim (UNVERIFIED pending independent proof):

    d(T,N) = b,
    M(T,N) = N^c * product of L_i over bad cycles,
    E(T,N) = N^c if b=0, and 0 otherwise.

Proof:

1. If all equations on a cycle of length L hold, summing their increments gives
   L=0 mod N. Each bad cycle therefore forces at least one failed equation.
   Distinct cycles have disjoint edges, so D>=b. A failure on an incoming tree
   cannot repair the contradiction around a cycle.
2. On a good cycle choose an initial phase, then increment by one around the
   cycle. On a bad cycle choose an edge to break, choose a phase, and increment
   along its remaining L-1 edges. The closing equation really fails since
   L is nonzero mod N. This also works for L=1, whose only edge is a loop.
3. Extend backward uniquely on every incoming tree by f(x)=f(T(x))-1 mod N.
   Depth induction is valid because T is total and finite; trees introduce
   neither defects nor additional phase choices. This constructs D=b.
4. Every minimizer must attain each cycle lower bound and have zero tree
   defects. A good cycle has exactly N choices. A bad cycle has exactly L*N:
   its unique failed edge and its phase recover the choice uniquely. Choices
   in distinct components are independent, giving the displayed product.
5. Setting b=0 gives E. For nonempty X, any good cycle of length divisible by N
   visits every target label, hence every exact labeling is surjective.

Consequently, for an arbitrary nonempty finite self-map, an exact regular
C_N factor exists iff every directed cycle length is divisible by N. Bijectivity
of T is unnecessary. For example T=[1,0,1],N=2 is not injective yet has the
surjective exact labeling [0,1,0] and exactly two exact labelings.

Falsifiers: a missing component, another tree choice at minimum defect, a
bad cycle requiring zero failures, or a constructed labeling whose cost differs
from b. This theorem is not asserted for partial/infinite maps, arbitrary edge
weights, several outgoing constraints, or a nonregular target action.

## Approach 2: preserve the surjectivity constraint

SURJECTIVITY_SHORTCUT, derived hypothesis, falsified: n>=N does not imply that
an unconstrained minimum-defect labeling is surjective, nor even that there
exists a surjective labeling at the same minimum.

Take T=[0,0,0],N=3. The loop at 0 must fail. Achieving only that failure forces
both leaves to have color f(0)-1, so any one-defect labeling uses just two colors.
There are three such labelings, represented by [0,2,2]. A surjective labeling
uses all three colors, so its leaves have distinct colors and at most one leaf
edge can hold. Its minimum is therefore two, achieved by [0,1,2]; all six
surjective labelings attain it. Direct exhaustion of all 27 assignments checks
the gap independently.

More generally for the n-vertex constant map T(x)=0:

* N=1: d=d_sur=0 and both counts are 1.
* N>=2: d=1 and M=N, with every unconstrained minimizer using at most two colors.
* n<N: no surjection exists.
* n>=N>=2: d_sur=N-1 and M_sur=N*(n-1)!/(n-N+1)!.

For the last statement fix the center's color a. Exactly the leaf color a-1
satisfies an edge. Surjectivity requires the N-2 colors other than a and a-1
at distinct leaves, costing at least N-2 failed leaf edges plus the loop.
At equality each of those colors appears once, and all remaining leaves have
color a-1; at least one such leaf exists since n>=N. Choose a and inject the
N-2 distinguished colors into n-1 leaf positions. This gives the count, including
N=2 where the injection is empty. These formulas concern constrained approximate
labelings, not exact factors.

The simpler statement that every unconstrained optimizer is surjective already
fails in other ways; the exhibited example proves the stronger minimum-gap claim.
It does not refute the previous zero-defect surjectivity argument.

## Approach 3: exhaustive equations rather than cycle formulas

The verification program was authored and its baseline executed before the
theory implementation. It enumerates every label tuple, counts failed equations
directly, and separately tests surjectivity. It uses no graph decomposition or
cycle-length formula. The theory program removes incoming trees by indegree
peeling, reads the remaining directed cycles, and extends labels in reverse
removal order. This is a concrete algorithmic separation; authorship is shared.

## Reproducible finite evidence

The census covers all total maps for n=0,...,5 and N=1,2,3, plus all total maps
for n=0,...,4 and N=4: 10,531 systems and 955,958 direct label assignments.
The n=0 domain has one empty function (0^0=1 in the enumeration). There are
23 aggregate domain rows and 24 constant-map controls for n=1,...,6,N=1,...,4.
Twenty-eight constructed minimum-defect labelings include empty, singleton,
noninjective, mixed-cycle and incoming-tree cases.

The per-system canonical stream [n,T,N,d,M,E] has SHA-256
a89062e94d6c73278ce5b88089c63c5c7f879e516e88fa786dd5662c18b35604 in both
implementations. Full streams are reconstructed by code rather than stored;
aggregate tables and certificates are stored. Theory's label_assignments field
describes the verifier's workload, not assignments enumerated by theory.

Reproduce with python experiments/run.py baseline, theory, verify and replay
(four commands, five bounded mathematical child processes). Each child has a
fresh isolated Python environment, exact integer arithmetic and resource limits.
Finite agreement is not a proof for all finite maps.

## Source and remaining objections

See the separate source notes. The historical workshop text motivates cyclic
factors but does not assert this defect statistic, formula or counterexample.
The exact imported fragment and its extraction artifacts remain frozen; only
the source URL scheme was normalized from HTTP to a freshly accessible HTTPS
path to meet the snapshot contract. No imported status was changed.

Same-assistant authorship/shared specification remains a limitation. The
functional-graph lemma and counting proofs have no independent human/model or
kernel verification. Applying the statistic to actual dynamics would require a
defined action and natural target map; arbitrary cyclic labels alone do not
define or explain resonance. Retain the assumption reduction and regression
certificate, seek independent proof/scope review, and rotate. A larger census
of this same formula is not a new progress unit.
