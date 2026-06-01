class FakeLlamaIndexLLM:
    """
    Minimal fake LlamaIndex-style LLM for deterministic testing.
    """

    def __init__(self, responses):
        self.responses = list(responses)
        self.index = 0

    def complete(self, prompt: str) -> str:
        """
        Simulate a LlamaIndex LLM `.complete()` call.
        Returns a strict-format string.
        """
        if self.index >= len(self.responses):
            raise IndexError("No more fake responses available")

        response = self.responses[self.index]
        self.index += 1
        return response