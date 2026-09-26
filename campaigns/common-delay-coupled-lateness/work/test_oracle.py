from check import legal_target, solve_target, valid_target


def test_hand_cases():
    one = {"p": 1, "jobs": [{"b": 0, "deadline": 2}]}
    assert legal_target(one)
    assert solve_target(one) == {"start": [0]}
    assert valid_target(one, {"start": [0]})
    assert not valid_target(one, {"start": [1]})
    impossible = {"p": 1, "jobs": [{"b": 1, "deadline": 2}]}
    assert solve_target(impossible) == {"status": "NO-SOLUTION"}
    pair = {"p": 1, "jobs": [{"b": 1, "deadline": 3}, {"b": 1, "deadline": 4}]}
    assert valid_target(pair, {"start": [0, 1]})
    assert not valid_target(pair, {"start": [0, 0]})
    assert not legal_target({"p": 0, "jobs": []})


if __name__ == "__main__":
    test_hand_cases()
