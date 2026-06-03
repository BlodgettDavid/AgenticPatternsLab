import pytest
from AgenticPatternsLab.patterns.react.pure_python.react_runner import PurePythonReactRunner


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
    runner = PurePythonReactRunner(provider)
    assert runner.run("This will never terminate normally.") == "FORMAT ERROR"