from unittest.mock import patch, MagicMock
from patterns.memory_agent.tools.web_fetch_tool import WebFetchTool

def test_web_fetch_success():
    mock_response = MagicMock()
    mock_response.read.return_value = b"hello world"
    mock_response.headers.get_content_charset.return_value = "utf-8"

    # Make __enter__ return the mock itself
    mock_response.__enter__.return_value = mock_response

    with patch("urllib.request.urlopen", return_value=mock_response):
        tool = WebFetchTool()
        result = tool.run("http://example.com")
        assert result == "hello world"

def test_web_fetch_invalid_url():
    with patch("urllib.request.urlopen", side_effect=Exception("fail")):
        tool = WebFetchTool()
        result = tool.run("http://bad-url")
        assert "error" in result.lower()

def test_web_fetch_empty_url():
    tool = WebFetchTool()
    result = tool.run("")
    assert "no url" in result.lower()