# Residual regularity: a dimension-qualified certificate

## Scope, definitions and assumptions

The frozen parent is an odd-primary Wood-filtration question. The imported summary
reduces one proposed rank-one witness to nonvanishing of (g-1)^(p^n-1) on a residual
representation. This audit tests that algebraic step, not its spectral realization.
Imported claims, including equivalence to external filtrations, remain unverified.

Let k have characteristic p, q=p^n with n>=1, and V be finite-dimensional. A cyclic
action is a linear g with g^q=I. Put N=g-I. Then N^q=0, since in characteristic p
(g-I)^q=g^q-I. The group algebra k[C_q] is k[t]/(t^q), with t corresponding to g-1.
Rank-one regular means isomorphic to this module, in particular dim_k V=q.
All experiments use prime fields; general-field statements below are ordinary
UNVERIFIED arguments, not extrapolations from the census.

## Two approaches

1. Compute matrix powers N^j. If dim V=q and N^(q-1) is nonzero, choose a standard
   basis vector v with N^(q-1)v nonzero. The chain v,Nv,...,N^(q-1)v is a basis.
   Its binomial change of basis gives v,gv,...,g^(q-1)v.
2. Independently iterate g on vectors, test g^q=I, and use modular elimination to
   check whether the orbit spans V. Finite differences recover N-powers without
   multiplying N matrices. The verification lane implements this route.

Falsification targets: omitted dimension constraint, weakened exponent, invalid
group action, a singular purported orbit basis, or an incorrect cyclic wraparound.

## Ordinary proof (UNVERIFIED by independent author/kernel)

Assume dim V=q. If N^(q-1)v is nonzero, any nontrivial relation among the chain has
a least nonzero coefficient a_j. Applying N^(q-1-j) leaves a_j N^(q-1)v=0, a
contradiction. Thus the chain is a basis and t acts as a single nilpotent block.
Conversely multiplication by t on k[t]/t^q has nonzero t^(q-1). The binomial matrix
from N-powers to g-powers is triangular with diagonal one, so the orbit basis also
has full rank. In that basis g is the cyclic permutation matrix, an explicit
regular-representation isomorphism. No algebraic closure is required.

This argument certifies an ordinary residual module, not a spectrum. An actual
Morava K-cohomology action, finite realizing complex, grading and descent/filtration
comparison would still be required. A p^n-cell count cannot silently substitute
for an independently verified residual dimension calculation.

## Counterexamples to weakened tests

Use N=J_3 direct-sum J_1 over F_3. Then g=I+N satisfies g^3=I and N^2 is nonzero,
but dim V=4, so it is not rank-one regular over F_3[C_3]. This does not refute the
imported claim with its q-dimensional hypothesis; it prevents a weakened checker.

Use N=J_2 direct-sum J_1 over F_3. This has dimension 3 and N is nonzero, but N^2=0.
It is not regular: the exponent q-1 cannot be replaced by q-2. Analogous controls
at (p,q)=(5,5) and (3,9) retain those distinctions.

## Finite evidentiary delta

Exhaust all 19,683 matrices N over F_3 in dimension 3 and all 16 over F_2 in
dimension 2 (the latter is a boundary control, not odd-primary evidence).
There are 729 and 4 valid cyclic actions respectively. Of these, 624 and 3 are
regular. Every accepted regular action has an explicit standard-vector generator
and orbit-basis certificate. All 733 valid actions satisfy the dimension-qualified
test; nine specified block controls test q=3,5,9 and dimension q or q+1.
No exhaustive claim is made in dimensions 5 or 9.

This is known linear algebra made reproducible for future residual candidates,
not novel mathematics or a Wood-filtration construction. Carrick's cited defect
formula is background; deriving a lower bound for a specific external T(r)-free
witness still requires the relevant spectral bridge and hypotheses.
