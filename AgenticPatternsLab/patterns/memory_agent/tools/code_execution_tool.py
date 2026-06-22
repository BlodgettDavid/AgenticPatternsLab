import io
import sys
from contextlib import redirect_stdout
from dataclasses import dataclass


@dataclass
class CodeExecutionTool:
    """
    A simple, sandboxed code execution tool.

    - Accepts a Python code string.
    - Executes it in an isolated namespace.
    - Captures stdout and returns it as a string.
    """

    def run(self, code: str) -> str:
        # Local namespace for execution
        local_vars = {}

        # Capture stdout
        stdout_buffer = io.StringIO()
        try:
            with redirect_stdout(stdout_buffer):
                exec(code, {}, local_vars)
        except Exception as e:
            # Return a simple error string; you can refine this later
            return f"ERROR: {e}"

        output = stdout_buffer.getvalue().strip()
        return output