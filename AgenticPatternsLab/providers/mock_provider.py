"""
Deterministic Unified Mock Provider for the Agentic Patterns Lab.

Consolidates simple text generation, multi-step execution tracing,
interactive tool-calling evaluation, and structured schema routing into a single provider.
"""

from typing import Any, Type
import json
from pydantic import BaseModel


class MockLLM:
    def __init__(self):
        self.name = "mock"

    def generate(self, prompt: str) -> str:
        """Evaluates prompt keywords to simulate different execution behaviors 
        for ReAct loops, planning, and tool evaluation.
        """
        # --- 1. Handle Multi-Step ReAct Scenarios ---
        if "france capital" in prompt.lower() or "paris population" in prompt.lower():
            if "Observation:" not in prompt:
                return (
                    "Thought: I should break this down.\n"
                    "Action: search(\"France capital\")"
                )

            if prompt.count("Observation:") == 1:
                return (
                    "Thought: Now I need the population.\n"
                    "Action: search(\"Paris population\")"
                )

            return (
                "Thought: I can now answer.\n"
                "FinalAnswer: Paris is the capital of France and has a population of about 2M."
            )

        # --- 2. Default Fallback Scenario ---
        return (
            "Thought: I already know the answer.\n"
            "FinalAnswer: Hello from MockLLM!"
        )
    
    
    def generate_structured(self, system_prompt: str, user_prompt: str, response_model: Type[BaseModel]) -> str:
        """Simulates structured output generation by parsing keywords and returning

        a valid JSON string matching the expected Pydantic response model.
        """
        prompt_content = user_prompt.lower()
        
        # Default fallback values
        intent = "pass"
        reasoning = "Mock evaluation: input looks like a valid submission."

        # Simulate Triage Agent Classifications
        if "poem" in prompt_content or "weather" in prompt_content or "quantum" in prompt_content:
            intent = "derail"
            reasoning = "Mock classification: detected off-topic conversation or distraction."
        elif "stuck" in prompt_content or "hint" in prompt_content or "help" in prompt_content:
            intent = "fail"
            reasoning = "Mock classification: student explicitly requested instructional support."
            
        # Build a dictionary conforming strictly to the requested schema keys
        mock_data = {
            "intent": intent,
            "reasoning": reasoning
        }
        
        return json.dumps(mock_data)


    def run(self, prompt: str, tools: dict = None) -> Any:
        """Compatibility bridge matching the Agent framework execution contract."""
        raw_text = self.generate(prompt)

        class ProviderResponse:
            def __init__(self, text: str):
                self.final_answer = text
                self.trace = {}

        return ProviderResponse(raw_text)