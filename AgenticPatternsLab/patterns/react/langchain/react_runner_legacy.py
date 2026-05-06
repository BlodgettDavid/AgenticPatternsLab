# AgenticPatternsLab/patterns/react/langchain/react_runner.py

from langchain_core.prompts import PromptTemplate
from AgenticPatternsLab.utils.logging import create_logger, log_event

# We will use the ProviderManager exactly like pure_python
# The provider manager exposes: provider_manager.run(prompt)
# which returns model_output or raises an error.

def run_react_pattern(provider_manager, user_prompt=None):
    """
    LangChain implementation of the ReAct pattern.
    Mirrors the pure_python runner but uses LangChain prompt templates
    and message structures.
    """

    log_path = create_logger(prefix="react_langchain")
    log_event(log_path, "start", f"prompt={user_prompt}")

    # ------------------------------------------------------------
    # Build the ReAct prompt using LangChain PromptTemplate
    # ------------------------------------------------------------
    template = """
You are an AI agent that MUST follow the ReAct (Reasoning + Acting) pattern.
You MUST obey every rule below with ZERO exceptions.

===========================
REQUIRED OUTPUT FORMATS
===========================

CRITICAL TERMINATION RULE:
If the Observation already contains the answer to the user’s question,
you MUST immediately produce:

Thought: I now know the answer.
Final Answer: <the answer>

(1) When reasoning or deciding what to do next:
Thought: <your reasoning>
Action: search('<query>')

(2) When you have enough information to answer:
Thought: <your reasoning>
Final Answer: <your answer>

===========================
STRICT, NON‑NEGOTIABLE RULES
===========================

- You MUST begin EVERY response with "Thought:".
- You MUST include a Thought step before EVERY Action or Final Answer.
- You MUST NOT output anything before "Thought:".
- You MUST NOT invent tools. The ONLY tool you may use is: search(query).
- Tool calls MUST be formatted EXACTLY like: search('some query')
- After receiving an Observation, you MUST produce a NEW Thought.
- You MUST NOT answer directly without using the required format.
- You MUST NOT switch formats mid‑response.
- You MUST NOT include multiple Actions in one response.
- You MUST NOT include both Action AND Final Answer in the same response.
- If you violate ANY rule, you MUST output EXACTLY: FORMAT ERROR

===========================
YOUR TASK
===========================

Follow the rules above EXACTLY.
Never break character.
Never output anything except the required ReAct fields.

Here is the user input:
{user_input}
"""

    prompt = PromptTemplate(
        input_variables=["user_input"],
        template=template
    )

    # ------------------------------------------------------------
    # Format the prompt
    # ------------------------------------------------------------
    full_prompt = prompt.format(user_input=user_prompt)

    # ------------------------------------------------------------
    # Call the provider manager (same as pure_python)
    # ------------------------------------------------------------
    try:
        model_output = provider_manager.generate(full_prompt)
        log_event(log_path, "model_output", model_output)
    except Exception as e:
        log_event(log_path, "provider_error", str(e))
        print("Provider error:", e)
        return

    # ------------------------------------------------------------
    # For now, just print the model output.
    # Later we will add:
    # - ReAct parsing
    # - Action detection
    # - Observation loop
    # - FORMAT ERROR enforcement
    # ------------------------------------------------------------
    print(model_output)

    log_event(log_path, "complete", "react_langchain finished")
