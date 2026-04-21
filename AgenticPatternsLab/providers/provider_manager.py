"""
Provider Manager for the Agentic Patterns Lab.

Coordinates multiple LLM providers and implements a clean fallback chain.
Each provider is tried in order until one succeeds.
"""

from typing import List


class ProviderManager:
    def __init__(self, providers: List):
        """
        providers: an ordered list of provider instances.
        The manager will try them in this order.
        """

        # Remove duplicate provider types while preserving order

        seen = set()
        unique = []

        for p in providers:
            if type(p) not in seen:
                unique.append(p)
                seen.add(type(p))

        self.providers = unique

    
    def generate(self, prompt: str) -> str:
        """
        Try each provider in order.
        If one succeeds, return its result.
        If all fail, raise a RuntimeError.
        """
        last_error = None

        for provider in self.providers:
            provider_name = provider.__class__.__name__
            print(f"[ProviderManager] Trying provider: {provider_name}")

            try:
                result = provider.generate(prompt)
                print(f"[ProviderManager] Provider {provider_name} succeeded.")
                return result

            except Exception as e:
                print(f"[ProviderManager] Provider {provider_name} failed: {e}")
                print("[ProviderManager] Moving to next provider...\n")
                last_error = e
                continue

        raise RuntimeError(f"All providers failed. Last error: {last_error}") from last_error



# ---------------------------------------------------------------------------
# Intended provider chain (future-ready documentation)
#
# This shows the full architecture, including providers not yet implemented.
#
# providers = [
#     GeminiLLM(),
#     OpenAILLM(),        # not implemented yet
#     AzureOpenAILLM(),   # not implemented yet
#     OllamaLLM(),
#     MockLLM()
# ]
#
# ---------------------------------------------------------------------------