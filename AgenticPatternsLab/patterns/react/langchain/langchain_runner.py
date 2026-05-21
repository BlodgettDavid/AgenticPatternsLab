# patterns/react/langchain/langchain_runner.py
from typing import Any
from langchain_core.language_models import BaseLanguageModel
from langchain_core.messages import HumanMessage, AIMessage

from AgenticPatternsLab.patterns.react.pure_python.react_runner import (
    PurePythonReactRunner,
)


class LangChainReactRunner(PurePythonReactRunner):
    """
    LangChain-backed ReAct runner.

    This class reuses the strict ReAct engine implemented in PurePythonReactRunner:
    - strict Thought / Action / Final Answer parsing
    - strict ACTION_RE validation
    - strict multi-step loop
    - strict action execution
    - strict error semantics

    Only the LLM invocation is overridden to use LangChain's .invoke() API.
    """
    def __init__(self, llm: BaseLanguageModel, max_steps: int = 10, *args, **kwargs):
        provider_chain = {
            "type": "langchain",
            "llm": llm,
        }

        # Initialize strict engine
        super().__init__(provider_chain=provider_chain, *args, **kwargs)

        # Store LLM
        self.llm = llm

        # Set max steps manually (PatternRunner does NOT accept it)
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
    # Override only the LLM call
    # ------------------------------------------------------------
    def ask_llm_for_step(self, prompt: str) -> str:
        """
        PurePythonReactRunner calls this method to get the next LLM step.
        Here we adapt that call to LangChain's .invoke() API.
        """
        # LangChain chat models expect a list of messages
        result = self.llm.invoke([HumanMessage(content=prompt)])
        return self._extract_text(result)