# Fixed points are not trivial monodromy

## Frozen scope and definitions

This is a first cycle for rank20, not a continuation of another problem's
hidden-extension audit. The exact damaged imported statement and its hash remain
in snapshot.json. Visual reading of the original AIM Question9 recovers its
notation; it does not validate the dataset's narrower finite-group formulation
or its imported partially-solved status. Source notes separate these claims.

Work over ordinary integral homology only. For integers m>=2, 0<=k<m and L>=1,
let X be the oriented CW circle with N=mL vertices and N edges. The generator
of C_m translates every vertex and edge by kL modulo N. With N=2 there are
two distinct edges, not one edge of an abstract simplicial complex. Write
X_hC_m=(EC_m x X)/C_m, and distinguish it from the coarse orbit space X/C_m.
Every rotation acts trivially on H1(X;Z)=Z. A group-fixed point means a point
fixed by every element, which in this family occurs exactly when k=0.

Target: can trivial action on H1 replace a group-fixed basepoint in a claimed
H1 splitting into fiber coinvariants and C_m? No assertion about A1-localization,
Nisnevich sheaves, motivic convergence, or the parent problem follows here.

## Approach 1: lifted rotation and a two-generator presentation

Let t be a positive fiber circuit and b the negative rotation lift, with
projection to a generator of C_m (choice of its inverse is immaterial).
The proposed ordinary fundamental-group extension has commuting generators
t,b and relation k*t+m*b=0. One way to justify the relation is to lift rotation
by -k/m to the universal cover R: m lifts translate by -k. Retain the group
element as well as its translation when the action is nonfaithful; otherwise
this construction would incorrectly erase the stabilizer.

For d=gcd(m,k), an integral change of basis for the row (k,m) gives
H1(X_hC_m;Z)=Z direct-sum Z/d. Z/1 denotes zero. The map to the free quotient
can be chosen primitive with t mapping to m/d and b mapping to -k/d.
This universal topological argument is DERIVED, UNVERIFIED pending independent
proof review; the finite presentations and their chain realization are checked
below. A failed lifting interpretation, omitted stabilizer, or invalid integral
basis change falsifies the proposed universal argument.

For m=2,k=1,L=2 the verifier instead computes the full bar/cellular chain
complex and obtains H1=Z. The fiber class has primitive free coordinate2.
Thus the ordinary extension is 0 -> Z --times2--> Z -> C2 -> 0, not a split
extension. There is no element of order2 in the middle group that could be the
image of a section. The induced action on H1(X) is nevertheless the identity.
The shortcut is FALSIFIED; a wrong chain matrix, Smith reduction or fiber
coordinate would invalidate this finite witness. This is a known-model
calibration, not a novel topological theorem.

The control m=2,k=0 has actual fixed points and H1=Z direct-sum C2. Here the
Borel construction is the product X x BC2. In contrast X/C2 is still a circle.
So replacing homotopy quotient by coarse quotient without freeness also fails.
For k coprime to m the action is free; it is then legitimate to use the coarse
quotient. The nonfaithful control m=4,k=2 instead retains a C2 summand.

## Approach 2: keep the extension in the spectral sequence

The ordinary equivariant spectral sequence has degree-one graded pieces Z
and C_m for these rotations. Since H2(C_m;Z)=0, there is no incoming degree-two
transgression to the fiber H1 term. That only yields an extension; trivial
monodromy is not a section. The half-turn extension above discriminates the
two possibilities. A genuine fixed point gives a section of the Borel fibration
and removes this obstruction; for k=0 the direct product verifies it explicitly.
Retire the proposed replacement of a fixed point by trivial H1 action, and the
coarse-quotient substitution for nonfree actions. Do not retire the imported
statement that actually retains its fixed-basepoint hypothesis.

## Finite evidence and certificates

experiments/theory.py uses the two-generator gcd formula, not the bar matrices.
It predicts all60 profiles for m=2..6, k=0..m-1, L=1..3. Forty-five profiles
disagree with Z direct-sum C_m. Three subdivisions of each action are retained
as boundary/model controls, not60 distinct topological actions.

For the chord coordinates consisting of the last circle edge followed by
[g,v], the supplied free covector is m/d on the circle chord and
floor((v+g*kL)/N)*(m/d)-g*(k/d) on [g,v]. Six explicit covectors certify the
fiber's free coordinate. They are primitive and kill all460 relevant relation
columns. They do not by themselves certify absence of torsion: the separate
integral Smith calculation supplies that information.

Typed claims, dependencies, origins and falsifiers are in cycle.json. FINITE
and CERT are EXPERIMENTALLY_SUPPORTED, not universal proofs. Exact output and
source hashes are recorded in execution logs and the canonical manifest.

## Changed evidentiary state and next objection

Before this packet the imported splitting prerequisite had no local test.
Now the fixed-point weakening and nonfree coarse-quotient shortcut each have
an exact ordinary counterexample, with explicit chains, homology profiles,
fiber covectors and independent-method checks. The next substantive task is
an independently reviewed comparison with the intended A1-homology framework,
including its exact hypotheses. More subdivisions alone would not be progress.
