import time
import ollama
from typing import Any, Type
from pydantic import BaseModel

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

    def generate_structured(self, system_prompt: str, user_prompt: str, response_model: Type[BaseModel]) -> str:
        """Forces the local Ollama model to format output exactly to the structural target schema."""
        backoff = self.initial_backoff
        
        # Combine system prompt guidelines and user text cleanly for the chat generation format
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        for attempt in range(self.max_retries + 1):
            try:
                # Using chat endpoint to separate system instructions cleanly
                response = ollama.chat(
                    model=self.model_name,
                    messages=messages,
                    format=response_model.model_json_schema(), # Enforces structural JSON schema mapping
                    options={"temperature": 0.1}
                )
                return response["message"]["content"].strip()

            except Exception as e:
                retryable = ("connect" in str(e).lower() or "timeout" in str(e).lower())

                if attempt < self.max_retries and retryable:
                    time.sleep(backoff)
                    backoff *= self.backoff_factor
                    continue

                raise RuntimeError(f"Ollama structured provider error: {e}")
            
    def run(self, prompt: str, tools: dict = None) -> Any:
        """Compatibility bridge matching the Agent framework execution contract."""
        raw_text = self.generate(prompt)
        
        class ProviderResponse:
            def __init__(self, text: str):
                self.final_answer = text
                self.trace = {}
                
        return ProviderResponse(raw_text)