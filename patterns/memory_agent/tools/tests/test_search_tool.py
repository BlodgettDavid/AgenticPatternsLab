from patterns.memory_agent.tools.search_tool import SearchTool

def test_search_tool_exact_match():
    tool = SearchTool()
    result = tool.run("quantum computing")
    assert "qubits" in result.lower()

def test_search_tool_no_match():
    tool = SearchTool()
    result = tool.run("unknown topic")
    assert "no direct match" in result.lower()

def test_search_tool_empty_query():
    tool = SearchTool()
    result = tool.run("")
    assert "no query provided" in result.lower()