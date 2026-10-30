"""
utils/tool_base.py

Defines the abstract base class and standardized data models for all executable
tools within AgenticPatternsLab.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Optional
import time


'''
Captures execution success/failure, output data, error messages, execution time, 
    and auxiliary metadata uniformly.
'''
@dataclass
class ToolResult:
    """Standardized result returned by any tool execution."""
    success: bool
    output: Any
    error: Optional[str] = None
    execution_time_sec: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

'''
Enforces that all child tools define their name, description, and implement run(**kwargs).
'''
class BaseTool(ABC):
    """
    Abstract Base Class for all tools in the AgenticPatternsLab architecture.
    Enforces unified metadata definitions and a standardized execution interface.
    """

    name: str = "base_tool"
    description: str = "Abstract base tool definition."
    parameters_schema: Dict[str, Any] = field(default_factory=dict)

    @abstractmethod
    def run(self, **kwargs: Any) -> Any:
        """
        Core execution logic for the tool. Must be implemented by subclasses.
        """
        pass

    '''
    Wraps the raw execution in a try-except block with performance measurement so failures never crash the agent runtime.        
    '''
    def execute(self, **kwargs: Any) -> ToolResult:
        """
        Wrapped execution handler that measures performance, catches exceptions,
        and returns a standardized ToolResult.
        """
        start_time = time.perf_counter()
        try:
            output = self.run(**kwargs)
            elapsed = time.perf_counter() - start_time
            return ToolResult(
                success=True,
                output=output,
                execution_time_sec=elapsed
            )
        except Exception as e:
            elapsed = time.perf_counter() - start_time
            return ToolResult(
                success=False,
                output=None,
                error=str(e),
                execution_time_sec=elapsed
            )