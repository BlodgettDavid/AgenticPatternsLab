"""
Provider registry for the Agentic Patterns Lab.

Maps provider names (strings) to their corresponding classes so the
orchestrator can dynamically construct provider chains.
"""

from .gemini_provider import GeminiLLM
from .ollama_provider import OllamaLLM
from .mock_provider import MockLLM

PROVIDER_REGISTRY = {
    "gemini": GeminiLLM,
    "ollama": OllamaLLM,
    "mock": MockLLM,
}