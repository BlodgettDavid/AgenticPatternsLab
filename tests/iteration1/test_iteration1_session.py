"""
tests/test_iteration1_session.py

Unit tests for Iteration 1: Core State & Memory (Session Models, Manager, and Windowing).
"""

import unittest
import shutil
from pathlib import Path

from utils.session_models import SessionState, Message, PerformanceMetrics
from utils.session_manager import SessionManager
from patterns.memory_agent.memory_manager import MemoryManager


class TestIteration1Session(unittest.TestCase):

    def setUp(self):
        """Set up a temporary test directory for session persistence."""
        self.test_storage_dir = "data/test_sessions"
        self.session_manager = SessionManager(storage_dir=self.test_storage_dir)
        self.session_id = "unit_test_session_01"

    def tearDown(self):
        """Clean up test session files and directory after tests complete."""
        if Path(self.test_storage_dir).exists():
            shutil.rmtree(self.test_storage_dir)

    def test_session_model_and_messages(self):
        """Test creating a SessionState, adding messages, and checking defaults."""
        session = SessionState(session_id=self.session_id)
        self.assertEqual(session.session_id, self.session_id)
        self.assertEqual(session.fsm_state, "IDLE")
        self.assertTrue(session.is_active)
        self.assertEqual(len(session.messages), 0)

        # Add messages using helper method
        session.add_message(role="system", content="You are a helpful AI instructor.")
        session.add_message(role="user", content="Hello, let's build an agent.")
        session.add_message(role="assistant", content="Understood! Let's get started.")

        self.assertEqual(len(session.messages), 3)
        self.assertEqual(session.messages[0].role, "system")
        self.assertEqual(session.messages[1].role, "user")
        self.assertEqual(session.messages[2].role, "assistant")

    def test_session_manager_crud(self):
        """Test saving, loading, and deleting a session through SessionManager."""
        session = SessionState(session_id=self.session_id, fsm_state="PLANNING")
        session.add_message(role="user", content="Test persistence persistence.")
        session.variables["current_topic"] = "Quantum Computing"

        # 1. Save session
        self.session_manager.save_session(session)
        file_path = self.session_manager._get_file_path(self.session_id)
        self.assertTrue(file_path.exists())

        # 2. Load session back
        loaded_session = self.session_manager.load_session(self.session_id)
        self.assertIsNotNone(loaded_session)
        self.assertEqual(loaded_session.session_id, self.session_id)
        self.assertEqual(loaded_session.fsm_state, "PLANNING")
        self.assertEqual(loaded_session.variables["current_topic"], "Quantum Computing")
        self.assertEqual(len(loaded_session.messages), 1)
        self.assertEqual(loaded_session.messages[0].content, "Test persistence persistence.")

        # 3. Delete session
        deleted = self.session_manager.delete_session(self.session_id)
        self.assertTrue(deleted)
        self.assertFalse(file_path.exists())
        self.assertIsNone(self.session_manager.load_session(self.session_id))


    def test_memory_windowing_manager(self):
        """Test sliding window truncation and system prompt preservation."""
        session = SessionState(session_id=self.session_id)
        
        # Add a system prompt and 10 conversational turns
        session.add_message(role="system", content="System instruction: Stay focused.")
        for i in range(10):
            session.add_message(role="user", content=f"User query number {i}")
            session.add_message(role="assistant", content=f"Assistant response number {i}")

        # Total messages: 1 (system) + 20 (10 pairs) = 21 messages
        self.assertEqual(len(session.messages), 21)

        # Initialize MemoryManager with a tight window of 6 messages max
        memory_manager = MemoryManager(max_context_messages=6)
        windowed_context = memory_manager.build_context_window(session)

        # Should preserve the system prompt at the head, plus the last 5 messages
        self.assertLessEqual(len(windowed_context), 6)
        self.assertEqual(windowed_context[0]["role"], "system")
        self.assertEqual(windowed_context[0]["content"], "System instruction: Stay focused.")


if __name__ == "__main__":
    unittest.main()