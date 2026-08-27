# Inseparable diagonal: exactness is not enough

This is a bounded audit of an imported obstruction, not a new solution. The
canonical statement and its status are unchanged in snapshot.json. The original
Q/zero notation and intended category hypotheses require human scope review.

## Definitions and scope

For a prime p and m>=2 let R=Fp[e]/(e^m). Coefficients are listed from constant
term upward. For f in R define v(f) as its lowest nonzero degree, with v(0)=m.
The alternating rank-one sequence has consecutive differentials multiplication
by f and g. It is a complex iff fg=0. At either positive position its homology
is ker(f)/im(g) or ker(g)/im(f). Exactness requires these quotients to vanish;
composition zero alone only ensures that the quotients are defined.

The finite scope is every ordered pair over p=2,3 and m=2,3,4,5. The second
scope is eight augmented algebras: Fp[z]/z^p and Fp[z]/(z^p-z) for p=2,3,5,7,
with augmentation z->0, and Ext degrees 0 through 12. No finite-field
inseparable extension is claimed. The coefficient computations transfer to L
below by scalar extension. In input.json the extra punctuation after Fp(t)
is a prose typo; the field meant here is exactly the rational function field.

## Approaches considered

1. Classify multiplication maps by valuation/principal ideals. This makes
   exactness and full enumeration inexpensive and exposes a proof step.
2. Compute quotient multiplication matrices and modular ranks. This is the
   verification approach, with no reliance on the valuation classification.
3. Use a displayed periodic sequence or its ranks as a shortcut for the
   obstruction. This fails: a sequence may not be exact, and two exact
   sequences with the same ranks may yield different positive Ext groups.

## Typed claims, origins, and falsifiers

CHAIN (FALSIFIED, DERIVED proposal): fg=0 would suffice for exactness. Take
R=F2[e]/e^3 and f=g=e^2. Both maps have image span(e^2), kernel span(e,e^2),
and the quotient has dimension one. A wrong quotient product or rank would
falsify this witness. Boundary checks include both zero maps, a unit and zero,
and f=g=e in the dual numbers.

CENSUS (EXPERIMENTALLY_SUPPORTED, DERIVED): among 67,780 pairs, 1,640 form
complexes and 1,157 are exact. All accepted index sets and homology histograms
are retained, not just aggregate counts. A missing tuple, incorrect index, or
any matrix/valuation disagreement falsifies this finite claim.

| p | m | pairs | complexes | exact |
|---:|---:|---:|---:|---:|
| 2 | 2 | 16 | 8 | 5 |
| 2 | 3 | 64 | 20 | 12 |
| 2 | 4 | 256 | 48 | 28 |
| 2 | 5 | 1024 | 112 | 64 |
| 3 | 2 | 81 | 21 | 16 |
| 3 | 3 | 729 | 81 | 60 |
| 3 | 4 | 6561 | 297 | 216 |
| 3 | 5 | 59049 | 1053 | 756 |

CONTROL (EXPERIMENTALLY_SUPPORTED, DERIVED): all eight augmented
controls have map ranks (p-1,1), but the nilpotent controls have Ext dimension
one in degrees 0..12 and separable controls have dimensions (1,0,...,0).
The stored separable splitting idempotent is 1-z^(p-1). Any quotient product,
cochain rank, idempotent, or recorded Frobenius coefficient failure falsifies
the corresponding finite certificate. There are 104 recorded Ext entries.

OBSTRUCTION (UNVERIFIED, IMPORTED_UNVERIFIED): the arbitrary-characteristic
argument below reconstructs the imported inseparable obstruction. It is an
ordinary proof audit, not independently authored or kernel accepted. Failure
of irreducibility, the tensor presentation, exactness in some degree, the
Ext obstruction, or the definition of allowed diagonal pieces defeats it.

SOURCE (PRIMARY_SOURCE_SUPPORTED, PRIMARY_SOURCE): the cited sources support
the field example and separate Rouquier bounds described in source notes;
they are not evidence for the imported positive diagonal gluing formula.
A mismatched version/locator or upgrading a Rouquier bound to a diagonal bound
would defeat this restricted citation claim.

## Ordinary proof steps, not a kernel result

First, over any coefficient field, f=e^a times a unit when f!=0. Its image is
(e^a), its kernel is (e^(m-a)), and its rank is m-a. With the convention for
zero these statements also cover a=m. Thus fg=0 iff a+b>=m; if so each positive
homology dimension is a+b-m. The enumeration tests this classification rather
than proving it for every field or m.

Now fix any prime p, k=Fp(t) with t transcendental, and
L=k[u]/(u^p-t). The t-adic valuation of t is 1, whereas a pth power has valuation
divisible by p. Therefore t has no pth root in k; the primary irreducibility
lemma makes L a degree-p field extension. Regard this as a k-linear category,
not as L-linear when forming the diagonal tensor product.

The multiplication module L over A=L tensor_k L has presentation
A=L[z]/(z^p-u^p)=L[e]/e^p with e=z-u. Its augmentation is e->0. The free
resolution of L begins A->L and alternates multiplication by e and e^(p-1).
The principal-ideal kernel calculation proves exactness in every positive
degree; at degree zero im(e)=ker(augmentation). Applying Hom_A(-,L) makes
every differential zero, so Ext_A^n(L,L)=L for every n>=0. A bounded projective
resolution would force these groups to vanish above its length. Consequently
the diagonal is not perfect. The arbitrary-degree conclusion comes from this
ordinary argument, not the degree-12 computation.

Every bounded complex of finite-dimensional L-vector spaces splits into its
cohomology; Perf(L) is generated by L using shifts, finite sums and summands,
without cones. It has Rouquier dimension zero and a singleton presentation
with arrow-depth zero. Exterior products of perfect L-complexes are perfect
over A, since each is built from L and their exterior product is built from A.
Finite cones and summands preserve perfectness. Hence the non-perfect diagonal
cannot occur in any finite such exterior-product resolution. This explains
why there can be no unrestricted finite depth-to-diagonal bound under these
definitions. It says nothing against a theorem that excludes imperfect ground
fields or requires smooth categories or additional perfect gluing hypotheses.

## Separable control and precise gap retired

For A=Fp[z]/(z^p-z), the alternating maps z and z^(p-1)-1 still have complementary
ranks and form an exact sequence, by the complementary factors of the modulus.
On Hom_A(-,Fp), however, the maps alternate 0 and -1. Positive cohomology is
zero. The element e0=1-z^(p-1) satisfies e0^2=e0, z*e0=0 and augmentation(e0)=1;
it splits the augmentation. Periodicity or map ranks alone therefore cannot
certify infinite projective dimension. The required extra check is the induced
Hom differential, plus actual exactness of the free resolution.

## Reproduction and boundaries

Run python experiments/run.py baseline, theory, verify, then replay, each as a
separate invocation from this directory (or use the script's absolute path).
Five mathematical child processes were used, including two replay children.
The resource wrapper is reused unchanged from the rank-10 packet; mathematical
implementations are new and import neither each other nor prior experiments.

The earlier interrupted workspace was lost. This packet reconstructs the same
bounded target from freshly verified inputs, without reusing any unsealed
output. It is the first accepted packet for this target, not a second claimed
advance. Neither the parent comparison question nor the imported positive
perfect-admissible diagonal formula is settled. No novelty is asserted.
