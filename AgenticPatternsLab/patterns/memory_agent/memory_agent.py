# patterns/memory_agent/memory_agent.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, List

from .memory_store import MemoryStore, MemoryItem
from .memory_extractor import MemoryExtractor
from .tools.search_tool import SearchTool

import uuid




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
    ):
        self.runner = runner
        self.memory_store = memory_store
        self.extractor = extractor

    def run(self, user_message: str) -> MemoryAgentResult:
        # 1) Retrieve relevant memory
        retrieved = self.memory_store.get_relevant(user_message)

        # 2) Build enriched prompt
        enriched_prompt = self._build_enriched_prompt(
            user_message=user_message,
            memories=retrieved,
        )

        # 3) Call runner
        result = self.runner.run(
            enriched_prompt,
            tools=self.get_tools()
        )

        final_answer = result.final_answer
        trace = result.trace

        # 4) Extract new memories
        new_items = self.extractor.extract(
            user_message=user_message,
            enriched_prompt=enriched_prompt,
            final_answer=final_answer,
            trace=trace,
        )

        # 5) Store new memory
        if new_items:
            self.memory_store.add(new_items)

        # 6) Return final answer
        return MemoryAgentResult(
            final_answer=final_answer,
            trace=trace,
        )

    def _build_enriched_prompt(
        self,
        user_message: str,
        memories: List[MemoryItem],
    ) -> str:

        memory_block = "\n".join(f"- {m.content}" for m in memories)

        return f"""

You are a strict ReAct agent.

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