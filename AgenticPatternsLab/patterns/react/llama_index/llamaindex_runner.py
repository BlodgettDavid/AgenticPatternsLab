from AgenticPatternsLab.patterns.react.shared.react_engine import StrictReactEngine
from AgenticPatternsLab.patterns.react.shared.tool_registry import ToolRegistry
from .llamaindex_adapter import LlamaIndexLLMAdapter


class LlamaIndexReactRunner:
    """
    Runner that wires a LlamaIndex LLM into the StrictReactEngine
    via the LlamaIndexLLMAdapter.
    """

    def __init__(self, llm=None):
        # 1) If no LLM provided, require explicit injection
        #    (LlamaIndex does not have a universal default like LangChain)
        if llm is None:
            raise ValueError("LlamaIndexReactRunner requires an llm instance.")

        # 2) Wrap in adapter
        self.adapter = LlamaIndexLLMAdapter(llm)

        # 3) Tool registry
        self.registry = ToolRegistry()

        # 4) Create strict engine
        self.engine = StrictReactEngine(
            llm_callback=self.adapter.complete,
            tool_callback=lambda name, input: self.registry.call(name, input),
        )

    def run(self, prompt: str) -> str:
        # Pure-python and LangChain both pass raw prompt
        return self.engine.run(prompt)


def llamaindex_react(prompt: str, llm=None) -> str:
    """
    Backwards-compatible helper that mirrors the old API.
    """
    runner = LlamaIndexReactRunner(llm=llm)
    return runner.run(prompt)