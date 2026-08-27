# Theory: a regular cyclic factor needs every orbit, not merely global order

## Frozen target and definitions

The canonical statement is preserved byte-for-byte in `snapshot.json` with
dataset provenance. Its imported summary is an unverified lead, not a proof.
The bounded target here is its regular cyclic-factor criterion and the meaning
of weighting a divisibility profile. No ASM, rowmotion, PL, or birational map is
constructed or analysed.

Let X be finite, T:X→X a bijection, and N a positive integer. Write C_N for
Z/NZ with action R(y)=y+1. An equivariant map satisfies
f(Tx)=f(x)+1 modulo N for every x. A **factor** additionally means surjective.
Let the T-orbits have lengths l_1,...,l_c. For nonempty X define

- S_N = sum of l_i for N dividing l_i, divided by |X| (uniform state sampling);
- O_N = number of such orbits divided by c (uniform orbit sampling).

The empty set is allowed in computation, but S_N and O_N are undefined there.
No primitivity, faithful source action, or injectivity of f is assumed.

## Two approaches

1. Decompose T into cycles, impose the closing congruence on each cycle, and
   choose a free initial phase for each consistent cycle. This gives a count
   and a constructive representative (`theory.py`).
2. Treat each equation as a modular difference constraint on an edge-labelled
   graph. Propagate colors and detect inconsistent closed walks, then compare
   against enumeration of all label assignments (`verify.py`). This algorithm
   was authored/run before the theory implementation and reads no theory data.

Global permutation order alone is a tempting but insufficient shortcut.
Counting only many states with compatible periods is also insufficient to
certify a factor on all of X.

## Counting derivation (ordinary mathematics, not kernel accepted)

For any source orbit and any starting point x, repeated equivariance gives
f(T^j x)=f(x)+j modulo N for every nonnegative j. At j=l_i, closure forces
N|l_i. If any cycle fails this test, there are zero equivariant maps.

Conversely, if every l_i is divisible by N, choose an initial color a_i in
C_N independently on each cycle and set f(T^j x_i)=a_i+j modulo N. Closure
makes the definition well-defined. Every equivariant map arises uniquely in
this way, so the exact count is N^c. If X is nonempty, any one cycle traverses
all N colors, hence all these maps are surjective. If X is empty, there is
exactly one equivariant empty map and zero surjective factors: the nonempty
assumption cannot be omitted from the factor-existence statement.

## Concrete falsification

The constructed shortcut “N divides the order of T, therefore a regular
C_N factor exists” fails for T=(0 1)(2), N=2. The order is 2, but the fixed
point requires f(2)=f(2)+1 modulo 2. The verifier exhausts all eight color
assignments and finds none. This shortcut is ours to test; it is not attributed
to the AIM authors or imported summary.

## Weighting cannot replace the universal condition

For each integer k≥1, take one cycle of length 2k² and k fixed points, with
N=2. Then S_2=2k/(2k+1) tends to one and O_2=1/(k+1) tends to zero. No member
has a regular C_2 factor because of the fixed points. At k=20, the same 820
states yield S_2=40/41 and O_2=1/21. Thus even arbitrarily high state-weighted
compatible mass gives neither high orbit-weighted mass nor an exact factor.
This is a family of finite counterexamples to those shortcuts, not evidence
that the AIM combinatorial systems exhibit these profiles.

## Changed evidentiary state

Previously the repository had no packet for this ranked candidate. It now has
a falsified global-order shortcut, an explicit weighting-separation family,
and a reproducible exact count audit: 47,312 permutation/modulus systems for
|X|=0,...,7 and N=1,...,8. There are 7,180 systems with a surjective factor;
the eight empty-domain systems instead each have one nonsurjective map.
The order shortcut has 10,919 false positives on this finite domain.
These counts are bounded experiments, not proofs by extrapolation. The
unbounded counting/family statements rely on the displayed derivations.

## Source boundary and objections

The May 29, 2015 AIM workshop list, printed page 5, places the frozen opening
after Problem 2.4 and before the resonance discussion; the actual resonance
question is Problem 2.5. Its page 6 gives a cyclic-factor motivation using link
patterns. The imported fragment is not a standalone question and needs human
scope review. See `sources.json`; no canonical record or status is repaired here.

The criterion is elementary/known in character; no novelty is claimed. Both
implementations have the same assistant author. Neither a formal kernel nor
an independent human/model has reviewed the general derivation. No natural
factor, actual ASM orbit inventory, or resonance theorem follows from this audit.
