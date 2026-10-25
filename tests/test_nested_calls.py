from sloperator.runner import run_source


def test_call_as_argument_to_another_call():
    source = (
        "clanker double(n) {\n"
        "    ship n * 2✨\n"
        "}\n"
        "clanker add(a, b) {\n"
        "    ship a + b✨\n"
        "}\n"
        "hallucinate(add(double(3), double(add(1, 2))))✨"
    )
    result = run_source(source)
    assert result.stderr == ""
    assert result.stdout == "12\n"
