import os
import datetime
import json

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


def get_snapshot_path() -> str:
    # Ensure local project .run directory exists
    run_dir = os.path.join(os.getcwd(), ".run")
    os.makedirs(run_dir, exist_ok=True)
    return os.path.join(run_dir, "state_snapshot.json")


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

def log_execution_artifact(pipeline_type: str, run_name: str, data: Dict[str, Any]) -> str:
    """Saves execution payloads, routing decisions, and metrics to artifacts_pipeline/."""
    target_dir = os.path.join(REPO_ROOT, "artifacts_pipeline", pipeline_type)
    os.makedirs(target_dir, exist_ok=True)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{run_name}_{timestamp}.json"
    filepath = os.path.join(target_dir, filename)

    payload_record = {
        "timestamp": datetime.datetime.now().isoformat(),
        "pipeline_type": pipeline_type,
        "run_name": run_name,
        **data
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(payload_record, f, indent=2)

    return filepath