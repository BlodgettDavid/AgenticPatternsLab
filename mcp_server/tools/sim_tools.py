"""
Quantum Simulation & Physical Dynamics Tools Suite
Exposes time-evolution and expectation value evaluation tools.
"""

from typing import List, Dict, Any

from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp, Statevector
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.synthesis import LieTrotter

def register_sim_tools(mcp) -> None:

    @mcp.tool()
    def execute_trotter_simulation(
        pauli_terms: List[List[Any]], 
        time: float, 
        trotter_steps: int = 1
    ) -> Dict[str, Any]:
        """
        Simulates time evolution under a target Hamiltonian using Trotterization.
        H(t) = \sum c_i P_i
        
        Args:
            pauli_terms: List of tuples/lists where each entry is [pauli_string, coefficient], e.g., [["ZZ", 1.0], ["X", 0.5]].
            time: Total evolution time t.
            trotter_steps: Number of Suzuki-Trotter time steps.
            
        Returns:
            Dict containing success status, final statevector probabilities, and circuit depth.
        """
        try:
            # Build SparsePauliOp from input list
            ops = [(term[0], float(term[1])) for term in pauli_terms]
            hamiltonian = SparsePauliOp.from_list(ops)
            num_qubits = hamiltonian.num_qubits

            # Create Trotter evolution gate
            evolution_gate = PauliEvolutionGate(hamiltonian, time=time, synthesis=LieTrotter(reps=trotter_steps))

            # Construct circuit
            qc = QuantumCircuit(num_qubits)
            qc.append(evolution_gate, range(num_qubits))

            # Simulate statevector evolution starting from |0...0>
            statevec = Statevector.from_instruction(qc)
            probs = statevec.probabilities_dict()

            # Sort top measured bitstrings by probability
            sorted_probs = sorted(probs.items(), key=lambda x: x[1], reverse=True)[:4]
            top_states = [{"bitstring": bs, "probability": float(prob)} for bs, prob in sorted_probs]

            return {
                "status": "success",
                "num_qubits": num_qubits,
                "evolution_time": time,
                "trotter_steps": trotter_steps,
                "circuit_depth": qc.depth(),
                "top_states": top_states
            }

        except Exception as e:
            return {"status": "error", "message": str(e)}