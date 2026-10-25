from patterns.memory_agent.tools.calculator_tool import CalculatorTool

def test_calculator_simple_addition():
    tool = CalculatorTool()
    result = tool.run("2 + 3")
    assert result == "5"

def test_calculator_complex_expression():
    tool = CalculatorTool()
    result = tool.run("2 + 3 * 4")
    assert result == "14"

def test_calculator_invalid_expression():
    tool = CalculatorTool()
    result = tool.run("2 + unknown")
    assert "invalid expression" in result.lower()

def test_calculator_empty_expression():
    tool = CalculatorTool()
    result = tool.run("")
    assert "no expression" in result.lower()