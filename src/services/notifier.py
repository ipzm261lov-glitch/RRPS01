class NotificationService:
    """Сервіс відправки сповіщень користувачам."""

    def send_email(self, recipient: str, subject: str, body: str) -> None:
        print(f"[EMAIL -> {recipient}] Тема: '{subject}' | Текст: {body}")

    def send_security_alert(self, admin_email: str, message: str) -> None:
        print(f"[ТРИВОГА -> {admin_email}] {message}")