from AgenticPatternsLab.patterns.react.pure_python.react_runner import PurePythonReactRunner

# This provider intentionally violates the ReAct format
class BadProvider_MissingThought:
    def generate(self, prompt: str) -> str:
        return "Action: search('capital of France')"  # Missing Thought

class BadProvider_DoubleQuotes:
    def generate(self, prompt: str) -> str:
        return (
            "Thought: I should search.\n"
            "Action: search(\"capital of France\")"  # Wrong quotes
        )

class BadProvider_ActionAndFinal:
    def generate(self, prompt: str) -> str:
        return (
            "Thought: I know the answer.\n"
            "Action: search('capital of France')\n"
            "Final Answer: Paris."
        )

class BadProvider_MultipleActions:
    def generate(self, prompt: str) -> str:
        return (
            "Thought: I should search.\n"
            "Action: search('capital of France')\n"
            "Action: search('population of Seattle')"
        )

def run_test(provider, label):
    print(f"\n=== TEST: {label} ===")
    runner = PurePythonReactRunner(provider)
    try:
        result = runner.run("What is the capital of France?")
        print("Unexpected success:", result)
    except Exception as e:
        print("Caught expected error:", e)

def main():
    run_test(BadProvider_MissingThought(), "Missing Thought")
    run_test(BadProvider_DoubleQuotes(), "Double Quotes in Action")
    run_test(BadProvider_ActionAndFinal(), "Action + Final Answer")
    run_test(BadProvider_MultipleActions(), "Multiple Actions")

if __name__ == "__main__":
    main()