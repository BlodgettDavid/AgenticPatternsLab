"""FastMCP Server Implementation for AgenticPatternsLab.

Exposes registered agent tools (Calculator, CodeExecution, FileTools, Search,
WebFetch, and QMLSimulator) over Model Context Protocol (MCP) stdio transport.
"""

from mcp.server.fastmcp import FastMCP

# Import unified tool dispatcher and registry from Iteration 2
from utils.tool_dispatcher import tool_dispatcher
from utils.tool_registry import global_tool_registry

# Initialize FastMCP Server instance
mcp = FastMCP("QuantumMCPServer")


@mcp.tool()
def execute_agent_tool(tool_name: str, payload: dict) -> dict:
  """Dispatches execution requests to registered tools in AgenticPatternsLab.

  Args:
      tool_name: The name of the tool to execute (e.g., 'calculator',
        'qml_simulator').
      payload: Parameters required by the target tool.

  Returns:
      Standardized dictionary containing 'status' and 'result' or 'error'.
  """
  return tool_dispatcher.dispatch(tool_name, payload)


@mcp.tool()
def list_available_tools() -> list:
  """Returns the list of registered tool schemas and definitions."""
  return global_tool_registry.list_tools()


if __name__ == "__main__":
  mcp.run(transport="stdio")