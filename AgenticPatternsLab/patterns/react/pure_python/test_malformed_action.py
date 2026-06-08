import pytest
from AgenticPatternsLab.patterns.react.pure_python.react_runner import PurePythonReactRunner
from AgenticPatternsLab.providers.provider_manager import provider_manager
from AgenticPatternsLab.providers.mock_provider import MockLLM

# --- Providers with malformed Action lines ---

class BadAction_DoubleQuotes:
    def generate(self, prompt: str) -> str:
        return (
            "Thought: I should search.\n"
            "Action: search(\"capital of France\")"
        )

class BadAction_NoQuotes:
    def generate(self, prompt: str) -> str:
        return (
            "Thought: I should search.\n"
            "Action: search(capital of France)"
        )

class BadAction_MismatchedQuotes:
    def generate(self, prompt: str) -> str:
        return (
            "Thought: I should search.\n"
            "Action: search('capital of France\")"
        )

class BadAction_ExtraText:
    def generate(self, prompt: str) -> str:
        return (
            "Thought: I should search.\n"
            "Action: search('capital of France') extra"
        )

class BadAction_MissingParen:
    def generate(self, prompt: str) -> str:
        return (
            "Thought: I should search.\n"
            "Action: search 'capital of France'"
        )

# --- Reset ProviderManager before each test ---

@pytest.fixture(autouse=True)
def reset_provider_manager():
    provider_manager.set_providers([MockLLM()])

# --- Pytest tests ---

@pytest.mark.parametrize("provider", [
    BadAction_DoubleQuotes(),
    BadAction_NoQuotes(),
    BadAction_MismatchedQuotes(),
    BadAction_ExtraText(),
    BadAction_MissingParen(),
])
def test_malformed_actions(provider):
    provider_manager.set_providers([provider])
    runner = PurePythonReactRunner()
    assert runner.run(...) == "FORMAT ERROR"