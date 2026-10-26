# patterns/memory_agent/memory_agent.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, List, Optional
import uuid

from .memory_store import MemoryStore, MemoryItem
from .memory_extractor import MemoryExtractor
from .tools.search_tool import SearchTool
from .tools.calculator_tool import CalculatorTool
from .tools.file_tools import FileTools
from .tools.web_fetch_tool import WebFetchTool
from patterns.memory_agent.tools.code_execution_tool import CodeExecutionTool

from utils.session_models import SessionState


@dataclass
class MemoryAgentResult:
    """Unified result returned by MemoryAgent."""
    final_answer: str
    trace: dict


class MemoryAgent:
    """
    MemoryAgent wraps the entire reasoning system:
        User → MemoryAgent → Runner → Engine → Tools → MemoryAgent → User
    """

    def __init__(
        self,
        runner: Any,
        memory_store: MemoryStore,
        extractor: MemoryExtractor,
        max_context_messages: int = 20,
    ):
        self.runner = runner
        self.memory_store = memory_store
        self.extractor = extractor
        self.max_context_messages = max_context_messages

    def run(self, user_message: str, session: Optional[SessionState] = None) -> MemoryAgentResult:
        # 1) If a session is provided, log the incoming user message
        if session:
            session.add_message(role="user", content=user_message)

        # 2) Retrieve relevant long-term memory
        retrieved = self.memory_store.get_relevant(user_message)

        # 3) Build enriched prompt (incorporating session window history if available)
        enriched_prompt = self._build_enriched_prompt(
            user_message=user_message,
            memories=retrieved,
            session=session,
        )

        # 4) Call runner
        result = self.runner.run(
            enriched_prompt,
            tools=self.get_tools()
        )

        final_answer = result.final_answer
        trace = result.trace

        # 5) Log assistant response back to session state if available
        if session:
            session.add_message(role="assistant", content=final_answer, metadata={"trace": trace})

        # 6) Extract new long-term memories
        new_items = self.extractor.extract(
            user_message=user_message,
            enriched_prompt=enriched_prompt,
            final_answer=final_answer,
            trace=trace,
        )

        # 7) Store new memory items
        if new_items:
            self.memory_store.add(new_items)

        # 8) Return final answer
        return MemoryAgentResult(
            final_answer=final_answer,
            trace=trace,
        )

    def _build_enriched_prompt(
        self,
        user_message: str,
        memories: List[MemoryItem],
        session: Optional[SessionState] = None,
    ) -> str:
        memory_block = "\n".join(f"- {m.content}" for m in memories)
        
        # Build sliding window history context if session exists
        history_block = ""
        if session and session.messages:
            # Apply sliding window truncation
            recent_msgs = session.messages[-self.max_context_messages:]
            history_lines = [f"{msg.role.upper()}: {msg.content}" for msg in recent_msgs[:-1]] # Exclude latest just added user message
            if history_lines:
                history_block = "\nRecent Conversation History:\n" + "\n".join(history_lines) + "\n"

        return f"""
You are a strict ReAct agent.
{history_block}
Relevant prior context:
{memory_block}

User message:
{user_message}
""".strip()
    
    # ---------------------------------------------------------
    # Tools exposed to StrictReactEngine
    # ---------------------------------------------------------
    def get_tools(self):
        return {
            "search_memory": self._tool_search_memory,
            "write_memory": self._tool_write_memory,
            "search": SearchTool().run,
            "calculate": CalculatorTool().run,
            "file_read": FileTools().read,
            "file_write": FileTools().write,
            "file_append": FileTools().append,
            "file_delete": FileTools().delete,
            "web_fetch": WebFetchTool().run,
            "code_exec": CodeExecutionTool().run,
        }
  
    def _tool_search_memory(self, query: str) -> str:
        items = self.memory_store.get_relevant(query)
        if not items:
            return "No relevant memory found"
        return "; ".join(item.content for item in items)

    def _tool_write_memory(self, content: str) -> str:
        item = MemoryItem(
            id=str(uuid.uuid4()),
            type="agent_written",
            content=content,
            metadata={}
        )
        self.memory_store.add([item])
        return "Memory stored"