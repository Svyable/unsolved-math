# Counterexample-first verification

## Actual independence

verify.py was authored and successfully baseline-run before theory.py existed.
It builds an explicit finite F2-algebra and the span of Frobenius-ideal
generators, rather than using the length-transport formula or a closed
monomial count. Each child runs with Python -I, empty environment and bounded
CPU/memory. Boundary and census computation precede any proposal read.
Evidence paths are distinct. Same-assistant authorship and shared model,
input, Python/runtime and serialization remain limitations; this is not
independent human/model review or kernel checking.

## Boundary search

The first cases are (r,d,q)=(2,1,2),(2,1,1),(1,1,2),(2,2,2).
Their pullback lengths are5,1,3,11. Comparing r=2 with r=1 at d=1,q=2
discriminates the preservation shortcut. The q=1 and r=1 controls expose
the mistaken use of a coefficient-vector-space dimension as intrinsic module
length. The suspension case checks that the dimension exponent is not always1.

## Finite algebra and rank method

For each q, enumerate monomials with every exponent at most q and xy=0.
The ambient pullback algebra has one constant basis vector and r coefficient
basis vectors for each positive monomial. The coordinate cap q+1 is deliberate:
it retains x^q and its analogues, so ideal generators are not silently erased.
Excluded higher powers lie in the intended ideal because finite-field q-th
roots supply every coefficient of each variable's q-th power. The finite
quotient therefore computes the intended local quotient, conditional on the
ordinary local-model argument audited below.

The maximal ideal is generated over A by beta_j times each variable. The
verifier explicitly computes every generator's q-th power and its product
with every ambient F2-basis vector. Frobenius additivity justifies using this
finite generating set. Each product is encoded as a bit vector, and XOR
elimination gives the ideal's F2-rank. It uses neither the factor (2q-1) nor
the coefficient-transport formula. Polynomial-basis finite fields use moduli
3,7,11,19 (binary polynomials of degrees1..4); every element satisfies
a^(2^r)=a and every nonzero element has a multiplicative inverse in the
implemented arithmetic. This checks the supplied small field presentations.

All48 profiles match. The census emits220110 generator-product columns,
including zero and repeated columns; this is not220110 distinct independent
relations. Ordered column hashes permit replay. Four certificates list full
quotient bases. Appending their vectors to the computed ideal basis must
increase rank each time and span the whole ambient space. Coefficient-root
witnesses are checked by independent powering. These total132 checks:
100 quotient-basis vectors and32 coefficient-root equations.

Six altered packets are rejected: wrong length, missing basis vector,
duplicate vector, ideal vector substituted for a quotient vector, wrong
coefficient root, and missing census profile. Replay reproduces both output
files byte-for-byte. Five successful children and one failed setup child used
six of eight invocations; see execution-notes.md for the missing-input failure
and incomplete failure logging. No output from that failure supports a claim.

## Proof-step and citation audit

1. For the finite-type model, beta_j-variable generators produce all positive
   coefficient monomials. Local denominator normalization identifies its
   local ring with k+m. This must not be confused with simply restricting the
   base field of B, which changes no ring.
2. The proof that m^[q]_A is a B-ideal uses K's q-th roots. Perfectness is an
   actual hypothesis, not something demonstrated by the length table.
3. Once ideal equality holds, B/A=K/k and the short exact sequence supply
   the finite correction. The module-length restriction lemma applies to
   B/I as a B-module; it is not applied to A/I as a B-module.
4. The formula for the node counts two branches, subtracting their common
   z-monomials. The constant term is counted once over k, not once over K.
5. An all-q formula yields the stated limits for positive d. Four q-values
   alone do not certify any Hilbert–Kunz limit or descending sequence.

The cited Stacks lemmas support length restriction/additivity, not the whole
pullback theorem. Huneke's definitions use local module length. Brenner–Monsky
is scope evidence only; no quartic kernel theorem is reproduced here. AIM
failed over both HTTP and HTTPS, so its source wording and intended fixed-base
versus fixed-residue interpretation have not been independently recovered.

The finite claims are EXPERIMENTALLY_SUPPORTED and the two finite shortcut
claims FALSIFIED. General transport, local-model identification and exact-limit
arguments remain UNVERIFIED pending independently authored proof review.
No normal-domain example, quartic calculation, new descending family, or
parent solution is claimed.
