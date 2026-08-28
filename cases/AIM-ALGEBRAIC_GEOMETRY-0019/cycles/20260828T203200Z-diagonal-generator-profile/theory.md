# Equal degree does not determine the diagonal Ext profile

## Frozen question and changed evidence

The schema-v2 packet freezes the imported statement, not a corrected version of it.
Selection is ranked queue position 11 after cooldown exclusions. The parent cycle
`20260827T183200Z-inseparable-diagonal-audit` checked one-generator truncated
polynomial diagonals and the failure of composition-zero to imply exactness.
This follow-up asks one narrower, falsifiable question: does equal algebra dimension
(and, in the proposed field realization, equal extension degree) determine the
diagonal Ext profile? It does not. This is not a claim that degree cannot bound it.

New exact witness: for any coefficient field K, compare R1=K[x]/(x^4) and
R2=K[x,y]/(x^2,y^2), both of dimension four, with residue module K. Their
augmentation ideals satisfy

- I1=(x,x^2,x^3), I1^2=(x^2,x^3), so dim(I1/I1^2)=1;
- I2=(x,y,xy), I2^2=(xy), so dim(I2/I2^2)=2.

The duals of the displayed quotient bases give explicit Ext^1 certificates.
The packet checks them by a bar differential, not by assuming the proposed
periodic resolution. Hence a dimension-only profile shortcut is retired.

## Definitions, quantifiers and assumptions

Let K be a field, r>=1, and m_1,...,m_r>=2. Set
R=K[x_1,...,x_r]/(x_1^m_1,...,x_r^m_r), with augmentation epsilon(x_i)=0
and I=ker(epsilon). All modules are ordinary ungraded R-modules; homological
degree is separate from monomial exponent. Define beta_n=dim_K Ext_R^n(K,K).
The augmentation and coefficient field are fixed. The diagonal realization below
uses tensor products over k, not over L. No assertion covers arbitrary local
algebras or arbitrary inseparable extensions with the same number of generators.

The finite experiment uses precisely primes 2,3,5; exponent lists (2),(3),(4),(2,2);
and n=0,...,4. Differentials through degree 5 test these homology degrees. The
bar contraction is checked on basis elements of free-bar degrees 0,...,3.
Odd-characteristic square-zero examples are algebra controls, not purported
inseparable degree-four field extensions. No numerical floating point is used.

## Approach A: tensor periodic resolutions (ordinary universal derivation)

For R_i=K[x_i]/(x_i^m_i), the augmented rank-one resolution has d_n equal to
multiplication by x_i for odd n, and x_i^(m_i-1) for positive even n.
Its exactness follows from the two annihilator ideals. Tensor these complexes
over the field K. In the first-quadrant total complex,

P_n = direct sum over |a|=n of R e_a,

D(e_a)=sum over j with a_j>0 of
(-1)^(a_1+...+a_(j-1)) t_j(a_j) e_(a-e_j),

where t_j is the alternating multiplier above. Same-factor compositions vanish;
the mixed terms cancel with opposite signs. Exactness of the augmented total
complex follows by tensor exactness/Kunneth over K, with finitely many summands
in each degree. Each entry lies in I, so applying Hom_R(-,K) gives zero
differentials. Counting weak compositions proposes

beta_n = binomial(n+r-1,r-1), for every n>=0.

In particular R1 has sequence 1,1,1,1,... and R2 has 1,2,3,4,... . The all-degree
derivation remains UNVERIFIED under the repository's independent-proof standard;
finite tests are not its proof. The finite tensor matrices do check augmentation,
D^2, ranks, and zero Hom differentials independently of this counting assertion.

## Approach B: augmentation quotients and bar complexes

Ext^1 is the dual of I/I^2: the reduced bar differential I tensor I -> I is
minus multiplication, while the degree-one to degree-zero differential is zero.
Taking duals makes cocycles precisely functionals killing I^2, with no degree-one
coboundaries. This gives the small witness without assuming Approach A's
all-degree exactness. The independent lane builds higher bar differentials and
an explicit free-bar contraction as a cross-check of the resolution model.
The basis order for R2 is (1,y,x,xy); the two certificates on I are (0,1,0)
and (1,0,0). For R1 it is (1,0,0) on (x,x^2,x^3).

## Construction audit: the tensor sign is necessary

On e_(1,1), the two unsigned composition paths give xy+yx=2xy. This is nonzero
in the frozen characteristics 3 and 5, and zero in characteristic 2. The correct
signed differential gives xy-yx=0. Thus characteristic-two-only tests would miss
this implementation error. The literal two-path checker is separate from both
resolution implementations. This auxiliary falsification concerns construction
of the same profile calculation, not a second parent problem.

## Proposed field realization and category boundary

Let k=F2(s,t), with algebraically independent variables. Put L1=k(u), u^4=s,
and L2=k(v,w), v^2=s, w^2=t. For L1, first adjoin q with q^2=s, then u with
u^2=q. The s-adic valuation in k and q-adic valuation in F2(q,t) show that the
successive elements are not squares. For L2, use s-adic and then t-adic
valuations in F2(v,t). Each tower has two irreducible quadratic steps, so both
degrees are four and both extensions are purely inseparable. The cited Stacks
lemmas supply the irreducibility and tower facts; the valuation applications
here are our ordinary derivation.

As left Li-algebras, translation of the right generators gives

L1 tensor_k L1 = L1[e]/(e^4),
L2 tensor_k L2 = L2[e1,e2]/(e1^2,e2^2).

The multiplication diagonal is the augmentation module Li. The prime-field
matrix ranks persist after scalar extension, but the rational-function-field
presentations and their universal interpretation are not computed by this census.
They remain UNVERIFIED pending independently authored or kernel review.
Perf(Li) still has Rouquier dimension zero and a singleton presentation, just as
in the parent example. Nothing here constructs a general comparison between
diagonal length and homotopy-colimit depth, refutes a published theorem, or
changes the imported status. Perfect exterior-product hypotheses must not be
replaced by arbitrary bimodule terms.

## Typed claim ledger and falsifiers

- DIMENSION-SHORTCUT — FALSIFIED, DERIVED proposal: dimension four determines
  beta_1. Falsifier/certificate: quotient dimensions 1 versus 2; invalidate this
  result by a wrong multiplication table, noncocycle or dependent quotient basis.
- PROFILE — UNVERIFIED, DERIVED: the all-n binomial formula for the explicitly
  tensor-truncated family. Falsify by failed exactness, sign or totalization step.
- FIELD — UNVERIFIED, DERIVED with primary-source dependencies: the two field
  realizations have degree four and the stated diagonals. Falsify by a square in
  a tower step, wrong base tensor product, or incorrect presentation dimension.
- SIGN — FALSIFIED, DERIVED proposal: unsigned tensorization always forms a
  complex. Falsifier: 2xy in characteristics 3 and 5; char2 is a negative control.
- FINITE — EXPERIMENTALLY_SUPPORTED, DERIVED: 12 algebras and 60 Ext entries
  agree between implementations; 12 Ext1 certificates pass. Falsify by any
  omitted frozen tuple, changed rank, mismatched profile or accepted corruption.
- SOURCE — PRIMARY_SOURCE_SUPPORTED, PRIMARY_SOURCE: the cited diagonal and
  homotopy-colimit bounds are separate sufficient estimates, with the specified
  hypotheses. Falsify by a contrary text or attribution. See source notes.

## Handoff

This is a known-algebra calibration and assumption distinction, not a new
mathematical theorem. Seek independent review of the universal tensor and field
arguments before extending the obstruction ledger. More primes or degrees alone
would not constitute material progress. Rotate after this packet.
