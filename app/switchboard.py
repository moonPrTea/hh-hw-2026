from __future__ import annotations

from dataclasses import dataclass

from app.users import User, ForeignUser, LocalUser


LOCAL_PHONE_PREFIX = "+7"


@dataclass(slots=True)
class ActiveCall:
    caller: User
    receiver: User

    @property
    def is_cross_border(self) -> bool:
        return type(self.caller) is not type(self.receiver)


class Switchboard:
    def __init__(self) -> None:
        self._active_calls: list[ActiveCall] = []
        self._count_local_foreign_calls: int = 0
        
    def create_user(self, id: str, fullname: str, phone: str) -> User:
        user_id = int(id)
        
        if phone.startswith(LOCAL_PHONE_PREFIX):
            return LocalUser(user_id, fullname, phone)
        
        return ForeignUser(user_id, fullname, phone)

    def register_call(self, raw_call: str) -> ActiveCall:
        '''
        Метод должен принимать только 1 строку и возвращать класс ActiveCall.
        На входе строка должна быть вида "caller_id,caller_name,caller_phone,reciever_id,reciever_name,reciever_phone"

        Например: "1001,Иван Петров,+71234567890,1085,Адам Яковлев,+71255556666"
        '''
        
        call_parts = [item.strip() for item in raw_call.split(",")]
        
        if len(call_parts) != 6:
            raise ValueError(f"Ожидается строка из 6 полей, передано {len(call_parts)}")
        
        caller_id, caller_fullname, caller_phone, receiver_id, receiver_fullname, receiver_phone = call_parts
        
        caller_user = self.create_user(
            id=caller_id, fullname=caller_fullname,
            phone=caller_phone
        )
        
        receiver_user = self.create_user(
            id=receiver_id, fullname=receiver_fullname, 
            phone=receiver_phone
        )
        
        active_call = ActiveCall(caller_user, receiver_user)
        self._active_calls.append(active_call)
        
        if active_call.is_cross_border:
            self._count_local_foreign_calls += 1
        
        return active_call
    
    # Функция len() выполняется за O(1)
    def get_active_calls_count(self) -> int:
        return len(self._active_calls)
    
    # для реализации O(1) был создан счетчик, значения в который записываются в случае выполнения условия на этапе создания звонка
    def get_cross_border_calls_count(self) -> int:
        return self._count_local_foreign_calls
