from unittest import result

from langchain_core.language_models import FakeListLLM
from langchain_community.llms import Ollama
from AgenticPatternsLab.patterns.react.pure_python.react_runner import build_react_prompt
from AgenticPatternsLab.utils.logging import create_logger, log_event

# ---------------------------------------------------------
# FUTURE PROVIDER SCAFFOLDING (COMMENTED OUT)
# ---------------------------------------------------------

# --- OpenAI (LangChain) ---
# from langchain_openai import ChatOpenAI
# Example usage:
# llm = ChatOpenAI(
#     model="gpt-4o",
#     api_key="YOUR_OPENAI_API_KEY"
# )

# --- Azure OpenAI (LangChain) ---
# from langchain_openai import AzureChatOpenAI
# Example usage:
# llm = AzureChatOpenAI(
#     model="gpt-4o",
#     azure_endpoint="https://YOUR_RESOURCE.openai.azure.com/",
#     api_key="YOUR_AZURE_OPENAI_KEY",
#     api_version="2024-02-15-preview"
# )


def run_react_pattern(provider: str):
    print(f"Running React pattern using LangChain provider: {provider}")

    # -------------------------
    # PROVIDER SELECTION
    # -------------------------
    if provider == "mock":
        llm = FakeListLLM(responses=[
            "Thought: I should look this up.\nAction: search('France capital')",
            "Observation: The capital of France is Paris.\nThought: I now know the answer.\nFinal Answer: Paris."
        ])

    elif provider == "ollama":
        print("Using real LangChain Ollama provider.")
        llm = Ollama(model="llama3", base_url="http://localhost:11434")

    elif provider == "openai":
        print("⚠️ OpenAI provider not yet implemented. Using mock LLM instead.")
        # Uncomment this when ready:
        # llm = ChatOpenAI(model="gpt-4o", api_key="YOUR_OPENAI_API_KEY")
        llm = FakeListLLM(responses=[
            "Thought: Using fallback mock LLM.\nAction: search('France capital')",
            "Observation: The capital of France is Paris.\nThought: I now know the answer.\nFinal Answer: Paris."
        ])

    elif provider == "azure":
        print("⚠️ Azure provider not yet implemented. Using mock LLM instead.")
        # Uncomment this when ready:
        # llm = AzureChatOpenAI(
        #     model="gpt-4o",
        #     azure_endpoint="https://YOUR_RESOURCE.openai.azure.com/",
        #     api_key="YOUR_AZURE_OPENAI_KEY",
        #     api_version="2024-02-15-preview"
        # )
        llm = FakeListLLM(responses=[
            "Thought: Using fallback mock LLM.\nAction: search('France capital')",
            "Observation: The capital of France is Paris.\nThought: I now know the answer.\nFinal Answer: Paris."
        ])

    else:
        print(f"⚠️ Unknown provider '{provider}'. Using mock LLM instead.")
        llm = FakeListLLM(responses=[
            "Thought: Unknown provider.\nAction: search('France capital')",
            "Observation: The capital of France is Paris.\nThought: I now know the answer.\nFinal Answer: Paris."
        ])

    # -------------------------
    # LOGGING SETUP
    # -------------------------
    log_path = create_logger(prefix="react_langchain")
    log_event(log_path, "start", f"provider={provider}")

    # -------------------------
    # INITIAL PROMPT
    # -------------------------
    prompt = "What is the capital of France?"
    log_event(log_path, "prompt", prompt)

    # -------------------------
    # REACT LOOP
    # -------------------------
    while True:

        react_prompt = build_react_prompt(prompt)
        result = llm.invoke(react_prompt)

        print("\nLLM Output:")
        print(result)

        log_event(log_path, "llm_output", result)

        # Final answer?
        if "Final Answer:" in result:
            final = result.split("Final Answer:")[1].strip()
            log_event(log_path, "final_answer", final)
            print(f"\nFinal Answer: {final}")
            break

        # Action?
        if "Action:" in result:
            action_index = result.find("Action:")
            if action_index != -1:
                action_line = result[action_index + len("Action:"):].strip()

            log_event(log_path, "action", action_line)
            print(f"\nParsed Action: {action_line}")

            # Simulated tool execution
            observation = "The capital of France is Paris."
            log_event(log_path, "observation", observation)

            # Feed back into LLM
            prompt = f"Observation: {observation}"
            log_event(log_path, "next_prompt", prompt)

        else:
            log_event(log_path, "error", "No action found")
            print("No action found. Stopping.")
            break