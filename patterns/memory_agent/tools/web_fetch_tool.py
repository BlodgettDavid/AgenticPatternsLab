import urllib.request

class WebFetchTool:
    """
    A minimal deterministic web fetch tool.
    Performs a simple HTTP GET and returns the response body as text.
    """

    name = "web_fetch"

    def run(self, url: str) -> str:
        url = url.strip()
        if not url:
            return "No URL provided."

        try:
            with urllib.request.urlopen(url, timeout=5) as response:
                charset = response.headers.get_content_charset() or "utf-8"
                return response.read().decode(charset)
        except Exception as e:
            return f"Error fetching URL: {url}"