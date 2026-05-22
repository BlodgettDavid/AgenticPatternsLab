from AgenticPatternsLab.patterns.react.pure_python.react_runner import PurePythonReactRunner


class LlamaIndexProviderChain:
    """
    Wraps a LlamaIndex-style LLM that exposes .complete(prompt: str) -> str
    into the interface expected by PurePythonReactRunner.
    """
    def __init__(self, llm):
        self.llm = llm

    def generate(self, prompt: str) -> str:
        return self.llm.complete(prompt)


def llamaindex_react(llm, user_prompt: str = "What is the capital of France?"):
    """
    Thin adapter that wraps a LlamaIndex-style LLM and feeds it into the strict engine.
    """
    provider_chain = LlamaIndexProviderChain(llm)
    runner = PurePythonReactRunner(provider_chain=provider_chain)
    return runner.run(user_prompt)
