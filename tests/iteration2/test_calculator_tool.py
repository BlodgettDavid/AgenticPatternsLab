from patterns.memory_agent.tools.calculator_tool import CalculatorTool

def test_calculator_simple_addition():
    tool = CalculatorTool()
    result = tool.execute(expression="2 + 3")
    assert result.success is True
    assert "5" in str(result.output)

def test_calculator_complex_expression():
    tool = CalculatorTool()
    result = tool.execute(expression="2 + 3 * 4")
    assert result.success is True
    assert "14" in str(result.output)

def test_calculator_invalid_expression():
    tool = CalculatorTool()
    result = tool.execute(expression="2 + unknown")
    assert result.success is False

def test_calculator_empty_expression():
    tool = CalculatorTool()
    result = tool.execute(expression="")
    assert result.success is False