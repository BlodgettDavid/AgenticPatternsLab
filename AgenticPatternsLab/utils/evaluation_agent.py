import json
from pydantic import BaseModel, Field
from AgenticPatternsLab.providers.provider_manager import ProviderManager


class EvaluationResponse(BaseModel):
    """The structural contract required from the Evaluation Agent."""
    is_correct: bool = Field(
        ..., 
        description="True if the student's code or answer is correct and meets requirements, False otherwise."
    )
    feedback: str = Field(
        ..., 
        description="Encouraging feedback if correct, or a gentle pointing out of the structural flaw if incorrect."
    )


class EvaluationAgent:
    """The specialist agent that grades student submissions and ensures high code accuracy standards."""
    
    def __init__(self, provider_chain: ProviderManager):
        self.provider = provider_chain

    def evaluate_submission(self, lesson_context: str, student_input: str) -> EvaluationResponse:
        """Invokes the provider chain to evaluate student code or text answers against a correct rubric."""
        
        system_instructions = (
            "You are the Evaluation Agent for an automated Computer Science Lab.\n"
            "Your job is to read the provided lesson context and evaluate the student's submission.\n"
            "Determine if the solution correctly implements the logic requested.\n\n"
            "CRITICAL DIRECTIVE: Focus entirely on correct code scenarios. Ensure structural logic matches intent.\n"
            "You must respond with a clean JSON object containing exactly two keys: 'is_correct' (boolean) and 'feedback' (string)."
        )

        user_prompt = (
            f"Lesson Context / Exercise Rules:\n{lesson_context}\n\n"
            f"Student Submission:\n\"{student_input}\""
        )

        try:
            json_string = self.provider.generate_structured(
                system_prompt=system_instructions,
                user_prompt=user_prompt,
                response_model=EvaluationResponse
            )
            
            data = json.loads(json_string)
            return EvaluationResponse(**data)
            
        except Exception as e:
            # Safe system fallback if the provider fails mid-grading
            return EvaluationResponse(
                is_correct=False,
                feedback=f"System evaluation suspended due to unexpected exception: {str(e)}"
            )