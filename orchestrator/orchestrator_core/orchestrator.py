import importlib

from utils.logging import create_logger, log_event
from providers.provider_manager import ProviderManager
from providers.provider_registry import PROVIDER_REGISTRY

# Fallback providers must be imported directly
from providers.gemini_provider import GeminiLLM
from providers.ollama_provider import OllamaLLM
from providers.mock_provider import MockLLM


def run_orchestrator(pattern_name, framework, provider, user_prompt=None, resume=False):

    print("Running the Agentic Patterns Orchestrator...")
    print(f"Pattern: {pattern_name}, Framework: {framework}, Provider: {provider}, Resume: {resume}")

    log_path = create_logger(prefix="orchestrator")
    log_event(
        log_path,
        "start",
        f"pattern={pattern_name}, framework={framework}, provider={provider}, prompt={user_prompt}, resume={resume}"
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

        # Deduplicated fallback chain
        defaults = [GeminiLLM(), OllamaLLM(), MockLLM()]
        fallback_list = [primary] + [p for p in defaults if type(p) != type(primary)]
        
        provider_chain = ProviderManager(fallback_list)

    # ----------------------------------------------------------------------
    # Dynamic import routing override for the custom multi-agent triage pattern
    # ----------------------------------------------------------------------
    if pattern_name in ("triage", "multi_agent_triage"):
        module_path = "patterns.multi_agent_triage.custom.multi_agent_triage_runner"
        function_name = "run_multi_agent_triage_pattern"
    else:
        module_path = f"patterns.{pattern_name}.{framework}.{pattern_name}_runner"
        function_name = f"run_{pattern_name}_pattern"

    try:
        module = importlib.import_module(module_path)
        log_event(log_path, "import_success", module_path)

        pattern_fn = getattr(module, function_name)
        log_event(log_path, "runner_call", function_name)

        # Pass provider manager and include our asynchronous resume flag
        if user_prompt is not None:
            pattern_fn(provider_chain, user_prompt, resume=resume)
        else:
            pattern_fn(provider_chain, resume=resume)

        log_event(log_path, "complete", "orchestrator finished")

    except ModuleNotFoundError:
        print(f"⚠ Framework '{framework}' not implemented for pattern '{pattern_name}'.")
        print(f"Expected module: {module_path}.py")

    except AttributeError as e:
        print("⚠ AttributeError occurred inside the runner or during getattr():")
        print("   ", e)
        print(f"While loading: {module_path}.py")
        print(f"Expected function: {function_name}")
        raise