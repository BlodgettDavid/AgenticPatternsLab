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


def test_router_heuristics_matrix_dim():
    router = QuantumHeuristicRouter(max_classical_matrix_dim=32)
    
    # Below matrix dimension threshold -> classical
    small_matrix = [[1.0]*16 for _ in range(16)]
    assert router.evaluate_routing("circuit_simulator", {"matrix": small_matrix}) == "classical"

    # Above matrix dimension threshold -> quantum
    large_matrix = [[1.0]*64 for _ in range(64)]
    assert router.evaluate_routing("circuit_simulator", {"matrix": large_matrix}) == "quantum"


def test_router_heuristics_qaoa():
    router = QuantumHeuristicRouter(max_classical_nodes=8)
    
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
    assert "qml_simulator" in tools


def test_real_mcp_tool_exposure():
    tools = list_available_tools()
    assert isinstance(tools, list)
    assert len(tools) > 0
    # Verify core production tools & new quantum benchmark tools are present
    assert "calculator" in tools
    assert "file" in tools
    assert "qml_simulator" in tools
    assert "execute_qsvm_kernel" in tools
    assert "execute_qaoa_solver" in tools
    assert "execute_trotter_simulation" in tools