from typing import Any
try:
    from langchain_core.messages import BaseMessage
except ImportError:
    BaseMessage = object


class LangChainLLMAdapter:
    """
    Thin adapter that normalizes a LangChain LLM / ChatModel / Runnable
    to the simple complete(prompt: str) -> str interface required by
    the StrictReactEngine.
    """

    def __init__(self, llm: Any):
        self.llm = llm

    def _invoke_llm(self, prompt: str) -> Any:
        try:
            return self.llm.invoke(prompt)
        except TypeError:
            return self.llm.invoke([{"role": "user", "content": prompt}])

    def _normalize_output(self, result: Any) -> str:
        if isinstance(result, BaseMessage) and hasattr(result, "content"):
            return result.content

        if isinstance(result, str):
            return result

        if isinstance(result, dict) and "content" in result:
            return str(result["content"])

        return str(result)

    def complete(self, prompt: str) -> str:
        result = self._invoke_llm(prompt)
        return self._normalize_output(result)