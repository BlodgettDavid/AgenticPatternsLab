from .langchain_adapter import LangChainLLMAdapter
from AgenticPatternsLab.patterns.react.shared.react_engine import StrictReactEngine
from AgenticPatternsLab.patterns.react.shared.tool_registry import ToolRegistry


def langchain_react(prompt: str, llm=None) -> str:
    # 1) If no LLM provided, use a real one
    if llm is None:
        # Import here so tests don't require langchain_openai
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(model="gpt-4o-mini")

    # 2) Wrap it in the adapter
    adapter = LangChainLLMAdapter(llm)

    registry = ToolRegistry()

    # 3) Create the strict engine
    engine = StrictReactEngine(
        llm_callback=adapter.complete,
        tool_callback=lambda name, input: registry.call(name, input),
    )

    # 4) Run the loop
    return engine.run(prompt)