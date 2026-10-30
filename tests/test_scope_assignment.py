from sloperator.runner import run_source


def run(source: str) -> str:
    result = run_source(source)
    assert result.stderr == "", result.stderr
    return result.stdout


def test_nested_block_assignment_updates_nearest_enclosing_binding():
    source = """slop score = 1✨
{
    slop score = 2✨
    {
        score = 3✨
    }
    hallucinate(score)✨
}
hallucinate(score)✨
"""
    assert run(source) == "3\n1\n"


def test_nested_block_reads_enclosing_block_binding():
    source = """{
    slop x = 5✨
    {
        hallucinate(x)✨
    }
}
"""
    assert run(source) == "5\n"


def test_nested_block_assignment_reaches_outer_block_binding():
    source = """slop x = 1✨
{
    slop y = 2✨
    {
        y = 9✨
        x = 7✨
    }
    hallucinate(y)✨
}
hallucinate(x)✨
"""
    assert run(source) == "9\n7\n"
