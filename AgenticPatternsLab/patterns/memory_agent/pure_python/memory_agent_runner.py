# patterns/memory_agent/pure_python/memory_agent_runner.py

from __future__ import annotations
from dataclasses import dataclass

from ...react.pure_python.pure_python_runner import PurePythonReactRunner
from ...react.pure_python.fake_llm import FakeLLM


@dataclass
class RunnerResult:
    final_answer: str
    trace: dict


class MemoryAgentRunner:
    def __init__(self):
        self.runner = PurePythonReactRunner()
        self.llm = FakeLLM()

    def run(self, enriched_prompt: str) -> RunnerResult:
        final_answer = self.runner.run(enriched_prompt, llm=self.llm)
        return RunnerResult(final_answer=final_answer, trace={})