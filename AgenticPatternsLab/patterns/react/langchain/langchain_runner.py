# patterns/react/langchain/langchain_runner.py

from typing import Any, List
from langchain_core.language_models import BaseLanguageModel
from langchain_core.messages import HumanMessage, AIMessage

from AgenticPatternsLab.patterns.react.pure_python.prompting import build_react_prompt
from AgenticPatternsLab.patterns.react.pure_python.react_runner import (
    parse_llm_output,
    execute_action,
)


class LangChainReactRunner:
    """
    Local LangChain ReAct runner (Step 3g).
    Mirrors the pure‑Python runner but uses LangChain's LLM interface.
    """

    def __init__(self, llm: BaseLanguageModel, max_steps: int = 10):
        self.llm = llm
        self.max_steps = max_steps

    # ------------------------------------------------------------
    # Normalize LangChain outputs into a plain string
    # ------------------------------------------------------------
    def _extract_text(self, result: Any) -> str:
        """
        LangChain providers return different shapes:
        - AIMessage(content="...")
        - {"text": "..."}
        - {"content": "..."}
        - ChatMessage(content="...")
        This normalizes all of them into a single string.
        """
        if isinstance(result, AIMessage):
            return result.content

        if isinstance(result, dict):
            if "text" in result:
                return result["text"]
            if "content" in result:
                return result["content"]

        if hasattr(result, "content"):
            return result.content

        return str(result)

    # ------------------------------------------------------------
    # Main ReAct loop (local version)
    # ------------------------------------------------------------
    def run(self, user_query: str) -> str:
        transcript: List[str] = []
        prompt = build_react_prompt(user_query, transcript)

        for step in range(self.max_steps):
            # 1. Call LangChain LLM
            lc_result = self.llm.invoke([HumanMessage(content=prompt)])
            llm_output = self._extract_text(lc_result)

            # 2. Parse Thought / Action / Final Answer
            parsed = parse_llm_output(llm_output)

            # 3. Final Answer → return immediately
            if parsed["final_answer"] is not None:
                return parsed["final_answer"]

            # 4. Execute Action
            if parsed["action"] is not None:
                observation = execute_action(parsed["action"])
                transcript.append(f"Observation: {observation}")

            # 5. Rebuild prompt with updated transcript
            prompt = build_react_prompt(user_query, transcript)

        raise RuntimeError("Max steps reached without producing a final answer.")