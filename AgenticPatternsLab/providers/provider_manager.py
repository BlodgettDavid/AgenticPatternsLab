"""
Provider Manager for the Agentic Patterns Lab.

Coordinates multiple LLM providers and implements a clean fallback chain.
Each provider is tried in order until one succeeds.
"""

from typing import List, Any


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

    def run(self, prompt: str, tools: dict = None) -> Any:
        """
        Compatibility bridge matching the Agent framework execution contract.
        Forwards the call down to the fallback sequence and wraps the result 
        in an object containing both .final_answer and .trace to satisfy Agent contracts.
        """
        raw_text = self.generate(prompt)
        
        # Create a lightweight wrapper object to mimic a structured response
        class ProviderResponse:
            def __init__(self, text: str):
                self.final_answer = text
                self.trace = {}  # Added to satisfy tracking contracts in executor agents
                
        return ProviderResponse(raw_text)
    
    def set_providers(self, providers):
        seen = set()
        unique = []
        for p in providers:
            if type(p) not in seen:
                unique.append(p)
                seen.add(type(p))
        self.providers = unique        
    
# ---------------------------------------------------------------------------
# Intended provider chain (future-ready documentation)
# ---------------------------------------------------------------------------
from AgenticPatternsLab.providers.mock_provider import MockLLM

provider_manager = ProviderManager([
    MockLLM(),
])