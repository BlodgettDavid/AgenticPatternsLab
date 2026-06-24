# patterns/planner_executor/pure_python/student_fsm.py
from enum import Enum, auto
from typing import Dict, Any, Optional
from dataclasses import dataclass, field

class StudentState(Enum):
    LESSON_DELIVERY = auto()
    STUDENT_INPUT = auto()
    EVALUATION = auto()
    REVIEW_REMEDIATION = auto()
    COMPLETED = auto()

@dataclass
class FSMContext:
    """Carries the active state, student history, and execution logs."""
    current_state: StudentState = StudentState.LESSON_DELIVERY
    current_lesson: str = "Intro to Python Loops"
    student_response: Optional[str] = None
    execution_success: bool = True
    history: list = field(default_factory=list)

class StudentFSM:
    """Layer 1: FSM managing high-level student learning transitions."""
    
    def __init__(self, context: Optional[FSMContext] = None):
        self.context = context or FSMContext()

    def transition(self, event: str, payload: Dict[str, Any]) -> StudentState:
        """
        State transition logic.
        Validates event triggers and moves the context to the next state.
        """
        old_state = self.context.current_state
        
        if old_state == StudentState.LESSON_DELIVERY:
            if event == "lesson_presented":
                self.context.current_state = StudentState.STUDENT_INPUT
                
        elif old_state == StudentState.STUDENT_INPUT:
            if event == "student_submitted":
                self.context.student_response = payload.get("response")
                self.context.current_state = StudentState.EVALUATION
                
        elif old_state == StudentState.EVALUATION:
            if event == "evaluation_complete":
                self.context.execution_success = payload.get("success", False)
                if self.context.execution_success:
                    self.context.current_state = StudentState.COMPLETED
                else:
                    self.context.current_state = StudentState.REVIEW_REMEDIATION
                    
        elif old_state == StudentState.REVIEW_REMEDIATION:
            if event == "remediation_delivered":
                self.context.current_state = StudentState.STUDENT_INPUT

        self.context.history.append({
            "from": old_state.name,
            "to": self.context.current_state.name,
            "event": event
        })
        return self.context.current_state