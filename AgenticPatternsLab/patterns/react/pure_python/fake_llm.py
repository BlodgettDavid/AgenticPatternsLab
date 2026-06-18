class FakeLLM:
    """
    Minimal fake LLM for PurePythonReactRunner.
    Always returns a FinalAnswer so the engine stops.
    """

    def generate(self, prompt: str) -> str:
        return "FinalAnswer: Paris"