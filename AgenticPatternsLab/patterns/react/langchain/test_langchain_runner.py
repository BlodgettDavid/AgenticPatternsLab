# AgenticPatternsLab/patterns/react/langchain/test_langchain_runner.py
from pydantic import PrivateAttr
import pytest
from langchain_core.messages import AIMessage
from langchain_core.language_models import SimpleChatModel

from AgenticPatternsLab.patterns.react.langchain.langchain_runner import (
    LangChainReactRunner,
)

# ---------------------------------------------------------------------
# Fake LangChain LLM for testing
# ---------------------------------------------------------------------
class FakeLangChainLLM(SimpleChatModel):
    """
    A controllable fake LangChain LLM for testing.
    Uses a Pydantic private attribute to store responses.
    """

    _responses: list = PrivateAttr()

    def __init__(self, responses):
        super().__init__()
        self._responses = list(responses)

    def invoke(self, messages, **kwargs):
        if not self._responses:
            raise RuntimeError("FakeLangChainLLM: no more responses available")
        return AIMessage(content=self._responses.pop(0))

    # Required abstract method
    def _call(self, messages, **kwargs):
        return self.invoke(messages, **kwargs)

    @property
    def _llm_type(self):
        return "fake-llm"

# ---------------------------------------------------------------------
# 1. Final Answer test (single-step)
# ---------------------------------------------------------------------
def test_final_answer_single_step():
    llm = FakeLangChainLLM([
        "Thought: I know the answer.\nFinal Answer: Paris"
    ])
    runner = LangChainReactRunner(llm)

    result = runner.run("What is the capital of France?")
    assert result == "Paris"


# ---------------------------------------------------------------------
# 2. Multi-step test
# ---------------------------------------------------------------------
def test_multistep_final_answer():
    llm = FakeLangChainLLM([
        # Step 1
        "Thought: I should search.\nAction: search('capital of france')",
        # Step 2
        "Thought: I know the answer.\nFinal Answer: Paris"
    ])
    runner = LangChainReactRunner(llm)

    result = runner.run("What is the capital of France?")
    assert result == "Paris"


# ---------------------------------------------------------------------
# 3. Malformed action → strict ValueError
# ---------------------------------------------------------------------
def test_malformed_action_raises():
    llm = FakeLangChainLLM([
        "Thought: I should search.\nAction: search(bad)"  # missing quotes
    ])
    runner = LangChainReactRunner(llm)

    with pytest.raises(ValueError):
        runner.run("test")


# ---------------------------------------------------------------------
# 4. Missing Thought → strict ValueError
# ---------------------------------------------------------------------
def test_missing_thought_raises():
    llm = FakeLangChainLLM([
        "Action: search('x')"  # Thought missing
    ])
    runner = LangChainReactRunner(llm)

    with pytest.raises(ValueError):
        runner.run("test")


# ---------------------------------------------------------------------
# 5. Max steps reached → RuntimeError
# ---------------------------------------------------------------------
def test_max_steps_reached():
    # Always returns a Thought, never a Final Answer
    llm = FakeLangChainLLM([
        "Thought: thinking..." for _ in range(5)
    ])
    runner = LangChainReactRunner(llm)
    runner.max_steps = 3

    with pytest.raises(ValueError):
        runner.run("test")