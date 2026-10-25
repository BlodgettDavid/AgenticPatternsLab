# patterns/memory_agent/memory_store.py

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict
import uuid
import time


# ---------------------------------------------------------
# Memory Item
# ---------------------------------------------------------
@dataclass
class MemoryItem:
    """
    A single memory entry stored by MemoryAgent.
    - type: "episodic" or "semantic"
    - content: the text of the memory
    - metadata: tags, timestamps, source, etc.
    """
    id: str
    type: str
    content: str
    metadata: Dict = field(default_factory=dict)


# ---------------------------------------------------------
# Memory Store
# ---------------------------------------------------------
class MemoryStore:
    """
    Simple in-memory store for episodic + semantic memory.
    Iteration 1: list-based storage with naive retrieval.
    """

    def __init__(self):
        # Store everything in a single list for now
        self._items: List[MemoryItem] = []

    # -----------------------------------------------------
    # Public API
    # -----------------------------------------------------
    def add(self, items: List[MemoryItem]) -> None:
        """Add new memory items to the store."""
        for item in items:
            # Ensure ID + timestamp exist
            if not item.id:
                item.id = str(uuid.uuid4())
            item.metadata.setdefault("timestamp", time.time())

            self._items.append(item)

    def get_relevant(self, user_message: str) -> List[MemoryItem]:
        """
        Retrieve relevant memory items.
        Iteration 1: naive keyword match.
        Later: scoring, semantic search, recency weighting.
        """
        user_lower = user_message.lower()
        results = []

        for item in self._items:
            if any(word in item.content.lower() for word in user_lower.split()):
                results.append(item)

        # Optional: limit number of memories returned
        return results[:10]

    def all_items(self) -> List[MemoryItem]:
        """Return all memory items (debugging / inspection)."""
        return list(self._items)