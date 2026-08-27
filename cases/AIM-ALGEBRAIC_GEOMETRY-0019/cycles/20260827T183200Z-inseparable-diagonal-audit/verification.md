# Fresh-execution, independent-method verification

## Independence and recovery

The earlier unsealed rank-11 workspace was absent after recovery. These
programs were newly authored from the frozen specification. The current
verifier and its baseline were executed before the current theory.py existed.
Verification starts with counterexamples and boundaries, then reconstructs
the entire core before reading the theory output. It uses quotient polynomial
multiplication and modular row reduction, not valuation formulas.

Both implementations and these notes have same-assistant authorship;
the author already knew the prior unsealed conclusions from conversation.
This is therefore not a blind or independently authored model/human review.
Independence is algorithmic and fresh-process only, with separate evidence files.
Both share Python integer arithmetic, the ring definitions and the specification.
No Lean or other proof kernel was used.

## Counterexamples and boundaries first

The first computed case is F2[e]/e^3 with f=g=e^2. The actual products vanish,
both multiplication matrices have rank one, and ker/image has dimension one.
This refutes composition-zero as an exactness certificate. Zero/zero has
homology dimension three; unit/zero is exact; e/e in F2[e]/e^2 is exact. These
checks precede exhaustive enumeration and any certificate access.

## Full finite computation

Every coefficient tuple is enumerated lexicographically. Products are reduced
in the quotient; actual multiplication ranks are cached per element. For every
zero product the dimension m-rank(f)-rank(g) is recorded. The complete complex
index sets, exact index sets and homology histograms agree with the valuation
implementation, across 67,780 pairs. There are 1,640 complexes, 1,157 exact
sequences and 483 complexes with nonzero positive homology.

For each of p=2,3,5,7 both nilpotent and separable controls are computed using
their respective quotient relations. The checker verifies products and
complementary ranks, calculates Hom differential ranks via augmentation, and
records degrees 0 through 12. All 104 entries match; these are finite entries,
not an all-degree computational proof. The separable idempotents are directly
squared and multiplied by z. Repeated multiplication of the bivariate z-u
polynomial checks the Frobenius coefficient arrays separately from the theory
program's binomial coefficients.

Seven deliberately changed certificate cores are rejected by comparison against
the fully recomputed core: erase bad-case homology, remove an exact pair, add
zero/zero as exact, erase nilpotent positive Ext, invent separable positive Ext,
break the idempotent, and insert a middle Frobenius coefficient. This is a
strict finite-core equality verifier, not a general proof-certificate parser
or a security audit. Positive and negative controls are both retained.

## Proof-step and citation audit

The irreducibility step needs an imperfect field: Fp(t), not Fp. The tensor
product is over k, not over L. The kernel/image ideal computation must be made
before applying Hom. Nonzero Ext in arbitrarily high degrees, not mere
periodicity, is the obstruction to finite projective dimension. Finally one
must restrict the diagonal pieces to exterior products of perfect modules;
arbitrary bimodules would make the claim vacuous. These dependency checks find
no gap in the displayed elementary argument, but same-author inspection is
not independent proof acceptance. OBSTRUCTION remains UNVERIFIED.

The separate source note checks the downloaded versioned PDF against the HTML
locators. In particular the height-layer inequality bounds Rouquier dimension;
substituting diagonal dimension into it is unsupported by that citation. The
imported stronger positive formula is not verified here. The AIM section was
unavailable and its intended hypotheses still need human review.

## Execution boundary

run.py launches python -I in a fresh process with an empty environment, CPU
limit 180 seconds, wall timeout 200 seconds, 512 MiB memory and a 16 MiB file
limit. Programs make no network calls; isolation is not a network namespace.
Logs retain interpreter version, command, input/source/output SHA-256, times,
exit status and stdout/stderr. Replay reproduced both output files byte for
byte. No mathematics from the lost workspace is accepted by reference.

Remaining objections: original statement scope and positive comparison formula;
independently authored or kernel verification of the infinite argument;
applicability beyond the specified inseparable example. No parent-problem or
novel-result claim is made, and imported statuses remain unchanged.
