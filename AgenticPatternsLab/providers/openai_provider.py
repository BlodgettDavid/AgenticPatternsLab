"""
OpenAI provider for the Agentic Patterns Lab.

This is a future‑ready stub implementation. It exposes the unified
`.generate(prompt)` interface so it can participate in ProviderManager
fallback chains.

Later, you will replace the body of `generate()` with real OpenAI API calls.
"""

class OpenAILLM:
    def __init__(self, model_name="gpt-4.1"):
        self.name = "openai"
        self.model_name = model_name

    def generate(self, prompt: str) -> str:
        """
        Placeholder OpenAI implementation.
        Replace this with real OpenAI API calls later.
        """
        raise RuntimeError(
            "OpenAI provider not implemented yet. "
            "This is a documentation stub for future integration."
        )