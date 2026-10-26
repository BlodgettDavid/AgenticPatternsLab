"""
patterns/memory_agent/memory_manager.py

Handles context windowing, message filtering, and formatting for LLM payloads
within AgenticPatternsLab.
"""

from typing import Any, Dict, List, Optional
from utils.session_models import SessionState, Message


class MemoryManager:
    """Manages context window truncation and provider message formatting."""
    
    def __init__(self, max_context_messages: int = 20):
        """
        Args:
            max_context_messages: Maximum number of recent messages to retain in active LLM context.
        """
        self.max_context_messages = max_context_messages

    def build_context_window(self, session: SessionState) -> List[Dict[str, str]]:
        """
        Extracts and windows messages from session state, preserving system prompts
        while sliding the window over recent turns.
        """
        messages = session.messages
        
        if len(messages) <= self.max_context_messages:
            return [self._format_message(msg) for msg in messages]

        preserved_head = []
        recent_messages = messages[-self.max_context_messages:]
        
        if messages and messages[0].role == "system":
            if messages[0] not in recent_messages:
                preserved_head = [self._format_message(messages[0])]
                recent_messages = messages[-(self.max_context_messages - 1):]

        formatted_recent = [self._format_message(msg) for msg in recent_messages]
        return preserved_head + formatted_recent

    def _format_message(self, msg: Message) -> Dict[str, str]:
        """Converts a Message Pydantic model into a standard provider dict payload."""
        payload = {
            "role": msg.role,
            "content": msg.content
        }
        if msg.name:
            payload["name"] = msg.name
        return payload