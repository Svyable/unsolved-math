# Counterexample-first verification

## Independence and order

The verifier was authored and baseline-executed before theory.py was written.
It starts with the free half-turn, trivial action, and nonfaithful rotation,
then computes the complete bounded census before opening theory-output.json.
Each run uses a fresh Python -I child, empty environment and resource limits.
The verifier imports neither theory.py nor a previous cycle implementation.
Its method family is integral chain-matrix homology; theory uses a lifted
rotation presentation and gcd formula. Distinct baseline/verification files
contain the actual evidence. Same-assistant authorship and a shared mathematical
model, input, serialization and Python runtime limit independence. This is
neither independent human/model review nor kernel verification.

## Boundary search before confirmation

The first three computations give respectively H1=Z, Z direct-sum C2, and
Z direct-sum C2 for (m,k,L)=(2,1,2),(2,0,2),(4,2,1). Thus both a genuine
fixed-point control and a nonfaithful-action control are present. The free
half-turn fails the proposed Z direct-sum C2 prediction despite trivial
homology action. The trivial action also refutes identifying every homotopy
quotient with its coarse circle quotient. N=2 is a two-edge CW circle;
negative k is represented modulo m, and k=0 is not discarded.

## Computation and integral proof-step audit

For N=mL, C0 has N generators. C1 has N circle edges plus (m-1)N bar edges
[g,v] going from v to v+gkL. C2 has m(m-1)N generators. Its columns are
e_(v+gkL)-e_v-[g,v+1]+[g,v] and
[h,v+gkL]-[g+h mod m,v]+[g,v], with [0,v] omitted. Direct incidence arithmetic
checks d1*d2=0 on all11004 census columns. These formulas are the normalized
bar/cellular total differential with the minus sign on the mixed term.

The first N-1 circle edges form a spanning tree. On integral cycles, deleting
their coordinates is an integral isomorphism to the remaining chord lattice:
each chord closes uniquely along the tree, with integral coefficients. This
explains why merely deleting rows of the relation matrix is justified here;
it would not hold for an arbitrary collection of edges. Connectivity gives
rank(d1)=N-1. Higher total degrees cannot alter H1=ker(d1)/im(d2).

The Smith routine uses only unit pivots and integral elementary elimination.
Each pivot splits off one invariant factor1. It then explicitly checks that
all two-by-two minors of the residual matrix vanish. For a nonzero rank-one
integer matrix the only nonzero invariant factor is the gcd of its entries;
the all-zero case is handled separately. It does not silently assume the
residual rank is one. This restriction is enough for every recorded case,
not a claim to implement general Smith normal form.

All60 ordered homology profiles agree with theory, with profile digest
f3c99cd73318c0680f558fd9f383f52fe60b9a3bc30beb52404afbcf0b73cecc.
There are45 failures of the weakened splitting formula. The six supplied
covectors are checked for length, primitivity, all460 relation pairings,
agreement with independently computed torsion/free rank, and the claimed
positive fiber coordinate. A primitive homomorphism from a rank-one-free
abelian group to Z induces its free quotient up to sign; torsion maps to zero.
Consequently the half-turn fiber coordinate2 has its asserted meaning.
The certificate's two-generator `relation` field is explanatory metadata,
not an independently checked presentation isomorphism. The verifier checks
the actual bar-relation matrix and homology profile instead.

Six corruptions are rejected: zero covector, a changed coefficient, wrong
torsion, wrong fiber coordinate, missing profile, and missing certificate.
Both theory and verifier replay byte-identically. Five mathematical children
were used: baseline, theory, verification, and two replay children. There were
no failed mathematical children. Tests are discriminating but do not prove
the validator secure against every possible malformed input.

## Claim, citation and universal-proof checks

The finite matrix claims have direct evidence. The proposed all-m,k,L formula
has a plausible lifting/abelianization argument, including stabilizers, but
remains UNVERIFIED at the universal-proof level. Splitting is stronger than
trivial monodromy. The fixed-point product control supports, rather than
refutes, the original hypothesis. The spectral-sequence approach must retain
the abutment extension; no E-infinity direct-sum assertion is used.

The primary-source audit is in sources/verification-source.md. Brown's
ordinary Borel chain model supports the setting; the exact bar-sign convention
is derived and checked here, not quoted as a theorem from that source. AIM's
visually recovered Question9 does not establish the dataset's finite-group
specialization or current status. The frozen damaged statement is not edited.

Remaining objections: ordinary topology only; no Nisnevich sheaf, A1-local
chain comparison, strong-convergence result in that category, or parent
solution. Universal presentation and model-identification arguments need
independently authored proof review. Agent assistance is disclosed throughout.
