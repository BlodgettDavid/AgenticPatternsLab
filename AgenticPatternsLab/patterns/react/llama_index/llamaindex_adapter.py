class LlamaIndexLLMAdapter:
    """
    Thin adapter that normalizes a LlamaIndex-style LLM into the
    interface expected by the StrictReactEngine.
    """

    def __init__(self, llm):
        self.llm = llm

    def complete(self, prompt: str) -> str:
        """
        LlamaIndex LLMs typically expose `.complete(prompt)`.
        """
        return self.llm.complete(prompt)