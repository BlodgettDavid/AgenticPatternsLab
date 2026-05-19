from AgenticPatternsLab.patterns.react.pure_python.strict_react_runner import run_strict_react


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


def llamaindex_react(llm):
    """
    Thin adapter that wraps a LlamaIndex-style LLM and feeds it into the strict engine.
    """
    def llm_wrapper(prompt: str) -> str:
        return llm.complete(prompt)

    return run_strict_react(llm_wrapper)
