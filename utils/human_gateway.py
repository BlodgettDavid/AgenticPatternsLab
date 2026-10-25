import os
import json
import time
from AgenticPatternsLab.utils.state_snapshot import StateSnapshot, HumanSignal
from AgenticPatternsLab.utils.logging import get_snapshot_path  # Centralized path resolver

def run_human_gateway():
    print("\n========================================================")
    print("      ENTERPRISE HUMAN-IN-THE-LOOP INTERVENTION GATEWAY")
    print("========================================================\n")

    # Resolve our absolute, root-anchored runtime path contract
    snapshot_path = get_snapshot_path()

    if not os.path.exists(snapshot_path):
        print(f" Error: No frozen state snapshot found at '{snapshot_path}'.")
        print("Run a fresh multi-agent workflow that triggers an escalation first.")
        return

    # 1. Load the frozen snapshot
    with open(snapshot_path, "r") as f:
        snapshot_data = json.load(f)
    
    snapshot = StateSnapshot(**snapshot_data)
    
    print(f" FOUND FROZEN STATE SNAPSHOT [Session: {snapshot.session_id}]")
    print(f" Frozen At: {time.ctime(snapshot.frozen_at)}")
    print(f" Frozen State: [ {snapshot.current_state} ]")
    print(f" Trace History: {' -> '.join(snapshot.execution_trace)}")
    print("-" * 56)
    print(f" Assignment Context:\n   \"{snapshot.assignment}\"")
    print(f" Untrusted Student Submission:\n   \"{snapshot.student_input}\"")
    print("-" * 56)
    
    if "evaluation" in snapshot.agent_reasoning:
        print(" Automated Evaluator Insight:")
        print(f"   Feedback: {snapshot.agent_reasoning['evaluation'].get('feedback', 'No feedback provided.')}")
        print("-" * 56)

    # 2. Prompt human administrator for override decision
    print("Select Administrative Intervention Action:")
    print(" [1] APPROVE  - Override automated grader and force a PASS state.")
    print(" [2] REJECT   - Confirm logic failure and route to Pedagogical Coach.")
    
    choice = input("\nEnter option (1 or 2): ").strip()
    
    decision = "APPROVE" if choice == "1" else "REJECT"
    notes = input("\nEnter custom administrative notes or review feedback: ").strip()

    # 3. Inject human signal metadata into the snapshot contract
    snapshot.human_intervention = HumanSignal(
        decision=decision,
        notes=notes if notes else f"Manually processed as {decision} by administrator.",
        processed_at=time.time()
    )

    # 4. Save the snapshot back to disk in the managed .run/ directory
    with open(snapshot_path, "w") as f:
        json.dump(snapshot.model_dump(), f, indent=4)

    print(f"\n Human signal '{decision}' injected and saved successfully.")
    print("You can now resume the main orchestrator loop using the '--resume' flag.\n")
    print("========================================================\n")

if __name__ == "__main__":
    run_human_gateway()