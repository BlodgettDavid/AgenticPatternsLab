"""
Deterministic Mock Provider for the Agentic Patterns Lab.

This provider returns predictable, canned responses for testing
the ReAct loop, fallback behavior, and orchestrator correctness.
"""

"""
Deterministic Mock Provider for the Agentic Patterns Lab.
"""

import time


class MockLLM:
    def __init__(self):
        self.name = "mock"
        self.max_retries = 2
        self.initial_backoff = 0.5
        self.backoff_factor = 2

    def generate(self, prompt: str) -> str:
        backoff = self.initial_backoff

        for attempt in range(self.max_retries + 1):
            try:
                return "mock response"
            except Exception:
                time.sleep(backoff)
                backoff *= self.backoff_factor

        return "mock response"
