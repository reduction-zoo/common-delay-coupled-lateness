"""Fix a seeded Partition corpus before reduction construction."""

import json
import random
from pathlib import Path


EDGE_CASES = [
    ([1], False), ([2], False), ([1, 1], True), ([1, 2], False),
    ([2, 2], True), ([1, 1, 2], True), ([1, 2, 3], True),
    ([1, 1, 1], False), ([2, 3, 5], True), ([2, 2, 2], False),
    ([1, 1, 1, 1], True), ([1, 2, 2], False), ([3, 3, 4], False),
    ([1, 3, 4], True), ([4, 5, 9], True), ([1, 2, 4], False),
    ([3, 5, 8], True), ([1, 2, 3, 6], True), ([5, 5, 5], False),
    ([3, 4, 5], False),
]


def random_source(seed):
    rng = random.Random(seed)
    if seed % 2 == 0:
        weights = [rng.randint(1, 30) for _ in range(rng.randint(1, 7))]
        weights.append(sum(weights))
        rng.shuffle(weights)
    else:
        weights = [rng.randint(1, 30) for _ in range(rng.randint(1, 8))]
    return {"weights": weights}


def build_cases():
    from check import solve_source

    cases = []
    seen = set()

    def add(source, kind, seed=None, hand_answer=None):
        key = json.dumps(source, sort_keys=True, separators=(",", ":"))
        if key in seen:
            return False
        seen.add(key)
        answer = solve_source(source)
        if hand_answer is not None and ("subset" in answer) != hand_answer:
            raise AssertionError(f"Hand label disagrees with oracle: {source}")
        case = {"source": source, "kind": kind, "expected": answer}
        if seed is not None:
            case["seed"] = seed
        cases.append(case)
        return True

    for weights, answer in EDGE_CASES:
        add({"weights": weights}, "edge", hand_answer=answer)
    seed = 0
    while sum(case["kind"] == "random" for case in cases) < 100:
        add(random_source(seed), "random", seed=seed)
        seed += 1
    return cases


if __name__ == "__main__":
    path = Path(__file__).with_name("cases.json")
    cases = build_cases()
    path.write_text(json.dumps(cases, indent=2) + "\n")
    print(f"Wrote {len(cases)} cases to {path}")
