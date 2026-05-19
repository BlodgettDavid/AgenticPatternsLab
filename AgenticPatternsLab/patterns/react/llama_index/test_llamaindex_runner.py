from AgenticPatternsLab.patterns.react.llama_index.llamaindex_runner import (
    FakeLlamaIndexLLM,
    llamaindex_react,
)


def test_llamaindex_react_smoke():
    llm = FakeLlamaIndexLLM(
        responses=[
            "Thought: I should look this up.\nAction: search('France capital')",
            "Observation: The capital of France is Paris.\nThought: I now know the answer.\nFinal Answer: Paris."
        ]
    )

    result = llamaindex_react(llm)
    assert result == "Paris"
