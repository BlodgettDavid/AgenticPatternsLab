"""FastMCP Server Implementation for AgenticPatternsLab.

Exposes registered agent tools over Model Context Protocol (MCP) stdio transport,
integrated with the heuristic decision router.
"""

from mcp.server.fastmcp import FastMCP

# Import unified tool dispatcher and registry from Iteration 2
from utils.tool_dispatcher import global_tool_dispatcher as tool_dispatcher
from utils.tool_registry import global_tool_registry

# Import heuristic routing engine for Iteration 3
from quantum_mcp_server.router_engine import router_engine

# Import real production tools from Iteration 2
from patterns.memory_agent.tools.calculator_tool import CalculatorTool
from patterns.memory_agent.tools.code_execution_tool import CodeExecutionTool
from patterns.memory_agent.tools.file_tools import FileTools
from patterns.memory_agent.tools.search_tool import SearchTool
from patterns.memory_agent.tools.web_fetch_tool import WebFetchTool

# Register tool instances into the global registry
global_tool_registry.register(CalculatorTool())
global_tool_registry.register(CodeExecutionTool())
global_tool_registry.register(FileTools())
global_tool_registry.register(SearchTool())
global_tool_registry.register(WebFetchTool())

# Initialize FastMCP Server instance
mcp = FastMCP("QuantumMCPServer")


@mcp.tool()
def execute_agent_tool(tool_name: str, payload: dict) -> dict:
    """Dispatches execution requests to registered tools in AgenticPatternsLab
    with dynamic heuristic routing between classical and quantum backends.
    """
    routing_decision = router_engine.evaluate_routing(tool_name, payload)
    payload["routing_decision"] = routing_decision
    return tool_dispatcher.dispatch(tool_name, payload)


@mcp.tool()
def list_available_tools() -> list:
    """Returns the list of registered tool schemas and definitions."""
    return global_tool_registry.list_tools()


if __name__ == "__main__":
    mcp.run(transport="stdio")