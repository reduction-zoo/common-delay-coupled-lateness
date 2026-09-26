# Partition → Common-delay coupled-task deadline feasibility

Category: Complexity open

## Source

The source gives positive binary integer weights. A valid output is a subset whose sum is half the total, or NO-SOLUTION if no such subset exists.

## Target

On one machine, each job has a first operation of common length p, an exact delay p, a second operation of length b_i, and a deadline d_i. Binary integer start times must avoid overlap and meet every deadline; zero-length second operations are allowed.

## Required result

Construct deterministic polynomial-time maps F and G: F sends every legal source instance to a legal target instance, and G(x,y) is a valid source output for every valid output y of F(x). Preserve the stated threshold, domain and promises. The requested complexity conclusion is NP-hardness for the stated target problem.

## Acceptance

Give explicit construction and recovery algorithms, a general proof for every legal input and every valid target output, and polynomial runtime and encoding-size bounds. Specify finite output encodings and handle NO-SOLUTION outputs when applicable. Tests compare recovered source outputs with independent source solutions.

## Why it matters

A hardness result would isolate the effect of deadlines in a highly uniform coupled-task scheduling model.

## Difficulty

Local ordering gadgets must compose under the common delay. Restricted pair-orientation tests have not supplied a general construction.

## Literature context

Results for general coupled tasks do not directly classify deadline feasibility when both the first-operation length and the intervening delay equal the same value.

Literature checked 2026-09-16. This summarizes the archived literature search on the date above. Unpublished, unindexed and overlooked work remains outside coverage; no new novelty assessment was performed.

## References

- [On scheduling coupled tasks with exact delays to minimize maximum lateness](https://arxiv.org/html/2602.20010v1): Kubiak, On scheduling coupled tasks with exact delays to minimize maximum lateness, Sections 1 and 6, explicitly leaves the general problem open. Sections 2 and 3 give algorithms for agreeable and disagreeable deadline/processing-time orders. Section 5 handles a specified partition into jobs determining makespan and the remaining jobs. The conclusion conjectures a pseudopolynomial algorithm. Hardness with job-dependent delays or unequal common first processing time and delay does not settle the present restriction. Common-deadline instances reduce to the known polynomial makespan case, so that specialization is not a viable Partition encoding.
- [version record](https://arxiv.org/abs/2602.20010): On 2026-09-16 searched "2026" "remains open" "complexity" "scheduling" -site:researchgate.net -pinwheel, "2602.20010" complexity, and "coupled tasks" "maximum lateness" "NP-hard" 2026. Inspected the primary definitions, pair timing, general-case discussion and version record. No later resolution was identified in this bounded search. This does not guarantee complete coverage.

Fixed from board record `website/questions/common-delay-coupled-lateness.json` in board checkout at 6c7d3bd9c0a8f595279969a9c0a4d1853a3f5c17; the record was copied from the current working tree.
