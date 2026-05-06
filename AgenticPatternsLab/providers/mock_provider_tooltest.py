class MockLLM_ToolTest:
    def __init__(self):
        self.name = "mock_tooltest"

    def generate(self, prompt: str) -> str:
        # First step: produce an Action
        if "Observation:" not in prompt:
            return (
                "Thought: I should look this up.\n"
                "Action: search(\"France capital\")"
            )

        # Second step: after Observation is injected
        return (
            "Thought: Now I know the answer.\n"
            "FinalAnswer: The capital of France is Paris."
        )