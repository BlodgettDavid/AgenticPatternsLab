import json
from pydantic import BaseModel, Field
from providers.provider_manager import ProviderManager


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
            "You are the expert Code Evaluation Agent for an automated Computer Science Lab.\n"
            "Your critical directive is to strictly evaluate whether a student's submission is fully correct and meets every constraint specified in the lesson context.\n\n"
            "CRITICAL GRADING CRITERIA:\n"
            "1. BOUNDARY CONDITIONS: Pay extreme attention to boundary limits, ranges, and loop termination conditions.\n"
            "2. OFF-BY-ONE ERRORS: In Python, range(start, stop) is inclusive of 'start' but exclusive of 'stop'. If an exercise requests printing from 1 to 5, range(1, 5) is WRONG because it terminates at 4. The code must iterate or execute exactly the specified number of times.\n"
            "3. RIGOR: Do not be generous or lenient. If the code misses an edge case or produces an incorrect output sequence, 'is_correct' MUST be set to False.\n"
            "4. FOCUS: Focus entirely on validating correct code execution paths. If it fails a condition, clearly and concisely identify the flaw in the feedback text without giving away the exact line-by-line solution.\n\n"
            "You must respond with a clean JSON object containing exactly two keys: 'is_correct' (boolean) and 'feedback' (string)."
        )

        user_prompt = (
            f"Lesson Context / Exercise Rules:\n{lesson_context}\n\n"
            f"Student Submission:\n\"{student_input}\""
        )

        try:
            # Route the call through our structured fallback engine
            eval_res = self.provider.generate_structured(
                system_prompt=system_instructions,
                user_prompt=user_prompt,
                response_model=EvaluationResponse
            )
            
            # Handle string fallbacks safely (if any provider returns a raw string)
            if isinstance(eval_res, str):
                import json
                data = json.loads(eval_res)
                return EvaluationResponse(**data)
                
            return eval_res
            
        except Exception as e:
            return EvaluationResponse(
                is_correct=False,
                feedback=f"System evaluation suspended due to unexpected exception: {str(e)}"
            )