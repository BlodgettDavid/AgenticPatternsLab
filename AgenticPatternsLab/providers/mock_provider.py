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
        """Simulates structured output generation by detecting the target Pydantic model

        schema and returning valid JSON matching its exact keys.
        """
        prompt_content = user_prompt.lower()
        
        # 1. Handle Triage Agent Target Schema
        if response_model.__name__ == "TriageResponse":
            intent = "pass"
            reasoning = "Mock evaluation: input looks like a valid submission."

            if "poem" in prompt_content or "weather" in prompt_content or "quantum" in prompt_content:
                intent = "derail"
                reasoning = "Mock classification: detected off-topic conversation or distraction."
            elif "stuck" in prompt_content or "hint" in prompt_content or "help" in prompt_content:
                intent = "fail"
                reasoning = "Mock classification: student explicitly requested instructional support."
                
            return json.dumps({"intent": intent, "reasoning": reasoning})
            
        # 2. Handle Evaluation Agent Target Schema 🎓
        elif response_model.__name__ == "EvaluationResponse":
            # Simulate a correct submission unless it explicitly contains a typo/error keyword
            is_correct = True
            feedback = "Excellent work! Your computational logic is perfectly correct."
            
            if "error" in prompt_content or "broken" in prompt_content or "wrong" in prompt_content:
                is_correct = False
                feedback = "Reviewing code logic: structural flaw detected in your loop termination bounds."
                
            return json.dumps({"is_correct": is_correct, "feedback": feedback})
            
        # Fallback default dict matching fundamental string schemas
        return json.dumps({"status": "success"})


    def run(self, prompt: str, tools: dict = None) -> Any:
        """Compatibility bridge matching the Agent framework execution contract."""
        raw_text = self.generate(prompt)

        class ProviderResponse:
            def __init__(self, text: str):
                self.final_answer = text
                self.trace = {}

        return ProviderResponse(raw_text)