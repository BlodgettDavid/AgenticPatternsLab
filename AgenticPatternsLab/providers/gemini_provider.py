"""
Gemini provider for the Agentic Patterns Lab.

This class exposes a unified `.generate(prompt)` interface so it can be used
inside ProviderManager fallback chains.

Implements the official Google AI Python SDK (`google-genai`).
"""

import time
import os
from google import genai
from google.genai.types import GenerateContentConfig
from typing import Any, Type
from pydantic import BaseModel


class GeminiLLM:
    def __init__(self, model_name: str = "gemini-2.0-flash-lite"):
        self.name = "gemini"
        self.model_name = model_name

        self.max_retries = 2
        self.initial_backoff = 0.5
        self.backoff_factor = 2

        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise RuntimeError("GOOGLE_API_KEY environment variable is not set.")

        try:
            self.client = genai.Client(api_key=api_key)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Gemini client: {e}")

    def generate(self, prompt: str) -> str:
        backoff = self.initial_backoff

        for attempt in range(self.max_retries + 1):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=GenerateContentConfig(
                        temperature=0.2,
                        max_output_tokens=2048,
                    )
                )
                return response.text.strip()

            except Exception as e:
                message = str(e)
                retryable = (
                    "503" in message or
                    "UNAVAILABLE" in message or
                    "429" in message or
                    "RESOURCE_EXHAUSTED" in message
                )

                if attempt < self.max_retries and retryable:
                    time.sleep(backoff)
                    backoff *= self.backoff_factor
                    continue

                raise RuntimeError(f"Gemini provider error: {e}")

    def generate_structured(self, system_prompt: str, user_prompt: str, response_model: Type[BaseModel]) -> str:
        """Forces Gemini to return text that conforms exactly to the provided Pydantic model schema."""
        backoff = self.initial_backoff

        for attempt in range(self.max_retries + 1):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=user_prompt,
                    config=GenerateContentConfig(
                        system_instruction=system_prompt,
                        temperature=0.1,  # Lower temperature for strict matching accuracy
                        response_mime_type="application/json",
                        response_schema=response_model,
                    )
                )
                return response.text.strip()

            except Exception as e:
                message = str(e)
                retryable = ("503" in message or "UNAVAILABLE" in message or "429" in message or "RESOURCE_EXHAUSTED" in message)

                if attempt < self.max_retries and retryable:
                    time.sleep(backoff)
                    backoff *= self.backoff_factor
                    continue

                raise RuntimeError(f"Gemini structured provider error: {e}")
            
    def run(self, prompt: str, tools: dict = None) -> Any:
        """Compatibility bridge matching the Agent framework execution contract."""
        raw_text = self.generate(prompt)
        
        class ProviderResponse:
            def __init__(self, text: str):
                self.final_answer = text
                self.trace = {}
                
        return ProviderResponse(raw_text)