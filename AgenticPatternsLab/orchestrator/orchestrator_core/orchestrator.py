import importlib

from AgenticPatternsLab.utils.logging import create_logger, log_event
from AgenticPatternsLab.providers.provider_manager import ProviderManager
from AgenticPatternsLab.providers.provider_registry import PROVIDER_REGISTRY

# Fallback providers must be imported directly
from AgenticPatternsLab.providers.gemini_provider import GeminiLLM
from AgenticPatternsLab.providers.ollama_provider import OllamaLLM
from AgenticPatternsLab.providers.mock_provider import MockLLM


def run_orchestrator(pattern_name, framework, provider, user_prompt=None):

    print("Running the Agentic Patterns Orchestrator...")
    print(f"Pattern: {pattern_name}, Framework: {framework}, Provider: {provider}")

    log_path = create_logger(prefix="orchestrator")
    log_event(
        log_path,
        "start",
        f"pattern={pattern_name}, framework={framework}, provider={provider}, prompt={user_prompt}"
    )

    # ----------------------------------------------------------------------
    # PROVIDER SELECTION
    # ----------------------------------------------------------------------
    if provider is None:
        # Default provider chain: Gemini → Ollama → Mock
        provider_chain = ProviderManager([
            GeminiLLM(),
            OllamaLLM(),
            MockLLM()
        ])
    else:
        # User explicitly selected a provider
        if provider not in PROVIDER_REGISTRY:
            raise RuntimeError(f"Unknown provider: {provider}")

        primary_provider_class = PROVIDER_REGISTRY[provider]
        primary = primary_provider_class()

        # Explicit fallback chain
        provider_chain = ProviderManager([
            primary,
            GeminiLLM(),
            OllamaLLM(),
            MockLLM()
        ])


    # ----------------------------------------------------------------------
    # Dynamic import of the runner module
    # ----------------------------------------------------------------------
    module_path = f"AgenticPatternsLab.patterns.{pattern_name}.{framework}.{pattern_name}_runner"

    try:
        module = importlib.import_module(module_path)
        log_event(log_path, "import_success", module_path)

        function_name = f"run_{pattern_name}_pattern"
        pattern_fn = getattr(module, function_name)
        log_event(log_path, "runner_call", function_name)

        # Pass provider manager instead of a single provider
        if user_prompt is not None:
            pattern_fn(provider_chain, user_prompt)
        else:
            pattern_fn(provider_chain)

        log_event(log_path, "complete", "orchestrator finished")

    except ModuleNotFoundError:
        print(f"⚠ Framework '{framework}' not implemented for pattern '{pattern_name}'.")
        print(f"Expected module: {module_path}.py")

    except AttributeError as e:
        print("⚠ AttributeError occurred inside the runner or during getattr():")
        print("   ", e)
        print(f"While loading: {module_path}.py")
        print(f"Expected function: run_{pattern_name}_pattern")
        raise
