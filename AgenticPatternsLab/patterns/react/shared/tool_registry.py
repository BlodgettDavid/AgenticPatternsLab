from AgenticPatternsLab.tools.search_tool import search_tool

class ToolRegistry:
    def __init__(self):
        self.tools = {
            "search": search_tool,
        }

    def get(self, name: str):
        return self.tools.get(name)