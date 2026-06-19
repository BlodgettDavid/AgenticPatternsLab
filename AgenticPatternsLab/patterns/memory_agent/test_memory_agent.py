from patterns.memory_agent.memory_agent import MemoryAgent
from patterns.memory_agent.memory_store_json import JSONMemoryStore
from patterns.memory_agent.memory_extractor import MemoryExtractor
from patterns.memory_agent.pure_python.memory_agent_runner import MemoryAgentRunner
import os


def test_memory_agent_persistent_store():
    path = "test_memory.json"

    # Ensure clean start
    if os.path.exists(path):
        os.remove(path)

    store = JSONMemoryStore(path=path)
    extractor = MemoryExtractor()
    runner = MemoryAgentRunner()

    agent = MemoryAgent(runner, store, extractor)

    result = agent.run("What is the capital of France?")
    assert isinstance(result.final_answer, str)
    assert len(result.final_answer) > 0

    # Memory should now be persisted
    store2 = JSONMemoryStore(path=path)
    all_items = store2.all_items()
    assert len(all_items) > 0

    # Retrieval should work across runs
    retrieved = store2.get_relevant("Paris")
    assert len(retrieved) > 0

    # Cleanup
    #os.remove(path)