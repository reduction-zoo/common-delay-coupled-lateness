# Preparation evidence

Prepared on 2026-09-26 before construction. The fixed corpus has 120 distinct
legal Partition instances: 20 hand-labelled edge cases and 100 seeded random
cases, with 66 YES and 54 NO decisions and one to eight weights. Each source
answer is stored in `cases.json`; `generate_cases.py` retains the seeds and
generator. The exact subset-enumeration oracle agrees with an independent
subset-sum dynamic program on every case. Witnesses are validated by summing
the original weights; negative answers require exhaustive enumeration.

The target oracle uses Z3 4.16.0 with integer start variables, deadline
inequalities, and pairwise disjunctions preventing positive-length operation
overlap. A satisfying assignment corresponds directly to a legal schedule;
every legal schedule satisfies those constraints. Each returned model is
checked again by interval comparisons independent of the encoding. Z3 UNSAT
is treated as conclusive; unknown raises an error. A separate exhaustive
start-time enumeration agreed with Z3's decisions on 64 target configurations
with zero to three jobs and common length one or two. Hand fixtures cover exact
delay, zero-length second operations, an impossible deadline, overlap and
illegal input. [The source paper](https://arxiv.org/html/2602.20010v1)
defines the second start exactly `p` after first completion, so it is
`start+2p` here.

Reproduce from the repository root:

```sh
uv sync --locked
uv run --locked python campaigns/common-delay-coupled-lateness/work/check.py --self-test
```

The self-test starts with the corpus gate, regenerates random cases, checks
all source labels, and runs the independent target comparisons. The candidate
runner uses separate forward and recovery subprocesses and examines up to
three target schedules per case. An incorrect injected candidate was rejected
after solving its target and directly invalidating its recovery. No actual
reduction candidate exists. This finite corpus does not establish hardness or
the correctness of a future construction. Target exhaustive cross-checks have
only the sizes stated above.
