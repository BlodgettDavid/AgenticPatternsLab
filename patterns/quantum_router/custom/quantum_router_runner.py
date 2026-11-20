"""Runner for the Quantum MCP Router pattern in AgenticPatternsLab."""

from utils.mcp_client_bridge import mcp_client_bridge
from utils.logging import create_logger, log_event

def run_quantum_router_pattern(provider_chain, user_prompt=None, resume=False):
    """Executes workflows by routing requests through the MCP client bridge
    and heuristic decision router.
    """
    print("Initializing Quantum MCP Router Pattern...")
    log_path = create_logger(prefix="quantum_router")
    
    prompt = user_prompt or "Execute default quantum vs classical routing benchmark workflow."
    log_event(log_path, "start_workflow", f"prompt: {prompt}")

    # Determine tool based on keyword or default to qml_simulator / search
    tool_name = "qml_simulator" if "quantum" in prompt.lower() or "qml" in prompt.lower() else "search"
    
    payload = {
        "feature_dimension": 16 if "quantum" in prompt.lower() else 4,
        "query": prompt
    }

    print(f"Dispatching tool '{tool_name}' through MCP client bridge...")
    result = mcp_client_bridge.run_sync_execute(tool_name, payload)

    print(f"Execution Result: {result}")
    log_event(log_path, "execution_success", str(result))
    print("Quantum Router pattern execution complete.")