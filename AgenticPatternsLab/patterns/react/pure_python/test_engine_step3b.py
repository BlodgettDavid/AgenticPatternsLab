from AgenticPatternsLab.providers.mock_provider_tooltest import MockLLM_ToolTest
from AgenticPatternsLab.patterns.react.shared.react_engine import ReactEngine, EngineState
from AgenticPatternsLab.patterns.react.shared.tool_registry import ToolRegistry

def main():
    engine = ReactEngine(tool_registry=ToolRegistry().tools)
    llm = MockLLM_ToolTest()

    state = EngineState()

    # First step
    output1 = llm.generate("What is the capital of France?")
    step1 = engine.step(state, output1)

    # Second step (after Observation)
    prompt2 = "What is the capital of France?\nObservation: " + step1.observation.text
    output2 = llm.generate(prompt2)
    step2 = engine.step(state, output2)

    print("Final Answer:", step2.observation.text)

if __name__ == "__main__":
    main()