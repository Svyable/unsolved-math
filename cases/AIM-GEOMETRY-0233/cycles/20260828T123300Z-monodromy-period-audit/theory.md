# Local monodromy period, not total cover degree

## Scope and changed evidence

The previous packet improved a conditional cover-count denominator to 3,996.
It did not construct a uniform simple-lift degree. This packet does not recount
those covers or enlarge that census. It isolates a different, falsifiable step:
does connectedness make the period of one generator equal the total degree?
An exact three-sheet counterexample answers no. The corrected endpoint rule
uses a local orbit, with a certificate that can be retained by future work.

The canonical statement is still a transition fragment, not the neighboring
question. No geometric continuation, source-scope expansion or parent solution
is claimed. The prior concentration lemma remains conditional and unchanged.

## Definitions, quantifiers and assumptions

For every integer d>=1, let A,B be permutations of X={0,...,d-1} whose generated
action is transitive. For every x in X and integer n>=0, read the walk B^n A:
first n B-edges, then one A-edge. This is a cyclic rotation of the word ab^n,
with x immediately after the a-edge. It is closed iff A(B^n(x))=x.
Let m=min{j>=1:B^j(x)=x}. The local period m satisfies 1<=m<=d.
It need not be the order of B, either: the latter is the least common multiple
of all cycle lengths, whereas this calculation concerns only x's cycle.

The winding count here means the number of complete traversals of that
directed B-cycle during n steps. It is purely combinatorial. A graph-simple
certificate consists of n+1 distinct vertices followed by a closing A-edge.
No converse from surface simplicity to graph simplicity is assumed.

## Approaches

1. Replace m by d, on the grounds that the cover/action is connected. This
   shortcut is **FALSIFIED**; transitivity of <A,B> does not say B is transitive.
2. Decompose B into cycles and retain x's cycle. This gives an exact endpoint
   and quotient/remainder description without a single-cycle assumption.
3. Independently reconstruct paths by literal traversal and connectivity by
   union-find, before opening the generated certificate.

## Typed claims and proof steps

**P1 — DERIVED, FALSIFIED.** Transitivity and closure suffice to replace m by d
in B^n(x)=B^(n mod d)(x) and the winding formula floor(n/d).
Take A=[2,0,1], B=[1,0,2], x=0, n=5. A alone is a three-cycle, so the joint
action is transitive. The B-path is 0,1,0,1,0,1; A(1)=0 closes it. Thus m=2,
endpoint=1, winding=2, remainder=1. The degree substitutions give endpoint
B^2(0)=0 and winding=1. Falsifier: this certificate fails a permutation,
connectivity, closure or arithmetic check. It is not a simple surface lift.

**P2 — DERIVED, UNVERIFIED universal proof; experimentally supported instances.**
Write n=qm+r with 0<=r<m. Successive applications of B list distinct vertices
until the first return: otherwise invertibility would yield an earlier return
to x. They then repeat with period m. Therefore B^n(x)=B^r(x), and exactly q
positive-time returns to x occur by time n. Closure is equivalent to A(B^r(x))=x.
This proof does not require joint transitivity; that hypothesis is needed only
when interpreting the entire action as a connected cover. Falsifier: a missed
noninvertible assumption, incorrect time convention, or contrary permutation.

**P3 — DERIVED, UNVERIFIED universal proof; certified finite examples.**
For each n>=0, d=n+1 and A=B=(0 1 ... n) give a connected graph cover with
the indicated walk a graph-simple circle. Distinct labels denote distinct
edges even when their permutations coincide. Conversely n+1 distinct vertices
require d>=n+1. This is a graph criterion only. Seventeen certificates check
n=0,...,16. Falsifier: nonbijection, failed closure, repeated preclosure vertex,
or unnoticed identification of differently labelled edges.

**S1 — PRIMARY_SOURCE, PRIMARY_SOURCE_SUPPORTED.** Gaster v1, Proposition 6,
states a growing simple-lift lower bound for its specified pair-of-pants family.
See the source ledger; its topology is not independently proved here.

## Quantifier dependency and exact remaining gap

Let delta(gamma) be minimum simple-lift degree. The prior finite-pigeonhole
argument requires one D with delta(gamma)<=D throughout the selected family.
Pointwise finiteness, forall gamma exists D_gamma, does not supply that D.
Even infinitely many finite values can increase without bound (delta_n=n+1).
An infinite subfamily is uniformly bounded precisely when for some integer D
infinitely many members lie in {gamma:delta(gamma)<=D}; this is not entailed by
pointwise finiteness. Neither unboundedness on all curves nor on a particular
sequence rules out a different infinite bounded-degree subfamily.

The source-backed family makes the quantifier objection relevant, but the
packet's executable certificate does not verify a surface lower bound. In
particular repeated graph vertices alone cannot certify surface intersection.
Likewise the counterexample tests the blanket algebraic substitution, not the
additional simplicity hypothesis inside a contradiction proof. It establishes
no error in the published theorem. A future proof using local periods still
needs the ribbon-neighborhood and geometric-minimality steps checked.

## Results and limits

15,017 permutation pairs contain 11,520 transitive actions. Across 742,417
rooted exponent cases, 115,089 walks close; 75,582 have m<d. The degree-based
endpoint and winding shortcuts fail on 41,244 and 44,604 closed walks,
respectively. All 65 aggregate rows and 17 constructive certificates agree with
the fresh verifier. These counts discriminate the two methods, not asymptotic
or geometric claims. Same-assistant authorship; no independent human/model or
kernel proof review. No novelty or new universal simple-lifting result claimed.
