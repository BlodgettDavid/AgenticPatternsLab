from AgenticPatternsLab.patterns.react.llama_index.fake_llamaindex_llm import FakeLlamaIndexLLM
from AgenticPatternsLab.patterns.react.llama_index.llamaindex_runner import llamaindex_react


def test_llamaindex_react_basic():
    fake_llm = FakeLlamaIndexLLM([
        "Thought: I should answer.\nFinal Answer: Hello from LlamaIndex!"
    ])

    result = llamaindex_react("Hello?", llm=fake_llm)

    assert result == "Hello from LlamaIndex!"