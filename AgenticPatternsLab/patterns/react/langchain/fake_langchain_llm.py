from langchain_core.messages import AIMessage

class FakeLangChainLLM:
    """
    Minimal fake LangChain-style LLM for PoC testing.
    It returns deterministic AIMessage outputs.
    """

    def __init__(self, responses):
        self._responses = responses
        self._i = 0

    def invoke(self, messages):
        """
        LangChain chat models expect a list of messages.
        We ignore the content for PoC and return deterministic output.
        """
        text = self._responses[self._i]
        self._i += 1
        return AIMessage(content=text)
