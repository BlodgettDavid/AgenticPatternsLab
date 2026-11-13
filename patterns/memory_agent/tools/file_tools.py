import os
from typing import Any, Dict
from utils.tool_base import BaseTool


class FileTools(BaseTool):
    """
    Safe, deterministic file operations for the MemoryAgent tool system.
    Supports read, write, append, and delete.
    """

    name = "file"
    description = "Performs safe file operations (read, write, append, delete)."
    parameters_schema: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "action": {"type": "string", "enum": ["read", "write", "append", "delete"]},
            "filename": {"type": "string"},
            "content": {"type": "string"}
        },
        "required": ["action", "filename"]
    }

    def __init__(self, base_dir="."):
        super().__init__()
        # Restrict file operations to a safe root
        self.base_dir = os.path.abspath(base_dir)

    def _safe_path(self, filename: str) -> str:
        """
        Prevent directory traversal by resolving the absolute path
        and ensuring it stays within base_dir.
        """
        full_path = os.path.abspath(os.path.join(self.base_dir, filename))
        if not full_path.startswith(self.base_dir):
            raise ValueError("Unsafe file path")
        return full_path

    def read(self, filename: str) -> str:
        try:
            path = self._safe_path(filename)
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return f"File not found: {filename}"
        except Exception:
            return f"Error reading file: {filename}"

    def write(self, filename: str, content: str = "") -> str:
        try:
            path = self._safe_path(filename)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return "OK"
        except Exception:
            return f"Error writing file: {filename}"

    def append(self, filename: str, content: str = "") -> str:
        try:
            path = self._safe_path(filename)
            with open(path, "a", encoding="utf-8") as f:
                f.write(content)
            return "OK"
        except Exception:
            return f"Error appending to file: {filename}"

    def delete(self, filename: str) -> str:
        try:
            path = self._safe_path(filename)
            os.remove(path)
            return "OK"
        except FileNotFoundError:
            return f"File not found: {filename}"
        except Exception:
            return f"Error deleting file: {filename}"

    def run(self, **kwargs: Any) -> Any:
        """Unified BaseTool execution interface."""
        action = kwargs.get("action", "read")
        filename = kwargs.get("filename", "")
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
            raise ValueError(f"Unknown file action: {action}")