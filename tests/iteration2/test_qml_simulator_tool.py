"""
tests/iteration2/test_qml_simulator_tool.py

Unit tests for QMLSimulatorTool under the Iteration 2 tool execution framework.
"""

from patterns.memory_agent.tools.qml_simulator_tool import QMLSimulatorTool


def test_qml_simulator_default_execution():
    """Verify default parameters return a successful simulation payload."""
    tool = QMLSimulatorTool()
    result = tool.run()
    
    assert isinstance(result, dict)
    assert result["status"] == "success"
    assert result["algorithm"] == "unknown"
    assert result["dataset"] == "default"
    assert result["shots"] == 1024
    assert "fidelity" in result


def test_qml_simulator_custom_parameters():
    """Verify custom algorithm, dataset, and shots are correctly processed."""
    tool = QMLSimulatorTool()
    result = tool.run(algorithm="qsvm", dataset="parity", shots=512)
    
    assert isinstance(result, dict)
    assert result["status"] == "success"
    assert result["algorithm"] == "qsvm"
    assert result["dataset"] == "parity"
    assert result["shots"] == 512
    assert result["fidelity"] > 0.0