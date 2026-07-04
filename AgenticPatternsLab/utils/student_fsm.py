from enum import Enum
from typing import Tuple
from pydantic import BaseModel
from .session_models import StudentSession
from .session_manager import SessionManager

class StudentState(Enum):
    LESSON_DELIVERY = "lesson_delivery"
    EVALUATION      = "evaluation"
    REMEDIATION     = "remediation"
    OUT_OF_BOUNDS   = "out_of_bounds"

class FSMOrchestrator:
    """Manages the state transitions and workflow routing for student interaction paths."""
    
    def __init__(self, session_manager: SessionManager):
        self.sm = session_manager

    def process_turn(self, session_id: str, student_input: str, mock_signal: str) -> Tuple[StudentSession, str]:
        """Processes a single conversational turn through the FSM routing logic.
        
        Args:
            session_id: The unique ID of the student session.
            student_input: The raw string text from the user.
            mock_signal: Simulated agent routing decision ('pass', 'fail', 'derail').
        """
        # 1. Pull the session from our Milestone 2 database
        session = self.sm.load_session(session_id)
        if not session:
            raise ValueError(f"Session '{session_id}' not found in registry.")

        # 2. Append the conversation history for context
        session.chat_history.append({"role": "user", "content": student_input})

        # 3. Read current location state (default to LESSON_DELIVERY if not explicit)
        current_state = session.current_lesson_id

        # 4. Process routing logic transitions
        system_response = ""
        
        if mock_signal == "derail":
            # 🚨 PATH 3: Out of Bounds Guardrail
            # The state remains exactly where it was; we do not advance or loop.
            system_response = "Let's stay focused on our computer science lab goals! What questions do you have about the lesson?"
            
        elif mock_signal == "fail":
            # 🔄 PATH 2: Remediation Loop
            session.metrics.attempts_count += 1
            session.current_lesson_id = StudentState.REMEDIATION.value
            
            # Record the conceptual bottleneck if any
            if "concept" not in session.metrics.flagged_concepts:
                session.metrics.flagged_concepts.append("loops_logic")
                
            system_response = f"That code doesn't look quite right (Attempt #{session.metrics.attempts_count}). Let's look closer at the logic. Here is a helpful hint..."
            
        elif mock_signal == "pass":
            # 🎯 PATH 1: The Linear Success Path
            session.metrics.completed_lessons.append(current_state)
            session.metrics.attempts_count = 0  # Reset for next unit
            
            # Advance to the next lesson node identifier
            session.current_lesson_id = StudentState.LESSON_DELIVERY.value
            system_response = "Sensational work! Your solution compiled perfectly. Moving on to the next concept!"

        # 5. Commit state changes securely back down to our local JSON layer
        self.sm.save_session(session)
        
        return session, system_response