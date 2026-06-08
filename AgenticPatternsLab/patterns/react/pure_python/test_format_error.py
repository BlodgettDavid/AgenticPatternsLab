import pytest
from AgenticPatternsLab.patterns.react.pure_python.react_runner import PurePythonReactRunner
from AgenticPatternsLab.providers.provider_manager import provider_manager
from AgenticPatternsLab.providers.mock_provider import MockLLM


# -----------------------------
# Providers that violate format
# -----------------------------
class BadProvider_MissingThought:
    def generate(self, prompt: str) -> str:
        return "Action: search('capital of France')"


class BadProvider_DoubleQuotes:
    def generate(self, prompt: str) -> str:
        return (
            "Thought: I should search.\n"
            "Action: search(\"capital of France\")"
        )


class BadProvider_ActionAndFinal:
    def generate(self, prompt: str) -> str:
        return (
            "Thought: I know the answer.\n"
            "Action: search('capital of France')\n"
            "FinalAnswer: Paris."
        )


class BadProvider_MultipleActions:
    def generate(self, prompt: str) -> str:
        return (
            "Thought: I should search.\n"
            "Action: search('capital of France')\n"
            "Action: search('population of Seattle')"
        )

@pytest.fixture(autouse=True)
def reset_provider_manager():
    provider_manager.set_providers([MockLLM()])

# -----------------------------
# Tests
# -----------------------------
def test_missing_thought():
    provider = BadProvider_MissingThought()
    provider_manager.set_providers([provider])
    runner = PurePythonReactRunner()
    assert runner.run(...) == "FORMAT ERROR"

def test_double_quotes_in_action():
    provider = BadProvider_DoubleQuotes()
    provider_manager.set_providers([provider])
    runner = PurePythonReactRunner()
    assert runner.run(...) == "FORMAT ERROR"

def test_action_and_final_answer_same_step():
    provider = BadProvider_ActionAndFinal()
    provider_manager.set_providers([provider])
    runner = PurePythonReactRunner()
    assert runner.run(...) == "FORMAT ERROR"

def test_multiple_actions():
    provider = BadProvider_MultipleActions()
    provider_manager.set_providers([provider])
    runner = PurePythonReactRunner()
    assert runner.run(...) == "FORMAT ERROR"