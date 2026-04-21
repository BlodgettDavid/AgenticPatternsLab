from AgenticPatternsLab.utils.logging import create_logger, log_event
from llama_index.llms.ollama import Ollama


# -------------------------------------------------
# Minimal mock LLM with a LlamaIndex-style interface
# -------------------------------------------------
class MockLlamaIndexLLM:
    def __init__(self, responses):
        self.responses = responses
        self.index = 0

    def complete(self, prompt: str) -> str:
        """Simulate LlamaIndex LLM completion."""
        if self.index < len(self.responses):
            out = self.responses[self.index]
            self.index += 1
            return out
        return "Final Answer: No more responses."


# -------------------------------------------------
# LlamaIndex ReAct Runner
# -------------------------------------------------
def run_react_pattern(provider: str):
    print(f"Running React pattern using LlamaIndex provider: {provider}")

    # -------------------------
    # PROVIDER SELECTION
    # -------------------------
    if provider == "mock":
        llm = MockLlamaIndexLLM(responses=[
            "Thought: I should look this up.\nAction: search('France capital')",
            "Observation: The capital of France is Paris.\nThought: I now know the answer.\nFinal Answer: Paris."
        ])
    else:
        print(f"⚠️ Unknown provider '{provider}'. Using mock LLM instead.")
        llm = MockLlamaIndexLLM(responses=[
            "Thought: Unknown provider.\nAction: search('France capital')",
            "Observation: The capital of France is Paris.\nThought: I now know the answer.\nFinal Answer: Paris."
        ])

    # -------------------------
    # LOGGING SETUP
    # -------------------------
    log_path = create_logger(prefix="react_llama_index")
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
        result = llm.complete(prompt)
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
            action_line = result.split("Action:")[1].strip()
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