# A uniform-annihilator audit, not a TC computation

## Frozen scope and definitions

The exact parent question is in snapshot.json. Its imported research summary proposes a
rationalization/Tate obstruction and finite torsion windows. Those remain external
unverified claims. This packet checks a prerequisite: finite-stage torsion does not
justify moving rationalization through an inverse limit. No actual Tate tower,
cyclotomic Frobenius or motivic filtration is constructed here.

Fix a prime p. Let A_n=Z/p^n for n>=1 with reduction maps A_(n+1)->A_n.
Let A be the group of compatible infinite sequences. Rationalization means
S^(-1)A for S=Z minus zero. A coordinate being torsion means its annihilator
may depend on that coordinate. A rationalized sequence vanishes only if one
nonzero integer annihilates the entire sequence. This is a change of quantifiers.

## Approaches and falsification

1. Closed cyclic-group formulas and p-adic valuations give exact order spectra
   and the first coordinate escaping any proposed annihilator.
2. Direct repeated addition and exhaustive residue paths reconstruct finite
   groups without these formulas; this is the separate verification lane.
3. The shortcut 'every finite stage rationalizes to zero, so does the limit'
   is rejected by the ordinary argument below. Finite searches alone cannot reject
   a universal claim about the infinite object.

Falsifiers include a unit sequence failing compatibility, a nonzero d killing
every unit coordinate, incorrect first escape level, or an incorrect transition
fiber. Zero elements, level one, and bounded-exponent towers are controls.

## Exact ordinary argument (UNVERIFIED by independent author/kernel)

The sequence u=(1 mod p^n)_n is compatible. For any nonzero integer d, write
d=p^k e with p not dividing e. At coordinate k+1, d*u is nonzero modulo p^(k+1).
Thus no nonzero d annihilates u. The localization equivalence relation implies
u/1 is nonzero in S^(-1)A. Yet every A_n is killed by p^n, so S^(-1)A_n=0.
Consequently the canonical map S^(-1)(lim A_n)->lim S^(-1)A_n is not injective.
This proves the algebraic counterexample by an ordinary argument, not by the
finite census and not by formal verification. Identifying A with Z_p is optional;
the argument uses only compatible coordinates.

For the control B_n=Z/p^min(n,2), reductions eventually become identities.
The common annihilator p^2 kills every coordinate, hence the limit and its
rationalization vanish after localization. More generally a common nonzero
annihilator is sufficient for zero rationalization of the limit; it is not
claimed necessary for all towers or for each elementwise-torsion group.

## Reproducible finite evidence

The experiment covers p=2,3,5,7 and n=1,...,4, both A_n and B_n: 32 groups
and 4,008 elements. It records every additive order and complete transition
fiber counts. For d=1,...,120 at each prime, 480 certificates record the first
coordinate where d*u survives. Another 52 certificates show p^k survives
at level k+1 for k=0,...,12. The witness d=2,p=2 already separates level one
from level two. All finite bounds are explicit; the universal argument above
is a separate proof obligation.

## Source and novelty boundaries

This is a standard inverse-limit/localization counterexample, not novel mathematics.
Stacks 00CM supplies the localization definition. HRW v3's abstract establishes
the scope of their filtration construction, not this packet's claimed computation.
The Segal-conjecture source explicitly warns that inverse limits of spectral
sequences require care. None identifies our elementary group tower with the
Tate construction. Such a comparison, convergence, graded pieces, and the imported
positive-weight torsion-window claim remain unverified. Finite amplitude alone
also does not imply finite cardinality: infinite direct sums of Z/p are a
separate elementary obstruction. We do not promote any imported status.
