"""
tests/iteration2/test_iteration2_dispatcher.py

Unit tests for ToolDispatcher routing and execution.
"""

from utils.tool_dispatcher import ToolDispatcher
from utils.tool_registry import global_tool_registry
from patterns.memory_agent.tools.calculator_tool import CalculatorTool

def test_dispatcher_successful_execution():
    """Verify the dispatcher correctly routes and executes a registered tool."""
    calc = CalculatorTool()
    global_tool_registry.register(calc)
    
    dispatcher = ToolDispatcher()
    # Use calc.name dynamically to match its registered key
    result = dispatcher.dispatch(calc.name, {"expression": "10 + 5"})
    
    assert result.success is True
    assert "15" in str(result.output)

def test_dispatcher_unknown_tool():
    """Verify the dispatcher gracefully handles unknown tool names."""
    dispatcher = ToolDispatcher()
    
    result = dispatcher.dispatch("nonexistent_tool", {"param": "value"})
    assert result.success is False
    assert "not found" in str(result.error).lower()