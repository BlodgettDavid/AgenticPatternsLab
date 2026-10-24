import json
import os
import matplotlib.pyplot as plt
import numpy as np

def visualize_benchmarks(json_file="results/quantum_benchmark_results.json"):
    if not os.path.exists(json_file):
        print(f"Error: Benchmark results not found at {json_file}. Run run_quantum_benchmarks.py first.")
        return

    with open(json_file, "r") as f:
        data = json.load(f)
        
    benchmarks = data["benchmarks"]
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle(f"Agentic Quantum R&D Benchmark Summary ({data['timestamp'][:10]})", fontsize=14, fontweight='bold')
    
    # 1. QML Kernel Heatmap
    qml_data = benchmarks["qml_kernel"]
    kernel_matrix = np.array(qml_data["kernel_matrix"])
    im1 = axes[0].imshow(kernel_matrix, cmap="Blues", vmin=0, vmax=1)
    axes[0].set_title("QML Kernel Gram Matrix")
    axes[0].set_xlabel("Data Point Index")
    axes[0].set_ylabel("Data Point Index")
    fig.colorbar(im1, ax=axes[0], fraction=0.046, pad=0.04)
    
    # 2. QAOA Bitstring Probabilities
    qaoa_data = benchmarks["qaoa_optimization"]
    bitstrings = [item["bitstring"] for item in qaoa_data["top_bitstrings"]]
    probs = [item["probability"] for item in qaoa_data["top_bitstrings"]]
    axes[1].bar(bitstrings, probs, color="purple", alpha=0.8)
    axes[1].set_title(f"QAOA Max-Cut (Energy: {qaoa_data['optimal_energy']:.3f})")
    axes[1].set_xlabel("Bitstring")
    axes[1].set_ylabel("Probability")
    axes[1].set_ylim(0, 1.0)
    
    # 3. Hamiltonian Simulation Probabilities
    sim_data = benchmarks["hamiltonian_simulation"]
    sim_states = [item["bitstring"] for item in sim_data["top_states"]]
    sim_probs = [item["probability"] for item in sim_data["top_states"]]
    axes[2].bar(sim_states, sim_probs, color="teal", alpha=0.8)
    axes[2].set_title(f"Trotter Sim (t={sim_data['evolution_time']}s, steps={sim_data['trotter_steps']})")
    axes[2].set_xlabel("State")
    axes[2].set_ylabel("Probability")
    axes[2].set_ylim(0, 1.0)
    
    plt.tight_layout()
    output_img = os.path.join("results", "quantum_benchmark_summary.png")
    plt.savefig(output_img, dpi=300)
    print(f"Visualization saved successfully to {output_img}")
    plt.show()

if __name__ == "__main__":
    visualize_benchmarks()