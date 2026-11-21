from typing import List
from src.models.user import User


class AccessGroup:
    """Група доступу. Демонструє агрегацію: користувачі існують незалежно від групи."""

    def __init__(self, group_name: str):
        self.group_name = group_name
        self.members: List[User] = []

    def add_member(self, user: User) -> None:
        if user not in self.members:
            self.members.append(user)

    def remove_member(self, user: User) -> None:
        if user in self.members:
            self.members.remove(user)

    def get_member_count(self) -> int:
        return len(self.members)