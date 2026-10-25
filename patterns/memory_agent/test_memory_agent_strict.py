# patterns/memory_agent/test_memory_agent_strict.py

from patterns.memory_agent.memory_agent import MemoryAgent
from patterns.memory_agent.memory_store_json import JSONMemoryStore
from patterns.memory_agent.memory_extractor import MemoryExtractor
from patterns.memory_agent.pure_python.memory_agent_runner import MemoryAgentRunner

import os


def test_memory_agent_strict_react():
    """
    Iteration 3:
    - StrictReactEngine must parse Thought/Action/Final Answer
    - Tools must be called
    - Trace must contain parsed steps
    - Memory must be written
    """

    # ---------------------------------------------------------
    # 1. Clean persistent store
    # ---------------------------------------------------------
    path = "test_memory_strict.json"
    if os.path.exists(path):
        os.remove(path)

    store = JSONMemoryStore(path=path)
    extractor = MemoryExtractor()

    # ---------------------------------------------------------
    # 2. Deterministic fake LLM for strict ReAct loop
    # ---------------------------------------------------------
    def fake_llm(prompt: str) -> str:
        """
        The engine will feed back:
            Observation: <tool output>

        So we branch on that.
        """
        if "Observation:" not in prompt:
            # First step → search memory
            return (
                "Thought: I should search memory.\n"
                "Action: search_memory('France')"
            )

        if "No relevant memory found" in prompt:
            # Second step → write memory
            return (
                "Thought: I should store the capital.\n"
                "Action: write_memory('Paris is the capital of France')"
            )

        if "Memory stored" in prompt:
            # Final step → produce final answer
            return (
                "Thought: I now know the answer.\n"
                "Final Answer: The capital of France is Paris."
            )

        # Safety fallback
        return "Thought: I am confused.\nFinal Answer: Unknown."

    runner = MemoryAgentRunner(llm=fake_llm)
    agent = MemoryAgent(runner, store, extractor)

    # ---------------------------------------------------------
    # 3. Run the agent
    # ---------------------------------------------------------
    result = agent.run("What is the capital of France?")

    # ---------------------------------------------------------
    # 4. Assertions
    # ---------------------------------------------------------
    assert isinstance(result.final_answer, str)
    assert "Paris" in result.final_answer

    # Trace must contain multiple steps
    assert isinstance(result.trace, list)
    assert len(result.trace) >= 2

    # Memory must now contain the stored fact
    store2 = JSONMemoryStore(path=path)
    all_items = store2.all_items()
    assert any("Paris is the capital of France" in m.content for m in all_items)