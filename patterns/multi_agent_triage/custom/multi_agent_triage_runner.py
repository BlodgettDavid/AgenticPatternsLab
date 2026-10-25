import os
import json
import uuid
from typing import Optional
from providers.provider_manager import ProviderManager
from utils.triage_agent import TriageAgent
from utils.evaluation_agent import EvaluationAgent
from utils.coaching_agent import CoachingAgent
from utils.state_snapshot import StateSnapshot
from utils.logging import get_snapshot_path


def run_multi_agent_triage_pattern(provider_chain: ProviderManager, user_prompt: Optional[str] = None, resume: bool = False):
    """
    Executes the Milestone 5 Asynchronous Multi-Agent Triage Pattern with HITL Gateway.
    Can cleanly freeze state to disk or re-hydrate an execution snapshot to resume workflows.
    """
    print("\n========================================================")
    print("INITIALIZING ASYNCHRONOUS MULTI-AGENT STATE MACHINE")
    print("========================================================\n")

    # Resolve our absolute, root-anchored runtime path contract
    snapshot_path = get_snapshot_path() 

    # 1. Initialize our trio of specialized agents
    triage_agent = TriageAgent(provider_chain)
    evaluation_agent = EvaluationAgent(provider_chain)
    coaching_agent = CoachingAgent(provider_chain)

    # 2. Setup baseline state control variables
    assignment_prompt = "Write a Python loop that prints numbers from 1 to 5."
    execution_trace = []
    evaluation_feedback = ""
    agent_reasoning_log = {}

    # Check if we are resuming an existing frozen state snapshot from our dedicated .run/ directory
    if resume and os.path.exists(snapshot_path):
        print(f" Resuming from state snapshot: {snapshot_path}...")
        with open(snapshot_path, "r") as f:
            snapshot_data = json.load(f)
            snapshot = StateSnapshot(**snapshot_data)
        
        # Hydrate the pipeline context completely from disk data
        student_submission = snapshot.student_input
        current_state = snapshot.current_state
        execution_trace = snapshot.execution_trace
        agent_reasoning_log = snapshot.agent_reasoning
        
        print(f"Loaded Snapshot Context. Current State: [ {current_state} ]")
        print(f"Human Decision Injected: '{snapshot.human_intervention.decision}'")
        
        # Process the human signal override path directly
        if snapshot.human_intervention.decision == "APPROVE":
            current_state = "SUCCESS"
            print(" Administrative Override: APPROVED. Routing directly to SUCCESS.")
        else:
            current_state = "COACHING"
            evaluation_feedback = snapshot.human_intervention.notes or "Rejected by administrative human audit."
            print(" Administrative Override: REJECTED. Routing to Pedagogical Coach.")
            
    else:
        # Default fresh run execution path
        student_submission = user_prompt if user_prompt else "for i in range(1, 5): print(i)"
        current_state = "START"
        print(f"Assignment: '{assignment_prompt}'")
        print(f"Student Input: '{student_submission}'\n")

    # 3. Finite State Machine Core Loop
    while current_state not in ["SUCCESS", "DERAILED", "OUTPUT", "PAUSED_FOR_REVIEW"]:
        execution_trace.append(current_state)
        print(f"State Transition -> [ {current_state} ]")

        if current_state == "START":
            triage_res = triage_agent.analyze_input(student_submission)
            agent_reasoning_log["triage"] = triage_res.model_dump()
            print(f"   [Agent A Triage] Intent: '{triage_res.intent}'")
            
            if triage_res.intent == "derail":
                current_state = "DERAILED"
            elif triage_res.intent == "fail":
                current_state = "COACHING"
                evaluation_feedback = "Student explicitly requested instructional support or a hint."
            else:
                current_state = "EVALUATION"

        elif current_state == "EVALUATION":
            eval_res = evaluation_agent.evaluate_submission(assignment_prompt, student_submission)
            agent_reasoning_log["evaluation"] = eval_res.model_dump()
            print(f"   [Agent B Evaluator] Is Correct: {eval_res.is_correct}")
            
            if eval_res.is_correct:
                current_state = "SUCCESS"
            else:
                # If the code is broken, check if it fits our structural edge-cases for review
                if "range" in student_submission:
                    current_state = "PAUSED_FOR_REVIEW"
                    evaluation_feedback = eval_res.feedback
                    print("\n [CRITICAL ESCALATION POINT TRIGGERED]")
                    print("Submission meets boundary edge-case rules. Freezing execution thread...")
                    
                    # Construct and serialize the Pydantic state model
                    snapshot = StateSnapshot(
                        session_id=str(uuid.uuid4()),
                        current_state="PENDING_HUMAN_APPROVAL",
                        assignment=assignment_prompt,
                        student_input=student_submission,
                        execution_trace=execution_trace,
                        agent_reasoning=agent_reasoning_log
                    )
                    
                    with open(snapshot_path, "w") as f:
                        json.dump(snapshot.model_dump(), f, indent=4)
                        
                    print(f" State trace successfully written to disk: {snapshot_path}")
                    print("Execution process safely terminated. Awaiting asynchronous human signal.\n")
                else:
                    current_state = "COACHING"
                    evaluation_feedback = eval_res.feedback

        elif current_state == "COACHING":
            coach_res = coaching_agent.coach_student(assignment_prompt, student_submission, evaluation_feedback)
            current_state = "OUTPUT"
            print("\n [Agent C Pedagogical Coach Output]")
            print(f"   Strategic Hint:    {coach_res.conceptual_hint}")
            print(f"   Guiding Question:  {coach_res.guiding_question}")

    # Append terminal or pause state to trace log string
    execution_trace.append(current_state)
    print(f"\n State Machine Run Concluded -> [ {current_state} ]")
    print(f" Full FSM Execution Trace: {' -> '.join(execution_trace)}")
    print("========================================================\n")

    # 4. Automated File Lifecycle Clean Teardown Policy
    if current_state in ["SUCCESS", "DERAILED", "OUTPUT"]:
        if os.path.exists(snapshot_path):
            os.remove(snapshot_path)
            print(f"[Lifecycle] Terminal state reached. Cleaned up snapshot from: {snapshot_path}\n")