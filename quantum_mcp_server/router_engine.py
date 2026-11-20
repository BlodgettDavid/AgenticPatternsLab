"""Heuristic Decision Router for AgenticPatternsLab.

Evaluates computational complexity profiles (qubit count, matrix dimensions,
problem scale) to determine optimal execution routing between classical baselines
and quantum simulation backends.
"""

from typing import Dict, Any


class QuantumHeuristicRouter:
    """Evaluates payloads and routes execution pathways based on defined
    computational thresholds.
    """

    def __init__(
        self,
        max_classical_qubits: int = 12,
        max_classical_matrix_dim: int = 64,
        max_classical_nodes: int = 8,
    ):
        self.max_classical_qubits = max_classical_qubits
        self.max_classical_matrix_dim = max_classical_matrix_dim
        self.max_classical_nodes = max_classical_nodes

    def evaluate_routing(self, tool_name: str, payload: Dict[str, Any]) -> str:
        """Determines whether a tool request should execute via 'classical'
        or 'quantum' pathways based on heuristic complexity profiling.
        """
        # 1. QML Kernel / QML Simulator routing checks (Qubit / Feature scale)
        if tool_name in ["qml_simulator", "execute_qsvm_kernel"]:
            data_points = payload.get("data_points", [])
            feature_dim = payload.get(
                "feature_dimension", 
                len(data_points[0]) if data_points and isinstance(data_points[0], (list, tuple)) else len(data_points)
            )
            qubits = payload.get("num_qubits", feature_dim)

            if qubits > self.max_classical_qubits or feature_dim > self.max_classical_qubits:
                return "quantum"

        # 2. Matrix Dimension / Statevector / Quantum Circuit simulation checks
        elif tool_name in ["circuit_simulator", "matrix_solver", "quantum_circuit"]:
            matrix = payload.get("matrix", [])
            state_vector = payload.get("state_vector", [])
            dim = payload.get("matrix_dimension", 0)

            if not dim and matrix:
                dim = len(matrix)
            elif not dim and state_vector:
                dim = len(state_vector)

            if dim > self.max_classical_matrix_dim:
                return "quantum"

        # 3. Optimization / QAOA combinatorial complexity checks
        elif tool_name in ["execute_qaoa_solver", "combinatorial_optimization"]:
            adjacency = payload.get("adjacency_matrix", [])
            num_nodes = payload.get("num_nodes", len(adjacency))

            if num_nodes > self.max_classical_nodes:
                return "quantum"

        # 4. General payload complexity heuristic check
        complexity_score = payload.get("complexity_score", 0)
        if complexity_score > 100:
            return "quantum"

        # Default fallback to classical execution baseline
        return "classical"


# Global singleton router instance
router_engine = QuantumHeuristicRouter()