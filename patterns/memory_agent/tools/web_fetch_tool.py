import urllib.request
from typing import Any, Dict
from utils.tool_base import BaseTool


class WebFetchTool(BaseTool):
    """
    A minimal deterministic web fetch tool.
    Performs a simple HTTP GET and returns the response body as text.
    """

    name = "web_fetch"
    description = "Performs an HTTP GET request to fetch the content of a given URL."
    parameters_schema: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "url": {
                "type": "string",
                "description": "The target URL to fetch.",
            }
        },
        "required": ["url"],
    }

    def run(self, url: str = "", **kwargs: Any) -> str:
        if not url and "url" in kwargs:
            url = kwargs.get("url", "")
        url = str(url).strip()

        if not url:
            return "No URL provided."

        try:
            with urllib.request.urlopen(url, timeout=5) as response:
                charset = response.headers.get_content_charset() or "utf-8"
                return response.read().decode(charset)
        except Exception as e:
            return f"Error fetching URL: {url}"