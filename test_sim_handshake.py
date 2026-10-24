import asyncio
from providers.mcp_client import MCPClientProvider

async def main():
    print("Testing Hamiltonian Trotterization Simulation over FastMCP stdio...")
    async with MCPClientProvider() as provider:
        # Transverse-field Ising model: H = Z0 Z1 + 0.5 X0 + 0.5 X1
        hamiltonian_terms = [
            ["ZZ", 1.0],
            ["IX", 0.5],
            ["XI", 0.5]
        ]
        
        result = await provider.call_tool(
            "execute_trotter_simulation", 
            {
                "pauli_terms": hamiltonian_terms, 
                "time": 1.0, 
                "trotter_steps": 2
            }
        )
        print("\nSimulation Result:")
        print(result)

if __name__ == "__main__":
    asyncio.run(main())