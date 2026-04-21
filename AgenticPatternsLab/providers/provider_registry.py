"""
Provider registry for the Agentic Patterns Lab.

Maps provider names (strings) to their corresponding classes so the
orchestrator can dynamically construct provider chains.
"""

from .gemini_provider import GeminiLLM
from .openai_provider import OpenAILLM
from .azure_openai_provider import AzureOpenAILLM
from .ollama_provider import OllamaLLM
from .mock_provider import MockLLM

PROVIDER_REGISTRY = {
    "gemini": GeminiLLM,
    "openai": OpenAILLM,
    "azure_openai": AzureOpenAILLM,
    "ollama": OllamaLLM,
    "mock": MockLLM,
}