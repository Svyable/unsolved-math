# Separate source/quantifier audit — 2026-08-28

Directly inspected https://stacks.math.columbia.edu/tag/012K:

- Definition 12.24.9(1) compares E-infinity with graded cohomology, not with
  the whole cohomology group as an unfiltered additive object.
- Parts (2)–(3) require separation, exhaustiveness, regularity and completeness.
- Lemma 12.24.11 assumes finite termwise filtrations. Its proof uses that
  hypothesis to obtain a finite filtration of cohomology. Our infinite examples
  are outside that lemma's hypothesis, even though the complex has one degree.

The module relation in https://stacks.math.columbia.edu/tag/00CM was checked
with (m,1) and (0,1): a single nonzero integer must annihilate m. Coordinatewise
choices cannot be substituted. This supports the localization step only.

The HRW v3 abstract at https://arxiv.org/abs/2206.11208v3 names the sphere;
it is not a verification of the imported positive-weight torsion window.
The versioned Segal PDF https://arxiv.org/pdf/2403.06724v1 states the sphere
result and explicitly discusses the care needed with inverse limits of Adams
spectral sequences. Neither source identifies our carry model with that tower.
AIM retrieval failed twice. Separate notes do not imply separate authorship
or expert endorsement; source, citation and computation claims remain distinct.
