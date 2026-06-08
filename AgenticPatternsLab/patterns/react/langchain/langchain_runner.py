from .langchain_adapter import LangChainLLMAdapter
from AgenticPatternsLab.patterns.react.shared.react_engine import StrictReactEngine
from AgenticPatternsLab.patterns.react.shared.tool_registry import ToolRegistry


class LangChainReactRunner:
    """
    Runner that wires a LangChain LLM into the StrictReactEngine
    via the LangChainLLMAdapter.
    """

    def __init__(self, llm=None):
        # 1) If no LLM provided, use a real one
        if llm is None:
            # Imported lazily so tests don't require langchain_openai
            from langchain_openai import ChatOpenAI
            llm = ChatOpenAI(model="gpt-4o-mini")

        # 2) Wrap it in the adapter
        self.adapter = LangChainLLMAdapter(llm)

        # 3) Tool registry
        self.registry = ToolRegistry()

        # 4) Create the strict engine
        self.engine = StrictReactEngine(
            llm_callback=self.adapter.complete,
            tool_callback=lambda name, input: self.registry.call(name, input),
        )

    def run(self, prompt: str) -> str:
        # Pure-python runner passes raw prompt → so we do the same
        return self.engine.run(prompt)


def langchain_react(prompt: str, llm=None) -> str:
    """
    Backwards-compatible helper that mirrors the old API:
    langchain_react(prompt, llm=...)
    """
    runner = LangChainReactRunner(llm=llm)
    return runner.run(prompt)