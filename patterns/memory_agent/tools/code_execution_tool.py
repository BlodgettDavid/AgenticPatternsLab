import io
import sys
from contextlib import redirect_stdout
from typing import Any, Dict
from utils.tool_base import BaseTool


class CodeExecutionTool(BaseTool):
    """
    A simple, sandboxed code execution tool.

    - Accepts a Python code string.
    - Executes it in an isolated namespace.
    - Captures stdout and returns it as a string.
    """

    name = "code_execution"
    description = "Executes Python code strings in a sandboxed namespace and captures stdout."
    parameters_schema: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "code": {
                "type": "string",
                "description": "The Python code snippet to execute.",
            }
        },
        "required": ["code"],
    }

    def run(self, code: str = "", **kwargs: Any) -> str:
        if not code and "code" in kwargs:
            code = kwargs.get("code", "")
        code = str(code)

        # Local namespace for execution
        local_vars = {}

        # Capture stdout
        stdout_buffer = io.StringIO()
        try:
            with redirect_stdout(stdout_buffer):
                exec(code, {}, local_vars)
        except Exception as e:
            return f"ERROR: {e}"

        output = stdout_buffer.getvalue().strip()
        return output