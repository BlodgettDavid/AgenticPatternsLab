"""MCP Client Bridge for AgenticPatternsLab.

Establishes stdio-based Model Context Protocol (MCP) client sessions to communicate
with the Quantum MCP Server and invoke registered tools dynamically.
"""

import asyncio
import sys
from typing import Dict, Any, List
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPClientBridge:
    """Manages stdio MCP process communication for agent orchestrator nodes."""

    def __init__(self, python_executable: str = sys.executable):
        self.python_executable = python_executable
        self.server_params = StdioServerParameters(
            command=self.python_executable,
            args=["-m", "quantum_mcp_server.quantum_mcp_server"],
        )

    async def execute_tool(self, tool_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Spawns or connects to the MCP server via stdio, executes the tool, and returns the result."""
        async with stdio_client(self.server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool(
                    "execute_agent_tool",
                    arguments={"tool_name": tool_name, "payload": payload}
                )
                # Parse text/content from MCP tool response
                if result.content and hasattr(result.content[0], "text"):
                    import json
                    try:
                        return json.loads(result.content[0].text)
                    except json.JSONDecodeError:
                        return {"raw_output": result.content[0].text}
                return {"result": str(result.content)}

    async def list_tools(self) -> List[Dict[str, Any]]:
        """Retrieves available tool schemas from the MCP server."""
        async with stdio_client(self.server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool("list_available_tools", arguments={})
                if result.content and hasattr(result.content[0], "text"):
                    import json
                    try:
                        return json.loads(result.content[0].text)
                    except json.JSONDecodeError:
                        return []
                return []

    def run_sync_execute(self, tool_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Synchronous wrapper for orchestrator FSM node execution."""
        return asyncio.run(self.execute_tool(tool_name, payload))


# Global singleton bridge instance
mcp_client_bridge = MCPClientBridge()