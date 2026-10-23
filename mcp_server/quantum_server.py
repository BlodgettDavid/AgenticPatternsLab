"""
FastMCP Quantum Server Entrypoint (stdio Transport)
Exposes Qiskit 2.x computational tools across QML, Optimization, and Physical Simulation.


"Fast" in FastMCP is an explicit design analogy to web frameworks like FastAPI.
In the standard model context protocol SDK, 
setting up tools manually requires 
    writing verbose, low-level JSON-RPC schema definitions, 
    defining capabilities, and implementing request handler callbacks. 
    
    FastMCP provides a high-level Pythonic decorator interface (@mcp.tool()) 
    that automatically inspects 
        Python function signatures, 
        type hints, 
        and docstrings to auto-generate the underlying JSON-RPC tool schemas on the fly. 
        It drastically speeds up server development while reducing boilerplate.


stdio stands directly for Standard Input / Standard Output (stdin / stdout).
    -In system architecture, stdio transport means the MCP client (providers/mcp_client.py) 
    spawns the MCP server (mcp_server/quantum_server.py) 
    as a child process and communicates with it through OS-level data streams:

    stdin (Standard Input): The client sends JSON-RPC requests by writing text directly 
    into the server's input stream.

    stdout (Standard Output): The server sends responses back by printing JSON-RPC messages 
    to its output stream.

    Because no network ports, HTTP sockets, or web servers (like UVicorn) are opened, 
    stdio is local-first, highly secure, fast, and eliminates port collision issues on host machines.
"""

from mcp.server.fastmcp import FastMCP
from mcp_server.tools.qml_tools import register_qml_tools
from mcp_server.tools.opt_tools import register_opt_tools
from mcp_server.tools.sim_tools import register_sim_tools

# Initialize FastMCP Server instance
mcp = FastMCP("Quantum-Execution-Engine")

# Register domain tool suites
register_qml_tools(mcp)
register_opt_tools(mcp)
register_sim_tools(mcp)

if __name__ == "__main__":
    # Run server listening on standard I/O streams
    mcp.run(transport="stdio")