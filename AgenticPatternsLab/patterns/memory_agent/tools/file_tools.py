import os

class FileTools:
    """
    Safe, deterministic file operations for the MemoryAgent tool system.
    Supports read, write, append, and delete.
    """

    name = "file"

    def __init__(self, base_dir="."):
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

    def write(self, filename: str, content: str) -> str:
        try:
            path = self._safe_path(filename)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return "OK"
        except Exception:
            return f"Error writing file: {filename}"

    def append(self, filename: str, content: str) -> str:
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