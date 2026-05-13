import re

THOUGHT_RE = re.compile(r"Thought:\s*(.*)")


#ACTION_RE = re.compile(
#    r"Action:\s*(\w+)\(['\"]([^'\"]+)['\"]\)"
#)
#ACTION_RE = re.compile(
#    r"Action:\s*([a-zA-Z_]+)\('([^']+)'\)"
#)
ACTION_RE = re.compile(
    r"^Action:\s*([a-zA-Z_]+)\('([^']+)'\)$",
    re.MULTILINE
)
FINAL_RE = re.compile(r"Final\s*Answer:\s*(.*)")


def parse_llm_output(llm_output: str) -> dict:
    if not isinstance(llm_output, str):
        raise ValueError("FORMAT ERROR: LLM output must be a string.")

    llm_output = llm_output.strip()

    # --- FinalAnswer handling ---
    final_match = FINAL_RE.search(llm_output)
    if final_match:
        # FinalAnswer cannot appear with an Action
        if ACTION_RE.search(llm_output):
            raise ValueError("FORMAT ERROR: FinalAnswer cannot appear with Action.")
        return {
            "thought": None,
            "action": None,
            "final_answer": final_match.group(1).strip()
        }

    # --- Thought handling ---
    thought_match = THOUGHT_RE.search(llm_output)
    if not thought_match:
        raise ValueError("FORMAT ERROR: Missing Thought.")
    thought = thought_match.group(1).strip()

    # --- Action handling ---
    actions = re.findall(r"^Action:", llm_output, re.MULTILINE)
    if len(actions) > 1:
        raise ValueError("FORMAT ERROR: Multiple Actions not allowed.")

    action_match = ACTION_RE.search(llm_output)
    if not action_match:
        raise ValueError("FORMAT ERROR: Missing Action.")
    tool = action_match.group(1).strip()
    arg = action_match.group(2).strip()

    return {
        "thought": thought,
        "action": f"{tool}('{arg}')",
        "final_answer": None
    }


def execute_action(action: str) -> str:
    match = ACTION_RE.match(f"Action: {action}")
    if not match:
        raise ValueError("FORMAT ERROR: Malformed action.")
    tool = match.group(1)
    arg = match.group(2)
    if tool == "search":
        return f"Search results for '{arg}'"
    if tool == "lookup":
        return f"Lookup result for '{arg}'"
    raise ValueError(f"FORMAT ERROR: Unknown tool '{tool}'.")

class StrictReactRunner:
    def __init__(self, llm, max_steps: int = 10):
        self.llm = llm
        self.max_steps = max_steps

    def build_prompt(self, user_query: str, transcript: list[str]) -> str:
        history = "\n".join(transcript)
        return (
            "You are a strict ReAct agent.\n"
            "Use Thought/Action/Observation steps.\n"
            "Finish with FinalAnswer.\n\n"
            f"User: {user_query}\n\n"
            f"{history}\n"
            "Thought:"
        )

    def run(self, user_query: str) -> str:
        transcript = []
        for _ in range(self.max_steps):
            prompt = self.build_prompt(user_query, transcript)
            llm_output = self.llm.generate(prompt)
            parsed = parse_llm_output(llm_output)
            if parsed["final_answer"] is not None:
                return parsed["final_answer"]
            observation = execute_action(parsed["action"])
            transcript.append(f"Thought: {parsed['thought']}\nAction: {parsed['action']}\nObservation: {observation}")
        raise RuntimeError("Max steps reached without producing a final answer.")