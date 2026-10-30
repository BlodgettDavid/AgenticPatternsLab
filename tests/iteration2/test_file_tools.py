"""
tests/iteration2/tools/test_file_tools.py

Unit tests for FileTools under the Iteration 2 ToolResult interface.
"""

from patterns.memory_agent.tools.file_tools import FileTools

def test_file_write_and_read(tmp_path):
    tool = FileTools(base_dir=tmp_path)
    filename = "test.txt"

    # Write file via execute
    write_result = tool.execute(action="write", path=filename, content="hello")
    assert write_result.success is True
    
    # Read file via execute
    read_result = tool.execute(action="read", path=filename)
    assert read_result.success is True
    assert read_result.output == "hello"

def test_file_append(tmp_path):
    tool = FileTools(base_dir=tmp_path)
    filename = "test.txt"

    tool.execute(action="write", path=filename, content="a")
    tool.execute(action="append", path=filename, content="b")
    
    read_result = tool.execute(action="read", path=filename)
    assert read_result.success is True
    assert read_result.output == "ab"

def test_file_delete(tmp_path):
    tool = FileTools(base_dir=tmp_path)
    filename = "test.txt"

    tool.execute(action="write", path=filename, content="data")
    delete_result = tool.execute(action="delete", path=filename)
    assert delete_result.success is True

    read_result = tool.execute(action="read", path=filename)
    assert "not found" in read_result.output.lower() or not read_result.success

def test_file_invalid_path(tmp_path):
    tool = FileTools(base_dir=tmp_path)
    read_result = tool.execute(action="read", path="../escape.txt")
    assert "unsafe" in read_result.output.lower() or "error" in read_result.output.lower() or not read_result.success