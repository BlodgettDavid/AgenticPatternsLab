from AgenticPatternsLab.patterns.react.pure_python.react_runner import PurePythonReactRunner

# Each provider returns a malformed Action line.
# The runner should reject all of them.

class BadAction_DoubleQuotes:
    def generate(self, prompt: str) -> str:
        return (
            "Thought: I should search.\n"
            "Action: search(\"capital of France\")"
        )

class BadAction_NoQuotes:
    def generate(self, prompt: str) -> str:
        return (
            "Thought: I should search.\n"
            "Action: search(capital of France)"
        )

class BadAction_MismatchedQuotes:
    def generate(self, prompt: str) -> str:
        return (
            "Thought: I should search.\n"
            "Action: search('capital of France\")"
        )

class BadAction_ExtraText:
    def generate(self, prompt: str) -> str:
        return (
            "Thought: I should search.\n"
            "Action: search('capital of France') extra"
        )

class BadAction_MissingParen:
    def generate(self, prompt: str) -> str:
        return (
            "Thought: I should search.\n"
            "Action: search 'capital of France'"
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
    run_test(BadAction_DoubleQuotes(), "Double Quotes")
    run_test(BadAction_NoQuotes(), "No Quotes")
    run_test(BadAction_MismatchedQuotes(), "Mismatched Quotes")
    run_test(BadAction_ExtraText(), "Extra Text After Action")
    run_test(BadAction_MissingParen(), "Missing Parentheses")

if __name__ == "__main__":
    main()