import pytest
from AgenticPatternsLab.patterns.react.shared.tool_registry import ToolRegistry


def test_tool_exists():
    registry = ToolRegistry()
    assert registry.get("echo") is not None
    assert registry.get("reverse") is not None
    assert registry.get("calculator") is not None
    assert registry.get("search") is not None


def test_tool_executes_echo():
    registry = ToolRegistry()
    result = registry.call("echo", "hello")
    assert result == "hello"


def test_tool_executes_reverse():
    registry = ToolRegistry()
    result = registry.call("reverse", "abc")
    assert result == "cba"


def test_tool_executes_calculator():
    registry = ToolRegistry()
    result = registry.call("calculator", "2 + 3")
    assert result == "5"


def test_unknown_tool_raises():
    registry = ToolRegistry()
    with pytest.raises(KeyError):
        registry.call("does_not_exist", "anything")