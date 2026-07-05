import json
from pydantic import BaseModel, Field
from typing import Literal
from AgenticPatternsLab.providers.provider_manager import ProviderManager


class TriageResponse(BaseModel):
    """The explicit structural format required from the Triage Agent."""
    intent: Literal["pass", "fail", "derail"] = Field(
        ..., 
        description="The target category: 'pass' for explicit code solutions or direct answers, 'fail' for help requests, confusion, or hint prompts, and 'derail' for off-topic talk."
    )
    reasoning: str = Field(
        ..., 
        description="A brief sentence explaining why this specific category was selected."
    )


class TriageAgent:
    """The system Gatekeeper that interprets raw student input and maps it to FSM tokens."""
    
    def __init__(self, provider_chain: ProviderManager):
        self.provider = provider_chain

    def analyze_input(self, student_input: str) -> TriageResponse:
        """Invokes the fallback provider chain to parse the input into a structured response object."""
        
        system_instructions = (
            "You are the Core Triage Agent for an automated Computer Science Lab.\n"
            "Your singular responsibility is to analyze incoming student messages and categorize them into exactly one of three string tokens:\n\n"
            "1. 'pass': The student has provided a solution, written code, or directly answered a curriculum challenge.\n"
            "2. 'fail': The student says they are stuck, requests a hint, displays confusion, or explicitly asks for help.\n"
            "3. 'derail': The student is talking about topics completely unrelated to their computer science lab (e.g., weather, cooking recipes, poems, or general trivia).\n\n"
            "You must respond with a clean JSON object matching the required schema keys: 'intent' and 'reasoning'."
        )

        user_prompt = f"Student Conversation Turn: \"{student_input}\""

        try:
            # Route the call through our new structured fallback engine
            json_string = self.provider.generate_structured(
                system_prompt=system_instructions,
                user_prompt=user_prompt,
                response_model=TriageResponse
            )
            
            # Parse the clean string validation token back into our Pydantic object
            data = json.loads(json_string)
            return TriageResponse(**data)
            
        except Exception as e:
            # Fallback to safety: if everything melts down, default to a benign derail to prevent state crashes
            return TriageResponse(
                intent="derail",
                reasoning=f"System Exception encountered during triage assessment: {str(e)}"
            )