from typing import Optional
from AgenticPatternsLab.providers.provider_manager import ProviderManager
from AgenticPatternsLab.utils.triage_agent import TriageAgent
from AgenticPatternsLab.utils.evaluation_agent import EvaluationAgent
from AgenticPatternsLab.utils.coaching_agent import CoachingAgent

def run_multi_agent_triage_pattern(provider_chain: ProviderManager, user_prompt: Optional[str] = None):
    """
    Executes the Milestone 4 Multi-Agent Triage FSM Pattern.
    Routes, evaluates, or coaches a student submission using specialized local-first agents.
    """
    print("\n========================================================")
    print("INITIALIZING MULTI-AGENT TRIAGE STATE MACHINE")
    print("========================================================\n")

    # 1. Initialize our trio of specialized agents with the resilient provider chain
    triage_agent = TriageAgent(provider_chain)
    evaluation_agent = EvaluationAgent(provider_chain)
    coaching_agent = CoachingAgent(provider_chain)

    # 2. Setup baseline assignment parameters
    assignment_prompt = "Write a Python loop that prints numbers from 1 to 5."
    
    # Use the CLI user_prompt if provided, otherwise default to a broken attempt to test the full loop
    student_submission = user_prompt if user_prompt else "for i in range(1, 5): print(i)"
    
    print(f"Assignment: '{assignment_prompt}'")
    print(f"Student Input: '{student_submission}'\n")

    # 3. Execute Finite State Machine Loop
    current_state = "START"
    execution_trace = []
    evaluation_feedback = ""

    while current_state not in ["SUCCESS", "DERAILED", "OUTPUT"]:
        execution_trace.append(current_state)
        print(f"State Transition -> [ {current_state} ]")

        if current_state == "START":
            # Step A: Audit input intent
            triage_res = triage_agent.analyze_input(student_submission)

            print(f"   [Agent A Triage] Intent: '{triage_res.intent}' | Reasoning: {triage_res.reasoning}")
            
            if triage_res.intent == "derail":
                current_state = "DERAILED"
                print("   Off-topic input detected. Routing to terminal containment.")
            elif triage_res.intent == "fail":
                current_state = "COACHING"
                evaluation_feedback = "Student explicitly requested instructional support or a hint."
                print("   Direct help requested. Routing straight to Pedagogical Coach.")
            else:
                current_state = "EVALUATION"
                print("   Valid attempt. Routing to Evaluation Grader.")

        elif current_state == "EVALUATION":
            # Step B: Grade execution logic
            eval_res = evaluation_agent.evaluate_submission(assignment_prompt, student_submission)
            print(f"   [Agent B Evaluator] Is Correct: {eval_res.is_correct}")
            print(f"   [Agent B Evaluator] Feedback: {eval_res.feedback}")
            
            if eval_res.is_correct:
                current_state = "SUCCESS"
            else:
                current_state = "COACHING"
                evaluation_feedback = eval_res.feedback
                print("   Logical error detected. Routing to Pedagogical Coach for scaffolding.")

        elif current_state == "COACHING":
            # Step C: Generate UDL scaffolded hint
            coach_res = coaching_agent.coach_student(assignment_prompt, student_submission, evaluation_feedback)
            current_state = "OUTPUT"
            print("\n [Agent C Pedagogical Coach Output]")
            print(f"   Strategic Hint:    {coach_res.conceptual_hint}")
            print(f"   Guiding Question:  {coach_res.guiding_question}")

    # Append terminal state to history trace
    execution_trace.append(current_state)
    print(f"\n State Machine Terminated -> [ {current_state} ]")
    print(f" Full FSM Execution Trace: {' -> '.join(execution_trace)}")
    print("========================================================\n")