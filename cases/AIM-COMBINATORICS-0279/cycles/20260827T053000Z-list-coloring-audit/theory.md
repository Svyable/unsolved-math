# A bounded list-coloring audit

Agent output is unverified research assistance, not a mathematical result.

## Frozen input and scope

`snapshot.json` retains the exact fragment and its SHA-256. `selection.json`
records actual rank 2 and the validated queue/history on open PR #8. The imported
`open` and `exact` labels are unchanged, not endorsed. The fragment does not state
a complete conjecture. This packet tests the associated corollary as a DERIVED
target, not an invented completion or replacement canonical statement.

Target: determine the precise hypothesis/dependency boundary of the assertion
that finite triangle-free even-hole-free graphs have equal ordinary and list
chromatic numbers, with values 0, 1, 2, 3 in the null, non-null edgeless, forest
with an edge, and cyclic cases respectively. No novelty is claimed.

## Definitions and quantifiers

All graphs here are finite, simple, undirected. A hole is an induced cycle of
length at least four; an even hole has even length, including four. Triangle-free
means no 3-cycle. A graph is d-degenerate if every nonempty induced subgraph has
a vertex of degree at most d. The empty graph has degeneracy zero by convention.

A list assignment gives each vertex a finite set of allowed color labels. An
L-coloring is a proper vertex coloring using its assigned lists. The choice number
ch(G) is the least k such that EVERY assignment of lists of size at least k is
colorable, over arbitrary finite color palettes. Ordinary chromatic number is
chi(G). Both invariants are set to zero on the null graph in this packet.

The finite executable claim quantifies over all 33,868 labelled graphs on 0..6
vertices, then filters by both forbidden-induced-subgraph conditions. The
unbounded corollary additionally relies on the external bisimplicial-vertex theorem;
enumeration does not prove that theorem or the unbounded assertion.

## Two approaches and an explicitly retired shortcut

1. Hereditary structure: apply the external bisimplicial-vertex result to every
   induced subgraph; derive a peeling order and color arbitrary lists in reverse.
2. Direct finite audit: enumerate all labelled graphs, recognize induced even
   holes, store peeling certificates, and compare against independent exhaustive
   coloring and all-induced-subgraph degree tests.

The shortcut 'bipartite and 2-degenerate implies 2-choosable' is false. The exact
K2,4 list assignment below retires it. A proper 2-coloring alone is never a proof
that every 2-list assignment works.

## Conditional proof steps (not kernel accepted)

External dependency D: every non-null even-hole-free graph has a bisimplicial
vertex, meaning its neighborhood is covered by two cliques. See `sources.json`
for the replacement paper and the documented problem in the older proof.

1. Every induced subgraph preserves triangle-freeness and even-hole-freeness.
   In a triangle-free graph a neighborhood is independent. Each of its two
   covering cliques therefore has size at most one. Dependency D gives degree
   at most two in every nonempty induced subgraph, hence 2-degeneracy.
2. Remove a vertex of degree at most two repeatedly. In reverse order at most
   two already colored neighbors forbid colors, so every list of size at least
   three retains a color. This proves the conditional bound ch(G)<=3.
3. A nonempty edgeless graph is 1-choosable. A forest is 1-degenerate and thus
   2-choosable by the same argument; an edge requires two ordinary colors.
4. If G has a cycle, a shortest cycle has no chord. It has length at least five
   by the two exclusions and has odd length. Thus chi(G)>=3. The general inequality
   chi(G)<=ch(G) follows by taking identical lists. This supplies the cyclic lower
   bound and the stated conditional classification, including disconnected graphs.

The theorem dependency remains a primary-source-supported external premise;
neither its long proof nor these proof steps were kernel checked here.

## Exact assumption counterexample

Let K2,4 have left vertices a,b and right vertices x00,x01,x10,x11. Give a the
list {0,1}, b the list {2,3}, and xij the list {i,j+2}. Each of the four choices
of colors on a,b blocks both colors at its matching right vertex. There is no
list coloring. Nevertheless the graph is bipartite, 2-degenerate, and ordinarily
2-colorable. It has an induced C4, so it does not contradict the audited corollary.
The input lists and edges, four-pair obstruction certificate, and all 64 failed
assignments are replayable from `input.json` and `theory_check.py`.

Removing the triangle-free hypothesis invalidates the degeneracy bound, witnessed
by K4; removing even-hole-freeness does so for K3,3. C5 shows that the upper bound
three is needed even inside the intended class. These are calibration witnesses,
not new constructions or claims about unsolved conjectures.

## Evidentiary delta

The prior imported summary is now paired with exact executable certificates and
a checked dependency map rather than trusted as a theorem. The theory recognizes
holes by connected induced 2-regular subsets and computes minimum-degree peeling.
It accepts 3,716 graphs, stores one order per graph in `peeling-certificates.jsonl`,
and finds no degree-bound violation. All nonempty cyclic accepted graphs in the
enumerated domain receive the predicted value three. The independent lane checks
ordinary chromatic numbers without using this prediction.

Typed claims, statuses and falsifiers are in `cycle.json`. Human scope review is
required for the incomplete canonical fragment. No imported status is changed,
and no parent-problem solution or novelty claim is made.
