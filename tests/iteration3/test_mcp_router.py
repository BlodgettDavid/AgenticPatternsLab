"""Unit tests for Iteration 3: Heuristic Decision Router and MCP Server Core."""

import pytest
from quantum_mcp_server.router_engine import QuantumHeuristicRouter
from quantum_mcp_server.quantum_mcp_server import list_available_tools


def test_router_heuristics_qml():
    router = QuantumHeuristicRouter(max_classical_qubits=10)
    
    # Below threshold -> classical
    assert router.evaluate_routing("qml_simulator", {"feature_dimension": 6}) == "classical"
    # Above threshold -> quantum
    assert router.evaluate_routing("qml_simulator", {"feature_dimension": 14}) == "quantum"


def test_router_heuristics_qaoa():
    router = QuantumHeuristicRouter()
    
    # Small graph nodes -> classical
    small_adj = [[0, 1], [1, 0]]
    assert router.evaluate_routing("execute_qaoa_solver", {"adjacency_matrix": small_adj}) == "classical"

    # Large graph nodes -> quantum
    large_adj = [[0]*10 for _ in range(10)]
    assert router.evaluate_routing("execute_qaoa_solver", {"adjacency_matrix": large_adj}) == "quantum"


def test_real_mcp_tool_exposure():
    tools = list_available_tools()
    assert isinstance(tools, list)
    assert len(tools) > 0
    # Verify core production tools are present
    assert "calculator" in tools
    assert "file" in tools