"""
utils/session_models.py

Defines the core data structures for message turns, performance metrics,
and session state tracking using Pydantic for validation and serialization.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class PerformanceMetrics(BaseModel):
    """Tracks lesson engagement and bottlenecks to drive FSM branch logic."""
    attempts_count: int = Field(default=0, description="Number of attempts on the current lesson step.")
    completed_lessons: List[str] = Field(default_factory=list, description="List of lesson IDs successfully passed.")
    flagged_concepts: List[str] = Field(default_factory=list, description="Concepts where weakness was shown.")
    last_interaction: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}


class Message(BaseModel):
    """Represents a single conversational turn or execution step."""
    role: str = Field(..., description="'user', 'assistant', 'system', or 'tool'")
    content: str = Field(..., description="Text content of the message")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    name: Optional[str] = Field(default=None, description="Tool or agent name if applicable")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional context or metrics")

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}


class SessionState(BaseModel):
    """The master state model representing session tracking and FSM synchronization."""
    session_id: str = Field(..., description="Unique identifier for the session.")
    fsm_state: str = Field(default="IDLE", description="Tracks current control flow phase from FSM Engine.")
    is_active: bool = Field(default=True, description="Tracks whether the session is currently live.")
    
    # Nested behavioral state & metrics
    metrics: PerformanceMetrics = Field(default_factory=PerformanceMetrics)
    
    # Structured conversation thread
    messages: List[Message] = Field(default_factory=list, description="Thread memory for agent context.")
    variables: Dict[str, Any] = Field(default_factory=dict, description="Scratchpad for workflow variables.")
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def add_message(self, role: str, content: str, name: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> Message:
        """Helper to append a new message turn and update the timestamp."""
        msg = Message(role=role, content=content, name=name, metadata=metadata or {})
        self.messages.append(msg)
        self.updated_at = datetime.now(timezone.utc)
        return msg

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}