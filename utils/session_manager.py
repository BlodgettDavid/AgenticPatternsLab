import os
import json
from pathlib import Path
from typing import Optional
from .session_models import StudentSession

class SessionManager:
    """Handles CRUD operations for StudentSession states using local JSON storage."""
    
    def __init__(self, storage_dir: str = "data/sessions"):
        # Ensure pathing is relative to the project environment execution root
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def _get_file_path(self, session_id: str) -> Path:
        """Helper to generate standard file target paths."""
        return self.storage_dir / f"{session_id}.json"

    def save_session(self, session: StudentSession) -> None:
        """Serializes and saves or updates a student's session file."""
        file_path = self._get_file_path(session.session_id)
        
        # Pydantic v2 method to dump a model cleanly to a JSON string
        json_data = session.model_dump_json(indent=4)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(json_data)

    def load_session(self, session_id: str) -> Optional[StudentSession]:
        """Loads and validates a student's session file back into a Pydantic model."""
        file_path = self._get_file_path(session_id)
        
        if not file_path.exists():
            return None
            
        with open(file_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
            
        # Pydantic v2 method to parse raw dictionary data back into an active object
        return StudentSession.model_validate(raw_data)

    def delete_session(self, session_id: str) -> bool:
        """Removes a session file from storage if it exists."""
        file_path = self._get_file_path(session_id)
        if file_path.exists():
            file_path.unlink()
            return True
        return False