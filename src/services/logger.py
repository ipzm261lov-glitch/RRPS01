import os
from datetime import datetime


class AuditLogger:
    """Сервіс журналювання подій безпеки."""

    def __init__(self, log_path: str):
        self.log_path = log_path
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)

    def log_event(self, event_type: str, details: str) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{timestamp}] [{event_type}] {details}\n"
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(line)