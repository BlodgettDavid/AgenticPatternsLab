"""
Deterministic Unified Mock Provider for the Agentic Patterns Lab.

Consolidates simple text generation, multi-step execution tracing,
and interactive tool-calling evaluation into a single provider.
"""

from typing import Any


class MockLLM:
    def __init__(self):
        self.name = "mock"

    def generate(self, prompt: str) -> str:
        """
        Evaluates prompt keywords to simulate different execution behaviors 
        for ReAct loops, planning, and tool evaluation.
        """
        # --- 1. Handle Multi-Step ReAct Scenarios (from mock_provider_multistep) ---
        if "france capital" in prompt.lower() or "paris population" in prompt.lower():
            # First turn: No observation injected yet -> return search action
            if "Observation:" not in prompt:
                return (
                    "Thought: I should break this down.\n"
                    "Action: search(\"France capital\")"
                )

            # Second turn: One observation returned -> request next tool action
            if prompt.count("Observation:") == 1:
                return (
                    "Thought: Now I need the population.\n"
                    "Action: search(\"Paris population\")"
                )

            # Final turn: Observations satisfied -> return final text synthesis
            return (
                "Thought: I can now answer.\n"
                "FinalAnswer: Paris is the capital of France and has a population of about 2M."
            )

        # --- 2. Default Fallback Scenario (Your clean baseline from earlier) ---
        return (
            "Thought: I already know the answer.\n"
            "FinalAnswer: Hello from MockLLM!"
        )
    
    def run(self, prompt: str, tools: dict = None) -> Any:
        """
        Compatibility bridge matching the Agent framework execution contract.
        """
        raw_text = self.generate(prompt)

        class ProviderResponse:
            def __init__(self, text: str):
                self.final_answer = text
                self.trace = {}

        return ProviderResponse(raw_text)