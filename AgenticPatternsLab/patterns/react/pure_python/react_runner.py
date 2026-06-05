from AgenticPatternsLab.utils.logging import create_logger, log_event
from .prompting import build_react_prompt
from AgenticPatternsLab.patterns.react.shared.react_engine import StrictReactEngine
from AgenticPatternsLab.patterns.react.shared.tool_registry import ToolRegistry


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

        self.registry = ToolRegistry()

        self.engine = StrictReactEngine(
            llm_callback=self.ask_llm_for_step,
            tool_callback=lambda tool, query: self.registry.call(tool, query),
            max_steps=self.max_steps
        )

    def build_initial_prompt(self, user_prompt: str) -> str:
        return build_react_prompt(user_prompt)

    def ask_llm_for_step(self, prompt: str) -> str:
        return self.provider_chain.generate(prompt)

    def run(self, user_prompt: str) -> str:
        initial_prompt = self.build_initial_prompt(user_prompt)
        return self.engine.run(initial_prompt)