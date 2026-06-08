from AgenticPatternsLab.patterns.react.langchain.fake_langchain_llm import FakeLangChainLLM
from AgenticPatternsLab.patterns.react.langchain.langchain_runner import langchain_react
from AgenticPatternsLab.patterns.react.langchain.langchain_runner import LangChainReactRunner


def test_langchain_react_basic():
    fake_llm = FakeLangChainLLM([
        "Thought: I should answer.\nFinal Answer: Hello from LangChain!"
    ])

    result = langchain_react("Hello?", llm=fake_llm)

    assert result == "Hello from LangChain!"


def test_langchain_multistep():
    fake_llm = FakeLangChainLLM([
        # Step 1: Action
        "Thought: I should search.\nAction: search('capital of France')",

        # Step 2: Action again
        "Thought: I need more info.\nAction: search('Paris population')",

        # Step 3: Final Answer
        "Thought: I now know the answer.\nFinal Answer: Paris."
    ])

    result = langchain_react("What is the capital of France?", llm=fake_llm)
    assert result == "Paris."


def test_langchain_format_error():
    fake_llm = FakeLangChainLLM([
        # Missing Thought → should trigger FORMAT ERROR
        "Action: search('foo')"
    ])

    result = langchain_react("Test malformed output", llm=fake_llm)
    assert result == "FORMAT ERROR"


def test_langchain_tool_calling():
    fake_llm = FakeLangChainLLM([
        # Step 1: Action
        "Thought: I should search.\nAction: search('foo')",

        # Step 2: Final Answer
        "Thought: Done.\nFinal Answer: result"
    ])

    runner = LangChainReactRunner(llm=fake_llm)

    # Monkeypatch the registry inside the runner
    calls = []
    runner.registry.register("search", lambda x: calls.append(x) or "dummy observation")

    result = runner.run("Test tool calling")

    assert result == "result"
    assert calls == ["foo"]