"""
tests/iteration2/tools/test_search_tool.py

Unit tests for SearchTool under the Iteration 2 ToolResult interface.
"""

from patterns.memory_agent.tools.search_tool import SearchTool

def test_search_tool_exact_match():
    tool = SearchTool()
    result = tool.execute(query="quantum computing")
    assert result.success is True
    assert "qubits" in result.output.lower()

def test_search_tool_no_match():
    tool = SearchTool()
    result = tool.execute(query="unknown topic")
    assert result.success is True  # or False depending on how your tool handles misses
    assert "no direct match" in result.output.lower()

def test_search_tool_empty_query():
    tool = SearchTool()
    result = tool.execute(query="")
    assert result.success is False or (result.output and "no query provided" in result.output.lower())