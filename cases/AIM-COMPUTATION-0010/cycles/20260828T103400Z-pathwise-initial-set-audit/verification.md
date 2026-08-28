# Independent verification lane

## Context and ordering

verify.py was authored and its baseline executed before theory.py was authored. baseline-execution.json establishes the execution time and source/input hashes. Every run starts Python -I in a fresh process with an empty environment. The verifier reconstructs its expectations before it reads the theory certificate; it imports no theory code. Independence is algorithmic and process-level only: the same assistant authored both implementations and shared input.json. No independent human/model or proof-kernel review occurred.

Method families: COUNTEREXAMPLE_SEARCH and INDEPENDENT_IMPLEMENTATION. The theory optimizes an absolute-value support envelope split at its kink. The verifier integrates each of four physical initial corners and constant-acceleration segments, finding segment maxima directly from velocity zeros. It does not implement the support-envelope formula or its kink rule.

## Counterexamples and boundaries first

Before the census, the verifier checks the interior-time witness, the all-zero model, and a nonzero initial set at T=0. It independently gets maximum 2/5 at time 2/3, sample maximum 3/8 and box maximum 1/2. Initial z=(1,-1) and constant w=1/5 satisfy the input constraints. The sampled-grid inference is rejected, while the threshold 9/20 succeeds with the exact support bound.

All 648 specified parameter instances are enumerated. For each, all four correlated initial corners and all eight +/-epsilon inputs on three equal-duration intervals are integrated, giving 20,736 exact trajectories. Every segment endpoint and admissible velocity-zero maximum is evaluated. Every trajectory lies below the independently computed constant-positive-input corner maximum, and some enumerated trajectory attains it. Zero-duration segments are included as degenerate tests. These tests do not by themselves establish the assertion for arbitrary measurable controls.

The verifier separately maximizes each of four coordinate-box corners and evaluates the three sample times. Its complete 648-row table agrees byte-for-byte with the theory table, including the earliest maximizing time, rather than merely matching the two headline examples. Each curvature class contains 216 cases. There are 35 strict sample misses and 160 strict box gaps.

## Certificate, computation and adversarial checks

The finite witness checker recomputes initial coordinates from z, validates |z_i|<=1 and |w|<=epsilon, validates the time interval, directly integrates the proposed witness, and checks both threshold comparisons plus the grid and box maxima. It accepts the unaltered certificate and rejects seven individually corrupted certificates: invalid z, excessive input, time outside the horizon, false initial position, false maximum, false sample maximum, false box maximum. These targeted controls are not a complete arbitrary-certificate parser or proof assistant.

All arithmetic is fractions.Fraction over integers. No floating tolerance, random seed, numerical integration error or third-party scientific library is involved. Table serialization is compact sorted JSON plus one LF. Each lane writes its own table path; equality is evidence of agreement, not evidence-file reuse. Runner replay repeats both lane subprocesses and requires unchanged output hashes. Five mathematical subprocesses total: baseline, theory, verify, theory replay, verification replay. Each has CPU 180s, wall 200s, address-space 512MiB limits; network isolation is not claimed, although these scripts make no network calls.

## Claim, citation and proof-step audit

1. The source page was freshly read on 2026-08-28. Its August 19, 2005 A.7 contribution is an agenda, not a theorem asserting the sample shortcut. The canonical imported statement and imported status remain unchanged; sources/primary-audit.json records the locator and scope. This is a distinct citation assessment, not independent source authorship.
2. The initial map has two independent generator coefficients, not two independent physical coordinates. The coordinate-box enlargement is sound; interpreting its failure as an actual violation would be wrong.
3. The variation-of-constants kernel t-s is nonnegative only for s in [0,t]. This justifies constant +epsilon for this model, not arbitrary sparse dynamics.
4. Suprema over time and admissible trajectories commute, but maximizing corners can change with time. The certificate only needs one corner attaining the global maximizing time.
5. A concave quadratic needs a stationary-point check; an affine or convex one on a compact interval needs endpoints. The kink must be retained. The verifier's direct-corner approach avoids that piecewise rule.
6. The finite rational witness and census are checked. The universal analytic proof still needs independently authored review or kernel formalization. Finite controls cannot prove the all-measurable-input claim, and no parent-problem conclusion follows.

The remaining objections are proof independence, narrow affine dynamics, scalar position-only bounds, and no feedback or high-dimensional result. This is a bounded discriminating certificate, not a new solution.
