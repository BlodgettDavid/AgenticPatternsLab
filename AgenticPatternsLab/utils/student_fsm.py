from enum import Enum
from typing import Tuple
from .session_models import StudentSession
from .session_manager import SessionManager
from .triage_agent import TriageAgent  


class StudentState(Enum):
    LESSON_DELIVERY        = "lesson_delivery"
    EVALUATION             = "evaluation"
    REMEDIATION            = "remediation"
    OUT_OF_BOUNDS          = "out_of_bounds"
    PENDING_HUMAN_APPROVAL = "pending_human_approval"  # The new asynchronous SaaS state


class FSMOrchestrator:
    """Manages the state transitions and workflow routing for student interaction paths."""
    
    def __init__(self, session_manager: SessionManager, triage_agent: TriageAgent):
        self.sm = session_manager
        self.triage = triage_agent

    def process_turn(self, session_id: str, student_input: str) -> Tuple[StudentSession, str]:
        """Processes a single conversational turn through the automated FSM routing logic.
        
        Args:
            session_id: The unique ID of the student session.
            student_input: The raw string text from the user.
        """
        # 1. Pull the session from our database layer
        session = self.sm.load_session(session_id)
        if not session:
            raise ValueError(f"Session '{session_id}' not found in registry.")

        # 2. Append the conversation history for context
        session.chat_history.append({"role": "user", "content": student_input})

        # 3. Read current location state
        current_state = session.current_lesson_id

        # If the state was explicitly frozen pending human review, handle it cleanly
        if current_state == StudentState.PENDING_HUMAN_APPROVAL.value:
            system_response = "This session is currently locked pending administrative or instructor review."
            return session, system_response

        # 4. Use the Triage Agent to automatically discover student intent
        triage_decision = self.triage.analyze_input(student_input)
        signal = triage_decision.intent
        
        # 5. Process routing logic transitions based on automated signal
        system_response = ""
        
        if signal == "derail":
            # PATH 3: Out of Bounds Guardrail
            system_response = "Let's stay focused on our computer science lab goals! What questions do you have about the lesson?"
            
        elif signal == "fail":
            # PATH 2: Remediation Loop
            session.metrics.attempts_count += 1
            session.current_lesson_id = StudentState.REMEDIATION.value
            
            if "loops_logic" not in session.metrics.flagged_concepts:
                session.metrics.flagged_concepts.append("loops_logic")
                
            system_response = f"That code doesn't look quite right (Attempt #{session.metrics.attempts_count}). Let's look closer at the logic. Here is a helpful hint..."
            
        elif signal == "pass":
            # PATH 1: The Linear Success Path
            session.metrics.completed_lessons.append(current_state)
            session.metrics.attempts_count = 0
            
            session.current_lesson_id = StudentState.LESSON_DELIVERY.value
            system_response = "Sensational work! Your solution compiled perfectly. Moving on to the next concept!"
            
        elif signal == "escalate":
            # NEW PATH: Escalating to the Human-in-the-Loop Gateway
            session.current_lesson_id = StudentState.PENDING_HUMAN_APPROVAL.value
            system_response = "Your submission requires an expert review. The system state has been serialized and paused."

        # 6. Commit state changes securely back down to our local JSON layer
        self.sm.save_session(session)
        
        return session, system_response