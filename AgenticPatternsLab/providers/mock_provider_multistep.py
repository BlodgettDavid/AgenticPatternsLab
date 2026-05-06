class MockLLM_MultiStep:
    def __init__(self):
        self.name = "mock_multistep"

    def generate(self, prompt: str) -> str:
        # Step 1: No observations yet → produce first Action
        if "Observation:" not in prompt:
            return (
                "Thought: I should break this down.\n"
                "Action: search(\"France capital\")"
            )

        # Step 2: After first observation → produce second Action
        if prompt.count("Observation:") == 1:
            return (
                "Thought: Now I need the population.\n"
                "Action: search(\"Paris population\")"
            )

        # Step 3: After second observation → produce FinalAnswer
        return (
            "Thought: I can now answer.\n"
            "FinalAnswer: Paris is the capital of France and has a population of about 2M."
        )