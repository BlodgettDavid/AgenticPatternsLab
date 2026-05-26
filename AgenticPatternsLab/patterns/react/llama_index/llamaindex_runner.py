from typing import Any
from llama_index.core.llms import LLM
from AgenticPatternsLab.patterns.react.pure_python.react_runner import (
    PurePythonReactRunner,
)


class LlamaIndexReactRunner(PurePythonReactRunner):
    """
    Thin LlamaIndex adapter for the strict ReAct engine.
    Mirrors the LangChain adapter structure.
    """

    def __init__(self, llm: LLM, max_steps: int = 10, *args, **kwargs):
        provider_chain = {
            "type": "llamaindex",
            "llm": llm,
        }

        super().__init__(provider_chain=provider_chain, *args, **kwargs)

        self.llm = llm
        self.max_steps = max_steps

    # ------------------------------------------------------------
    # Normalize LlamaIndex outputs
    # ------------------------------------------------------------
    def _extract_text(self, result: Any) -> str:
        """
        LlamaIndex LLMs typically return objects with a `.text` attribute.
        """
        if hasattr(result, "text"):
            return result.text

        if isinstance(result, dict) and "text" in result:
            return result["text"]

        return str(result)

    # ------------------------------------------------------------
    # Override only the LLM call
    # ------------------------------------------------------------
    def ask_llm_for_step(self, prompt: str) -> str:
        """
        PurePythonReactRunner calls this to get the next LLM step.
        LlamaIndex LLMs use `.complete(prompt)`.
        """
        result = self.llm.complete(prompt)
        return self._extract_text(result)
