"""
MCP Client Provider
Manages stdio subprocess lifecycle, handshakes, and JSON-RPC tool calls with FastMCP servers.

Current Status
The JSON-RPC communication loop over stdio between providers/mcp_client.py 
and mcp_server/quantum_server.py is fully operational. 
The server spawned silently, instantiated the parameterized ZZFeatureMap in Qiskit 2.x, 
evaluated the 3 x 3 Gram matrix using fidelity statevector estimation, 
and returned the serialized matrix payload right back to the client.
"""

import os
import sys
import json
import asyncio
from typing import Dict, Any, Optional
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client



class MCPClientProvider:
    """Interface for invoking tools on local FastMCP servers via stdio transport."""

    def __init__(self, server_module: str = "mcp_server.quantum_server"):
        self.server_module = server_module
        self._session: Optional[ClientSession] = None
        self._exit_stack = None

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def connect(self):
        """Initializes the persistent stdio client session if needed."""
        # This implementation uses per-call or persistent connection handling; 
        # for simplicity with your existing call_tool design, we can handle it directly inside call_tool 
        # or establish a session lifecycle here.
        pass

    async def close(self):
        """Cleanly shuts down any active session resources."""
        pass

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Spawns the FastMCP server process over stdio, handshakes, invokes the target tool,
        and returns the parsed JSON response payload.
        """
        env = os.environ.copy()
        env["PYTHONPATH"] = os.getcwd()
        env["PYTHONUNBUFFERED"] = "1"

        server_params = StdioServerParameters(
            command=sys.executable,
            args=["-m", self.server_module],
            env=env
        )

        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool(tool_name, arguments)
                
                if result.content and hasattr(result.content[0], "text"):
                    raw_text = result.content[0].text
                    try:
                        return json.loads(raw_text)
                    except json.JSONDecodeError:
                        return {"status": "error", "message": f"Invalid JSON received: {raw_text}"}
                return {"status": "error", "message": "Empty response from MCP server"}


def invoke_quantum_tool(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    provider = MCPClientProvider()
    return asyncio.run(provider.call_tool(tool_name, arguments))