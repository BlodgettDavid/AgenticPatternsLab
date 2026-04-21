import os
import datetime

LOG_DIR = "logs"

def get_log_path(prefix="react"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{prefix}_run_{timestamp}.log"
    return os.path.join(LOG_DIR, filename)

def create_logger(prefix="react"):
    path = get_log_path(prefix)
    os.makedirs(LOG_DIR, exist_ok=True)
    return path

def log_event(path, label, content):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {label.upper()}: {content}\n")