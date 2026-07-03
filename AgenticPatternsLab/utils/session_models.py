from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime, timezone

class PerformanceMetrics(BaseModel):
    """Tracks lesson engagement and bottlenecks to drive FSM branch logic."""
    attempts_count: int = Field(default=0, description="Number of attempts on the current lesson step.")
    completed_lessons: List[str] = Field(default_factory=list, description="List of lesson IDs successfully passed.")
    flagged_concepts: List[str] = Field(default_factory=list, description="Concepts where the student showed weakness.")
    # 👇 Modernized timezone-aware UTC default factory
    last_interaction: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StudentSession(BaseModel):
    """The master state model representing the 'Student Registry' entry."""
    session_id: str = Field(..., description="Unique UUID or string identifying the student session.")
    student_name: str = Field(..., description="Display name of the student for personalized UX.")
    current_lesson_id: str = Field(default="intro_python_01", description="Current node ID in the FSM curriculum.")
    is_active: bool = Field(default=True, description="Tracks whether the session is currently live.")
    
    # Nested behavioral state tracking
    metrics: PerformanceMetrics = Field(default_factory=PerformanceMetrics)
    
    # Conversational Memory (Structure: [{"role": "user/assistant/system", "content": "..."}])
    chat_history: List[Dict[str, str]] = Field(default_factory=list, description="Thread memory for agent context.")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }