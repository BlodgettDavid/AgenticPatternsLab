import pytest
from AgenticPatternsLab.patterns.react.pure_python.strict_react_runner import StrictReactRunner

class InfiniteActionProvider:
    """
    Simulates an LLM that never produces a Final Answer.
    It always returns a Thought + Action.
    """
    def generate(self, prompt: str) -> str:
        return (
            "Thought: I should keep searching.\n"
            "Action: search('loop forever')"
        )

def test_max_steps_termination():
    provider = InfiniteActionProvider()
    runner = StrictReactRunner(provider)

    with pytest.raises(Exception):
        runner.run("This will never terminate normally.")