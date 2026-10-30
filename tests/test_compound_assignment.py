from sloperator.runner import run_source


def run(source: str) -> str:
    result = run_source(source)
    assert result.stderr == "", result.stderr
    return result.stdout


def fails(source: str) -> str:
    result = run_source(source)
    assert result.exit_code == 1
    return result.stderr.rstrip("\n")


def test_plus_equal_adds_the_right_hand_expression():
    assert run("slop n = 2✨\nn += 3 * 4✨\nhallucinate(n)✨\n") == "14\n"


def test_plus_equal_joins_strings():
    assert run("slop s = “foo”✨\ns += “bar”✨\nhallucinate(s)✨\n") == "foobar\n"


def test_plus_equal_right_side_sees_old_value():
    assert run("slop n = 2✨\nn += n + 1✨\nhallucinate(n)✨\n") == "5\n"


def test_plus_equal_updates_nearest_binding():
    source = """slop x = 1✨
{
    slop x = 10✨
    {
        x += 5✨
    }
    hallucinate(x)✨
}
hallucinate(x)✨
"""
    assert run(source) == "15\n1\n"


def test_plus_equal_updates_outer_binding_from_block():
    assert run("slop x = 1✨\n{ x += 2✨ }\nhallucinate(x)✨\n") == "3\n"


def test_plus_equal_works_in_loops_and_functions():
    source = """clanker bump(n) {
    n += 1✨
    ship n✨
}
slop total = 0✨
slop i = 0✨
ralph i < 3 {
    total += bump(i)✨
    i += 1✨
}
hallucinate(total)✨
"""
    assert run(source) == "6\n"


def test_plus_equal_undefined_name():
    assert fails("x += 1✨") == "SlopLang runtime error at line 1: undefined variable 'x'"


def test_plus_equal_loadbearing_is_immutable():
    assert "cannot assign to loadbearing 'X'" in fails("loadbearing X = 1✨\nX += 1✨")


def test_plus_equal_rejects_mixed_types():
    message = fails("slop n = 1✨\nn += “a”✨")
    assert "operands of '+=' must both be numbers or both be strings" in message
    assert "got number and string" in message


def test_plus_equal_rejects_booleans():
    assert "operands of '+='" in fails("slop b = ✅✨\nb += ✅✨")
