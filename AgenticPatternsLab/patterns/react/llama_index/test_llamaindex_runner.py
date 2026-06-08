from AgenticPatternsLab.patterns.react.llama_index.fake_llamaindex_llm import FakeLlamaIndexLLM
from AgenticPatternsLab.patterns.react.llama_index.llamaindex_runner import (
    llamaindex_react,
    LlamaIndexReactRunner,
)


def test_llamaindex_react_basic():
    fake_llm = FakeLlamaIndexLLM([
        "Thought: I should answer.\nFinal Answer: Hello from LlamaIndex!"
    ])

    result = llamaindex_react("Hello?", llm=fake_llm)

    assert result == "Hello from LlamaIndex!"


def test_llamaindex_multistep():
    fake_llm = FakeLlamaIndexLLM([
        # Step 1
        "Thought: I should search.\nAction: search('capital of France')",

        # Step 2
        "Thought: I need more info.\nAction: search('Paris population')",

        # Step 3
        "Thought: I now know the answer.\nFinal Answer: Paris."
    ])

    result = llamaindex_react("What is the capital of France?", llm=fake_llm)

    assert result == "Paris."


def test_llamaindex_format_error():
    fake_llm = FakeLlamaIndexLLM([
        # Missing Thought → FORMAT ERROR
        "Action: search('foo')"
    ])

    result = llamaindex_react("Test malformed output", llm=fake_llm)

    assert result == "FORMAT ERROR"


def test_llamaindex_tool_calling():
    fake_llm = FakeLlamaIndexLLM([
        # Step 1
        "Thought: I should search.\nAction: search('foo')",

        # Step 2
        "Thought: Done.\nFinal Answer: result"
    ])

    runner = LlamaIndexReactRunner(llm=fake_llm)

    calls = []
    runner.registry.register("search", lambda x: calls.append(x) or "dummy observation")

    result = runner.run("Test tool calling")

    assert result == "result"
    assert calls == ["foo"]