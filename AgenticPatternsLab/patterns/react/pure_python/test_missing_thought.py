from AgenticPatternsLab.patterns.react.pure_python.react_runner import PurePythonReactRunner

class MissingThoughtProvider:
    """
    Simulates an LLM that incorrectly starts with Action instead of Thought.
    """
    def generate(self, prompt: str) -> str:
        return "Action: search('capital of France')"

def main():
    provider = MissingThoughtProvider()
    runner = PurePythonReactRunner(provider)

    try:
        result = runner.run("What is the capital of France?")
        print("Unexpected success:", result)
    except Exception as e:
        print("\n=== EXPECTED ERROR ===")
        print(e)

if __name__ == "__main__":
    main()