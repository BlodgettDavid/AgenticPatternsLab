from AgenticPatternsLab.patterns.react.pure_python.react_runner import PurePythonReactRunner

class MultiStepProvider:
    """
    Simulates a 3-step ReAct reasoning process:
    Step 1: Action
    Step 2: Action
    Step 3: Final Answer
    """
    def __init__(self):
        self.call_count = 0

    def generate(self, prompt: str) -> str:
        self.call_count += 1

        # STEP 1: First Action
        if self.call_count == 1:
            return (
                "Thought: I should gather initial information.\n"
                "Action: search('author of Dune')"
            )

        # STEP 2: Second Action
        if self.call_count == 2:
            return (
                "Thought: I should verify the publication year.\n"
                "Action: search('Dune publication year')"
            )

        # STEP 3: Final Answer
        return (
            "Thought: I now know the answer.\n"
            "Final Answer: Dune was written by Frank Herbert and published in 1965."
        )


def main():
    provider = MultiStepProvider()
    runner = PurePythonReactRunner(provider)

    result = runner.run("Who wrote Dune and when was it published?")
    print("\n=== FINAL RESULT ===")
    print(result)

    print("\n=== CALL COUNT ===")
    print(provider.call_count)


if __name__ == "__main__":
    main()
