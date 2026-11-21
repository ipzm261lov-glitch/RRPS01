import json
from datetime import datetime
from typing import Dict, List

from src.models.user import User, Student, Professor
from src.models.turnstile import Turnstile
from src.models.access_group import AccessGroup
from src.storage.db_storage import DatabaseStorage
from src.services.notifier import NotificationService
from src.services.logger import AuditLogger


class Campus:
    """Клас кампусу. Демонструє композицію: турнікети створюються всередині кампусу."""

    def __init__(self, name: str):
        self.name = name
        self.turnstiles: Dict[str, Turnstile] = {}

    def install_turnstile(self, gate_id: str, location: str, required_level: int) -> None:
        self.turnstiles[gate_id] = Turnstile(gate_id, location, required_level)


class CampusSystemManager:
    """
    GOD CLASS (Божественний клас):
    Порушує SRP — відповідає за конфігурацію, реєстрацію, перевірку доступу,
    управління турнікетами, сповіщення, логування та звітність.
    """

    def __init__(self, config_path: str):
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)

        # Надмірна зв'язаність (Tight Coupling): жорстке створення залежностей
        self.campus = Campus(self.config["campus_name"])
        self.storage = DatabaseStorage(self.config["db_file"])
        self.notifier = NotificationService()
        self.logger = AuditLogger(self.config["log_file"])

        self.users: Dict[str, User] = {}
        self.groups: List[AccessGroup] = []

    def setup_default_gates(self) -> None:
        self.campus.install_turnstile("G-01", "Головний корпус", 1)
        self.campus.install_turnstile("G-02", "Наукова лабораторія", 3)

    def register_student(self, user_id: str, name: str, email: str, faculty: str, course: int) -> Student:
        student = Student(user_id, name, email, faculty, course)
        self.users[user_id] = student
        self.storage.save_user(student.to_dict())
        self.notifier.send_email(email, "Реєстрація в кампусі", f"Вітаємо, {name}! Ваш ID: {user_id}")
        self.logger.log_event("REGISTER", f"Зареєстровано студента {name} ({user_id})")
        return student

    def register_professor(self, user_id: str, name: str, email: str, department: str) -> Professor:
        prof = Professor(user_id, name, email, department)
        self.users[user_id] = prof
        self.storage.save_user(prof.to_dict())
        self.notifier.send_email(email, "Реєстрація в кампусі", f"Вітаємо, проф. {name}! Ваш ID: {user_id}")
        self.logger.log_event("REGISTER", f"Зареєстровано викладача {name} ({user_id})")
        return prof

    def create_access_group(self, group_name: str, members: List[User]) -> AccessGroup:
        group = AccessGroup(group_name)
        for member in members:
            group.add_member(member)
        self.groups.append(group)
        return group

    def process_student_entry(self, user_id: str, gate_id: str) -> bool:
        """Навмисне дублювання логіки проходу (майже копія process_professor_entry)."""
        user = self.users.get(user_id)
        gate = self.campus.turnstiles.get(gate_id)

        if not user or not gate:
            self.logger.log_event("ERROR", f"Невідомий ID {user_id} або турнікет {gate_id}")
            return False

        if user.is_blocked:
            self.notifier.send_security_alert("security@campus.edu", f"Спроба входу заблокованого: {user.full_name}")
            self.logger.log_event("DENIED", f"Заблокований студент {user.full_name} на {gate_id}")
            return False

        if user.get_access_level() >= gate.required_level:
            gate.unlock()
            gate.lock()
            self.storage.save_entry_record({"user": user.full_name, "gate": gate_id, "time": str(datetime.now())})
            self.logger.log_event("ACCESS_GRANTED", f"Студент {user.full_name} пройшов через {gate_id}")
            return True
        else:
            self.notifier.send_email(user.email, "Відмова у доступі", f"Недостатньо прав для {gate.location}")
            self.logger.log_event("ACCESS_DENIED", f"Відмова студенту {user.full_name} на {gate_id}")
            return False

    def process_professor_entry(self, user_id: str, gate_id: str) -> bool:
        """Дублює метод process_student_entry."""
        user = self.users.get(user_id)
        gate = self.campus.turnstiles.get(gate_id)

        if not user or not gate:
            self.logger.log_event("ERROR", f"Невідомий ID {user_id} або турнікет {gate_id}")
            return False

        if user.is_blocked:
            self.notifier.send_security_alert("security@campus.edu", f"Спроба входу заблокованого: {user.full_name}")
            self.logger.log_event("DENIED", f"Заблокований викладач {user.full_name} на {gate_id}")
            return False

        if user.get_access_level() >= gate.required_level:
            gate.unlock()
            gate.lock()
            self.storage.save_entry_record({"user": user.full_name, "gate": gate_id, "time": str(datetime.now())})
            self.logger.log_event("ACCESS_GRANTED", f"Викладач {user.full_name} пройшов через {gate_id}")
            return True
        else:
            self.notifier.send_email(user.email, "Відмова у доступі", f"Недостатньо прав для {gate.location}")
            self.logger.log_event("ACCESS_DENIED", f"Відмова викладачу {user.full_name} на {gate_id}")
            return False

    def generate_summary_report(self) -> str:
        total_users = len(self.storage.get_all_users())
        return f"Звіт по '{self.campus.name}': зареєстровано користувачів — {total_users}, турнікетів — {len(self.campus.turnstiles)}."