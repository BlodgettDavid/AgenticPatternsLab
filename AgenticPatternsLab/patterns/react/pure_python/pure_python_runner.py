"""
Pure Python ReAct Runner
------------------------
This runner connects the shared ReactEngine to the provider_manager
without using LangChain or LlamaIndex.

It is the simplest, most transparent implementation of the ReAct loop.
"""

from AgenticPatternsLab.patterns.react.shared.tool_registry import ToolRegistry


from AgenticPatternsLab.patterns.react.shared.react_engine import (
    ReactEngine,
    EngineState,
)
from AgenticPatternsLab.providers.provider_manager import provider_manager



class PurePythonReactRunner:

    def __init__(self, model="gpt-4o-mini"):
        self.tool_registry = ToolRegistry().tools
        self.engine = ReactEngine(self.tool_registry)
        self.model = model
  
    
    # ------------------------------------------------------------
    # Prompt Formatting
    # ------------------------------------------------------------

    def build_prompt(self, state: EngineState, user_input: str) -> str:
        """
        Minimal prompt format for pure Python runner.
        Framework-specific runners can override this.
        """
        history = ""

        for step in state.steps:
            if step.thought:
                history += f"Thought: {step.thought.text}\n"
            if step.action:
                history += f"Action: {step.action.tool}[{step.action.input}]\n"
            if step.observation:
                history += f"Observation: {step.observation.text}\n"

        return (
            "You are a ReAct agent.\n"
            "Use Thought/Action/Observation steps.\n"
            "Finish with FinalAnswer.\n\n"
            f"User: {user_input}\n\n"
            f"{history}"
            "Thought:"
        )

    def step(self, state: EngineState, user_input: str, llm) -> dict:
        prompt = self.build_prompt(state, user_input)
        model_output = llm.generate(prompt)

        step_result = self.engine.step(state, model_output)

        return {
            "thought": step_result.thought.text if step_result.thought else None,
            "action": (
                f"{step_result.action.tool}[{step_result.action.input}]"
                if step_result.action
                else None
            ),
            "observation": (
                step_result.observation.text if step_result.observation else None
            ),
            "done": step_result.done,
            "raw_model_output": step_result.raw_model_output,
        }
    

    # ------------------------------------------------------------
    # Full Loop
    # ------------------------------------------------------------

    def run(self, user_input: str, llm, max_steps: int = 12) -> str:
        state = EngineState(max_steps=max_steps)

        while not self.engine.is_finished(state):
            result = self.step(state, user_input, llm)

            if result["done"]:
                return result["observation"]

        return "Error: Reached max steps without FinalAnswer."