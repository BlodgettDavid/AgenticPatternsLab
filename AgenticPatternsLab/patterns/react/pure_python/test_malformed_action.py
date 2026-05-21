import pytest
from AgenticPatternsLab.patterns.react.pure_python.react_runner import PurePythonReactRunner


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


# --- Pytest tests ---

@pytest.mark.parametrize("provider", [
    BadAction_DoubleQuotes(),
    BadAction_NoQuotes(),
    BadAction_MismatchedQuotes(),
    BadAction_ExtraText(),
    BadAction_MissingParen(),
])
def test_malformed_actions(provider):
    runner = PurePythonReactRunner(provider)
    with pytest.raises(ValueError):
        runner.run("What is the capital of France?")
