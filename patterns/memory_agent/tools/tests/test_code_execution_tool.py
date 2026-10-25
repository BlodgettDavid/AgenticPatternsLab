from patterns.memory_agent.tools.code_execution_tool import CodeExecutionTool


def test_code_exec_simple_print():
    tool = CodeExecutionTool()
    code = 'print("hello world")'
    result = tool.run(code)
    assert result == "hello world"


def test_code_exec_multiple_lines():
    tool = CodeExecutionTool()
    code = """
x = 2 + 3
print(x)
"""
    result = tool.run(code)
    assert result == "5"


def test_code_exec_no_output():
    tool = CodeExecutionTool()
    code = "x = 10 + 20"
    result = tool.run(code)
    assert result == ""


def test_code_exec_error():
    tool = CodeExecutionTool()
    code = "raise ValueError('bad things')"
    result = tool.run(code)
    assert result.startswith("ERROR:")