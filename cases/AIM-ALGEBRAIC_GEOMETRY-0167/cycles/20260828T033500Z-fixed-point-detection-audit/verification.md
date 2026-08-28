# Verification lane

## Independence and order

verify.py was authored and run before theory.py existed. Its fresh Python -I baseline first constructed the C2 counterexample and the nonnormal S3 product boundary, then reconstructed the census. Every verifying run rebuilds its expected data before opening the theory certificate. The verifier uses permutation actions, explicit coset fixed-point counts, subgroup closure, and coset partitions. Theory uses cyclic divisor formulas, conjugation normality, subgroup products, and the cyclic mark formula. For S3/D8, the verifier enumerates all subsets containing identity for closure; theory generates subgroups by adjoining generators. Shared group labels and the input specification are intentional.

Isolation is fresh process, empty environment and bounded resources, **not** a network namespace or independent author. Both programs and both prose lanes have same-assistant authorship and shared mathematical context. No independent human/model or proof-kernel review occurred. Fresh computational reconstruction is the concrete independence basis; the prose proof audit is not claimed to have fresh-model independence.

## Counterexamples and boundaries first

Direct action enumeration gives the point-orbit marks (1,1) and free-orbit marks (2,0), hence 3 times the former minus the latter gives (1,3). This defeats the underlying-only test. The cofiber interpretation is an ordinary application of the source's sphere-map degree correspondence and exact geometric fixed points, not a stable-homotopy computation by this script.

Two S3 transpositions yield a product of size 4 whose closure has size 6: normality cannot be silently omitted from the product-subgroup argument. The full census also retains K=e cases, so nontriviality is not imposed retroactively on every test. A free C2 orbit with U=e demonstrates why nontrivial finite N alone cannot force the conclusion. Trivial and signed-unit degree tables are boundary specifications, not seven additional independently computed spectrum controls.

## Computation and certificate checks

The baseline and theory tables are byte-identical. Separate algorithms agree on all 2,273 transport rows, the complete subgroup inventories of 25 groups, five mark matrices and all 1,425 coefficient vectors. There are 1,322 nontrivial-kernel rows, 381 cases requiring thickening to force intersection, and 57 underlying-degree false positives.

The verifier rejects seven altered packets: a changed C2 degree, invalid quotient image, omitted thickening, incorrect mark-matrix entry, changed coefficient-vector degree, missing transport row, and deleted normal-subgroup inventory. This is exact equality against independently rebuilt data, not a general-purpose proof certificate kernel. Full deterministic replay preserved both output hashes. Eight bounded mathematical child processes were used: five initial runs, then a new baseline and two replay children after lint-only edits. All mathematical runs passed. The first Ruff check found two ambiguous variable names and an unbound loop-variable warning in an immediately invoked helper; renaming and explicit binding resolved them without changing any output. Initial source bytes and execution logs are retained under initial-* names, including the original pre-theory baseline. The later baseline is a reproducibility check, not another fresh-authorship claim.

## Proof-step audit and objections

1. Finite-quotient presentation is a categorical premise, not inferred from finite group experiments. Compact descent is a published dependency.
2. K=N intersect U is closed normal. For arbitrary closed L, LK is a subgroup because K is normal and is closed because it is the continuous image of compact L x K. Compactness of the profinite group is essential to this argument.
3. q(LK)=q(L), and K is contained in LK intersect N. The former transports geometric fixed points; the latter activates the N-free vanishing condition. Neither says L itself meets N.
4. Vanishing for all L is established before invoking compact joint detection. No inference from underlying vanishing alone is used. The C2 example shows why this order matters.
5. If N is infinite, injection into finite G/U is impossible, giving K nontrivial. Conversely a nonzero N-free compact X would force N intersect U=e at its descent level and thus N finite. This is a source-dependent ordinary argument, not a computational or kernel theorem.
6. The marked cofiber is compact and genuinely nonzero, but is not N-free for N=C2; it refutes only the shortcut. It does not refute the imported compact obstruction.

Citation checks are in sources/verification-source.md. AIM retrieval was unavailable. The imported Wirthmuller classification and actual Adams equivalence are untouched. Remaining substantive objections: independent proof review, the exact N-free model translation, and construction/compatibility of duality maps. No blanket integral noncompact conservativity is assumed.

Packaging note: an initial cycle assembly was rejected because the schema permits only independent_context=true for formal check entries. The same-context prose proof and citation audits were therefore left in these notes, not relabeled independent. Only the fresh-process computational checks count toward the two-lane progress contract; source review is not counted as a separately independently verified progress unit. No schema rule was weakened.
