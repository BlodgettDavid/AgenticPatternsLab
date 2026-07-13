import os
import datetime

# ----------------------------------------------------------------------
# ROOT-ANCHORED RUNTIME PATH MANAGEMENT
# ----------------------------------------------------------------------
# __file__ is C:\Users\aliso\AgenticPatternsLab\AgenticPatternsLab\utils\logging.py
# Go up 2 levels to reach the true Repository Root: AgenticPatternsLab
UTILS_DIR = os.path.dirname(os.path.abspath(__file__))
PACKAGE_ROOT = os.path.dirname(UTILS_DIR)
REPO_ROOT = os.path.dirname(PACKAGE_ROOT)

# Centralize our runtime directories at the repository root
LOG_DIR = os.path.join(REPO_ROOT, "logs")
RUN_DIR = os.path.join(REPO_ROOT, ".run")


def get_snapshot_path():
    """Returns the absolute, root-anchored path for the state snapshot file."""
    os.makedirs(RUN_DIR, exist_ok=True)
    return os.path.join(RUN_DIR, "state_snapshot.json")


def get_log_path(prefix="react"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{prefix}_run_{timestamp}.log"
    return os.path.join(LOG_DIR, filename)


def create_logger(prefix="react"):
    os.makedirs(LOG_DIR, exist_ok=True)
    path = get_log_path(prefix)
    return path


def log_event(path, label, content):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {label.upper()}: {content}\n")