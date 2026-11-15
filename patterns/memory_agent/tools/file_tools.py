import os
from typing import Any, Dict
from utils.tool_base import BaseTool


class FileTools(BaseTool):
    name = "file"
    description = "Performs safe file operations (read, write, append, delete)."
    parameters_schema: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "action": {"type": "string", "enum": ["read", "write", "append", "delete"]},
            "filename": {"type": "string"},
            "content": {"type": "string"}
        },
        "required": ["action"]
    }

    def __init__(self, base_dir="."):
        super().__init__()
        self.base_dir = os.path.abspath(base_dir)

    def _safe_path(self, filename: str) -> str:
        if not filename:
            raise ValueError("Unsafe or empty file path")
        full_path = os.path.abspath(os.path.join(self.base_dir, filename))
        if not full_path.startswith(self.base_dir):
            raise ValueError("Unsafe file path (directory traversal)")
        return full_path

    def read(self, filename: str) -> str:
        try:
            path = self._safe_path(filename)
            if not os.path.exists(path):
                return f"File not found: {filename}"
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {e}"

    def write(self, filename: str, content: str = "") -> str:
        try:
            path = self._safe_path(filename)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return "OK"
        except Exception as e:
            return f"Error writing file: {e}"

    def append(self, filename: str, content: str = "") -> str:
        try:
            path = self._safe_path(filename)
            with open(path, "a", encoding="utf-8") as f:
                f.write(content)
            return "OK"
        except Exception as e:
            return f"Error appending to file: {e}"

    def delete(self, filename: str) -> str:
        try:
            path = self._safe_path(filename)
            if not os.path.exists(path):
                return f"File not found: {filename}"
            os.remove(path)
            return "OK"
        except Exception as e:
            return f"Error deleting file: {e}"

    def run(self, **kwargs: Any) -> Any:
        action = kwargs.get("action", "read")
        filename = kwargs.get("filename") or kwargs.get("path", "")
        content = kwargs.get("content", "")

        if action == "read":
            return self.read(filename)
        elif action == "write":
            return self.write(filename, content)
        elif action == "append":
            return self.append(filename, content)
        elif action == "delete":
            return self.delete(filename)
        else:
            return f"Unknown file action: {action}"