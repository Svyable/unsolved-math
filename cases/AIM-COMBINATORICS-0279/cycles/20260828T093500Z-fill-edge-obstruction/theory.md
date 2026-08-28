# Fill edges distinguish peeling from treewidth

## Scope and evidence delta

The frozen canonical statement is the incomplete extraction "Conjecture 2. Let G be an even-hole-free graph." It is not silently completed here. The prior cycle proved a conditional list-coloring corollary using the external bisimplicial-vertex theorem and audited small graphs. Its peeling orders omit fill edges, as is correct for degeneracy and reverse-greedy list coloring.

This follow-up tests a proposed alternative: could triangle-free even-hole-free graphs be treated as partial 2-trees, replacing the structural dependency with width-two elimination? This shortcut is introduced here, not attributed to the prior packet or any author. The new evidence is a 10-vertex obstruction, a precise fill-edge failure, and independently checked K4-minor and width-three decomposition certificates. This is a changed method and target, not a larger coloring census or new mathematics.

## Definitions and quantifiers

All graphs are finite, simple and undirected. A hole is an induced cycle of length at least four; C4 is excluded in even-hole-free graphs. Degeneracy is the minimum, over vertex orders, of the maximum remaining degree under vertex deletion without fill.

A tree decomposition assigns bags of vertices to nodes of a tree: every vertex appears, every edge is covered by a bag, and the bags containing any fixed vertex induce a connected subtree. Width is the largest bag size minus one. Treewidth is minimum width. Filled elimination deletes a vertex after making its remaining neighbors a clique. Its minimum maximum degree equals treewidth; unlike peeling, fill is essential.

A K4 minor certificate consists of four nonempty, pairwise-disjoint connected vertex sets with an edge between every pair. Treewidth is minor-monotone and K4 has treewidth three. These standard equivalences are ordinary mathematical dependencies, not kernel-accepted results in this packet.

For k>=3 and sector lengths l_i>=2, W(l_0,...,l_{k-1}) has a rim of r=sum(l_i) vertices labelled 0,...,r-1 and a hub r adjacent to a_i=sum_{j<i} l_j. Only the rim is subdivided. The finite domain is k in {3,4,5}, l_i in {2,3,4,5}: 1,344 ordered parameter instances, not isomorphism classes. The universal implication under test quantifies over all triangle-free even-hole-free graphs: degeneracy two would supposedly justify treewidth at most two.

## Approaches considered

1. Carry the low-degree peeling order into a width-two dynamic program without adding fill. Retired: the explicit witness acquires a remaining degree-three vertex after two eliminations.
2. Keep the invariants separate and provide independent upper/lower certificates: a width-three path decomposition and a K4 minor, plus a no-fill peeling order.
3. Use exact filled-elimination dynamic programming on the witness rather than accepting the minor argument alone. This is the verification approach, not the theory's proof of its lower bound.

## Exact witness and typed claims

CERTIFICATES [DERIVED; EXPERIMENTALLY_SUPPORTED]. Use W(3,3,3): the rim is C9 and hub 9 is joined to 0,3,6. Its twelve edges and four induced cycles are stored. The cycle lengths are 5,5,5,9, so it is triangle-free and even-hole-free. A no-fill peeling order is
1,2,0,8,7,3,4,5,6,9,
of maximum remaining degree two. A cycle supplies the matching degeneracy lower bound.

K4 branch sets are {9}, {0,1,2}, {3,4,5}, {6,7,8}. All are connected and mutually adjacent as branch sets. For i=1,...,7, use bag {9,0,i,i+1}, linked in path order. Each edge is covered and the running-intersection condition holds. Thus the standard minor lower bound and decomposition upper bound give treewidth exactly three.

Falsifiers: an even induced cycle, triangle, invalid peeling order, disconnected/overlapping branch sets, missing inter-branch edge, uncovered graph edge, disconnected bag occurrence set, or exact elimination optimum other than three.

SHORTCUT [DERIVED; FALSIFIED]. The proposed implication "triangle-free and even-hole-free plus degree-two peeling implies treewidth at most two" fails on this witness. The first elimination adds edge 0--2; the second adds 0--3. Vertex 0 then has neighbors 3,8,9. The stored fill trace locates the error: a degree-two bound from the original induced graph does not control the filled graph. This does not refute the prior reverse-greedy list-coloring proof.

FAMILY [DERIVED; UNVERIFIED by independent author/kernel]. The following ordinary argument explains the experiment for arbitrary k>=3 and l_i>=2. A cycle without the hub must be the whole rim. An induced cycle through the hub must use two consecutive spoke vertices along its rim path: any intermediate spoke would be a chord. Consequently the holes are exactly the rim and the k sector cycles, with lengths r and l_i+2. Hence even-hole-freeness is equivalent to all l_i odd and k odd. Triangle-freeness follows from l_i>=2.

The same four branch sets can use the hub and three contiguous rim arcs cut at the first three spoke vertices, so every member has a K4 minor. Bags {hub,0,i,i+1} give width three for every member. No-fill peeling has width two: delete internal sector vertices to break rim paths, then peel what remains; the rim gives a lower bound of two. These statements have elementary proofs but no independent author/kernel review. They are not inferred from the finite table.

EXPERIMENT [DERIVED; EXPERIMENTALLY_SUPPORTED]. The finite domain contains exactly 40 triangle-free even-hole-free instances: 8 with three spokes and 32 with five; none with four. All 40 have explicit minor, bag-tree and peeling certificates. Their smallest member has 10 vertices; no claim of global vertex minimality is made. Falsified by any domain omission or mismatch in the table, certificates or predicates.

SOURCE [PRIMARY_SOURCE; PRIMARY_SOURCE_SUPPORTED]. Primary texts distinguish the earlier bisimplicial theorem from treewidth and give a stronger pre-existing treewidth context; see sources/source-audit.md. No new best bound, theorem, or solved parent is claimed.

## Limits and reproduction

The long bisimplicial-vertex proof remains unaudited; the incomplete parent statement still needs human scope review. The correct family-specific width-three construction is not a width-three theorem for the entire triangle-free even-hole-free class.

From this directory run: python experiments/run.py baseline; python experiments/run.py theory; python experiments/run.py verify; python experiments/run.py replay. The table is canonical compact JSON; its SHA-256 matches both implementations. Re-running execution modes may rewrite manifest-covered execution logs; reseal only after validation.
