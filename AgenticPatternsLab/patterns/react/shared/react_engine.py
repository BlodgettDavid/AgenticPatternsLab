"""
Shared ReAct Engine
-------------------
This engine implements the core ReAct loop in a framework-agnostic way.

Framework-specific runners (pure_python, LangChain, LlamaIndex) will:
- format prompts
- call provider_manager.generate()
- parse actions
- call engine.step()
- handle tool execution
- return observations back into the loop

The engine itself:
- maintains state
- logs transitions
- enforces loop rules
- provides a clean API for runners
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Callable
import uuid
import time


# ------------------------------------------------------------
# State Models
# ------------------------------------------------------------

@dataclass
class Thought:
    text: str
    timestamp: float = field(default_factory=time.time)


@dataclass
class Action:
    tool: str
    input: str
    timestamp: float = field(default_factory=time.time)


@dataclass
class Observation:
    text: str
    timestamp: float = field(default_factory=time.time)


@dataclass
class StepResult:
    """Returned by engine.step()"""
    thought: Optional[Thought]
    action: Optional[Action]
    observation: Optional[Observation]
    done: bool
    raw_model_output: str


@dataclass
class EngineState:
    """Tracks the entire loop state."""
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    steps: List[StepResult] = field(default_factory=list)
    max_steps: int = 12
    finished: bool = False

    def add_step(self, step: StepResult):
        self.steps.append(step)
        if step.done:
            self.finished = True

    @property
    def last_observation(self) -> Optional[str]:
        if not self.steps:
            return None
        obs = self.steps[-1].observation
        return obs.text if obs else None


# ------------------------------------------------------------
# Shared Engine
# ------------------------------------------------------------

class ReactEngine:
    """
    Framework-agnostic ReAct engine.

    Responsibilities:
    - Maintain loop state
    - Accept model output from runners
    - Parse Thought / Action / FinalAnswer
    - Execute tools (via callback)
    - Produce StepResult objects
    """

    def __init__(self, tool_registry: Dict[str, Callable[[str], str]]):
        """
        tool_registry: { tool_name: callable(input_str) -> output_str }
        """
        self.tool_registry = tool_registry

    # ------------------------------------------------------------
    # Parsing
    # ------------------------------------------------------------

    def parse_model_output(self, text: str) -> Dict[str, Any]:
        """
        Minimal parser for:
        Thought: ...
        Action: tool_name[input]
        FinalAnswer: ...
        """
        lines = text.strip().splitlines()
        thought = None
        action = None
        final = None

        for line in lines:
            line = line.strip()

            if line.startswith("Thought:"):
                thought = line[len("Thought:"):].strip()

            elif line.startswith("Action:"):
                # Example: Action: search["weather in seattle"]
                raw = line[len("Action:"):].strip()
                tool, _, rest = raw.partition("[")
                tool = tool.strip()
                input_str = rest.rstrip("]").strip()
                action = (tool, input_str)

            elif line.startswith("FinalAnswer:"):
                final = line[len("FinalAnswer:"):].strip()

        return {
            "thought": thought,
            "action": action,
            "final": final,
        }

    # ------------------------------------------------------------
    # Tool Execution
    # ------------------------------------------------------------

    def execute_action(self, tool: str, input_str: str) -> str:
        if tool not in self.tool_registry:
            return f"Error: Unknown tool '{tool}'"

        try:
            return self.tool_registry[tool](input_str)
        except Exception as e:
            return f"Tool '{tool}' failed: {e}"

    # ------------------------------------------------------------
    # Main Step
    # ------------------------------------------------------------

    def step(self, state: EngineState, model_output: str) -> StepResult:
        """
        Called by framework-specific runners after provider_manager.generate().
        """
        parsed = self.parse_model_output(model_output)

        thought = Thought(parsed["thought"]) if parsed["thought"] else None
        action_obj = None
        observation_obj = None
        done = False

        # Final Answer
        if parsed["final"]:
            observation_obj = Observation(parsed["final"])
            done = True

        # Action
        elif parsed["action"]:
            tool, input_str = parsed["action"]
            result = self.execute_action(tool, input_str)
            action_obj = Action(tool=tool, input=input_str)
            observation_obj = Observation(result)

        step_result = StepResult(
            thought=thought,
            action=action_obj,
            observation=observation_obj,
            done=done,
            raw_model_output=model_output,
        )

        state.add_step(step_result)
        return step_result

    # ------------------------------------------------------------
    # Loop Control
    # ------------------------------------------------------------
    def is_finished(self, state: EngineState) -> bool:
        return state.finished or len(state.steps) >= state.max_steps
