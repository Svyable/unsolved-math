# All-subgroup detection audit

This is a bounded audit of the compact N-free obstruction, not a Wirthmuller or Adams construction. The imported summary is unverified. In particular, it does not supply the false proof step tested below; the underlying-only shortcut is an approach considered in this cycle, not an error attributed to an upstream author.

## Definitions, quantifiers, and target

Let G be profinite, N closed normal, U open normal, K=N intersect U, and q:G -> G/U. Let X be compact in the continuous genuine category, with a specified presentation X=infl(Y) from a compact G/U-spectrum. Use the following necessary N-freeness condition: for **every closed** H<=G with H intersect N nontrivial, Phi^H(X)=0. All geometric fixed points here are absolute, non-equivariant outputs, not categorical fixed points.

Target: if K is nontrivial, this condition forces X=0. The sharper obstruction is nontrivial K at a given descent level, not infinitude of N as a separate assumption. An infinite N necessarily has nontrivial intersection with every such U: otherwise N injects into the finite group G/U.

## Approach A: underlying-only detection, retired

Taking H=K proves only Phi^e(X)=0, because q(K)=e. The attempted final inference from this to X=0 is false in genuine equivariant homotopy theory.

Exact certificate: in A(C2), take a=3[C2/C2]-[C2/e]. In the orbit basis with subgroup orders (1,2), its coefficient vector is (-1,3); the mark matrix is [[2,1],[0,1]]. Thus its degrees are (1,3). The stable sphere map represented by a has cofiber X with underlying cofiber of degree 1, hence zero, but C2-geometric fixed points are the nonzero mod-3 Moore spectrum. X is compact as a cofiber of compact spheres. This does **not** give an N-free counterexample to the target: for N=C2, the nonzero C2-fixed piece violates the freeness hypothesis. The arithmetic is executable; the stable interpretation depends on the source facts recorded separately.

The census covers 1,425 Burnside coefficient vectors for C2,C3,C4,C6,C8, with coefficients in {-1,0,1,2,3}. It finds 57 maps with underlying degree a unit but some other degree not a unit. These are degree-test false positives, not computations of arbitrary equivariant spectra.

## Approach B: all-subgroup transport

For an arbitrary closed L<=G, set H=LK. Normality of K makes H a subgroup; compactness of L and K makes H closed in the Hausdorff group G. Moreover q(H)=q(L), since K<=U, and H intersect N contains K. Therefore the N-freeness condition kills Phi^H(X). Inflation compatibility gives Phi^L(X) equivalent to Phi^H(X), so **every** Phi^L(X) vanishes. Compact joint detection, not underlying detection, supplies the final implication X=0.

This is an ordinary conditional proof. It is not independently authored or kernel-checked. The model-specific inputs—compact descent, inflation compatibility, compact joint detection, and the interpretation of N-free—must remain explicit. The current cycle checks the fixed-point vanishing formulation, not an alternative construction of N-free localization. No claim about noncompact objects follows.

Finite discriminating experiment: 2,273 (G,N,U,L) rows over C2 through C24, S3, and D8, including trivial K boundaries. N and U range over all normal subgroups; L over all subgroups. There are 1,322 rows with nontrivial K, and 381 where omitting thickening would leave L intersect N trivial. All certified H=LK are subgroups with the required quotient image and intersection. These rows test the mechanism; they do not establish its profinite quantifiers.

Boundary controls: for finite N and U=e, K=e, the free C2 orbit is nonzero and N-free. If K is not normal, two distinct order-two subgroups in S3 have a four-element product but generate six elements, so the unqualified product-subgroup argument fails. Normality is sufficient here, not claimed necessary in every individual case.

## Typed claims and falsifiers

- MARK (DERIVED / EXPERIMENTALLY_SUPPORTED): the exact mark certificate is (1,3), and the finite census has 57 false positives. Falsified by any incorrect orbit count or omitted coefficient vector.
- TRANSPORT (DERIVED / EXPERIMENTALLY_SUPPORTED): the complete specified finite transport census satisfies the identities and counts above. Falsified by any subgroup, image, intersection, or completeness mismatch.
- REPAIR (DERIVED / UNVERIFIED): the all-closed-subgroup argument proves the stated conditional obstruction, assuming the cited categorical inputs. Falsified by a failure of closedness, normality, inflation compatibility, descent, or compact detection.
- SOURCES (PRIMARY_SOURCE / PRIMARY_SOURCE_SUPPORTED): the named locators supply the exact dependency statements, not acceptance of the whole imported synthesis. Falsified by a wrong theorem, model, or quantifier.

Material delta: retire a concrete insufficient detection test, supply its exact counterexample, and expose an all-subgroup replacement with a narrower kernel-intersection hypothesis. No parent status changes, new theorem priority, or full solution claim.
