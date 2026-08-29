# Coefficient pullback: exact finite-length correction

## Scope, definitions and quantifiers

The ranked candidate asks about descending Hilbert–Kunz multiplicities over a
fixed finite base field. The exact statement, including its quantifiers, is
frozen in snapshot.json. The imported research summary proposes a Monsky
construction and warns that forcing the residue field via k+m changes the
multiplicity. We audit only that warning, not the quartic construction,
normality of those quartics, or the parent question's resolution.

For a local ring (R,n) of characteristic p and dimension d, put q=p^e,
n^[q]=(a^q:a in n), L_R(q)=length_R(R/n^[q]), and
e_HK(R)=lim L_R(q)/q^d. Module length is measured over R, not an arbitrarily
chosen smaller coefficient field. Viewing a K-algebra B as a k-algebra leaves
its underlying ring and its intrinsic length unchanged.

By contrast, let k subset K be finite perfect fields, r=[K:k], let B be a
Noetherian local K-algebra with residue K, maximal ideal m and B=K+m, and put
A=k+m. Assume A is Noetherian of the same positive dimension d. A has residue
k and is a different ring. The bounded computational model has k=F2,
K=F_(2^r), r=1..4, and
B=(K[x,y,z_1,...,z_(d-1)]/(xy))_(x,y,z), d=1..3.
This reduced singular node family is not a domain and is not Monsky's quartic.

## Approach 1: exact sequence and coefficient roots

Claim TRANSPORT (DERIVED, UNVERIFIED pending independently authored proof):
for all q=p^e under the preceding assumptions,

    L_A(q) = r*L_B(q) - (r-1).

Indeed I=m^[q]_A is stable under K multiplication: for lambda in K choose
mu in K with mu^q=lambda, so lambda*a^q=(mu*a)^q and mu*a remains in m.
It is already stable under m, hence under B=K+m. Thus I=m^[q]_B, as actual
subsets of both rings, not just after extending an ideal. This is where
perfectness is used. One must not replace this step with an unproved assertion
that extension and contraction of arbitrary ideals agree.

There is an exact sequence of A-modules

    0 -> A/I -> B/I -> K/k -> 0.

Length restriction along A->B gives length_A(B/I)=r*length_B(B/I).
Also m annihilates K/k, whose k-dimension is r-1. Additivity gives the claimed
formula. Dividing by q^d, for d>0, yields the imported multiplier r on e_HK,
provided the relevant limits and ring hypotheses hold. Dimension zero is not
covered: the correction would not tend to zero. Failure of ideal stability,
the exact sequence, length restriction or the dimension hypothesis falsifies
this argument. The source-backed length lemmas are distinct from our application.

## Approach 2: normal forms in a singular finite-type model

Let C=K[x,y,z]/(xy) before localization and C0=k+C_+. The ring C0 is generated
over k by beta_j*x, beta_j*y and beta_j*z_i for a k-basis beta_j of K including1:
each positive monomial can put its coefficient on one variable. Hence C0 is
finite type. Localizing C0 at its positive ideal gives k+m inside B: normalize
any denominator to constant term1, and its inverse is allowed in C0's local
ring; a numerator with residue in k belongs to C0. B is finite over A since a
k-basis of K generates B=K+m as an A-module, and thus dimensions agree.
B has dimension d and embedding dimension d+1, so it is singular at the origin.
These model-identification steps remain ordinary proof arguments needing review.

Modulo x^q,y^q,z_i^q, the monomials have all exponents below q and cannot
contain both x and y. Counting the two branches and subtracting their overlap
gives L_B(q)=(2q-1)q^(d-1). In A only the constant coefficient loses r-1
dimensions. Thus the proposed exact model formula is

    L_A(q) = 1 + r*((2q-1)q^(d-1)-1).

It gives e_HK(B)=2 and e_HK(A)=2r by an exact limit calculation, not fitting
the four sampled q-values. The universal count/model proof is UNVERIFIED in
the repository's proof-review sense. The finite lengths are independently
checked by linear algebra rather than this count.

For r=2,d=1,q=2, B/I has K-basis 1,x,y (length3), while A/I has F2-basis
1,x,beta*x,y,beta*y (length5). The naive finite preservation claim is FALSIFIED.
The alternative formula r*L_B(q) predicts6 and is also FALSIFIED: it forgot
the constant correction. This does not by itself deduce different limits;
that deduction uses the all-q count above. For r=1, A=B; for q=1, both
residue quotients have intrinsic length1. These are mandatory controls.

## Finite evidence, typed status and progress

experiments/theory.py predicts48 profiles for four fields, dimensions1..3
and q=1,2,4,8. Preservation fails in27 cases; omitting the correction fails
in36. Four certificates give full quotient bases and all coefficient q-th
roots. Theory computes roots by polynomial convolution/long division and
repeated squaring, distinct from the verifier's shift/reduction and repeated
multiplication. All hashes and typed claims are in cycle.json and manifest.json.

The changed evidence is an exact finite correction to the imported asymptotic
warning and explicit singular-ring quotient witnesses. Retire naive
residue-field preservation and r-times-length without its constant correction.
Neither a descending sequence nor a fixed-residue-field solution is produced.
The next material step would review the general transport proof or compute
the actual pinned quartics, not add more node counts.
