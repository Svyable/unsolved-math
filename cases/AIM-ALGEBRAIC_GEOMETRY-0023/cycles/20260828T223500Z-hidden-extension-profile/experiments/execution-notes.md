# Execution accounting and retained failure

Seven mathematical child invocations were used, of the configured maximum eight:

1. Baseline with the original verifier: success.
2. Theory: success.
3. Verify: failed because a corrupted certificate was accepted. The original
   runner raised CalledProcessError before writing a log; the observed command
   was run.py verify. Its captured child stderr was not persisted or displayed.
4. Verify after adding failure logging to run.py: same source/input/proposal,
   failed at the wrong_modulus regression. failed-execution.json retains the
   exact command, times, hashes and stderr for this diagnostic repetition.
5. Verify after adding injectivity: success.
6–7. Theory and repaired verifier replay: success, byte-identical outputs.

baseline-verifier.txt is the exact source used in invocations 1,3,4. The only
mathematical checker change is the added injectivity assertion; baseline census
results were not changed. The old source and failing regression are retained
as evidence of the defect and repair. The runner was also formatted afterward;
no claim that its old version bytes are retained is made.

Preflight, dataset validation and 33 prior manifest checks passed before final
packaging. One operational import used the wrong module name oplab.packet;
it was corrected to oplab.cycle_store. A Ruff style finding in theory.py was
fixed before executing that program. These were not mathematical child runs.
