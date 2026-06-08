
from typing import Callable, Dict, Any

from AgenticPatternsLab.tools.search_tool import search_tool
from AgenticPatternsLab.tools.echo_tool import echo_tool
from AgenticPatternsLab.tools.reverse_tool import reverse_tool
from AgenticPatternsLab.tools.calculator_tool import calculator_tool



class ToolRegistry:
    """
    Canonical shared tool registry for all frameworks (pure_python, LangChain, LlamaIndex).

    Tools are simple Python callables that accept a string input and return a string output.
    """

    def __init__(self):
        self.tools = {
            "search": search_tool,
            "echo": echo_tool,
            "reverse": reverse_tool,
            "calculator": calculator_tool,
        }

    def register(self, name: str, func: Callable[[str], str]) -> None:
        """
        Register or override a tool by name.
        """
        self.tools[name] = func

    def get(self, name: str) -> Callable[[str], str]:
        """
        Return the tool function for the given name.
        Raises KeyError if the tool does not exist.
        """
        if name not in self.tools:
            raise KeyError(f"Unknown tool: {name}")
        return self.tools[name]

    def call(self, name: str, input_str: str) -> str:
        """
        Execute a tool by name with the given input.
        """
        tool_fn = self.get(name)
        return tool_fn(input_str)