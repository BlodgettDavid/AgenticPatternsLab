"""
Azure OpenAI provider for the Agentic Patterns Lab.

This is a future‑ready stub implementation. It exposes the unified
`.generate(prompt)` interface so it can participate in ProviderManager
fallback chains.

Later, you will replace the body of `generate()` with real Azure OpenAI
API calls using the Azure SDK.
"""

class AzureOpenAILLM:
    def __init__(self, deployment_name="gpt-4o-mini"):
        self.name = "azure_openai"
        self.deployment_name = deployment_name

    def generate(self, prompt: str) -> str:
        """
        Placeholder Azure OpenAI implementation.
        Replace this with real Azure OpenAI API calls later.
        """
        raise RuntimeError(
            "Azure OpenAI provider not implemented yet. "
            "This is a documentation stub for future integration."
        )