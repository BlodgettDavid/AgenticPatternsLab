# patterns/memory_agent/pure_python/memory_agent_runner.py

from dataclasses import dataclass
from typing import Any, Dict, Callable

import re


try:
    # TODO(strict-react): Replace with formal StrictReactEngine implementation once
    # patterns.react.shared.react_engine is built to our desired spec.
    from ...react.shared.react_engine import StrictReactEngine
except ImportError:
    # TEMPORARY SHIM for global test execution only:
    # - Revisit Thought / Action / Final Answer parsing edge cases (multi-line
    #   thoughts, escaped quotes in tool args, malformed action syntax).
    # - Confirm history schema/types match what downstream callers and tests expect.
    # - Decide on max_steps / loop-termination behavior when no Final Answer is emitted.
    # - Remove this fallback class once the real StrictReactEngine module is in place.
    class StrictReactEngine:
        def __init__(self, llm_callback, tool_callback=None, max_steps=10):
            self.llm_callback = llm_callback
            self.tool_callback = tool_callback
            self.max_steps = max_steps
            self.history = []

        def run(self, prompt: str) -> str:
            current_prompt = prompt
            self.history = []

            for _ in range(self.max_steps):
                output = self.llm_callback(current_prompt)
                thought_match = re.search(r"Thought:\s*(.+)", output)
                thought = thought_match.group(1).strip() if thought_match else ""

                final_match = re.search(r"Final Answer:\s*(.+)", output, re.DOTALL)
                if final_match:
                    final_answer = final_match.group(1).strip()
                    self.history.append({
                        "thought": thought,
                        "final_answer": final_answer,
                    })
                    return final_answer

                action_match = re.search(r"Action:\s*([a-zA-Z0-9_]+)\((['\"])(.*?)\2\)", output)
                if action_match and self.tool_callback:
                    tool_name, _, query = action_match.groups()
                    observation = self.tool_callback(tool_name, query)
                    self.history.append({
                        "thought": thought,
                        "action": f"{tool_name}({query})",
                        "observation": observation,
                    })
                    current_prompt = f"{current_prompt}\n{output}\nObservation: {observation}"
                else:
                    self.history.append({
                        "thought": thought,
                        "raw": output,
                    })
                    current_prompt = f"{current_prompt}\n{output}\nObservation: No action executed."

            return "Max steps reached without Final Answer."

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