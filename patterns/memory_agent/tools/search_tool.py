from typing import Any, Dict
from utils.tool_base import BaseTool


class SearchTool(BaseTool):
    """
    A minimal deterministic search tool.
    This is intentionally simple so that StrictReactEngine
    can rely on predictable, testable output.

    Later, you can replace the backend with:
    - Bing Search API
    - Local document search
    - Vector DB search
    - LangChain retrievers
    """

    name = "search"
    description = "Performs deterministic mock searches for keywords like quantum computing, machine learning, python, and qiskit."
    parameters_schema: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query term.",
            }
        },
        "required": ["query"],
    }

    def run(self, query: str = "", **kwargs: Any) -> str:
        if not query and "query" in kwargs:
            query = kwargs.get("query", "")
        query = str(query).strip()

        if not query:
            return "No query provided."

        # Deterministic mock responses
        canned = {
            "quantum computing": "Quantum computing uses qubits and superposition.",
            "machine learning": "Machine learning finds patterns in data.",
            "python": "Python is a high-level programming language.",
            "qiskit": "Qiskit is an open-source quantum SDK from IBM.",
        }

        # Exact match first
        if query.lower() in canned:
            return canned[query.lower()]

        # Fallback deterministic response
        return f"No direct match found. Searched for: '{query}'."