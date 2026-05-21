import pytest
from AgenticPatternsLab.patterns.react.pure_python.react_runner import PurePythonReactRunner


class MockProvider:
    def generate(self, prompt: str) -> str:
        # First call: produce an Action
        if "Observation:" not in prompt:
            return (
                "Thought: I should verify the answer.\n"
                "Action: search('capital of France')"
            )
        # Second call: produce a Final Answer
        return (
            "Thought: I now know the answer.\n"
            "Final Answer: Paris."
        )


def test_runner_basic_flow():
    provider = MockProvider()
    runner = PurePythonReactRunner(provider)

    result = runner.run("What is the capital of France?")

    # Assert final answer is correct
    assert "Paris" in result
