"""
Provider Manager for the Agentic Patterns Lab.

Coordinates multiple LLM providers and implements a clean, sticky fallback chain.
The manager remembers the last successful provider across sequential calls.
"""

from typing import List, Any, Type
from pydantic import BaseModel


class ProviderManager:
    def __init__(self, providers: List):
        """
        providers: an ordered list of provider instances.
        The manager will try them in this order, sticking to the successful one.
        """
        seen = set()
        unique = []

        for p in providers:
            if type(p) not in seen:
                unique.append(p)
                seen.add(type(p))

        self.providers = unique
        # Track the active working index in the provider chain
        self._current_provider_index = 0

    def generate(self, prompt: str) -> str:
        """
        Try providers starting from the last known working provider index.
        If a provider fails, dynamically shift the sticky index forward.
        """
        last_error = None
        num_providers = len(self.providers)

        # Loop through providers starting exactly where we last succeeded
        for i in range(num_providers):
            # Use modulo to wrap back around if needed, starting from the sticky index
            actual_index = (self._current_provider_index + i) % num_providers
            provider = self.providers[actual_index]
            provider_name = provider.__class__.__name__

            print(f"[ProviderManager] Trying provider: {provider_name}")

            try:
                result = provider.generate(prompt)
                print(f"[ProviderManager] Provider {provider_name} succeeded.")
                
                # Update the sticky marker to this index for all future calls
                self._current_provider_index = actual_index
                return result

            except Exception as e:
                print(f"[ProviderManager] Provider {provider_name} failed: {e}")
                print("[ProviderManager] Moving to next provider...\n")
                last_error = e
                continue

        raise RuntimeError(f"All providers failed. Last error: {last_error}") from last_error

    
    
    def generate_structured(self, system_prompt: str, user_prompt: str, response_model: Type[BaseModel]) -> str:
        """
        Executes a structured schema generation across the sticky fallback provider chain.
        Ensures the underlying active provider returns a JSON payload matching the target Pydantic model.
        """
        last_error = None
        num_providers = len(self.providers)

        for i in range(num_providers):
            actual_index = (self._current_provider_index + i) % num_providers
            provider = self.providers[actual_index]
            provider_name = provider.__class__.__name__

            print(f"[ProviderManager] Trying structured provider: {provider_name}")

            try:
                # Duck-typing check: Ensure the provider has implemented the structured method
                if not hasattr(provider, "generate_structured"):
                    raise AttributeError(f"Provider {provider_name} does not implement 'generate_structured'.")

                result = provider.generate_structured(system_prompt, user_prompt, response_model)
                print(f"[ProviderManager] Structured provider {provider_name} succeeded.")
                
                # Maintain sticky behavior parity
                self._current_provider_index = actual_index
                return result

            except Exception as e:
                print(f"[ProviderManager] Structured provider {provider_name} failed: {e}")
                print("[ProviderManager] Moving to next provider in fallback sequence...\n")
                last_error = e
                continue

        raise RuntimeError(f"All structured providers failed. Last error: {last_error}") from last_error
    
    
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
        # Reset tracker if providers list changes completely
        self._current_provider_index = 0