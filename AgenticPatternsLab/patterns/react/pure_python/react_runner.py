from AgenticPatternsLab.utils.logging import create_logger, log_event
from .prompting import build_react_prompt

# ------------------------------------------------------------
# Tool Simulation (kept exactly as-is)
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
# NEW: Import the shared strict engine
# ------------------------------------------------------------
from AgenticPatternsLab.patterns.react.shared.react_engine import StrictReactEngine


# ------------------------------------------------------------
# Pure-Python ReAct Runner (thin adapter)
# ------------------------------------------------------------
class PurePythonReactRunner:
    """
    Thin adapter that delegates all strict ReAct logic to StrictReactEngine.
    """

    def __init__(self, provider_chain, max_steps=10):
        self.provider_chain = provider_chain
        self.max_steps = max_steps

        self.engine = StrictReactEngine(
            llm_callback=self.ask_llm_for_step,
            tool_callback=lambda tool, query: simulate_search_tool(query),
            max_steps=self.max_steps
        )

    def build_initial_prompt(self, user_prompt: str) -> str:
        return build_react_prompt(user_prompt)

    def ask_llm_for_step(self, prompt: str) -> str:
        return self.provider_chain.generate(prompt)

    def run(self, user_prompt: str) -> str:
        initial_prompt = self.build_initial_prompt(user_prompt)
        return self.engine.run(initial_prompt)