"""
Base class for all pattern runners in the pure‑Python agentic system.

Every concrete pattern runner (ReAct, Plan‑and‑Execute, Debate, etc.)
must subclass PatternRunner and implement the abstract methods below.
"""

from abc import ABC, abstractmethod


class PatternRunner(ABC):
    """
    Abstract base class defining the interface for all pattern runners.
    The orchestrator will instantiate a concrete subclass and call run().
    """

    def __init__(self, provider_chain):
        """
        provider_chain: an object with a .generate(prompt) method
        (LLM provider abstraction)
        """
        self.provider_chain = provider_chain
        self.max_steps = 10
        self.steps = 0
        self.history = []  # optional: store Thought/Action/Observation blocks

    @abstractmethod
    def build_initial_prompt(self, user_prompt: str) -> str:
        """
        Construct the initial prompt for the LLM.
        Each pattern has its own prompt format.
        """
        pass

    @abstractmethod
    def ask_llm_for_step(self, prompt: str) -> str:
        """
        Call the LLM through provider_chain and return the raw output.
        """
        pass

    @abstractmethod
    def parse_llm_output(self, llm_output: str) -> dict:
        """
        Parse the LLM output into a structured dict, e.g.:

        {
            "thought": "...",
            "action": "search('query')" or None,
            "final_answer": "..." or None
        }
        """
        pass

    @abstractmethod
    def execute_action(self, action: str) -> str:
        """
        Execute the tool call (e.g., search('query')) and return an observation string.
        """
        pass

    @abstractmethod
    def is_done(self, parsed: dict) -> bool:
        """
        Return True if the pattern runner should stop (Final Answer reached).
        """
        pass

    @abstractmethod
    def collect_results(self, parsed: dict) -> str:
        """
        Extract the final answer from the parsed LLM output.
        """
        pass

    def run(self, user_prompt: str) -> str:
        """
        Main loop shared by all pattern runners.
        """
        prompt = self.build_initial_prompt(user_prompt)

        while self.steps < self.max_steps:
            self.steps += 1

            llm_output = self.ask_llm_for_step(prompt)
            parsed = self.parse_llm_output(llm_output)

            self.history.append(parsed)

            if self.is_done(parsed):
                return self.collect_results(parsed)

            if parsed.get("action"):
                observation = self.execute_action(parsed["action"])
                prompt = f"Observation: {observation}"
            else:
                raise RuntimeError("LLM output contained no action and no final answer.")

        raise RuntimeError("Max steps reached without producing a final answer.")
