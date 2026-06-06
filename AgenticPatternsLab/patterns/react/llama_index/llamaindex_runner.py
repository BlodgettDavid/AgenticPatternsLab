from AgenticPatternsLab.patterns.react.shared.react_engine import StrictReactEngine
from .llamaindex_adapter import LlamaIndexLLMAdapter
from AgenticPatternsLab.patterns.react.shared.tool_registry import ToolRegistry
from AgenticPatternsLab.patterns.react.shared.prompt_builder import build_react_prompt



def llamaindex_react(prompt: str, llm=None) -> str:
    """
    Thin LlamaIndex runner that mirrors the LangChain runner.
    Uses dependency injection for tests and lazy import for real LLMs.
    """

    # 1) If no LLM provided, use a real one
    if llm is None:
        raise ValueError("llamaindex_react requires an llm instance. Provide a LlamaIndex-compatible LLM.")


    # 2) Wrap in adapter
    adapter = LlamaIndexLLMAdapter(llm)

    registry = ToolRegistry()

    # 3) Create strict engine
    engine = StrictReactEngine(
        llm_callback=adapter.complete,
        tool_callback=lambda name, input: registry.call(name, input),
    )

    # 4) Run loop
    initial_prompt = build_react_prompt(prompt)
    return engine.run(initial_prompt)