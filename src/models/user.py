from abc import ABC, abstractmethod


class User(ABC):
    """Абстрактний базовий клас користувача кампусу."""

    def __init__(self, user_id: str, full_name: str, email: str):
        self.user_id = user_id
        self.full_name = full_name
        self.email = email
        self.is_blocked = False

    @abstractmethod
    def get_access_level(self) -> int:
        pass

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "full_name": self.full_name,
            "email": self.email,
            "role": self.__class__.__name__,
            "is_blocked": self.is_blocked,
        }


class Student(User):
    """Клас студента (наслідування від User)."""

    def __init__(self, user_id: str, full_name: str, email: str, faculty: str, course: int):
        super().__init__(user_id, full_name, email)
        self.faculty = faculty
        self.course = course

    def get_access_level(self) -> int:
        return 1  # Базовий рівень доступу (навчальні корпуси)


class Professor(User):
    """Клас викладача (наслідування від User)."""

    def __init__(self, user_id: str, full_name: str, email: str, department: str):
        super().__init__(user_id, full_name, email)
        self.department = department

    def get_access_level(self) -> int:
        return 3  # Розширений рівень доступу (корпуси + лабораторії)