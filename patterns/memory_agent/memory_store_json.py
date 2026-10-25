from __future__ import annotations
import json
import os
from dataclasses import dataclass
from typing import List
from typing import Optional



from dataclasses import dataclass, field
from typing import Any, Dict

@dataclass
class MemoryItem:
    id: str
    type: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    # Accept extra fields without breaking
    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.type = kwargs.get("type")
        self.content = kwargs.get("content")
        self.metadata = kwargs.get("metadata", {})

class JSONMemoryStore:
    """
    Persistent memory store backed by a JSON file.
    """

    def __init__(self, path: str = "memory_store.json"):
        self.path = path
        self.items: List[MemoryItem] = []
        self._load()

    # ---------------------------------------------------------
    # Persistence
    # ---------------------------------------------------------
    def _load(self):
        if not os.path.exists(self.path):
            self.items = []
            return

        with open(self.path, "r", encoding="utf-8") as f:
            raw = json.load(f)

        self.items = [MemoryItem(**item) for item in raw]

    def _save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump([item.__dict__ for item in self.items], f, indent=2)

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------
    def add(self, new_items: List[MemoryItem]):
        self.items.extend(new_items)
        self._save()

    def get_relevant(self, query: str) -> List[MemoryItem]:
        query_lower = query.lower()
        return [item for item in self.items if query_lower in item.content.lower()]

    def all_items(self) -> List[MemoryItem]:
        return list(self.items)