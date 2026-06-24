# patterns/planner_executor/pure_python/executor_agent.py
from __future__ import annotations
from typing import Any, Dict

# Precise cross-pattern imports pointing to your verified tools
from patterns.memory_agent.tools.search_tool import SearchTool
from patterns.memory_agent.tools.calculator_tool import CalculatorTool
from patterns.memory_agent.tools.file_tools import FileTools
from patterns.memory_agent.tools.web_fetch_tool import WebFetchTool
from patterns.memory_agent.tools.code_execution_tool import CodeExecutionTool

class ExecutorAgent:
    """
    Layer 3: The Tactical Engine.
    Executes specific atomic tasks handed down from the Planner
    using the ReAct runner and tools.
    """
    def __init__(self, runner: Any):
        """Accepts the shared runner instance containing ReAct orchestration."""
        self.runner = runner

    def execute_step(self, tool_directive: str, context_data: str) -> Dict[str, Any]:
        """
        Executes a targeted, tactical task using the shared runner 
        bound to the core system tools suite.
        """
        execution_prompt = f"""
        You are a tactical assistant performing an atomic execution step.
        Directive: {tool_directive}
        Context Data: {context_data}

        Use the appropriate tools if needed to fulfill the directive. 
        When done, output your final conclusion clearly.
        """

        # Execute using your exact root-level runner signature
        result = self.runner.run(
            execution_prompt,
            tools=self.get_tools()
        )

        return {
            "final_answer": result.final_answer,
            "trace": result.trace
        }

    def get_tools(self) -> Dict[str, Any]:
        """Maps your production-grade tools for tactical execution."""
        return {
            "search": SearchTool().run,
            "calculate": CalculatorTool().run,
            "file_read": FileTools().read,
            "file_write": FileTools().write,
            "file_append": FileTools().append,
            "file_delete": FileTools().delete,
            "web_fetch": WebFetchTool().run,
            "code_exec": CodeExecutionTool().run,
        }