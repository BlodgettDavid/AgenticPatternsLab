"""FastMCP Server Implementation for AgenticPatternsLab.

Exposes registered agent tools (Calculator, CodeExecution, FileTools, Search,
WebFetch, and QMLSimulator) over Model Context Protocol (MCP) stdio transport,
integrated with the heuristic decision router.
"""

from mcp.server.fastmcp import FastMCP

# Import unified tool dispatcher and registry from Iteration 2
#from utils.tool_dispatcher import tool_dispatcher
from utils.tool_dispatcher import global_tool_dispatcher as tool_dispatcher

from utils.tool_registry import global_tool_registry

# Import heuristic routing engine for Iteration 3
from quantum_mcp_server.router_engine import router_engine

# Initialize FastMCP Server instance
mcp = FastMCP("QuantumMCPServer")


@mcp.tool()
def execute_agent_tool(tool_name: str, payload: dict) -> dict:
  """Dispatches execution requests to registered tools in AgenticPatternsLab

  with dynamic heuristic routing between classical and quantum backends.
  """
  # Evaluate optimal execution pathway using our heuristic router
  routing_decision = router_engine.evaluate_routing(tool_name, payload)

  # Inject routing metadata into payload for transparent logging/tracking
  payload["routing_decision"] = routing_decision

  # Dispatch execution through the unified tool dispatcher
  return tool_dispatcher.dispatch(tool_name, payload)


@mcp.tool()
def list_available_tools() -> list:
  """Returns the list of registered tool schemas and definitions."""
  return global_tool_registry.list_tools()


if __name__ == "__main__":
  mcp.run(transport="stdio")