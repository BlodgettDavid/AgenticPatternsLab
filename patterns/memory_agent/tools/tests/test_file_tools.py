import os
from patterns.memory_agent.tools.file_tools import FileTools

def test_file_write_and_read(tmp_path):
    tool = FileTools(base_dir=tmp_path)
    filename = "test.txt"

    assert tool.write(filename, "hello") == "OK"
    assert tool.read(filename) == "hello"

def test_file_append(tmp_path):
    tool = FileTools(base_dir=tmp_path)
    filename = "test.txt"

    tool.write(filename, "a")
    tool.append(filename, "b")
    assert tool.read(filename) == "ab"

def test_file_delete(tmp_path):
    tool = FileTools(base_dir=tmp_path)
    filename = "test.txt"

    tool.write(filename, "data")
    assert tool.delete(filename) == "OK"
    assert "not found" in tool.read(filename).lower()

def test_file_invalid_path(tmp_path):
    tool = FileTools(base_dir=tmp_path)
    result = tool.read("../escape.txt")
    assert "unsafe" in result.lower() or "error" in result.lower()