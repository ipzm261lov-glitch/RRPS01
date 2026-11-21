class Turnstile:
    """Клас турнікета на вході в корпус."""

    def __init__(self, gate_id: str, location: str, required_level: int):
        self.gate_id = gate_id
        self.location = location
        self.required_level = required_level
        self.is_locked = True

    def unlock(self) -> None:
        self.is_locked = False
        print(f"[ТУРНІКЕТ {self.gate_id} - {self.location}]: ВІДКРИТО.")

    def lock(self) -> None:
        self.is_locked = True