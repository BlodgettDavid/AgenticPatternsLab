import inspect
import AgenticPatternsLab.patterns.react.langchain.react_runner as rr

print("Loaded module:", rr)
print("\nFile path:", rr.__file__)
print("\nSource code actually being imported:\n")
print(inspect.getsource(rr))