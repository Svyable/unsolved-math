# Operational failures and accounting

Before the first successful baseline, snapshot construction rejected the
imported HTTP source URL because the schema requires HTTPS. The corresponding
HTTPS URL is now recorded, with the normalization disclosed in selection_basis;
the original URL remains in the source audit. Both HTTP and HTTPS access failed.

The baseline command was mistakenly launched after that failed preparation,
without input.json. The child exited nonzero. The parent's failure logger also
tried hashing the absent input and raised FileNotFoundError, so it did not save
the child's stderr or a failed-execution.json. The observed parent traceback
ended with FileNotFoundError for this packet's input.json. This failed invocation
is counted against the eight-child budget, not hidden as a successful check.

The runner now checks for input.json before launching a child. Preparation and
the baseline were rerun before theory.py was authored. No mathematical output
from the failed invocation was used. The successful execution logs capture
source/input/output hashes. This operational correction is not counted as a
research progress unit.
