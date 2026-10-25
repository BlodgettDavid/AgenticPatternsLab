import time
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

class HumanSignal(BaseModel):
    """Encapsulates the human operator's administrative intervention payload."""
    decision: Optional[str] = Field(None, description="Must be either 'APPROVE' or 'REJECT' if processed.")
    notes: Optional[str] = Field(None, description="Optional annotations left by the instructor or administrator.")
    processed_at: Optional[float] = Field(None, description="Epoch timestamp marking when the human signal was captured.")

class StateSnapshot(BaseModel):
    """The data contract for serializing and rehydrating an entire FSM workflow execution."""
    session_id: str = Field(..., description="Unique UUID identifier for the tracking session.")
    current_state: str = Field("PENDING_HUMAN_APPROVAL", description="The exact FSM state token where execution was frozen.")
    frozen_at: float = Field(default_factory=time.time, description="Epoch timestamp marking when the state dropped to disk.")
    
    # Context Boundary Payload
    assignment: str = Field(..., description="The original task rules or lesson context.")
    student_input: str = Field(..., description="The unverified payload text submitted by the student.")
    
    # Multi-Agent Execution History
    execution_trace: List[str] = Field(default_factory=list, description="The sequence of FSM state transitions up to the pause.")
    agent_reasoning: Dict[str, Any] = Field(default_factory=dict, description="Captured intermediate structured data from specialized agents.")
    
    # Asynchronous Human Intervention Gateway
    human_intervention: HumanSignal = Field(default_factory=HumanSignal, description="Holds the external human override metadata.")