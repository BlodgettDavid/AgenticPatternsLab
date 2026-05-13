import pytest
from AgenticPatternsLab.patterns.react.pure_python.strict_react_runner import StrictReactRunner

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

# -----------------------------
# Tests
# -----------------------------

def test_missing_thought():
    runner = StrictReactRunner(BadProvider_MissingThought())
    with pytest.raises(ValueError):
        runner.run("What is the capital of France?")

def test_double_quotes_in_action():
    runner = StrictReactRunner(BadProvider_DoubleQuotes())
    with pytest.raises(ValueError):
        runner.run("What is the capital of France?")

def test_action_and_final_answer_same_step():
    runner = StrictReactRunner(BadProvider_ActionAndFinal())
    with pytest.raises(ValueError):
        runner.run("What is the capital of France?")

def test_multiple_actions():
    runner = StrictReactRunner(BadProvider_MultipleActions())
    with pytest.raises(ValueError):
        runner.run("What is the capital of France?")
