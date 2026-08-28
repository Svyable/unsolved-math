# Independent-process verification

## Concrete independence basis and order

The verifier and its baseline were authored and executed before theory.py existed. Both implementations were authored by the same assistant, with shared frozen input and output schema. This is algorithmic and process independence, not independent human/model authorship. Each mathematical run uses fresh Python -I, an empty environment, resource limits, and no imports from the theory lane. The verifier reconstructs its expected data before opening the theory certificate. No paid external model or proof kernel was used.

The five recorded mathematical subprocesses are baseline, theory, verify, then theory and verify in replay. Their source/input/output hashes are checked during assembly. Baseline and theory main outputs are byte-identical; replay preserves both main output hashes. CPU limit is 180 seconds, wall timeout 200 seconds, address space 512 MiB. Process isolation is not a network namespace; the mathematical programs make no network calls.

## Counterexamples and boundary cases first

Before confirmation the verifier evaluates all seven base-field projective points and obtains seven ones. Removing the X^4 term makes [1:0:0] a zero, exposing an omitted-term bug. The reducible modulus x^2+1 is rejected, guarding against mistaking a quotient ring for a field. The Fermat quartic's characteristic-two derivatives vanish, guarding against characteristic-zero Jacobian assumptions.

These are fixed adversarial controls, not a claim of exhaustive search over all quartics. The counterexample under audit concerns index-one effectivity; rational connectedness is not assumed or tested.

## Computation audit

The theory uses integer bit-polynomial reduction and a hand-expanded homogeneous evaluation. The verifier uses tuples of coefficients, convolution and remainder tables, generic evaluation of the frozen monomial list, and a linear map for Frobenius squaring. Every nonzero element also passes an inverse-existence check. Both enumerate normalized projective points; degrees 1..6 contain 5,592 ambient points in total.

Theory traverses Frobenius orbits; verification determines the first positive iterate fixing each point and divides the resulting counts by the orbit degree. Both agree on all retained points, six counts (0,14,24,14,0,38), orbit profiles, and the two explicit witnesses. These finite checks are not evidence that all extension fields were searched.

For each chart the verifier differentiates the monomial set, divides f by its two derivatives with a lexicographic monomial order, obtains remainder 1, and reconstructs the division equality. This differs from substituting the theory's proposed multipliers. The three division-quotient certificates are retained in verify-output.json.

The final full-output equality gate rejects seven altered packets: base-point value, degree-2 count, degree-3 modulus, degree-2 witness degree, degree-3 witness coordinate, chart remainder exponent, and signed-cycle degree. These mutation controls test exact equality against reconstruction; they are not seven independent mathematical algorithms or a general validator security test.

## Claim, citation and proof-step checks

POINTS: passed exact field, projective normalization, point evaluation, orbit-length and signed-degree checks. A degree-one closed point would have appeared among the seven base points.

JACOBIAN: passed exact polynomial division and identity reconstruction on all three charts. The identity excludes common zeros over every extension by substitution. Finite point counts are not used for this implication.

GEOMETRY: ordinary proof-step audit checks that projectivity is automatic, all charts are covered, repeated and distinct geometric factors are both excluded, and only the coprime closed-point degrees are needed for index one. The algebraic-geometry dependencies and genus formula are stated rather than kernel-verified. This audit shares the author's mathematical judgment and does not resolve the independent-proof-review objection.

SOURCE: the fetched primary model is identified by a characteristic-two expansion into the frozen nine monomials; source dates and page locators are recorded in sources/source-audit.md. The source's general classifications are not imported as proved facts by this experiment. The AIM passage is historical commentary; it does not identify this curve with Ax's rationally connected example.

## Verification delta and objections

New verifier evidence independently reconstructs the geometric example's exact finite data and three Jacobian ideal certificates; it is not a rerun of the old finite-etale profile calculation. Remaining: independently authored review or kernel acceptance of the geometric argument; no rationally connected example, no Ax/Colliot-Thelene--Madore proof reconstruction, and no parent-status or novelty claim. Genus three is precisely why this example does not meet the rational-connectedness hypothesis.
