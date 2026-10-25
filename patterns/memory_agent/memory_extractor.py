# patterns/memory_agent/memory_extractor.py

from __future__ import annotations
from typing import List, Dict
from dataclasses import dataclass

from .memory_store import MemoryItem


class MemoryExtractor:
    """
    Extracts new memory items from:
        - user message
        - enriched prompt
        - final answer
        - full reasoning trace (thoughts, actions, observations)

    Iteration 1: simple rule-based extraction.
    Later: LLM-based extraction, tagging, scoring, preference detection.
    """

    def extract(
        self,
        user_message: str,
        enriched_prompt: str,
        final_answer: str,
        trace: Dict,
    ) -> List[MemoryItem]:
        """
        Decide what to store from the interaction.
        Returns a list of MemoryItem objects.
        """

        items: List[MemoryItem] = []

        # -----------------------------------------------------
        # 1. Extract stable facts from final answer (very naive)
        # -----------------------------------------------------
        fact = self._extract_fact_from_answer(final_answer)
        if fact:
            items.append(
                MemoryItem(
                    id="",  # MemoryStore will assign UUID
                    type="semantic",
                    content=fact,
                    metadata={"source": "final_answer"},
                )
            )

        # -----------------------------------------------------
        # 2. Extract user preferences from user message
        # -----------------------------------------------------
        pref = self._extract_preference_from_message(user_message)
        if pref:
            items.append(
                MemoryItem(
                    id="",
                    type="semantic",
                    content=pref,
                    metadata={"source": "user_message"},
                )
            )

        # -----------------------------------------------------
        # 3. Store episodic memory (optional for Iteration 1)
        # -----------------------------------------------------
        # Example: store the fact that a tool was used
        tool_events = self._extract_tool_events(trace)
        for event in tool_events:
            items.append(
                MemoryItem(
                    id="",
                    type="episodic",
                    content=event,
                    metadata={"source": "trace"},
                )
            )

        return items

    # ---------------------------------------------------------
    # Internal extraction helpers
    # ---------------------------------------------------------
    def _extract_fact_from_answer(self, answer: str) -> str | None:
        """
        Very naive fact extraction.
        Later: use LLM to extract structured facts.
        """
        if "is" in answer and len(answer.split()) < 20:
            return answer.strip()
        return None

    def _extract_preference_from_message(self, message: str) -> str | None:
        """
        Detect simple preference statements.
        Example: "I prefer X", "I like Y", "I don't like Z"
        """
        lower = message.lower()

        if "i prefer" in lower:
            return message.strip()
        if "i like" in lower:
            return message.strip()
        if "i don't like" in lower:
            return message.strip()

        return None
            

    def _extract_tool_events(self, trace) -> List[str]:


        """
        Extract tool usage events from the Iteration 3 trace format.
        StrictReactEngine produces a list of dicts, each containing:
            - thought: str | None
            - action: str | None   (e.g., "search_memory('France')")
            - final_answer: str | None
        """
        events = []

        if not trace:
            return events

        # Iteration 3: trace is a list of parsed steps
        if isinstance(trace, list):
            for step in trace:
                action = step.get("action")
                if action:
                    # action looks like: "search_memory('France')"
                    tool_name = action.split("(")[0]
                    events.append(f"Used tool: {tool_name}")
            return events

        # Fallback for older formats (Iteration 1)
        if isinstance(trace, dict):
            steps = trace.get("steps", [])
            for step in steps:
                action = step.get("action")
                if action and action.get("type") == "tool":
                    tool_name = action.get("tool")
                    events.append(f"Used tool: {tool_name}")

        return events