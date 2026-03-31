from dataclasses import dataclass
from re import compile

from app.users.user import User

phone_pattern = compile(r'^\+[1-9]\d{1,14}$')

@dataclass(slots=True)
class ForeignUser(User):
    @classmethod
    def user_type(cls) -> str:
        return "foreign"
    
    def __post_init__(self):
        if not phone_pattern.search(self.phone):
            raise ValueError("Неверный формат номера телефона иностранного пользователя")
        