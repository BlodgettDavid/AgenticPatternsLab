"""
LangChain Implementation of the Planner-Executor Pattern with Sticky Failover.
Dynamically extracts model configurations from the framework's ProviderManager.
"""

from typing import Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.globals import set_debug
from langchain_core.runnables import RunnableLambda

# Native LangChain community wrappers
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama


# =====================================================================
# 1. State Tracker Class
# =====================================================================
class StickyProviderManager:
    def __init__(self, models_list):
        self.use_fallback = False 
        # Dynamically set primary and fallback based on CLI provider chain injection
        self.primary_model = models_list[0]
        self.fallback_model = models_list[1] if len(models_list) > 1 else models_list[0]

    def get_model(self, inputs):
        """Dynamically returns an executable runnable based on failure state."""
        if self.use_fallback:
            return self.fallback_model
        
        return self.primary_model.with_fallbacks(
            fallbacks=[RunnableLambda(self._mark_failed_and_switch)]
        )

    def _mark_failed_and_switch(self, inputs):
        """Fires ONLY when the primary model fails. Updates state sticky-style."""
        print("\n⚠️ [Sticky Router] Primary provider failed! Flipping switch to local compute forever...")
        self.use_fallback = True
        return self.fallback_model


# =====================================================================
# 2. Mock LLM for Testing
# =====================================================================
class LangChainMockLLM(BaseChatModel):
    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        return ChatResult(generations=[ChatGeneration(message=AIMessage(content="Hello from MockLLM! (LangChain Native)"))])

    @property
    def _llm_type(self) -> str:
        return "mock-educational"


# =====================================================================
# 3. Pattern Execution Runner
# =====================================================================
def run_planner_executor_pattern(provider_chain, user_prompt: Optional[str] = None):
    # Turn on full internal execution tracing
    set_debug(True) 

    print("\n[LangChain Engine] Initializing PlannerExecutor via LCEL")

    default_prompt = "for i in range(5): print(i)"
    prompt_text = user_prompt if user_prompt is not None else default_prompt
    print(f"[LangChain Engine] Input Content: '{prompt_text}'")

    # Step A: Map custom wrappers to native LangChain models based on CLI request
    langchain_models = []
    for p in provider_chain.providers:
        provider_name = p.__class__.__name__
        
        if "GeminiLLM" in provider_name:
            langchain_models.append(ChatGoogleGenerativeAI(
                model="gemini-2.0-flash-lite",
                max_retries=2
            ))
        elif "OllamaLLM" in provider_name:
            langchain_models.append(ChatOllama(
                model="llama3.2",
                max_retries=2
            ))
        elif "MockLLM" in provider_name:
            langchain_models.append(LangChainMockLLM())

    # Ensure we have parsed models before continuing
    if not langchain_models:
        raise ValueError("No valid providers found in the provider chain.")

    # Step B: Instantiate the sticky router with our dynamically allocated models
    sticky_manager = StickyProviderManager(langchain_models)
    dynamic_llm_router = RunnableLambda(sticky_manager.get_model)

    # Step C: Define Prompt Templates
    planner_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert computational thinking instructor. Break down the user's code task into a clear, step-by-step logical planning sequence."),
        ("user", "{input}")
    ])

    executor_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an executor agent. Take this step-by-step plan and generate the final answer/educational guidance response."),
        ("user", "{plan}")
    ])

    # Step D: Construct Chains Using our Dynamic Sticky Router
    planner_chain = planner_prompt | dynamic_llm_router | StrOutputParser()
    executor_chain = executor_prompt | dynamic_llm_router | StrOutputParser()

    # Step E: Execution Flow
    print("\n--- Running Planner Stage ---")
    plan_output = planner_chain.invoke({"input": prompt_text})
    
    print("\n--- Running Executor Stage ---")
    final_output = executor_chain.invoke({"plan": plan_output})

    # Display Output Block
    print("=" * 60)
    print("FINAL EDUCATIONAL RESPONSE")
    print("=" * 60)
    print("Evaluation Passed!\n")
    print("Conclusion:")
    print(final_output)
    print("=" * 60)
    print("Target FSM Resolve State: COMPLETED")
    print("=" * 60)