import json
import os


class DatabaseStorage:
    """Модуль збереження даних у JSON. Містить навмисне дублювання коду I/O."""

    def __init__(self, file_path: str):
        self.file_path = file_path
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump({"users": [], "logs": []}, f, indent=4)

    def save_user(self, user_data: dict) -> None:
        # Дублювання логіки читання/запису файлу №1
        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        data["users"].append(user_data)
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def save_entry_record(self, record: dict) -> None:
        # Дублювання логіки читання/запису файлу №2
        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        data["logs"].append(record)
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def get_all_users(self) -> list:
        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("users", [])