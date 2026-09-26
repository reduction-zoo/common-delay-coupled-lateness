# Prepared input and output contract

Partition source input is `{"weights": [w0, ...]}` with positive integers.
An output is `{"subset": [distinct indices]}` summing to half the total, or
`{"status": "NO-SOLUTION"}` exactly when no such subset exists.

The target input is `{"p": positive_integer, "jobs": [{"b":
nonnegative_integer, "deadline": integer}, ...]}`. All times are integers.
For each job `i`, first operation `[start[i], start[i]+p)` occupies the sole
machine; second operation `[start[i]+2p, start[i]+2p+b[i])` starts after the
exact delay of `p`. Start times are nonnegative, no positive-length operations
may overlap, and each second completion is at most its deadline. A valid
output is `{"start": [times]}`. `{"status": "NO-SOLUTION"}` is valid only
when no schedule exists. A zero-length second operation occupies no machine
time, though its completion must still meet its deadline.

A candidate `algorithm.py` reads one source JSON object from stdin and writes
one legal target JSON object to stdout. With `--extract`, it reads
`{"source": source, "target_solution": output}` and writes a valid source
output. Errors exit nonzero; diagnostics go to stderr. The two processes share
no memory. The candidate must run in deterministic polynomial time and recover
a valid source output from every valid target output, including alternate
schedules and NO-SOLUTION.

`check.py --candidate PATH` injects the fixed source cases, solves each target
independently, and validates each recovered source output.
