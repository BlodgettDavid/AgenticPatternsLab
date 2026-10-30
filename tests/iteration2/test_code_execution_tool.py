"""
tests/iteration2/tools/test_code_execution_tool.py

Unit tests for CodeExecutionTool under the Iteration 2 ToolResult interface.
"""

from patterns.memory_agent.tools.code_execution_tool import CodeExecutionTool


def test_code_exec_simple_print():
    tool = CodeExecutionTool()
    code = 'print("hello world")'
    result = tool.execute(code=code)
    assert result.success is True
    assert "hello world" in result.output


def test_code_exec_multiple_lines():
    tool = CodeExecutionTool()
    code = "x = 2 + 3\nprint(x)"
    result = tool.execute(code=code)
    assert result.success is True
    assert "5" in result.output


def test_code_exec_no_output():
    tool = CodeExecutionTool()
    code = "x = 10 + 20"
    result = tool.execute(code=code)
    assert result.success is True


def test_code_exec_error():
    tool = CodeExecutionTool()
    code = "raise ValueError('bad things')"
    result = tool.execute(code=code)
    assert result.success is False or "error" in result.output.lower()