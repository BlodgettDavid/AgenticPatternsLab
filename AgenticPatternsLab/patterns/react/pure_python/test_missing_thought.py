from AgenticPatternsLab.patterns.react.pure_python.react_runner import PurePythonReactRunner
from AgenticPatternsLab.providers.provider_manager import provider_manager


class MissingThoughtProvider:
    """
    Simulates an LLM that incorrectly starts with Action instead of Thought.
    """
    def generate(self, prompt: str) -> str:
        return "Action: search('capital of France')"


def test_missing_thought():
    provider = MissingThoughtProvider()
    provider_manager.set_providers([provider])
    runner = PurePythonReactRunner()
    assert runner.run("What is the capital of France?") == "FORMAT ERROR"