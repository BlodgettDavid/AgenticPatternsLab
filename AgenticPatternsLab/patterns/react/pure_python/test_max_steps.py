from AgenticPatternsLab.patterns.react.pure_python.react_runner import PurePythonReactRunner
from AgenticPatternsLab.providers.provider_manager import provider_manager


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
    provider_manager.set_providers([provider])
    runner = PurePythonReactRunner()
    assert runner.run(...) == "FORMAT ERROR"