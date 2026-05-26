import pytest
from pydantic import PrivateAttr
from llama_index.core.llms import LLM

from AgenticPatternsLab.patterns.react.llama_index.llamaindex_runner import (
    LlamaIndexReactRunner,
)


# ------------------------------------------------------------
# Fake LlamaIndex LLM for strict testing
# ------------------------------------------------------------
class FakeLlamaIndexLLM(LLM):
    _responses: list = PrivateAttr()

    def __init__(self, responses):
        super().__init__()
        self._responses = list(responses)

    # ------------------------------------------------------------
    # Required abstract methods (sync)
    # ------------------------------------------------------------
    def complete(self, prompt: str, **kwargs):
        if not self._responses:
            raise RuntimeError("FakeLlamaIndexLLM: no more responses available")
        return type("Obj", (), {"text": self._responses.pop(0)})

    def chat(self, messages, **kwargs):
        raise NotImplementedError()

    def stream_complete(self, prompt: str, **kwargs):
        raise NotImplementedError()

    def stream_chat(self, messages, **kwargs):
        raise NotImplementedError()

    # ------------------------------------------------------------
    # Required abstract methods (async)
    # ------------------------------------------------------------
    async def acomplete(self, prompt: str, **kwargs):
        raise NotImplementedError()

    async def achat(self, messages, **kwargs):
        raise NotImplementedError()

    async def astream_complete(self, prompt: str, **kwargs):
        raise NotImplementedError()

    async def astream_chat(self, messages, **kwargs):
        raise NotImplementedError()

    # ------------------------------------------------------------
    # Metadata
    # ------------------------------------------------------------
    @property
    def metadata(self):
        return {}

# ------------------------------------------------------------
# Tests
# ------------------------------------------------------------

def test_final_answer_single_step():
    llm = FakeLlamaIndexLLM(
        responses=[
            "Thought: I know this.\nFinal Answer: Paris"
        ]
    )
    runner = LlamaIndexReactRunner(llm)
    assert runner.run("What is the capital of France?") == "Paris"


def test_multistep_final_answer():
    llm = FakeLlamaIndexLLM(
        responses=[
            "Thought: Let me search.\nAction: search('France capital')",
            "Thought: I know it now.\nFinal Answer: Paris",
        ]
    )
    runner = LlamaIndexReactRunner(llm)
    assert runner.run("What is the capital of France?") == "Paris"


def test_malformed_action_raises():
    llm = FakeLlamaIndexLLM(
        responses=[
            "Thought: Let me search.\nAction: search(France capital)"
        ]
    )
    runner = LlamaIndexReactRunner(llm)
    with pytest.raises(ValueError):
        runner.run("test")


def test_missing_thought_raises():
    llm = FakeLlamaIndexLLM(
        responses=[
            "Action: search('France capital')"
        ]
    )
    runner = LlamaIndexReactRunner(llm)
    with pytest.raises(ValueError):
        runner.run("test")


def test_unknown_tool_raises():
    llm = FakeLlamaIndexLLM(
        responses=[
            "Thought: Let me write.\nAction: write('hello')"
        ]
    )
    runner = LlamaIndexReactRunner(llm)
    with pytest.raises(ValueError):
        runner.run("test")


def test_runner_multistep():
    llm = FakeLlamaIndexLLM(
        responses=[
            "Thought: Step one.\nAction: search('A')",
            "Thought: Step two.\nAction: search('B')",
            "Thought: Done.\nFinal Answer: Success",
        ]
    )
    runner = LlamaIndexReactRunner(llm)
    assert runner.run("test") == "Success"


def test_strict_engine_integration():
    llm = FakeLlamaIndexLLM(
        responses=[
            "Thought: Let me search.\nAction: search('France capital')",
            "Thought: I now know it.\nFinal Answer: Paris",
        ]
    )
    runner = LlamaIndexReactRunner(llm)
    assert runner.run("test") == "Paris"


def test_error_handling():
    llm = FakeLlamaIndexLLM(
        responses=[
            "Thought: I am thinking but doing nothing."
        ]
    )
    runner = LlamaIndexReactRunner(llm)
    with pytest.raises(ValueError):
        runner.run("test")
