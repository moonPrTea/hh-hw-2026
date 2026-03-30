from re import escape

import pytest

from app.switchboard import Switchboard
from app.users import ForeignUser, LocalUser


def test_register_call_creates_local_and_foreign_users() -> None:
    switchboard = Switchboard()

    active_call = switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,John Smith,+15551234567"
    )

    assert isinstance(active_call.caller, LocalUser)
    assert isinstance(active_call.receiver, ForeignUser)
    assert active_call.caller.id == 1
    assert active_call.receiver.id == 2


def test_register_creates_with_not_all_fields() -> None:
    switchboard = Switchboard()
    
    with pytest.raises(ValueError, match="Ожидается строка из 6 полей, передано 4"):
        active_call = switchboard.register_call(
        "1, Anton Gorodetsky, +79990000000,John Smith"
        )


def test_creating_local_user_with_invalid_phone() -> None:
    switchboard = Switchboard()
    
    with pytest.raises(ValueError, match=escape("Неверный формат номера телефона локального пользователя. Пример телефона: +71234567890")):
        active_call = switchboard.register_call(
        "1, Anton Gorodetsky,+79991fkfkf, 2, Peter Parker,+78880000000"
        )


def test_creating_foreign_user_with_invalid_phone() -> None:
    switchboard = Switchboard()
    
    with pytest.raises(ValueError, match=escape("Неверный формат номера телефона иностранного пользователя. Пример телефона: +81234567890")):
        active_call = switchboard.register_call(
        "1, Anton Gorodetsky,+79990000000, 2, Peter Parker,+89949449jfds"
        )


def test_register_call_counts_active_calls() -> None:
    switchboard = Switchboard()

    switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,Petr Petrov,+78880000000"
    )
    switchboard.register_call(
        "3,John Smith,+15551234567,4,Jane Doe,+33123456789"
    )

    assert switchboard.get_active_calls_count() == 2


def test_register_call_with_trims() -> None:
    switchboard = Switchboard()

    switchboard.register_call(
        "133 ,  Anton Gorodetsky  ,    +79990000000  ,  222  ,  Peter Parker  ,  +78880000000"
    )
    
    active_call = switchboard.get_active_calls()[-1]
    
    assert switchboard.get_active_calls_count() == 1
    assert active_call.caller.id == 133
    assert active_call.caller.fullname == "Anton Gorodetsky"
    assert active_call.receiver.id == 222
    assert active_call.receiver.fullname == "Peter Parker"
    assert active_call.receiver.phone == "+78880000000"
    


def test_register_call_counts_calls_between_local_and_foreign_users() -> None:
    switchboard = Switchboard()

    switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,John Smith,+15551234567"
    )
    switchboard.register_call(
        "3,Petr Petrov,+78880000000,4,Maria Petrova,+79991112233"
    )
    switchboard.register_call(
        "5,Jane Doe,+33123456789,6,Alex Doe,+442012345678"
    )

    assert switchboard.get_active_calls_count() == 3
    assert switchboard.get_cross_border_calls_count() == 1
