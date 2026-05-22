import pytest
from AgenticPatternsLab.patterns.react.llama_index.llamaindex_runner import (
    llamaindex_react,
)

class FakeLlamaIndexLLM:
    def __init__(self, responses):
        self.responses = responses
        self.index = 0

    def complete(self, prompt: str) -> str:
        out = self.responses[self.index]
        self.index += 1
        return out


def test_llamaindex_react_smoke():
    llm = FakeLlamaIndexLLM(
        responses=[
            # Step 1: valid Thought + Action
            "Thought: I should look this up.\nAction: search('France capital')",

            # Step 2: valid Thought + Final Answer
            "Thought: I now know the answer.\nFinal Answer: Paris"
        ]
    )

    result = llamaindex_react(llm)
    assert result == "Paris"


def test_llamaindex_react_multistep():
    llm = FakeLlamaIndexLLM(
        responses=[
            # Step 1: Thought + Action
            "Thought: I should search for the capital.\nAction: search('France capital')",

            # Step 2: Thought + Action (second step)
            "Thought: Let me double check.\nAction: search('Paris population')",

            # Step 3: Thought + Final Answer
            "Thought: I now know the answer.\nFinal Answer: Paris"
        ]
    )

    result = llamaindex_react(llm)
    assert result == "Paris"


def test_llamaindex_malformed_action():
    llm = FakeLlamaIndexLLM(
        responses=[
            # Step 1: Thought + malformed Action (missing quotes)
            "Thought: I should look this up.\nAction: search(France capital)"
        ]
    )

    with pytest.raises(ValueError):
        llamaindex_react(llm)


def test_llamaindex_missing_thought():
    llm = FakeLlamaIndexLLM(
        responses=[
            # INVALID: starts with Action instead of Thought
            "Action: search('France capital')"
        ]
    )

    with pytest.raises(ValueError):
        llamaindex_react(llm)


def test_llamaindex_unknown_tool():
    llm = FakeLlamaIndexLLM(
        responses=[
            # INVALID: "write" is not a supported tool
            "Thought: I should write something.\nAction: write('hello')"
        ]
    )

    with pytest.raises(ValueError):
        llamaindex_react(llm)

def test_llamaindex_runner_multistep():
    llm = FakeLlamaIndexLLM(
        responses=[
            # Step 1
            "Thought: Step one.\nAction: search('A')",

            # Step 2
            "Thought: Step two.\nAction: search('B')",

            # Step 3
            "Thought: Done.\nFinal Answer: Success"
        ]
    )

    result = llamaindex_react(llm)
    assert result == "Success"


def test_llamaindex_strict_engine_integration():
    llm = FakeLlamaIndexLLM(
        responses=[
            # Step 1: valid Thought + Action
            "Thought: Let me search.\nAction: search('France capital')",

            # Step 2: strict engine should send Observation, LLM responds with final answer
            "Thought: I now know it.\nFinal Answer: Paris"
        ]
    )

    result = llamaindex_react(llm)
    assert result == "Paris"


def test_llamaindex_error_handling():
    llm = FakeLlamaIndexLLM(
        responses=[
            # INVALID: Thought but no Action or Final Answer
            "Thought: I am thinking but doing nothing."
        ]
    )

    with pytest.raises(ValueError):
        llamaindex_react(llm)