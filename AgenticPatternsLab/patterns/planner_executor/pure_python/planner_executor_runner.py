# patterns/planner_executor/pure_python/planner_executor_runner.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict

from .student_fsm import StudentFSM, FSMContext, StudentState
from .planner_agent import PlannerAgent
from .executor_agent import ExecutorAgent

@dataclass
class PlannerExecutorResult:
    """Unified result matching your architectural engine contracts."""
    final_answer: str
    trace: dict

class PlannerExecutorRunner:
    """
    The orchestrator coordinating Layer 1 (FSM), Layer 2 (Planner), 
    and Layer 3 (Executor) into a unified sprint cycle.
    """
    def __init__(self, runner: Any):
        self.runner = runner
        self.planner = PlannerAgent(runner=self.runner)
        self.executor = ExecutorAgent(runner=self.runner)

    def run(self, current_lesson: str, student_input: str) -> PlannerExecutorResult:
        """Runs the multi-layered planner-executor pipeline."""
        
        # 1. Initialize Context and High-Level State Management (Layer 1)
        context = FSMContext(
            current_state=StudentState.STUDENT_INPUT,
            current_lesson=current_lesson,
            student_response=student_input
        )
        fsm = StudentFSM(context=context)
        
        # Transition to Evaluation State
        fsm.transition("student_submitted", {"response": student_input})
        
        # 2. Generate Strategic Steps (Layer 2)
        plan = self.planner.generate_plan(
            current_lesson=context.current_lesson,
            student_state=context.current_state.name,
            student_input=student_input
        )
        
        execution_trace = {
            "lesson_goal": plan.lesson_goal,
            "steps_executed": []
        }
        
        last_step_output = student_input
        step_success = True

        # 3. Loop Through and Execute Tactical Steps (Layer 3)
        for step in plan.steps:
            # Execute step using the underlying ReAct / tool architecture
            step_result = self.executor.execute_step(
                tool_directive=step.tool_directive,
                context_data=last_step_output
            )
            
            execution_trace["steps_executed"].append({
                "step_id": step.step_id,
                "task": step.task,
                "directive": step.tool_directive,
                "result": step_result
            })
            
            last_step_output = step_result["final_answer"]
            
            # Educational fallback evaluation check
            if "fail" in last_step_output.lower() or "error" in last_step_output.lower():
                step_success = False

        # 4. Resolve Workflow State via FSM Evaluation
        final_state = fsm.transition("evaluation_complete", {"success": step_success})
        
        execution_trace["final_fsm_state"] = final_state.name
        execution_trace["fsm_history"] = context.history

        # Construct educational feedback baseline based on the target state
        if final_state == StudentState.COMPLETED:
            final_feedback = f"Evaluation Passed!\n\nConclusion:\n{last_step_output}"
        else:
            final_feedback = f"Remediation Required.\n\nAnalysis Summary:\n{last_step_output}"

        return PlannerExecutorResult(
            final_answer=final_feedback,
            trace=execution_trace
        )
    
# Append to the bottom of patterns/planner_executor/pure_python/planner_executor_runner.py
def run_planner_executor_pattern(provider_chain: Any, user_prompt: str = None) -> None:
    """
    Orchestrator entry point. Maps the platform's execution request 
    to the core PlannerExecutorRunner engine.
    """
    # 1. Fallback to a default computer science teaching problem if none provided
    prompt = user_prompt or "Can you review my loop? for i in range(10): print(i)"
    
    print(f"\n[Sprint Engine] Initializing PlannerExecutorRunner Bridge")
    print(f"[Sprint Engine] Student Submission Content: '{prompt}'\n")
    
    # 2. Instantiate and execute the layered pipeline
    # Note: We pass provider_chain as the underlying 'runner' contract
    orchestrator_engine = PlannerExecutorRunner(runner=provider_chain)
    result = orchestrator_engine.run(
        current_lesson="Intro to Python Loops", 
        student_input=prompt
    )
    
    # 3. Output results to CLI
    print("=" * 60)
    print("FINAL EDUCATIONAL RESPONSE")
    print("=" * 60)
    print(result.final_answer)
    print("=" * 60)
    print(f"Target FSM Resolve State: {result.trace.get('final_fsm_state')}")
    print("=" * 60)