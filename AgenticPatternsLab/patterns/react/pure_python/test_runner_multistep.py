'''
from AgenticPatternsLab.providers.mock_provider_multistep import MockLLM_MultiStep
from AgenticPatternsLab.patterns.react.pure_python.pure_python_runner import PurePythonReactRunner
from AgenticPatternsLab.patterns.react.shared.tool_registry import ToolRegistry

def main():
    runner = PurePythonReactRunner(tool_registry=ToolRegistry().tools)
    runner = PurePythonReactRunner()

    llm = MockLLM_MultiStep()

    result = runner.run(
        user_input="Tell me about the capital of France.",
        llm=llm
    )

    print("Final Answer:", result)

if __name__ == "__main__":
    main()
''' 


from AgenticPatternsLab.providers.mock_provider_multistep import MockLLM_MultiStep
from AgenticPatternsLab.patterns.react.pure_python.pure_python_runner import PurePythonReactRunner

def main():
    runner = PurePythonReactRunner()
    llm = MockLLM_MultiStep()

    result = runner.run(
        user_input="Tell me about the capital of France.",
        llm=llm
    )

    print("Final Answer:", result)

if __name__ == "__main__":
    main()