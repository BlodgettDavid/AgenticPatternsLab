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

import re
ACTION_RE = re.compile(
    r"^Action:\s*([a-zA-Z_][a-zA-Z0-9_]*)\('([^'\n]+)'\)$"
)

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


# ------------------------------------------------------------
# Strict Shared ReAct Engine (new)
# ------------------------------------------------------------

class StrictReactEngine:
    """
    Framework-agnostic strict ReAct engine.
    This class will replace the older ReactEngine above.
    """

    def __init__(self, tool_registry, max_steps=10):
        self.tool_registry = tool_registry
        self.max_steps = max_steps
        self.steps = 0
        self.history = []

    # -----------------------------
    # Parsing (to be filled in)
    # -----------------------------
    def parse_llm_output(self, llm_output: str) -> dict:
        parsed = {
            "thought": None,
            "action": None,
            "final_answer": None,
        }

        lines = [line.rstrip() for line in llm_output.splitlines() if line.strip()]
        if not lines:
            raise ValueError("Empty LLM output.")

        # First line must be Thought
        if not lines[0].startswith("Thought:"):
            raise ValueError("LLM output must begin with 'Thought:'.")

        state = "thought"

        for line in lines:
            # -------------------------
            # Thought
            # -------------------------
            if line.startswith("Thought:"):
                if state != "thought":
                    raise ValueError("Thought may only appear once at the beginning.")
                if parsed["thought"] is not None:
                    raise ValueError("Multiple Thought lines are not allowed.")
                parsed["thought"] = line[len("Thought:"):].strip()
                state = "action_or_final"
                continue

            # -------------------------
            # Action
            # -------------------------
            if line.startswith("Action:"):
                if state != "action_or_final":
                    raise ValueError("Action in invalid position.")
                if parsed["action"] is not None:
                    raise ValueError("Multiple Actions are not allowed.")
                if parsed["final_answer"] is not None:
                    raise ValueError("Cannot have Action after Final Answer.")

                # Use strict regex
                match = ACTION_RE.match(line)
                if not match:
                    raise ValueError(f"Malformed action: {line}")

                tool_name = match.group(1)
                argument = match.group(2)
                parsed["action"] = f"{tool_name}('{argument}')"
                state = "done"
                continue

            # -------------------------
            # Final Answer
            # -------------------------
            if line.startswith("Final Answer:"):
                if state != "action_or_final":
                    raise ValueError("Final Answer in invalid position.")
                if parsed["final_answer"] is not None:
                    raise ValueError("Multiple Final Answer lines are not allowed.")
                if parsed["action"] is not None:
                    raise ValueError("Cannot have both Action and Final Answer.")

                parsed["final_answer"] = line[len("Final Answer:"):].strip()
                state = "done"
                continue

            # -------------------------
            # Anything else is illegal
            # -------------------------
            raise ValueError(f"Unexpected content in LLM output: {line}")

        # Final sanity check
        if parsed["action"] is None and parsed["final_answer"] is None:
            raise ValueError("LLM output contained no action and no final answer.")

        return parsed


    # -----------------------------
    # Tool execution (to be filled in)
    # -----------------------------
    def execute_action(self, action: str) -> str:
        # Reconstruct full Action: ... line for regex matching
        match = ACTION_RE.match(f"Action: {action}")
        if not match:
            raise ValueError(f"Malformed action: {action}")

        tool = match.group(1)
        query = match.group(2)

        if tool not in self.tool_registry:
            raise ValueError(f"Unknown tool: {tool}")

        return self.tool_registry[tool](query)

    # -----------------------------
    # Loop control (to be filled in)
    # -----------------------------
    def is_done(self, parsed: dict) -> bool:
        return parsed.get("final_answer") is not None

    # -----------------------------
    # Main loop (to be filled in)
    # -----------------------------
    def run(self, initial_prompt: str, ask_llm) -> str:
        prompt = initial_prompt

        while self.steps < self.max_steps:
            self.steps += 1

            llm_output = ask_llm(prompt)
            parsed = self.parse_llm_output(llm_output)

            self.history.append(parsed)

            if self.is_done(parsed):
                return parsed["final_answer"]

            if parsed.get("action"):
                observation = self.execute_action(parsed["action"])
                prompt = f"Observation: {observation}"
            else:
                raise RuntimeError("LLM output contained no action and no final answer.")

        raise RuntimeError("Max steps reached without producing a final answer.")