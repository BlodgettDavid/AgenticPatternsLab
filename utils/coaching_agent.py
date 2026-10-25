import json
from pydantic import BaseModel, Field
from providers.provider_manager import ProviderManager

class CoachingResponse(BaseModel):
    conceptual_hint: str = Field(
        ..., 
        description="A strategic hint pointing to the underlying programming concept without giving away the direct code syntax."
    )
    guiding_question: str = Field(
        ..., 
        description="A targeted, open-ended question that prompts the student to think through their specific logical bug."
    )

class CoachingAgent:
    def __init__(self, provider_manager: ProviderManager):
        self.pm = provider_manager

    def coach_student(self, prompt: str, student_code: str, evaluation_feedback: str) -> CoachingResponse:
        """
        Generates a structured pedagogical response to guide a struggling student
        without revealing the direct code solution.
        """
        system_instructions = (
            "You are an expert computer science tutor specializing in introductory logic. "
            "Your goal is to guide students using scaffolded feedback based on Universal Design "
            "for Learning (UDL) principles. NEVER give the student the direct code or solution syntax.\n\n"
            "Analyze their code against the original assignment and the evaluation feedback provided. "
            "Then, provide a high-quality conceptual hint and a single, clear guiding question "
            "to help them identify and fix their own logical gap.\n\n"
            "You must respond with a clean JSON object containing exactly two keys: 'conceptual_hint' (string) and 'guiding_question' (string)."
        )

        user_content = (
            f"Assignment Prompt: {prompt}\n"
            f"Student's Current Code: {student_code}\n"
            f"Evaluation Feedback: {evaluation_feedback}\n"
        )

        # Utilize our provider manager's unified schema-enforced contract
        response = self.pm.generate_structured(
            system_prompt=system_instructions,
            user_prompt=user_content,
            response_model=CoachingResponse
        )
        
        # Handle string fallbacks safely if the provider returns a raw JSON string
        if isinstance(response, str):
            data = json.loads(response)
            return CoachingResponse(**data)
            
        return response