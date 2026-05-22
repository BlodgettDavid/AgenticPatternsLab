from AgenticPatternsLab.patterns.react.llama_index.llamaindex_runner import (
    llamaindex_react,
)


class FakeLlamaIndexLLM:
    """
    Minimal mock LlamaIndex-style LLM.
    It exposes `.complete(prompt: str) -> str`.
    """
    def __init__(self, responses):
        self.responses = responses
        self.index = 0

    def complete(self, prompt: str) -> str:
        if self.index < len(self.responses):
            out = self.responses[self.index]
            self.index += 1
            return out
        return "Final Answer: No more responses."


def test_llamaindex_react_smoke():
    llm = FakeLlamaIndexLLM(
        responses=[
            "Thought: I should look this up.\nAction: search('France capital')",
            "Observation: The capital of France is Paris.\nThought: I now know the answer.\nFinal Answer: Paris."
        ]
    )

    result = llamaindex_react(llm)
    assert result == "Paris"