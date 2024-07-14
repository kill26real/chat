from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def correct() -> InlineKeyboardMarkup:
    """Функция, создающая Inline кнопки с проверкой корректности введенных даннных"""
    correct_markup = InlineKeyboardMarkup()

    key_yes = InlineKeyboardButton(text='Yes', callback_data='yes')
    key_no = InlineKeyboardButton(text='No', callback_data='no')

    correct_markup.add(key_yes, key_no)

    return correct_markup