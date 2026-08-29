# Hidden extensions, not a computation of TC

## Frozen target and changed evidentiary state

The prior cycle showed that torsion at each finite stage need not persist after
an inverse limit. This cycle asks a stronger diagnostic question: even with the
same finite graded pieces, a complete separated filtration, and a collapsed
convergent spectral sequence, is rational vanishing determined? We exhibit
extension data that the page forgets, and an exact bounded-carry repair in a
specified presentation family. The imported TC and positive-weight claims are
not inputs to our proofs, and remain unverified.

## Definitions and quantifiers

Fix a prime p, an integer n>=1, and e in {0,1}^{n-1}. Let G(p,e) be the abelian
group on x_0,...,x_(n-1) with relations p*x_i=e_i*x_(i+1), and p*x_(n-1)=0.
Its digit representatives have coordinates in {0,...,p-1}. Addition carries
from coordinate i to i+1 only if e_i=1. Truncation deletes the final digit.
F^s is the subgroup with its first s digits zero; F^s=G for s<=0.
Each nonzero successive quotient F^s/F^(s+1) is Z/p.

For a fixed infinite edge sequence e, A(e) is the inverse limit of its digit
truncations. F^s A is the kernel of projection to s digits. This filtration is
exhaustive, separated and complete. Rationalization here means Q tensor_Z A;
there is no topological tensor product. A block is a maximal interval of digits
joined by 1-edges. A block with L digits has L-1 carry edges. Block length,
filtration length and homological amplitude are different quantities.

## Approaches and falsifiers

1. Split at zero edges. Eliminate generators inside each block to obtain cyclic
   factors, their element orders and an explicit isomorphism matrix.
2. Independently normalize literal digit sums, add each element until zero, and
   test the proposed matrix on every element plus each generator. No block
   decomposition or cyclic-order formula is imported by the verifier.
3. Reading the total exponent from the number of nonzero extension edges, or
   rational vanishing from identical collapsed pages, loses essential data.

Falsifiers: a digit normal form collision, a nonhomomorphic truncation, unequal
graded layers, a false block isomorphism, an element violating the exponent,
or an infinite sequence with bounded blocks but no uniform annihilator.
The zero carry, all carry, one-digit and disjoint-carry cases are controls.

## Exact finite counterexample (computationally certified)

At p=2,n=4 compare e=(1,1,0) with e=(1,0,1). Both groups have 16 elements,
four graded layers Z/2, and exactly two nonzero carry edges. The first is
Z/8 plus Z/2 with exponent 8. The second is Z/4 plus Z/4 with exponent 4.
In the first, 4*x_0=x_2!=0; in the second, 4 annihilates the whole group.
The matrix certificates explicitly identify these groups and certify the
surviving multiples. Thus even counting the extensions is insufficient:
their arrangement matters. No assertion about an actual TC extension is made.

## Ordinary derivation (UNVERIFIED by independent author or kernel)

For every finite p,e, cut the digit interval at each zero edge, with resulting
block lengths L_1,...,L_r. Inside a block starting at a, x_(a+j)=p^j*x_a;
its last relation is p^L*x_a=0. Different blocks have no relations between
them. The digit-to-factor map is sum_j d_(a+j)*p^j modulo p^L. This gives
G(p,e) = product_j Z/p^(L_j) and exponent p^(max L_j). The number killed by
p^k is p^(sum_j min(k,L_j)), including k=0. Differences of these cardinalities
give exact element-order counts. These formulas apply to the full family,
not just the tested domain; the general argument is pending independent review.

For infinite e with infinitely many zero edges, A(e) is the product of the
finite cyclic blocks. This is a product, not a direct sum: arbitrary choices
in all blocks define compatible digit sequences. If there are finitely many
zero edges, a final infinite block contributes a copy of Z_p.

Consequently Q tensor A(e)=0 iff there is a finite uniform bound on all block
lengths. Sufficiency: p^L kills every factor and hence the whole limit.
Necessity for unbounded finite blocks: choose the element with value 1 in each
cyclic factor. For any nonzero integer d, choose a block with L>v_p(d); its
coordinate survives multiplication by d. For a final infinite block the same
argument uses a digit truncation of length v_p(d)+1. Localization therefore
does not kill this element. This is an infinite argument, not a consequence
of the 173-row experiment. It is specific to this nearest-neighbour family.

## Collapsed-page obstruction and finite-width repair

Take e identically 1 versus identically 0. The limits are Z_p versus product
of countably many Z/p. Their graded groups are identical: one Z/p in each
filtration degree s>=0. Regard each as a cochain complex concentrated in degree
zero. The associated spectral sequences have the same E_r^{s,-s}=Z/p for
all r>=0 and all other entries zero. Every differential is zero. They satisfy
the convergence conditions of Stacks Definition 12.24.9, since the filtrations
are complete, separated and exhaustive and the differentials are regular.
Nevertheless the rationalization of the first is nonzero, that of the second
zero. This does not contradict convergence: it specifies the associated
graded of the abutment, not its additive extensions.

The exact failed transfer is visible after rationalization. For Z_p,
Q tensor p^s Z_p equals Q tensor Z_p for every finite s, so the rationalized
filtration is not separated. It has zero graded groups but nonzero total
group. The example is concentrated in a single homological degree; bounded
homological amplitude is therefore not a bound on filtration width.

A valid finite-width statement: if F^0 A=A, F^L A=0, and p annihilates every
F^i/F^(i+1), then p^L A=0. Indeed p F^i is contained in F^(i+1), and iterate
L times. The all-carry length-L group shows this exponent is sharp; p need
not kill A. Finiteness of the layers also gives a finite group for finite L,
but not for infinitely many layers. This is a standard extension bound, not
a new theorem about a motivic spectral sequence.

## Evidence and limits

173 presentations, 21,142 digit elements and complete ordered order-table
digests agree. Six explicit isomorphisms pass 904 generator-homomorphism
checks. The independent small group-law audit covers 2,184 associativity
triples and 292 commutativity/truncation pairs. All results are exact integers.
The matrix checker initially omitted injectivity and admitted a quotient map;
that failure and the old bytes are retained, and the repaired checker rejects
all seven specified corruptions. This is an actual verification correction,
not evidence that arbitrary corruptions are rejected.

The two implementations have same-assistant authorship and shared inputs and
serialization. No independent human/model or kernel review, no actual Tate
tower or HRW graded calculation, no novelty and no parent solution is claimed.
