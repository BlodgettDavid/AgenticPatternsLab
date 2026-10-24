import asyncio
import json
import os
from datetime import datetime
from providers.mcp_client import MCPClientProvider

async def main():
    print("Initializing Agentic Quantum R&D Benchmark Suite...")
    
    # Ensure results directory exists
    os.makedirs("results", exist_ok=True)
    
    async with MCPClientProvider() as provider:
        results = {
            "timestamp": datetime.now().isoformat(),
            "benchmarks": {}
        }
        
        # 1. QML Kernel Benchmark
        print("\n[1/3] Running QML Kernel Gram Matrix Benchmark...")
        qml_res = await provider.call_tool(
            "execute_qsvm_kernel",
            {
                "data_points": [[0.1, 0.2], [0.5, 0.6], [0.9, 0.8]],
                "feature_dimension": 2,
                "reps": 2,
                "entanglement": "linear"
            }
        )
        results["benchmarks"]["qml_kernel"] = qml_res
        
        # 2. QAOA Optimization Benchmark
        print("[2/3] Running QAOA Max-Cut Optimization Benchmark...")
        graph = [
            [0.0, 1.0, 1.0, 0.0],
            [1.0, 0.0, 1.0, 1.0],
            [1.0, 1.0, 0.0, 1.0],
            [0.0, 1.0, 1.0, 0.0]
        ]
        opt_res = await provider.call_tool(
            "execute_qaoa_solver",
            {
                "adjacency_matrix": graph,
                "p_steps": 2,
                "maxiter": 40
            }
        )
        results["benchmarks"]["qaoa_optimization"] = opt_res
        
        # 3. Hamiltonian Simulation Benchmark
        print("[3/3] Running Trotterized Simulation Benchmark...")
        hamiltonian_terms = [
            ["ZZ", 1.0],
            ["IX", 0.5],
            ["XI", 0.5]
        ]
        sim_res = await provider.call_tool(
            "execute_trotter_simulation",
            {
                "pauli_terms": hamiltonian_terms,
                "time": 1.5,
                "trotter_steps": 3
            }
        )
        results["benchmarks"]["hamiltonian_simulation"] = sim_res
        
        # Save aggregated benchmark log into results/
        output_filename = os.path.join("results", "quantum_benchmark_results.json")
        with open(output_filename, "w") as f:
            json.dump(results, f, indent=4)
            
        print(f"\nBenchmarks complete! Results saved to {output_filename}")

if __name__ == "__main__":
    asyncio.run(main())