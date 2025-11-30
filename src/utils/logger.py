# src/utils/logger.py
import json
import os
from datetime import datetime
from typing import Any

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

class SimpleLogger:
    def __init__(self, path: str):
        ensure_dir(os.path.dirname(path) or ".")
        self.path = path
        self.entries = []

    def log(self, source: str, payload: Any):
        entry = {
            "ts": datetime.utcnow().isoformat() + "Z",
            "source": source,
            "payload": payload
        }
        self.entries.append(entry)
        # append to file
        with open(self.path, "w") as f:
            json.dump(self.entries, f, indent=2)

    def dump(self):
        with open(self.path, "w") as f:
            json.dump(self.entries, f, indent=2)
