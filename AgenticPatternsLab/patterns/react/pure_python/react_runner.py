from AgenticPatternsLab.utils.logging import create_logger, log_event

def build_react_prompt(user_prompt: str) -> str:
    return (
        "You are an AI agent that MUST follow the ReAct (Reasoning + Acting) pattern.\n"
        "You MUST obey every rule below with ZERO exceptions.\n\n"
        "===========================\n"
        "REQUIRED OUTPUT FORMATS\n"
        "===========================\n\n"
        "CRITICAL TERMINATION RULE:\n"
        "If the Observation already contains the answer to the user’s question,\n"
        "you MUST immediately produce:\n\n"
        "Thought: I now know the answer.\n"
        "Final Answer: <the answer>\n\n"
        "You MUST NOT perform another Action after this condition is met.\n\n"
        "(1) When reasoning or deciding what to do next:\n"
        "Thought: <your reasoning>\n"
        "Action: search('<query>')\n\n"
        "(2) When you have enough information to answer:\n"
        "Thought: <your reasoning>\n"
        "Final Answer: <your answer>\n\n"
        "===========================\n"
        "STRICT, NON‑NEGOTIABLE RULES\n"
        "===========================\n\n"
        "- You MUST begin EVERY response with \"Thought:\".\n"
        "- You MUST include a Thought step before EVERY Action or Final Answer.\n"
        "- You MUST NOT output anything before \"Thought:\".\n"
        "- You MUST NOT output explanations, greetings, apologies, or commentary.\n"
        "- You MUST NOT invent tools. The ONLY tool you may use is: search(query).\n"
        "- Tool calls MUST be formatted EXACTLY like: search('some query')\n"
        "- After receiving an Observation, you MUST produce a NEW Thought.\n"
        "- You MUST NOT answer directly without using the required format.\n"
        "- You MUST NOT switch formats mid‑response.\n"
        "- You MUST NOT include multiple Actions in one response.\n"
        "- You MUST NOT include both Action AND Final Answer in the same response.\n"
        "- If you already know the answer, you MUST STILL follow the ReAct format.\n"
        "- If you violate ANY rule, you MUST output EXACTLY: FORMAT ERROR\n\n"
        "===========================\n"
        "FEW‑SHOT EXAMPLES (FOLLOW THESE EXACTLY)\n"
        "===========================\n\n"
        "Example 1:\n"
        "User: What is the capital of France?\n"
        "Assistant:\n"
        "Thought: I should verify the answer using the search tool.\n"
        "Action: search('capital of France')\n\n"
        "Example 2 (after Observation):\n"
        "Observation: Paris.\n"
        "Assistant:\n"
        "Thought: I now know the answer.\n"
        "Final Answer: Paris.\n\n"
        "===========================\n"
        "YOUR TASK\n"
        "===========================\n\n"
        "Follow the rules above EXACTLY.\n"
        "Never break character.\n"
        "Never change the required format.\n"
        "Never output anything except the required ReAct fields.\n\n"
        "Here is the user input:\n"
        f"{user_prompt}"
    )

def simulate_search_tool(query: str) -> str:
    query = query.lower()

    if "author of dune" in query:
        return "Frank Herbert wrote Dune."

    if "capital of france" in query or "france capital" in query:
        return "Paris."

    if "population of seattle" in query:
        return "Seattle has a population of about 750,000."

    return "No relevant information found."


def run_react_pattern(provider_chain, user_prompt: str = "What is the capital of France?"):
    print(f"Running React pattern using Pure Python provider chain: {provider_chain}")

    log_path = create_logger(prefix="react_pure_python")
    log_event(log_path, "start", f"provider_chain={provider_chain}, prompt={user_prompt}")

    prompt = build_react_prompt(user_prompt)
    log_event(log_path, "prompt", prompt)

    MAX_STEPS = 10
    steps = 0

    while steps < MAX_STEPS:
        steps += 1

        # *** ProviderManager call ***
        result = provider_chain.generate(prompt)

        if "FORMAT ERROR" in result:
            log_event(log_path, "format_error", result)
            print("Model violated format. Stopping.")
            break

        if not result.strip().startswith("Thought:"):
            log_event(log_path, "format_error", "Missing Thought")
            print("Model violated format (missing Thought). Stopping.")
            break

        print("\nLLM Output:")
        log_event(log_path, "raw_action_block", result)
        print(result)

        log_event(log_path, "llm_output", result)

        if "Final Answer:" in result:
            final = result.split("Final Answer:", 1)[1].strip()
            log_event(log_path, "final_answer", final)
            print(f"\nFinal Answer: {final}")
            break

        if "Action:" in result:
            action_line = result.split("Action:", 1)[1].strip().split("\n")[0].strip()

            if not action_line.startswith("search('") or not action_line.endswith("')"):
                log_event(log_path, "format_error", f"Malformed action: {action_line}")
                print("Malformed action. Stopping.")
                break

            log_event(log_path, "action", action_line)
            print(f"\nParsed Action: {action_line}")

            query = action_line[len("search('"):-2]

            observation = simulate_search_tool(query)
            log_event(log_path, "observation", observation)

            prompt = f"Observation: {observation}"
            log_event(log_path, "next_prompt", prompt)

        else:
            log_event(log_path, "error", "No action found")
            print("No action found. Stopping.")
            break

    if steps >= MAX_STEPS:
        print("Max iterations reached. Stopping.")
        log_event(log_path, "max_iterations", f"Reached {MAX_STEPS} steps")