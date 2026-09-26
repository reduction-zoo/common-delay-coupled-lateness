"""Independent oracles for Partition and common-delay coupled-task feasibility."""

import argparse
import json
import subprocess
import sys
from itertools import product
from pathlib import Path

import z3


def legal_source(source):
    return (isinstance(source, dict) and isinstance(source.get("weights"), list)
            and all(type(weight) is int and weight > 0 for weight in source["weights"]))


def solve_source(source):
    if not legal_source(source):
        raise ValueError("Illegal Partition instance")
    weights = source["weights"]
    total = sum(weights)
    if total % 2:
        return {"status": "NO-SOLUTION"}
    for mask in range(1 << len(weights)):
        subset = [index for index in range(len(weights)) if mask & (1 << index)]
        if sum(weights[index] for index in subset) * 2 == total:
            return {"subset": subset}
    return {"status": "NO-SOLUTION"}


def valid_source(source, output):
    if not legal_source(source) or not isinstance(output, dict):
        return False
    if output == {"status": "NO-SOLUTION"}:
        return solve_source(source) == output
    subset = output.get("subset")
    weights = source["weights"]
    return (set(output) == {"subset"} and isinstance(subset, list)
            and all(type(index) is int and 0 <= index < len(weights) for index in subset)
            and len(set(subset)) == len(subset)
            and 2 * sum(weights[index] for index in subset) == sum(weights))


def legal_target(target):
    return (isinstance(target, dict) and type(target.get("p")) is int and target["p"] > 0
            and isinstance(target.get("jobs"), list)
            and all(isinstance(job, dict) and type(job.get("b")) is int and job["b"] >= 0
                    and type(job.get("deadline")) is int for job in target["jobs"]))


def intervals(target, starts):
    p = target["p"]
    return [(starts[i], starts[i] + p) for i in range(len(starts))] + [
        (starts[i] + 2*p, starts[i] + 2*p + job["b"])
        for i, job in enumerate(target["jobs"]) if job["b"] > 0]


def direct_schedule(target, starts):
    if not legal_target(target) or not isinstance(starts, list) or len(starts) != len(target["jobs"]):
        return False
    if not all(type(start) is int and start >= 0 for start in starts):
        return False
    if any(starts[i] + 2*target["p"] + job["b"] > job["deadline"]
           for i, job in enumerate(target["jobs"])):
        return False
    busy = intervals(target, starts)
    return all(a[1] <= b[0] or b[1] <= a[0]
               for i, a in enumerate(busy) for b in busy[i+1:])


def target_solutions(target, limit=3):
    if not legal_target(target):
        raise ValueError("Illegal coupled-task instance")
    p, jobs = target["p"], target["jobs"]
    starts = [z3.Int(f"start_{i}") for i in range(len(jobs))]
    solver = z3.Solver()
    for i, job in enumerate(jobs):
        solver.add(starts[i] >= 0, starts[i] + 2*p + job["b"] <= job["deadline"])
    busy = [(starts[i], p) for i in range(len(jobs))] + [
        (starts[i] + 2*p, job["b"]) for i, job in enumerate(jobs) if job["b"] > 0]
    for i, (a, length_a) in enumerate(busy):
        for b, length_b in busy[i+1:]:
            solver.add(z3.Or(a + length_a <= b, b + length_b <= a))
    outputs = []
    while len(outputs) < limit:
        result = solver.check()
        if result == z3.unsat:
            break
        if result != z3.sat:
            raise RuntimeError(f"Z3 result was {result}: {solver.reason_unknown()}")
        model = solver.model()
        answer = [model.eval(start).as_long() for start in starts]
        if not direct_schedule(target, answer):
            raise AssertionError("Z3 model violates direct schedule validation")
        outputs.append({"start": answer})
        solver.add(z3.Or(*[start != value for start, value in zip(starts, answer)]))
    return outputs or [{"status": "NO-SOLUTION"}]


def solve_target(target):
    return target_solutions(target, 1)[0]


def valid_target(target, output):
    if not legal_target(target) or not isinstance(output, dict):
        return False
    if output == {"status": "NO-SOLUTION"}:
        return solve_target(target) == output
    return set(output) == {"start"} and direct_schedule(target, output["start"])


def exhaustive_target(target):
    if not legal_target(target):
        raise ValueError("Illegal target")
    bounds = [range(max(0, job["deadline"] - 2*target["p"] - job["b"] + 1))
              for job in target["jobs"]]
    for starts in product(*bounds):
        if direct_schedule(target, list(starts)):
            return {"start": list(starts)}
    return {"status": "NO-SOLUTION"}


def self_test():
    from generate_cases import EDGE_CASES, random_source
    from test_oracle import test_hand_cases

    root = Path(__file__).resolve().parents[3]
    path = Path(__file__).with_name("cases.json")
    subprocess.run([sys.executable, str(root / "research/validate_preparation.py"), str(path)], check=True, cwd=root)
    cases = json.loads(path.read_text())
    for weights, answer in EDGE_CASES:
        assert ("subset" in solve_source({"weights": weights})) == answer
    for case in cases:
        source = case["source"]
        if case["kind"] == "random":
            assert random_source(case["seed"]) == source
        current = solve_source(source)
        reachable = {0}
        for weight in source["weights"]:
            reachable |= {value + weight for value in reachable}
        total = sum(source["weights"])
        assert ("subset" in current) == (total % 2 == 0 and total//2 in reachable)
        assert ("subset" in current) == ("subset" in case["expected"])
        assert valid_source(source, case["expected"])
    assert not valid_source({"weights": [1, 1]}, {"subset": []})
    assert not valid_source({"weights": [1, 1]}, {"subset": [0, 0]})
    test_hand_cases()
    checked = 0
    for p in (1, 2):
        for n in range(4):
            for pattern in range(8):
                jobs = [{"b": (i + pattern) % 3, "deadline": 2*p + (i*3 + pattern) % 5}
                        for i in range(n)]
                target = {"p": p, "jobs": jobs}
                assert ("start" in solve_target(target)) == ("start" in exhaustive_target(target))
                checked += 1
    print(f"Self-test passed: {len(cases)} independently labelled source cases and {checked} exhaustive target checks")


def candidate_check(path):
    self_test()
    cases = json.loads(Path(__file__).with_name("cases.json").read_text())
    recovered = 0
    for case in cases:
        source = case["source"]
        forward = subprocess.run([sys.executable, str(path)], input=json.dumps(source), text=True, capture_output=True, check=True)
        target = json.loads(forward.stdout)
        if not legal_target(target):
            raise AssertionError(f"Illegal candidate target: {target}")
        for output in target_solutions(target):
            if not valid_target(target, output):
                raise AssertionError(f"Target oracle returned invalid output: {output}")
            payload = {"source": source, "target_solution": output}
            extraction = subprocess.run([sys.executable, str(path), "--extract"], input=json.dumps(payload), text=True, capture_output=True, check=True)
            recovered_output = json.loads(extraction.stdout)
            if not valid_source(source, recovered_output):
                raise AssertionError(f"Invalid recovery from {output}: {recovered_output}")
            recovered += 1
    print(f"Candidate check passed: {len(cases)} source cases, {recovered} target outputs")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test", action="store_true")
    group.add_argument("--candidate", type=Path)
    args = parser.parse_args()
    if args.self_test:
        self_test()
    else:
        candidate_check(args.candidate)
