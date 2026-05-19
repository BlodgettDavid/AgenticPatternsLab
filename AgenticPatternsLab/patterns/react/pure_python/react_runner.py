from AgenticPatternsLab.utils.logging import create_logger, log_event
from .abstract_pattern_runner import PatternRunner
from .prompting import build_react_prompt
import re

# ------------------------------------------------------------
# Strict Action Regex (shared with tests)
# ------------------------------------------------------------
ACTION_RE = re.compile(
    r"^Action:\s*([a-zA-Z_][a-zA-Z0-9_]*)\('([^'\n]+)'\)$"
)

# ------------------------------------------------------------
# Tool Simulation
# ------------------------------------------------------------
def simulate_search_tool(query: str) -> str:
    query = query.lower()

    if "author of dune" in query:
        return "Frank Herbert wrote Dune."

    if "capital of france" in query or "france capital" in query:
        return "Paris."

    if "population of seattle" in query:
        return "Seattle has a population of about 750,000."

    return "No relevant information found."


# ------------------------------------------------------------
# Pure-Python ReAct Runner (strict engine)
# ------------------------------------------------------------
class PurePythonReactRunner(PatternRunner):
    """
    Pure-Python implementation of the ReAct pattern.
    Strict mode: exactly one Thought, at most one Action or Final Answer,
    no mixing, no malformed actions, no extra text.
    """

    def build_initial_prompt(self, user_prompt: str) -> str:
        return build_react_prompt(user_prompt)

    def ask_llm_for_step(self, prompt: str) -> str:
        return self.provider_chain.generate(prompt)

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

                # Use shared strict regex
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

    def execute_action(self, action: str) -> str:
        """
        Execute search('query') using simulate_search_tool.
        Other tools parse correctly but are not executable.
        """
        # Reconstruct full Action: ... line for regex matching
        match = ACTION_RE.match(f"Action: {action}")
        if not match:
            raise ValueError(f"Malformed action: {action}")

        tool = match.group(1)
        query = match.group(2)

        if tool != "search":
            raise ValueError(f"Unknown tool: {tool}")

        return simulate_search_tool(query)

    def is_done(self, parsed: dict) -> bool:
        return parsed.get("final_answer") is not None

    def collect_results(self, parsed: dict) -> str:
        return parsed["final_answer"]


# ------------------------------------------------------------
# Legacy procedural runner (deprecated)
# ------------------------------------------------------------
def run_react_pattern(provider_chain, user_prompt: str = "What is the capital of France?"):
    """
    Deprecated: replaced by PurePythonReactRunner.run()
    """
    print(f"Running React pattern using Pure Python provider chain: {provider_chain}")

    log_path = create_logger(prefix="react_pure_python")
    log_event(log_path, "start", f"provider_chain={provider_chain}, prompt={user_prompt}")

    prompt = build_react_prompt(user_prompt)
    log_event(log_path, "prompt", prompt)

    MAX_STEPS = 10
    steps = 0

    while steps < MAX_STEPS:
        steps += 1
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
