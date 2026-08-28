# Seeded threshold and ceiling audit

## Scope and definitions

The parent asks about unirational complex hypersurfaces. This packet audits only
the numerical smooth-hypersurface branch of the imported summary. It neither
constructs a parameterization nor audits the general-hypersurface Cheng branch.
Geometric applicability remains dependent on Beheshti--Riedl's published theorem.

For integer d>=2 define k_2=0 and
k_d=1+2*C(k_(d-1)+d-2,d-2)+C(k_(d-1)+d-1,d-1).
Put B_d=C(k_d+d,d) and n_d=k_d+ceil(B_d/(k_d+1)).
This is a sufficient threshold, not a claimed optimal unirationality boundary.
Its arithmetic characterization is (k_d+1)(n_d-k_d)>=B_d, with failure at n_d-1.
All stored large integers are hexadecimal strings, exactly recoverable by int(s,16).

## Approaches and falsification targets

1. Library binomial coefficients and quotient/remainder division give exact
   recurrence values and minimal integer inequality witnesses.
2. Rational products for binomial coefficients and a direct monotone inequality
   search give an independent algorithm, without a ceiling formula.
3. Seed propagation avoids full rapidly growing recurrences but loses sharpness.

Search for off-by-one rounding, altered seeds, unsafe dyadic rounding and a
closed bound smaller than the exact threshold. The universal estimates below
are ordinary UNVERIFIED proofs, not inferred from the bounded computations.

## Concrete counterexample to floor substitution

The first nonintegral division in the checked recurrence occurs at d=5:
k_5=1021684 and n_5=9080109248508232805010. Replacing the ceiling by floor gives
n_5-1; the dimension inequality then fails by exactly 204337. At n_5 it has slack
817348. This refutes a weakened arithmetic test, not unirationality of any
hypersurface at that smaller dimension. The published ceiling is correct.

## Seed bound and rational dyadic certificate

Let s=1021684 and A_d=(d-1)(d-1)!/24 for integer d>=5. The published binomial
estimate yields k_d<k_(d-1)^(d-1) for d>=6. Thus ordinary induction gives
k_d<=s^((d-1)!/24). For k>=6,d>=5, C(k+d,d)<k^d/4 and
k+ceil(C(k+d,d)/(k+1)) <= k+k^(d-1)/4+1 <= k^(d-1).
Consequently n_d<=s^A_d. This is a conditional arithmetic corollary of the
stated recurrence estimate, without a fresh proof of the geometry.

An exact integer comparison proves 2^638 < s^32 < 2^639. Therefore
n_d <= 2^ceil(639*A_d/32), using only integer exponents and no floating logarithms.
The coefficient 639 is minimal on the denominator-32 grid for bounding log2(s).
This improves the imported coarse exponent 20*A_d, but not the published exact
recursive threshold. At d=7 the rounded exponent is 3595 instead of 3600, a
factor-32 reduction in this particular coarse sufficient bound. It remains far
above the exact recursive threshold. No novelty or best-known-bound claim is made.

## Finite evidence and limits

Both algorithms compute seven exact recurrence rows (d=2..8), 1111 inequality
boundary cases (d=2..12,k=0..100), and sixteen symbolic exponent comparisons
(d=5..20). Floor substitution fails in 351 of the boundary cases. Exact powers
confirm n_d<=s^A_d<=2^ceil(639*A_d/32) for d=5..8 only; larger comparisons store
exponents without materializing the huge powers. Universal induction needs
independently authored or kernel review. Arithmetic below the sufficient
threshold does not establish a negative geometric result.
