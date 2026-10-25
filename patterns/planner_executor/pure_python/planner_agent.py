# patterns/planner_executor/pure_python/planner_agent.py
from __future__ import annotations
import json
from typing import Any, Dict, List
from dataclasses import dataclass

@dataclass
class PlanStep:
    step_id: int
    task: str
    tool_directive: str  # Direct instruction for the Executor

@dataclass
class ExecutionPlan:
    lesson_goal: str
    steps: List[PlanStep]

class PlannerAgent:
    """
    Layer 2: The Strategic Engine.
    Generates structured, deterministic JSON plans based on student context.
    """
    def __init__(self, runner: Any):
        self.runner = runner

    def generate_plan(self, current_lesson: str, student_state: str, student_input: str = "") -> ExecutionPlan:
        """Instructs the LLM to output a raw JSON plan matching our schema."""
        
        system_prompt = (
            "You are an expert curriculum planner. Your sole job is to output a raw JSON plan "
            "to evaluate or assist a student. You must NOT output any introductory text or markdown formatting. "
            "Respond strictly with a valid JSON object matching this schema:\n"
            "{\n"
            '  "lesson_goal": "string description",\n'
            '  "steps": [\n'
            '    {"step_id": 1, "task": "description", "tool_directive": "explicit instruction for executor"}\n'
            '  ]\n'
            "}"
        )

        user_prompt = f"""
        Current Lesson: {current_lesson}
        Student FSM State: {student_state}
        Latest Student Input: {student_input}
        
        Generate an execution sequence for this scenario.
        """

        combined_prompt = f"{system_prompt}\n\nUser Scenario:\n{user_prompt}"
        result = self.runner.run(combined_prompt, tools={})
        
        raw_content = result.final_answer.strip().lstrip("```json").rstrip("```").strip()
        return self._parse_json_to_plan(raw_content)

    def _parse_json_to_plan(self, raw_json: str) -> ExecutionPlan:
        """Parses the raw text into type-safe dataclasses."""
        try:
            data = json.loads(raw_json)
            steps = [
                PlanStep(
                    step_id=step.get("step_id"),
                    task=step.get("task"),
                    tool_directive=step.get("tool_directive")
                )
                for step in data.get("steps", [])
            ]
            return ExecutionPlan(lesson_goal=data.get("lesson_goal", ""), steps=steps)
        except Exception as e:
            return ExecutionPlan(
                lesson_goal="Fallback evaluation due to parsing error",
                steps=[PlanStep(step_id=1, task="Evaluate code structure manually", tool_directive="Review student_input for basic validation")]
            )