from telebot.handler_backends import StatesGroup, State


class States(StatesGroup):
    """Функция, создающая кастомные состояния"""
    first = State()
    second = State()
    third = State()
    fourth = State()
    fifth = State()

