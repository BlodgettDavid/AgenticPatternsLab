"""Unit tests for Iteration 3: Heuristic Decision Router and MCP Server Core."""

import pytest
from quantum_mcp_server.router_engine import QuantumHeuristicRouter
from quantum_mcp_server.quantum_mcp_server import list_available_tools
from utils.tool_registry import global_tool_registry
from utils.tool_base import BaseTool
from typing import Any, Dict


class DummyTool(BaseTool):
    name = "dummy_tool"
    description = "A dummy tool for testing."
    parameters_schema: Dict[str, Any] = {}

    def execute(self, **kwargs) -> Any:
        return "success"

    def run(self, **kwargs) -> Any:
        return self.execute(**kwargs)


def test_router_heuristics_qml():
    router = QuantumHeuristicRouter(max_classical_qubits=10)
    
    # Below threshold -> classical
    decision_classical = router.evaluate_routing("qml_simulator", {"feature_dimension": 6})
    assert decision_classical == "classical"

    # Above threshold -> quantum
    decision_quantum = router.evaluate_routing("qml_simulator", {"feature_dimension": 14})
    assert decision_quantum == "quantum"


def test_router_heuristics_qaoa():
    router = QuantumHeuristicRouter()
    
    # Small graph nodes -> classical
    small_adj = [[0, 1], [1, 0]]
    assert router.evaluate_routing("execute_qaoa_solver", {"adjacency_matrix": small_adj}) == "classical"

    # Large graph nodes (combinatorial threshold > 8) -> quantum
    large_adj = [[0]*10 for _ in range(10)]
    assert router.evaluate_routing("execute_qaoa_solver", {"adjacency_matrix": large_adj}) == "quantum"


def test_mcp_tool_exposure():
    # Register a tool so the registry isn't empty
    global_tool_registry.register(DummyTool())
    
    tools = list_available_tools()
    assert isinstance(tools, list)
    assert len(tools) > 0
    assert "dummy_tool" in tools