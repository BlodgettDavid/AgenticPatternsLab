from AgenticPatternsLab.patterns.react.shared.react_engine import StrictReactEngine
from .llamaindex_adapter import LlamaIndexLLMAdapter


def llamaindex_react(prompt: str, llm=None) -> str:
    """
    Thin LlamaIndex runner that mirrors the LangChain runner.
    Uses dependency injection for tests and lazy import for real LLMs.
    """

    # 1) If no LLM provided, use a real one
    if llm is None:
        # Lazy import so tests don't require llama-index installed
        from llama_index.llms.openai import OpenAI
        llm = OpenAI(model="gpt-4o-mini")

    # 2) Wrap in adapter
    adapter = LlamaIndexLLMAdapter(llm)

    # 3) Create strict engine
    engine = StrictReactEngine(
        llm_callback=adapter.complete,
        tool_callback=lambda name, input: "tool output",
    )

    # 4) Run loop
    return engine.run(prompt)