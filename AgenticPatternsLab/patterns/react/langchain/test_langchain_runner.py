# AgenticPatternsLab/patterns/react/langchain/test_langchain_runner.py

from AgenticPatternsLab.patterns.react.langchain.langchain_runner import LangChainReactRunner
from langchain_core.language_models import BaseLanguageModel
from langchain_core.messages import AIMessage


class FakeLangChainLLM(BaseLanguageModel):
    """
    Minimal fake LangChain LLM for testing.
    Always returns a Final Answer immediately.
    """

    def invoke(self, messages, **kwargs):
        return AIMessage(content="Thought: I know the answer.\nFinal Answer: Paris.")

    @property
    def _llm_type(self):
        return "fake-llm"


def main():
    llm = FakeLangChainLLM()
    runner = LangChainReactRunner(llm)

    result = runner.run("What is the capital of France?")

    print("\n=== FINAL RESULT ===")
    print(result)


if __name__ == "__main__":
    main()