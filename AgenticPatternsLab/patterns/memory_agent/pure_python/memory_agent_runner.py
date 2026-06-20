# patterns/memory_agent/pure_python/memory_agent_runner.py

from dataclasses import dataclass
from typing import Any, Dict, Callable

from ...react.shared.react_engine import StrictReactEngine


@dataclass
class RunnerResult:
    """Returned by the runner after executing the engine."""
    final_answer: str
    trace: Any


class MemoryAgentRunner:
    """
    Pure‑python runner that wires:
        - LLM callback
        - Tool callback
        - StrictReactEngine
    """

    def __init__(self, llm: Callable[[str], str] = None):
        """
        llm: a callable that takes a prompt and returns LLM output.
             If None, a trivial fake LLM is used.
        """
        self.llm = llm or self._default_llm

    # ---------------------------------------------------------
    # Default LLM (very dumb, only for testing)
    # ---------------------------------------------------------
    def _default_llm(self, prompt: str) -> str:
        """
        A trivial fake LLM that always emits a Final Answer.
        This is only for early testing — real tests will override this.
        """
        return "Thought: I will answer directly.\nFinal Answer: I don't know."

    # ---------------------------------------------------------
    # Main runner entry point
    # ---------------------------------------------------------
    def run(self, enriched_prompt: str, tools: Dict[str, Callable] = None) -> RunnerResult:
        """
        enriched_prompt: the prompt built by MemoryAgent
        tools: tool registry from MemoryAgent.get_tools()
        """

        if tools is None:
            tools = {}

        # Wrap tools into a callback for StrictReactEngine
        def tool_callback(tool_name: str, query: str) -> str:
            if tool_name not in tools:
                return f"Unknown tool: {tool_name}"
            try:
                return tools[tool_name](query)
            except Exception as e:
                return f"Tool error: {e}"

        # Instantiate strict engine
        engine = StrictReactEngine(
            llm_callback=self.llm,
            tool_callback=tool_callback,
            max_steps=10,
        )

        # Run strict ReAct loop
        final_answer = engine.run(enriched_prompt)

        # Return final answer + trace (engine.history)
        return RunnerResult(
            final_answer=final_answer,
            trace=engine.history,
        )