import time
import ollama
from typing import Any

class OllamaLLM:
    def __init__(self, model_name: str = "llama3.2"):
        self.name = "ollama"
        self.model_name = model_name

        self.max_retries = 2
        self.initial_backoff = 0.5
        self.backoff_factor = 2

    def generate(self, prompt: str) -> str:
        backoff = self.initial_backoff

        for attempt in range(self.max_retries + 1):
            try:
                response = ollama.generate(model=self.model_name, prompt=prompt)
                return response["response"].strip()

            except Exception as e:
                retryable = (
                    "connect" in str(e).lower() or
                    "timeout" in str(e).lower()
                )

                if attempt < self.max_retries and retryable:
                    print(f"Ollama retry {attempt+1}/{self.max_retries} after error: {e}")
                    time.sleep(backoff)
                    backoff *= self.backoff_factor
                    continue

                raise RuntimeError(f"Ollama provider error: {e}")
            
    def run(self, prompt: str, tools: dict = None) -> Any:
        """
        Compatibility bridge matching the Agent framework execution contract.
        """
        raw_text = self.generate(prompt)
        
        class ProviderResponse:
            def __init__(self, text: str):
                self.final_answer = text
                self.trace = {}
                
        return ProviderResponse(raw_text)