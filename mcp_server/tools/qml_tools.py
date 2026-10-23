"""
Quantum Machine Learning (QML) Tools Suite
Computes Quantum Feature Maps and Quantum Kernel Gram Matrices using Qiskit 2.x.

-A Quantum Feature Map is a process that translates classical data—like a list of 
numbers or physical measurements—into a quantum state.
-Instead of processing values on a standard computer, the feature map uses the data to 
set the angles and phases of quantum gates inside a circuit. 
-This encodes the original classical vector into a multi-qubit quantum state living in a vast 
mathematical space (Hilbert space). In this space, an algorithm can discover 
non-linear patterns and complex relationships between features that would be hidden
or hard to compute classically.


-A Quantum Kernel Gram Matrix is a grid of similarity scores generated from a group of data points. 
If you have a dataset with N items, the Gram matrix is an N times N square table that compares 
every item in the dataset against every other item.
-Instead of measuring distance in a standard spreadsheet, every data point is first loaded 
into a multi-qubit state using a Quantum Feature Map. 
-The matrix entries then measure how closely those quantum states overlap:Diagonal Values 
-(Self-Similarity): Comparing a data point to itself yields a perfect overlap score of 1.0.
-Off-Diagonal Values (Cross-Similarity): Comparing two different data points yields a score 
between 0.0 and 1.0, reflecting how similar their quantum representations are.
-Once computed by the quantum server, this table of similarity scores is handed directly 
to a classical machine learning model (such as a Support Vector Classifier). The classical model 
uses these quantum-calculated similarities to draw decision boundaries and solve complex classification 
or regression tasks.
"""

from typing import List, Dict, Any
import numpy as np
from qiskit.circuit.library import ZZFeatureMap
from qiskit_machine_learning.kernels import FidelityQuantumKernel

def register_qml_tools(mcp) -> None:

    @mcp.tool()
    def execute_qsvm_kernel(data_points: List[List[float]], feature_dimension: int, reps: int = 2,
                            entanglement: str = "linear"
    ) -> Dict[str, Any]:
        """Computes an N x N Quantum Kernel Gram matrix for input dataset using ZZFeatureMap."""
        X = np.array(data_points)
        num_samples = len(X)
        
        # Construct Feature Map
        feature_map = ZZFeatureMap(
            feature_dimension=feature_dimension, 
            reps=reps, 
            entanglement=entanglement
        )
        
        # Default FidelityQuantumKernel uses statevector evaluation natively
        quantum_kernel = FidelityQuantumKernel(feature_map=feature_map)
        
        # Evaluate Gram Matrix
        kernel_matrix = quantum_kernel.evaluate(x_vec=X)
        
        return {
            "status": "success",
            "matrix_shape": [num_samples, num_samples],
            "kernel_matrix": kernel_matrix.tolist(),
            "feature_dimension": feature_dimension,
            "entanglement": entanglement
        }