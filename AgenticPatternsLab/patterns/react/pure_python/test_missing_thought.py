import pytest
from AgenticPatternsLab.patterns.react.pure_python.strict_react_runner import StrictReactRunner

class MissingThoughtProvider:
    """
    Simulates an LLM that incorrectly starts with Action instead of Thought.
    """
    def generate(self, prompt: str) -> str:
        return "Action: search('capital of France')"

def test_missing_thought():
    provider = MissingThoughtProvider()
    runner = StrictReactRunner(provider)

    with pytest.raises(ValueError):
        runner.run("What is the capital of France?")