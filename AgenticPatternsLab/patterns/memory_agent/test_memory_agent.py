from patterns.memory_agent.memory_agent import MemoryAgent, MemoryAgentResult
from patterns.memory_agent.memory_store import MemoryStore
from patterns.memory_agent.memory_extractor import MemoryExtractor
from patterns.memory_agent.pure_python.memory_agent_runner import MemoryAgentRunner


def test_memory_agent_end_to_end():
    runner = MemoryAgentRunner()
    store = MemoryStore()
    extractor = MemoryExtractor()

    agent = MemoryAgent(runner, store, extractor)

    result: MemoryAgentResult = agent.run("What is the capital of France?")

    # Validate final answer
    assert isinstance(result.final_answer, str)
    assert len(result.final_answer) > 0

    # Validate trace (Option A: empty dict is fine)
    assert isinstance(result.trace, dict)

    # Validate memory was extracted + stored
    all_items = store.all_items()
    assert len(all_items) > 0

    # Validate retrieval works
    retrieved = store.get_relevant("Paris")
    assert len(retrieved) > 0