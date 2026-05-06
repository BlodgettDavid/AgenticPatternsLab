from AgenticPatternsLab.patterns.react.pure_python.react_runner import PurePythonReactRunner

class ObservationContainsAnswerProvider:
    """
    Step 1: Action
    Step 2: Final Answer (after seeing observation)
    """
    def __init__(self):
        self.call_count = 0

    def generate(self, prompt: str) -> str:
        self.call_count += 1

        # STEP 1: Ask the tool
        if self.call_count == 1:
            return (
                "Thought: I should search.\n"
                "Action: search('capital of France')"
            )

        # STEP 2: Use the observation to answer
        return (
            "Thought: I now know the answer.\n"
            "Final Answer: Paris."
        )


def main():
    provider = ObservationContainsAnswerProvider()
    runner = PurePythonReactRunner(provider)

    result = runner.run("What is the capital of France?")
    print("\n=== FINAL RESULT ===")
    print(result)

    print("\n=== CALL COUNT ===")
    print(provider.call_count)


if __name__ == "__main__":
    main()
