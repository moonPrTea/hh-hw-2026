from dataclasses import dataclass
from re import compile

from app.users.user import User

phone_pattern = compile(r'^\+7\d{10}$')

@dataclass(slots=True)
class LocalUser(User):
    @classmethod
    def user_type(cls) -> str:
        return "local"
    
    def __post_init__(self):
        if not phone_pattern.search(self.phone):
            raise ValueError("Неверный формат номера телефона локального пользователя. Пример телефона: +71234567890")
