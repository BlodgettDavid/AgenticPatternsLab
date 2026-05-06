from AgenticPatternsLab.patterns.react.pure_python.react_runner import PurePythonReactRunner

class InfiniteActionProvider:
    """
    Simulates an LLM that never produces a Final Answer.
    It always returns a Thought + Action.
    """
    def generate(self, prompt: str) -> str:
        return (
            "Thought: I should keep searching.\n"
            "Action: search('loop forever')"
        )

def main():
    provider = InfiniteActionProvider()
    runner = PurePythonReactRunner(provider)

    try:
        result = runner.run("This will never terminate normally.")
        print("Unexpected success:", result)
    except Exception as e:
        print("\n=== EXPECTED TERMINATION ===")
        print(e)

if __name__ == "__main__":
    main()
