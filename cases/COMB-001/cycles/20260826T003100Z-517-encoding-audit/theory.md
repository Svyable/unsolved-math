# Theory lane: exact encoding and symmetry lemma

## Frozen target

For the pinned CNP-SAT files `edge/517.edge` and
`cnf/517-4-sbp.cnf` at commit
`bb414955a6ef5f49f7df2b245b1e778aa67c068a`, determine whether the CNF is
exactly an exact-one four-coloring encoding of the graph, with only explicit
color-symmetry locks, and isolate the justification for those locks.

This target is strictly smaller than checking the unit-distance embedding or
checking that the CNF is unsatisfiable.

## Definitions and quantifiers

- (G=(V,E)) is the undirected graph parsed from the pinned edge file, with
  (V={1,ldots,517}).
- For every (vin V) and (cin{1,2,3,4}), variable
  (x_{v,c}=4(v-1)+c) means “vertex (v) receives color (c).”
- Exact-one coloring requires, for every vertex, at least one color and all six
  pairwise at-most-one clauses.
- Proper coloring requires, for every ({u,v}in E) and every color (c),
  the clause (lnot x_{u,c}lorlnot x_{v,c}).
- The observed symmetry locks are (x_{1,1}), (x_{2,2}), and (x_{6,3}).
- “Equivalent” below means equisatisfiable under a global permutation of the
  four color names; it does not assert that the two formulas have identical
  model sets.

## Assumptions

1. The two fetched byte streams are the files identified by their recorded
   SHA-256 hashes.
2. DIMACS variable numbering follows (x_{v,c}=4(v-1)+c).
3. Color names carry no semantic distinction, so a global permutation preserves
   proper coloring.
4. No geometric claim or unsatisfiability claim is assumed.

## Approaches considered

1. **Exact clause-set accounting.** Generate the canonical encoding directly
   from the edge set and compare clauses as mathematical sets. This approach is
   decisive for encoding fidelity and was executed in this cycle.
2. **Proof/core analysis.** Check the supplied SAT proof, extract a verified
   unsatisfiable core, and map core clauses back to graph constraints. This
   could expose a shorter forcing chain, but it cannot begin honestly until the
   proof artifact and checker path are pinned and reproduced.

## Typed claims and falsifiers

| Claim | Origin | Status | Statement | Falsification condition |
|---|---|---|---|---|
| C1 | Derived from pinned bytes | Experimentally supported | The graph parses as a simple graph on 517 vertices with 2,579 distinct edges. | A malformed row, loop, duplicate, out-of-range endpoint, count mismatch, or input-hash mismatch. |
| C2 | Derived from C1 and pinned CNF | Experimentally supported | The 13,935 CNF clauses are exactly 517 vertex presence/lock clauses, 3,102 pairwise at-most-one clauses, and 10,316 edge/color exclusion clauses, with no remainder. | Any missing or unexpected clause, duplicate clause, tautology, out-of-range literal, or header mismatch. |
| C3 | Derived from C1 and elementary color symmetry | Experimentally supported | Fixing vertices 1, 2, and 6 to colors 1, 2, and 3 is satisfiability-preserving because those vertices form a triangle. | Any one of edges {1,2}, {1,6}, {2,6} is absent, or color names are constrained by additional non-permutation-invariant semantics. |

## Progress unit: equivalent formulation

The exact accounting is:

[
517 + 517inom{4}{2} + 4(2579)
= 517 + 3102 + 10316
= 13935.
]

The three locked vertices replace their ordinary four-literal at-least-one
clauses with one positive unit clause each; every other expected clause remains
present. Vertices 1, 2, and 6 induce (K_3). In any proper four-coloring their
three colors are distinct. Therefore a permutation of the four color labels can
map those colors to 1, 2, and 3 while preserving all edge inequalities.
Consequently, the locked formula is satisfiable exactly when the ordinary
four-coloring encoding is satisfiable, up to this color-name normalization.

This is a concrete equivalent reformulation of the finite certificate input. It
does not establish whether either formula is satisfiable.

## Next theoretical obligation

Pin the proof artifact and checker, verify unsatisfiability independently, then
extract a checked core or forcing implication that is not merely global
color-name symmetry. Separately pin coordinates and verify every claimed unit
distance with exact arithmetic.
