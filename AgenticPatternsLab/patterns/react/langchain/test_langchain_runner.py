from AgenticPatternsLab.patterns.react.langchain.fake_langchain_llm import FakeLangChainLLM
from AgenticPatternsLab.patterns.react.langchain.langchain_runner import langchain_react

def test_langchain_react_basic():
    fake_llm = FakeLangChainLLM([
        "Thought: I should answer.\nFinal Answer: Hello from LangChain!"
    ])

    result = langchain_react("Hello?", llm=fake_llm)

    assert result == "Hello from LangChain!"