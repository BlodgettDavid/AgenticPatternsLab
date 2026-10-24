import asyncio
from providers.mcp_client import MCPClientProvider

async def main():
    print("Testing QAOA Solver Tool over FastMCP stdio transport...")
    async with MCPClientProvider() as provider:
        # 3-node triangle graph adjacency matrix
        graph = [
            [0.0, 1.0, 1.0],
            [1.0, 0.0, 1.0],
            [1.0, 1.0, 0.0]
        ]
        
        result = await provider.call_tool(
            "execute_qaoa_solver", 
            {"adjacency_matrix": graph, "p_steps": 1, "maxiter": 30}
        )
        print("\nQAOA Solver Result:")
        print(result)

if __name__ == "__main__":
    asyncio.run(main())